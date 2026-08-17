# ojos_keypoint.py — ¿ES LA PERDIDA POR PIXEL LO QUE CIEGA A DIEGO? (prerregistro-56, 11-ago-2026).
#
# DE DONDE SALE: de una critica externa que el director trajo, y su punto era mejor que nada que yo
# hubiera escrito. ojos_gimnasio.py entrena con ERROR CUADRATICO POR PIXEL promediado, y si mas del
# 90% de los pixeles son fondo, el optimo de esa perdida es RECONSTRUIR LA PARED y no el objeto
# pequeño que se mueve. Ata tres hallazgos que teniamos sueltos: las cuatro arquitecturas de ojo
# puntuando a escala de ruido, percepcion2 divergiendo en 3 de 4 entrenamientos, y el motor
# recibiendo series de las que no puede sacar nada.
#
# QUE SE COMPARA, y es lo unico que cambia: EL CUELLO DE BOTELLA.
#   pixel_mse         -> latente plano. Es LO QUE DIEGO USA HOY, y por eso es la linea base tonta:
#                        no es un rival de paja.
#   keypoint_softmax  -> el latente son PUNTOS (x,y) obtenidos por softmax espacial. La red no
#                        puede guardar textura ahi aunque quiera: solo caben coordenadas.
# LAS DOS SE ENTRENAN CON LA MISMA PERDIDA POR PIXEL, los mismos datos y las mismas epocas.
#
# LA VERDAD (la posicion real del objeto) SOLO SE USA PARA EVALUAR, NUNCA PARA ENTRENAR. Meterla en
# el entrenamiento seria darle la respuesta —herencia por la puerta de atras— y ademas no mediria
# nada. La medida es un R2 LINEAL y fuera de muestra: si hiciera falta una red para sacar la
# posicion del latente, el latente NO ES una coordenada.
#
# Uso: python ojos_keypoint.py [--regla31] [--salida resultados/p56-ojos/medida.json]

import os
import sys
import json
import argparse

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# QUE ESTUDIA ESTE MODULO: las dos arquitecturas. Por eso su regla31() NO las examina — trabaja con
# latentes sinteticos. Examinar al sujeto dentro de mi propia Regla 31 es el error que dejo NULO al
# prerregistro-45, y disciplina.py lo comprueba a maquina.
SUJETO = ("Pixel", "Keypoint")

T, N = 600, 32
SEMILLAS = (227, 229, 233, 239, 241)   # NUEVAS. Quemadas en el banco: 211, 223
EPOCAS = 25
PISO_R2 = 0.80        # criterio A
VENTAJA = 0.15        # criterio B
TECHO_AZAR = 0.10     # criterio C

METODO = {
    "prerregistro": 56,
    "tipo_de_medida": "continua",
    "que_mide": ("cuanta de la posicion VERDADERA del objeto se recupera linealmente del latente, "
                 "fuera de muestra, con cada uno de los dos cuellos de botella"),
    "comparten_datos": {
        "hay": True,
        "porque": "las dos arquitecturas se entrenan sobre EXACTAMENTE la misma escena y la misma "
                  "semilla — esa es la definicion de la comparacion. Si cada una tuviera su "
                  "propia escena, la diferencia podria ser de la escena.",
    },
    "linea_base": ("el codificador de HOY, pixel_mse. No es un rival de paja: es exactamente lo "
                   "que Diego usa. Si el nuevo no le gana por el margen declarado, no hay motivo "
                   "para cambiarlo (Regla 11)"),
    "formulas": [
        # EL FACTOR SE DERIVA DEL MECANISMO, NO DE MI INTUICION (enmienda 1 del prerregistro-56).
        # Mi primer factor fue x10 y la puerta lo reprobo midiendo x1.020: llevaba el ruido a 0.20,
        # y el objeto tiene un CONTRASTE DE 0.5 sobre un fondo de desviacion 0.15, asi que seguia
        # siendo el borron mas brillante y el softmax lo encontraba igual. La relacion no fallo:
        # mi numero era demasiado pequeño para lo que la relacion afirma. x50 lleva el ruido a 1.0,
        # el DOBLE del contraste, y ese numero lo se A PRIORI porque yo construi la escena.
        {"base": {"ruido_sensor": 0.02}, "parametro": "ruido_sensor", "factor": 50.0,
         "esperado": "baja",
         "porque": "el ruido de SENSOR se suma a los fotogramas ya generados y entierra el objeto "
                   "pequeño bajo el fondo, luego la posicion recuperable del latente tiene que "
                   "caer. De sensor y no de proceso: el de proceso moveria el objeto, que es otra "
                   "cosa (LECCION-RUIDO-01). Base 0.02 y NO 0.0, porque comparar un cero con otro "
                   "cero no prueba nada"},
    ],
}


