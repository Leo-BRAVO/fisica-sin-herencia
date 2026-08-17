# ojos_brazo.py — EL BRAZO DELGADO (prerregistro-57, 11-ago-2026).
#
# CONTINUACION DIRECTA DEL INFORME-66, que cerro con esta pregunta: "¿cambia todo esto con un brazo
# articulado en vez de un disco? La escena de juguete tiene un objeto compacto y brillante — el
# caso FACIL para cualquier codificador. La critica externa señalaba las ARTICULACIONES DELGADAS,
# y esa escena no las tiene."
#
# El prerregistro-56 midio el caso facil y el margen que declare no se cumplio por 0.044 en una
# semilla de cinco. Este mide EL CASO DIFICIL, que ademas es EL QUE DIEGO TIENE DE VERDAD: su
# gimnasio es un brazo articulado, no un disco.
#
# LO QUE SE REUTILIZA Y POR QUE. Las dos arquitecturas, el entrenamiento y la medida se IMPORTAN de
# `ojos_keypoint.py` en vez de copiarse. Si los copiara, cualquier diferencia entre los dos
# estudios podria venir de la copia y no de la escena — y la escena es LO UNICO que debe cambiar.
# Es la misma razon por la que sindy4 importa la forma debil de sindy3.
#
# Uso: python ojos_brazo.py [--regla31] [--salida resultados/p57-brazo/medida.json]

import os
import sys
import json
import argparse

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ojos_keypoint as OK                                                  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# QUE ESTUDIA: las dos arquitecturas. Su regla31() NO las entrena — trabaja con latentes
# sinteticos. Examinar al sujeto dentro de mi Regla 31 dejo NULO al prerregistro-45.
SUJETO = ("Pixel", "Keypoint")

T, N = 600, 32
SEMILLAS = (251, 257, 263, 269, 271)   # NUEVAS. Quemadas: 211,223 (banco) y 227,229,233,239,241
TECHO_DELGADO = 0.04     # criterio A: el brazo ocupa menos del 4% de los pixeles
VENTAJA_DEL_DISCO = 0.2693   # criterio B: el MAXIMO que dio el disco en el INFORME-66
TECHO_AZAR = 0.10

METODO = {
    "prerregistro": 57,
    "tipo_de_medida": "continua",
    "que_mide": ("cuanta de la posicion VERDADERA del extremo del brazo se recupera linealmente "
                 "del latente, fuera de muestra, con cada uno de los dos cuellos de botella"),
    "comparten_datos": {
        "hay": True,
        "porque": "las dos arquitecturas se entrenan sobre EXACTAMENTE la misma escena y la misma "
                  "semilla — esa es la definicion de la comparacion. Si cada una tuviera su "
                  "propia escena, la diferencia podria ser de la escena.",
    },
    "linea_base": ("el codificador de HOY, pixel_mse — el mismo rival que en el prerregistro-56, "
                   "y por la misma razon: es exactamente lo que Diego usa, no un rival de paja "
                   "(Regla 11)"),
    "formulas": [
        {"base": {"ruido_sensor": 0.02}, "parametro": "ruido_sensor", "factor": 50.0,
         "esperado": "baja",
         "porque": "el ruido de SENSOR se suma a los fotogramas ya generados; con desviacion al "
                   "doble del contraste del brazo, este deja de ser distinguible del fondo y la "
                   "posicion recuperable tiene que caer. El factor sale del MECANISMO —el "
                   "contraste, que conozco porque yo dibujo la escena— y no de mi intuicion: "
                   "elegirlo a ojo ya me reprobo la puerta una vez (enmienda 1 del "
                   "prerregistro-56). Base 0.02 y NO 0.0, porque comparar un cero con otro cero "
                   "no prueba nada"},
    ],
}