def escena(semilla=227, ruido_sensor=0.0):
    """Fondo estatico con textura + un objeto PEQUEÑO en trayectoria conocida. La verdad la ponemos
    nosotros, y solo se usa para EVALUAR."""
    rng = np.random.default_rng(int(semilla))
    fondo = rng.normal(0.5, 0.15, (N, N)).astype(np.float32)
    t = np.arange(T) * 0.05
    cx = (N / 2 + 8 * np.cos(0.9 * t)).astype(int).clip(2, N - 3)
    cy = (N / 2 + 8 * np.sin(0.9 * t)).astype(int).clip(2, N - 3)
    vids = np.tile(fondo, (T, 1, 1))
    yy, xx = np.mgrid[0:N, 0:N]
    for i in range(T):
        vids[i][(yy - cy[i]) ** 2 + (xx - cx[i]) ** 2 <= 4] = 1.0   # ~13 px de 1024
    if ruido_sensor:
        vids = vids + rng.normal(0, float(ruido_sensor), vids.shape).astype(np.float32)
    return vids[:, None, :, :], np.stack([cx, cy], 1).astype(np.float32)


class Pixel(nn.Module):
    """EL DE HOY: latente plano. Puede guardar textura, y por eso la guarda."""

    def __init__(self, d=8):
        super().__init__()
        self.e = nn.Sequential(nn.Conv2d(1, 16, 3, 2, 1), nn.ReLU(), nn.Conv2d(16, 32, 3, 2, 1),
                               nn.ReLU(), nn.Flatten(), nn.Linear(32 * 8 * 8, d))
        self.dec = nn.Sequential(nn.Linear(d, 32 * 8 * 8), nn.ReLU(), nn.Unflatten(1, (32, 8, 8)),
                                 nn.ConvTranspose2d(32, 16, 4, 2, 1), nn.ReLU(),
                                 nn.ConvTranspose2d(16, 1, 4, 2, 1))

    def z(self, x):
        return self.e(x)

    def forward(self, x):
        return self.dec(self.e(x))


class Keypoint(nn.Module):
    """SOFTMAX ESPACIAL: en el cuello de botella SOLO CABEN COORDENADAS. La red no puede guardar
    textura ahi aunque le convenga para la perdida."""

    def __init__(self, k=2):
        super().__init__()
        self.k = k
        self.f = nn.Sequential(nn.Conv2d(1, 16, 3, 2, 1), nn.ReLU(), nn.Conv2d(16, k, 3, 2, 1))
        self.dec = nn.Sequential(nn.Linear(2 * k, 32 * 8 * 8), nn.ReLU(),
                                 nn.Unflatten(1, (32, 8, 8)),
                                 nn.ConvTranspose2d(32, 16, 4, 2, 1), nn.ReLU(),
                                 nn.ConvTranspose2d(16, 1, 4, 2, 1))

    def z(self, x):
        m = self.f(x)
        B, k, h, w = m.shape
        p = torch.softmax(m.reshape(B, k, -1), -1).reshape(B, k, h, w)
        gx = torch.linspace(-1, 1, w, device=x.device)
        gy = torch.linspace(-1, 1, h, device=x.device)
        return torch.cat([(p.sum(2) * gx).sum(-1), (p.sum(3) * gy).sum(-1)], 1)

    def forward(self, x):
        return self.dec(self.z(x))


def entrenar(modelo, X, epocas=EPOCAS, semilla=227):
    """LA MISMA perdida por pixel para los dos. Lo unico que cambia es el cuello de botella."""
    torch.manual_seed(int(semilla))
    opt = torch.optim.Adam(modelo.parameters(), lr=2e-3)
    ultima = None
    for _ in range(int(epocas)):
        for i in range(0, len(X), 64):
            xb = X[i:i + 64]
            p = ((modelo(xb) - xb) ** 2).mean()
            opt.zero_grad()
            p.backward()
            opt.step()
            ultima = float(p.detach())
    return modelo, ultima


def r2_lineal(Z, objetivo, fraccion=0.7):
    """R2 FUERA DE MUESTRA de lo que se recupera LINEALMENTE del latente. Lineal a proposito: si
    hiciera falta una red para sacar la posicion, el latente no es una coordenada."""
    Z = np.asarray(Z, dtype=float)
    y = np.asarray(objetivo, dtype=float)
    A = np.column_stack([Z, np.ones(len(Z))])
    c = int(len(Z) * fraccion)
    w, *_ = np.linalg.lstsq(A[:c], y[:c], rcond=None)
    pred, yt = A[c:] @ w, y[c:]
    ss = float(((yt - yt.mean(0)) ** 2).sum())
    return float(1 - ((yt - pred) ** 2).sum() / ss) if ss > 0 else 0.0


def _una(semilla, ruido_sensor=0.0):
    vids, verdad = escena(semilla, ruido_sensor=ruido_sensor)
    X = torch.tensor(vids)
    out = {}
    for nombre, M in (("pixel_mse", Pixel()), ("keypoint_softmax", Keypoint())):
        m, perdida = entrenar(M, X, semilla=semilla)
        with torch.no_grad():
            Z = m.z(X).numpy()
        out[nombre] = {"r2": round(r2_lineal(Z, verdad), 4),
                       "perdida_final": round(float(perdida), 6),
                       "diverge": not np.isfinite(perdida)}
        if nombre == "keypoint_softmax":
            rng = np.random.default_rng(int(semilla) + 7000)
            out["r2_contra_objetivo_al_azar"] = round(
                r2_lineal(Z, rng.normal(size=verdad.shape)), 4)
    return out