def _linea(lienzo, x0, y0, x1, y1, valor=1.0):
    """Dibuja un segmento de UN PIXEL de grosor. Delgado a proposito: es el caso que la critica
    señalaba y el que el disco del prerregistro-56 no tenia."""
    n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for t in np.linspace(0, 1, n):
        xx, yy = int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t))
        if 0 <= yy < lienzo.shape[0] and 0 <= xx < lienzo.shape[1]:
            lienzo[yy, xx] = valor


def escena(semilla=251, ruido_sensor=0.0):
    """Brazo de DOS SEGMENTOS DELGADOS sobre fondo con textura. Los dos angulos se mueven a
    frecuencias distintas para que el extremo recorra una figura no trivial. La verdad —la
    posicion del extremo— la ponemos nosotros y SOLO SE USA PARA EVALUAR."""
    rng = np.random.default_rng(int(semilla))
    fondo = rng.normal(0.5, 0.15, (N, N)).astype(np.float32)
    t = np.arange(T) * 0.05
    a1 = 0.9 * t + rng.uniform(0, 2 * np.pi)
    a2 = 1.4 * t + rng.uniform(0, 2 * np.pi)
    bx, by = N / 2.0, N / 2.0
    L1 = L2 = 6.0
    cx = bx + L1 * np.cos(a1)
    cy = by + L1 * np.sin(a1)
    ex = cx + L2 * np.cos(a1 + a2)
    ey = cy + L2 * np.sin(a1 + a2)
    vids = np.tile(fondo, (T, 1, 1))
    for i in range(T):
        _linea(vids[i], bx, by, cx[i], cy[i])
        _linea(vids[i], cx[i], cy[i], ex[i], ey[i])
    if ruido_sensor:
        vids = vids + rng.normal(0, float(ruido_sensor), vids.shape).astype(np.float32)
    return vids[:, None, :, :], np.stack([ex, ey], 1).astype(np.float32)


def fraccion_de_brazo(semilla=251):
    """Que fraccion de los pixeles ocupa el brazo. Criterio A: si no es delgado, no es el caso
    dificil y el estudio se detiene."""
    v, _ = escena(semilla)
    return float((v > 0.99).mean())


def _una(semilla, ruido_sensor=0.0):
    vids, verdad = escena(semilla, ruido_sensor=ruido_sensor)
    X = torch.tensor(vids)
    out = {}
    for nombre, M in (("pixel_mse", OK.Pixel()), ("keypoint_softmax", OK.Keypoint())):
        m, perdida = OK.entrenar(M, X, semilla=semilla)
        with torch.no_grad():
            Z = m.z(X).numpy()
        out[nombre] = {"r2": round(OK.r2_lineal(Z, verdad), 4),
                       "perdida_final": round(float(perdida), 6),
                       "diverge": not np.isfinite(perdida)}
        if nombre == "keypoint_softmax":
            rng = np.random.default_rng(int(semilla) + 7000)
            out["r2_contra_objetivo_al_azar"] = round(
                OK.r2_lineal(Z, rng.normal(size=verdad.shape)), 4)
    return out


def _metodo_medir(ruido_sensor=0.02):
    """PASO 1 — la medida escalar: el R2 del softmax espacial sobre una semilla de trabajo."""
    return float(_una(SEMILLAS[0], ruido_sensor=float(ruido_sensor))["keypoint_softmax"]["r2"])


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿es esta escena de verdad el caso dificil?** Si el brazo
    ocupara tantos pixeles como el disco, este estudio seria el anterior con otro nombre."""
    fallos = []
    fr = fraccion_de_brazo()
    if fr >= TECHO_DELGADO:
        fallos.append(f"el brazo ocupa {fr:.4f} de los pixeles: no es delgado y esto no es el "
                      f"caso dificil")
    _, verdad = escena()
    if float(np.std(verdad)) < 1.0:
        fallos.append("el extremo del brazo apenas se mueve: no hay posicion que recuperar")
    return {"aprueba": not fallos, "fallos": fallos,
            "fraccion_de_pixeles_del_brazo": round(fr, 4),
            "desviacion_del_extremo": round(float(np.std(verdad)), 3)}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados, con latentes SINTETICOS.

    Aqui NO se entrena ninguna arquitectura: eso es el resultado que este estudio existe para
    medir, y meterlo haria que el criterio B no pudiera fallar."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-57: la escena y la medida, no las arquitecturas ==")

    fs = _metodo_sanidad()
    caso("CONTROL POSITIVO: la escena es el CASO DIFICIL (brazo delgado que se mueve)",
         fs["aprueba"], str(fs))

    _, verdad = escena()
    caso("CONTROL POSITIVO: la medida reconoce un latente que ES la posicion del extremo",
         OK.r2_lineal(verdad + np.random.default_rng(57).normal(0, 0.01, verdad.shape),
                      verdad) >= 0.9)
    caso("SEÑUELO: contra ruido puro el R2 no se infla",
         OK.r2_lineal(np.random.default_rng(571).normal(size=(T, 8)), verdad) <= TECHO_AZAR)

    caso("la lista de semillas NO esta vacia", len(SEMILLAS) > 0)
    caso("ninguna semilla de este estudio se uso antes",
         not (set(SEMILLAS) & {211, 223, 227, 229, 233, 239, 241}))

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la escena es el caso dificil y la medida distingue."
                                 if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    fs = _metodo_sanidad()
    por_semilla = {}
    for s in SEMILLAS:
        if verbose:
            print(f"  semilla {s}...")
        por_semilla[str(s)] = _una(s)

    r2k = [v["keypoint_softmax"]["r2"] for v in por_semilla.values()]
    r2p = [v["pixel_mse"]["r2"] for v in por_semilla.values()]
    azar = [v["r2_contra_objetivo_al_azar"] for v in por_semilla.values()]
    ventajas = [round(a - b, 4) for a, b in zip(r2k, r2p)]
    media = round(float(np.mean(ventajas)), 4)
    limpio, sucio = _metodo_medir(0.02), _metodo_medir(1.0)

    datos = {"prerregistro": 57, "semillas": list(SEMILLAS), "por_semilla": por_semilla,
             "r2_keypoint": r2k, "r2_pixel": r2p, "ventajas": ventajas,
             "ventaja_media": media, "ventaja_maxima_del_disco_INFORME_66": VENTAJA_DEL_DISCO,
             "r2_contra_objetivo_al_azar": azar,
             "ruido_sensor_bajo": round(limpio, 4), "ruido_sensor_alto": round(sucio, 4),
             "escena": fs,
             "criterios": {
                 "A_el_brazo_es_delgado": bool(fs["aprueba"]),
                 "B_la_ventaja_crece": bool(media > VENTAJA_DEL_DISCO),
                 "C_la_medida_no_se_infla": bool(all(a <= TECHO_AZAR for a in azar)),
                 "D_la_medida_responde": bool(sucio < limpio),
                 "E_ninguno_diverge": bool(all(not v[k]["diverge"] for v in por_semilla.values()
                                               for k in ("pixel_mse", "keypoint_softmax"))),
             }}
    c = datos["criterios"]
    if not c["A_el_brazo_es_delgado"]:
        datos["veredicto"] = "SE DETIENE — la escena no es el caso dificil"
    elif not c["C_la_medida_no_se_infla"]:
        datos["veredicto"] = "SE DETIENE — el R2 se infla solo y ninguna comparacion vale"
    elif not c["B_la_ventaja_crece"]:
        datos["veredicto"] = ("NO ES LA CAUSA — con un brazo delgado la ventaja NO supera la del "
                              "disco, asi que la perdida por pixel no explica la ceguera de Diego "
                              "y hay que buscarla en otro sitio")
    elif all(c.values()):
        datos["veredicto"] = ("ERA EL BRAZO DELGADO — la ventaja del cuello de botella espacial "
                              "CRECE cuando el objeto es delgado, que es el caso que Diego tiene")
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
    ap = argparse.ArgumentParser(description="Prerregistro 57: el brazo delgado")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p57-brazo/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