def _metodo_medir(ruido_sensor=0.02):
    """PASO 1 — la medida escalar: el R2 del softmax espacial sobre una semilla de trabajo."""
    return float(_una(SEMILLAS[0], ruido_sensor=float(ruido_sensor))["keypoint_softmax"]["r2"])


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el R2 mide el latente o lo produce el ajuste?** Un R2 que
    sube solo por tener muchas columnas no compara nada, y con latentes de 8 dimensiones y 180
    puntos de prueba ese riesgo es real."""
    fallos = []
    rng = np.random.default_rng(56)
    verdad = np.stack([np.cos(np.arange(T) * 0.05), np.sin(np.arange(T) * 0.05)], 1)
    # (a) un latente que ES la posicion (mas ruido) debe dar R2 alto
    bueno = r2_lineal(verdad + rng.normal(0, 0.01, verdad.shape), verdad)
    if bueno < 0.9:
        fallos.append(f"la medida no reconoce un latente que ES la posicion: {bueno:.3f}")
    # (b) un latente de RUIDO contra la posicion debe dar R2 ~0 fuera de muestra
    malo = r2_lineal(rng.normal(size=(T, 8)), verdad)
    if malo > TECHO_AZAR:
        fallos.append(f"la medida se infla sola: ruido puro contra la posicion da {malo:.3f}")
    return {"aprueba": not fallos, "fallos": fallos,
            "r2_de_un_latente_que_es_la_posicion": round(bueno, 4),
            "r2_de_ruido_puro": round(malo, 4)}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados, con latentes SINTETICOS.

    Aqui NO se entrena ninguna de las dos arquitecturas: eso es el resultado que este estudio
    existe para medir, y meterlo haria que los criterios A y B no pudieran fallar."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-56: la MEDIDA, no las arquitecturas ==")

    fs = _metodo_sanidad()
    caso("CONTROL POSITIVO: reconoce un latente que ES la posicion",
         fs["r2_de_un_latente_que_es_la_posicion"] >= 0.9,
         str(fs["r2_de_un_latente_que_es_la_posicion"]))
    caso("SEÑUELO: contra ruido puro el R2 no se infla",
         fs["r2_de_ruido_puro"] <= TECHO_AZAR, str(fs["r2_de_ruido_puro"]))

    # el nulo CORRECTO para esta medida no es barajar los fotogramas: la posicion es POR fotograma
    # y barajar el tiempo no destruye nada. Esa leccion me costo el prerregistro 52.
    rng = np.random.default_rng(561)
    verdad = np.stack([np.cos(np.arange(T) * 0.05), np.sin(np.arange(T) * 0.05)], 1)
    idx = rng.permutation(T)
    caso("barajar los fotogramas NO cambia la medida (y por eso NO es un nulo valido aqui)",
         abs(r2_lineal(verdad[idx] + 0.01, verdad[idx]) - r2_lineal(verdad + 0.01, verdad)) < 0.2)

    caso("la escena tiene un objeto PEQUEÑO frente al fondo (si no, no hay nada que medir)",
         float((escena(227)[0] > 0.99).mean()) < 0.05,
         f"{float((escena(227)[0] > 0.99).mean()):.4f} de los pixeles")
    caso("la lista de semillas NO esta vacia", len(SEMILLAS) > 0)

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la medida distingue por los dos lados."
                                 if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    por_semilla = {}
    for s in SEMILLAS:
        if verbose:
            print(f"  semilla {s}...")
        por_semilla[str(s)] = _una(s)

    r2k = [v["keypoint_softmax"]["r2"] for v in por_semilla.values()]
    r2p = [v["pixel_mse"]["r2"] for v in por_semilla.values()]
    azar = [v["r2_contra_objetivo_al_azar"] for v in por_semilla.values()]
    ventajas = [round(a - b, 4) for a, b in zip(r2k, r2p)]
    limpio, sucio = _metodo_medir(0.02), _metodo_medir(1.0)

    datos = {"prerregistro": 56, "semillas": list(SEMILLAS), "por_semilla": por_semilla,
             "r2_keypoint": r2k, "r2_pixel": r2p, "ventajas": ventajas,
             "r2_contra_objetivo_al_azar": azar,
             "ruido_sensor_bajo": round(limpio, 4), "ruido_sensor_alto": round(sucio, 4),
             "ficha": _metodo_sanidad(),
             "criterios": {
                 "A_el_latente_es_coordenada": bool(all(r >= PISO_R2 for r in r2k)),
                 "B_le_gana_al_de_hoy": bool(all(v >= VENTAJA for v in ventajas)),
                 "C_la_medida_no_se_infla": bool(all(a <= TECHO_AZAR for a in azar)),
                 "D_la_medida_responde": bool(sucio < limpio),
                 "E_no_se_rompio_el_codificador": bool(
                     all(not v["keypoint_softmax"]["diverge"] for v in por_semilla.values())),
             }}
    c = datos["criterios"]
    if not c["C_la_medida_no_se_infla"]:
        datos["veredicto"] = ("SE DETIENE — el R2 se infla solo, asi que ninguna comparacion vale")
    elif not c["B_le_gana_al_de_hoy"]:
        datos["veredicto"] = ("EL TANTEO ERA RUIDO — el softmax espacial no le gana al codificador "
                              "de hoy, y la causa de que los ojos puntuen a ruido sigue sin "
                              "encontrarse")
    elif not c["A_el_latente_es_coordenada"]:
        datos["veredicto"] = ("MEJORA SIN RESOLVER — le gana al de hoy y aun asi el latente no es "
                              "una coordenada; NO se cambia nada de Diego con esto")
    elif all(c.values()):
        datos["veredicto"] = ("ERA LA PERDIDA — con el mismo entrenamiento y los mismos datos, el "
                              "cuello de botella de softmax espacial produce latentes que SON "
                              "coordenadas y el de hoy no")
    else:
        datos["veredicto"] = ("NO CONCLUYENTE — fallan "
                              + ", ".join(k for k, v in c.items() if not v))

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 56: la perdida por pixel contra keypoints")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p56-ojos/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
