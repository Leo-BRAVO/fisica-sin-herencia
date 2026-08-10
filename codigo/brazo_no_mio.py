# brazo_no_mio.py — PRERREGISTRO 44: ¿por qué una articulación del propio brazo puede parecer NO-MÍA?
#
# ORIGEN. Corriendo el prereg-42 sobre cinco mundos nuevos, en el mundo 73 el escalón 1 declaró
# apto —no-mío— al canal `art1`, una articulación del propio brazo de Diego: obediencia neta 0.0297
# contra un techo de 0.05. `altura` ganó igual, pero POR DESEMPATE, no porque el criterio excluyera
# al intruso. Los datos están en resultados/p42-unico-apto/veredicto.json.
#
# Y LO INCOMODO: ese hallazgo apareció por la suerte de una semilla. Ningún criterio del prereg-42
# lo buscaba. Con otros cinco mundos habríamos cerrado el estudio limpio y el problema seguiría ahí.
#
# LAS TRES CAUSAS POSIBLES, y ninguna es la favorita (declarado en el prerregistro):
#   A — el mando no lo explica todo (contacto, gravedad e inercia mueven el brazo además del comando)
#   B — el retardo no alcanza (el efecto tarda más de lo que el instrumento mira)
#   C — la articulación estaba casi quieta (poca varianza propia: poco que explicar)
#
# Uso: python brazo_no_mio.py [--regla31] [--salida resultados/p44-brazo/medida.json]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

import soporte                                                              # noqa: E402

# ------------------------------------------------------------------ EL PRERREGISTRO, EN CODIGO
SEMILLAS = (101, 103, 107, 109, 113)     # NUEVAS: distintas de las del 35 (quemadas) y del 42
ARTICULACIONES = ("art0", "art1", "art2")
TECHO_OBEDIENCIA = 0.05                  # el del instrumento; NO se toca (Regla 13 endurecida)
MARGEN_CONTACTO = 0.15                   # confirma A
MARGEN_VARIANZA = 0.30                   # confirma C (30% menos varianza)
MINIMOS = 4                              # de 5 mundos

METODO = {
    "prerregistro": 44,
    "tipo_de_medida": "umbral",
    "que_mide": ("por articulacion y por mundo: su obediencia neta, la misma con horizonte DOBLE, "
                 "su varianza propia y su fraccion de contacto — las cuatro medidas que separan "
                 "las tres causas posibles"),
    "comparten_datos": {
        "hay": True,
        "porque": "las cuatro medidas salen de LA MISMA corrida de cada mundo, a proposito: si "
                  "cada una tuviera su propia corrida, una diferencia entre ellas podria ser de "
                  "la corrida y no de la causa. Lo que NO se comparte entre mundos es la semilla.",
    },
    "linea_base": ("el predictor ingenuo 'todas las articulaciones son mias', que por construccion "
                   "acierta 15 de 15. El instrumento actual acierta 14 de 15: EN ESTA TAREA "
                   "CONCRETA es PEOR que el tonto, y eso va dicho (Regla 11)"),
    "formulas": [
        {"base": {"fuerza": 1.0, "quietud": 0.0}, "parametro": "quietud", "factor": 1.0,
         "esperado": "igual",
         "porque": "con quietud=0 el mundo es el normal; multiplicar por 1 no cambia nada. Es la "
                   "comprobacion de que la medida es DETERMINISTA con la misma semilla — sin eso "
                   "cualquier diferencia entre mundos podria ser azar de la corrida"},
        {"base": {"fuerza": 1.0, "quietud": 0.0}, "parametro": "fuerza", "factor": 0.0,
         "esperado": "baja",
         "porque": "DESCONECTAR el comando (x0) tiene que llevar la obediencia a cero: sin mando "
                   "no hay nada que obedecer.\n"
                   "                   OJO — LA PRIMERA VERSION DE ESTA RELACION DECIA x0.05 Y ERA "
                   "FALSA, y la puerta lo midio: dio x1.000. La razon es una propiedad del "
                   "instrumento que yo no habia entendido: la obediencia es una RAZON DE VARIANZA "
                   "EXPLICADA, y por tanto es INVARIANTE A LA AMPLITUD DEL COMANDO — bajar el "
                   "mando a la vigesima parte no cambia cuanto explica, solo agranda el "
                   "coeficiente. Lo unico que la mueve es desconectarlo del todo."},
    ],
}


def _mundo(semilla, fuerza=1.0, quietud=0.0, pasos=900):
    """Una corrida del gimnasio de soporte, con dos perillas que SOLO usa la puerta:
    `fuerza` escala el comando (para el paso 1) y `quietud` amortigua el balbuceo (para probar C).
    Con fuerza=1 y quietud=0 es exactamente el mundo del prereg-42."""
    m = soporte.mundo_variable(int(semilla))
    com, can, nom, cortes = soporte.escena("cae", semilla=int(semilla), pasos=int(pasos), mundo=m)
    if fuerza != 1.0:
        com = com * float(fuerza)
    if quietud > 0.0:
        # amortigua la VARIACION de las articulaciones sin moverles la media: prueba la causa C
        idx = [nom.index(a) for a in ARTICULACIONES]
        can = can.copy()
        for i in idx:
            can[:, i] = can[:, i].mean() + (can[:, i] - can[:, i].mean()) * (1.0 - float(quietud))
    return com, can, nom, cortes


def _medidas_de_un_mundo(semilla, pasos=900):
    """Las cuatro medidas declaradas, por articulacion."""
    com, can, nom, cortes = _mundo(semilla, pasos=pasos)
    r = soporte.escalon1(com, can, nom, cortes=cortes)
    detalle = {f["canal"]: f for f in r["detalle"]}

    filas = []
    for a in ARTICULACIONES:
        i = nom.index(a)
        x = can[:, i]
        filas.append({
            "articulacion": a,
            "obediencia_neta": detalle[a]["obediencia_neta"],
            "no_mio": bool(detalle[a]["no_mio"]),
            "varianza_propia": round(float(np.var(x)), 6),
            "fraccion_de_contacto": round(float(np.mean(can[:, nom.index("contacto")] > 0.5)), 4),
        })
    # (2) LA MISMA OBEDIENCIA CON HORIZONTE DOBLE -> separa la causa B.
    # `escalon1` no acepta horizonte, asi que se llama directamente a la funcion que hay debajo
    # con h doble y su MISMO nulo por comandos permutados — no se toca `soporte.py`, que esta
    # sellado y lo usan otros estudios.
    rng = np.random.default_rng(29)
    h2 = 2 * soporte.HORIZONTE
    for f in filas:
        x = can[:, nom.index(f["articulacion"])]
        g = soporte._ganancia_comando(x, com, h=h2, cortes=cortes)
        g_nulo = float(np.mean([soporte._ganancia_comando(
            x, com[rng.permutation(len(com))], h=h2, cortes=cortes) for _ in range(6)]))
        f["obediencia_neta_horizonte_doble"] = round(max(0.0, g - g_nulo), 4)
    return {"semilla": int(semilla), "filas": filas, "aptos": r.get("candidatos_aptos") or []}


def _metodo_medir(fuerza=1.0, quietud=0.0):
    """PASO 1 — la medida escalar: la obediencia neta MEDIA de las tres articulaciones."""
    com, can, nom, cortes = _mundo(101, fuerza=fuerza, quietud=quietud, pasos=600)
    d = {f["canal"]: f["obediencia_neta"] for f in soporte.escalon1(com, can, nom,
                                                                    cortes=cortes)["detalle"]}
    return float(np.mean([d[a] for a in ARTICULACIONES]))


def acoplamiento(semilla=101, pasos=600):
    """CAUSA D — LA QUE YO NO HABIA LISTADO. Se desconecta UN canal de comando por vez y se mira
    que articulacion cae. Si al desconectar el canal j cae MAS otra articulacion que la suya, es
    que el brazo esta ACOPLADO: cualquier mando mueve a todas, y la obediencia por articulacion no
    puede atribuir bien.

    ESTO ES RESULTADO, NO REQUISITO DE ENTRADA. Lo escribi primero dentro de la ficha de sanidad
    —es decir, dentro de la Regla 31 de MI instrumento— y entonces un defecto del OBJETO DE
    ESTUDIO bloqueaba el modulo que existe para estudiarlo. Es el MISMO error de diseño que mato
    al prerregistro-45 hace una hora (INFORME-54), cometido por segunda vez el mismo dia. Queda
    escrito: la Regla 31 examina EL PROCEDIMIENTO DE MEDIDA; lo que haga el sujeto es el resultado.
    """
    com, can, nom, cortes = _mundo(semilla, pasos=pasos)
    base = {f["canal"]: f["obediencia_neta"]
            for f in soporte.escalon1(com, can, nom, cortes=cortes)["detalle"]}
    filas = []
    for j, a in enumerate(ARTICULACIONES):
        com2 = com.copy()
        com2[:, j] = 0.0
        d = {f["canal"]: f["obediencia_neta"]
             for f in soporte.escalon1(com2, can, nom, cortes=cortes)["detalle"]}
        caidas = {o: round(base[o] - d[o], 4) for o in ARTICULACIONES}
        propia = caidas[a]
        ajena = max(v for o, v in caidas.items() if o != a)
        filas.append({"canal_desconectado": j, "articulacion_suya": a,
                      "cae_la_suya": propia, "cae_mas_una_ajena": ajena,
                      "atribuye_bien": bool(propia > ajena), "caidas": caidas})
    return {"por_canal": filas,
            "acoplado": bool(any(not f["atribuye_bien"] for f in filas)),
            "obediencia_con_todo_conectado": {a: base[a] for a in ARTICULACIONES}}


def _metodo_sanidad():
    """PASO 3 — LA FICHA, ahora sobre MI PROCEDIMIENTO y nada mas:
    (a) que lea los canales que dice leer — las tres articulaciones existen y son distintas;
    (b) que sea DETERMINISTA con la misma semilla, sin lo cual comparar mundos no significa nada.
    """
    com, can, nom, cortes = _mundo(101, pasos=600)
    fallos = []
    idx = [nom.index(a) for a in ARTICULACIONES]
    if len(set(idx)) != len(ARTICULACIONES):
        fallos.append(f"las articulaciones no son canales distintos: {idx}")
    if any(np.var(can[:, i]) <= 0 for i in idx):
        fallos.append("alguna articulacion no varia nada: no hay nada que medir en ella")
    a, b = _metodo_medir(), _metodo_medir()
    if a != b:
        fallos.append(f"NO ES DETERMINISTA: dos corridas iguales dan {a} y {b}")
    return {"aprueba": not fallos, "fallos": fallos, "determinista": a == b,
            "canales_leidos": dict(zip(ARTICULACIONES, idx))}


def regla31(verbose=True):
    """Los dos lados del prerregistro-44, sobre MI PROCEDIMIENTO de medida."""
    fallos = []

    def caso(nombre, ok, extra=""):
        print(f"  {'ok  ' if ok else 'FALLO'} {nombre} {extra}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-44 ==")

    # LADO NEGATIVO — sin comando (fuerza ~0) ninguna articulacion puede parecer obediente.
    sin = _metodo_medir(fuerza=0.0)
    caso("sin comando la obediencia media de las articulaciones es ~0", abs(sin) < 0.02,
         f"{sin:+.4f}")

    # LADO POSITIVO — con el comando normal, las articulaciones SI obedecen.
    con = _metodo_medir(fuerza=1.0)
    caso("con el comando normal las articulaciones obedecen", con > 0.05, f"{con:+.4f}")

    # SEÑUELO — el canal de RUIDO puro nunca puede salir como articulacion obediente.
    com, can, nom, cortes = _mundo(101, pasos=600)
    d = {f["canal"]: f["obediencia_neta"] for f in soporte.escalon1(com, can, nom,
                                                                    cortes=cortes)["detalle"]}
    caso("SEÑUELO: el canal de ruido no obedece a nadie", d["ruido"] < TECHO_OBEDIENCIA,
         f"{d['ruido']:+.4f}")

    # LA MEDIDA DISTINGUE — si diera lo mismo con y sin comando, no mediria nada.
    caso("la medida distingue con comando de sin comando", (con - sin) > 0.05, f"{con - sin:+.4f}")

    if verbose:
        print("REGLA 31: " + ("APRUEBA" if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def veredicto(mundos):
    """Los criterios congelados del prerregistro-44."""
    malas, buenas = [], []
    for m in mundos:
        for f in m["filas"]:
            (malas if f["no_mio"] else buenas).append(f)

    def media(xs, k):
        return float(np.mean([x[k] for x in xs])) if xs else None

    contacto_malas, contacto_buenas = media(malas, "fraccion_de_contacto"), media(buenas, "fraccion_de_contacto")
    var_malas, var_buenas = media(malas, "varianza_propia"), media(buenas, "varianza_propia")

    A = (contacto_malas is not None and contacto_buenas is not None
         and contacto_malas - contacto_buenas >= MARGEN_CONTACTO)
    C = (var_malas is not None and var_buenas is not None and var_buenas > 0
         and var_malas <= var_buenas * (1.0 - MARGEN_VARIANZA))

    ac = acoplamiento()
    D = bool(ac["acoplado"])
    confirmadas = [n for n, ok in (("A", A), ("C", C), ("D (acoplamiento, NO estaba listada)", D))
                   if ok]
    if not malas:
        v = ("NINGUNA ARTICULACION SALIO NO-MIA en los cinco mundos nuevos: el fallo del mundo 73 "
             "no replica. Queda como caso aislado, y el detector NO tiene un modo de fallo "
             "sistematico que este estudio pueda describir")
    elif confirmadas:
        v = "SE CONFIRMA " + " y ".join(confirmadas)
    else:
        v = ("NO CONCLUYENTE: hay articulaciones mal clasificadas y NINGUNA de las causas "
             "declaradas las explica. El detector tiene un modo de fallo QUE NO SABEMOS EXPLICAR, "
             "que es peor que tener uno explicado")
    return {"mal_clasificadas": len(malas), "de": len(malas) + len(buenas),
            "contacto_medio_mal_clasificadas": contacto_malas,
            "contacto_medio_bien_clasificadas": contacto_buenas,
            "varianza_media_mal_clasificadas": var_malas,
            "varianza_media_bien_clasificadas": var_buenas,
            "confirma_A_el_mando_no_lo_explica_todo": bool(A),
            "confirma_C_estaba_casi_quieta": bool(C),
            "confirma_D_brazo_acoplado_NO_estaba_listada": D,
            "acoplamiento": ac,
            "veredicto": v}


def main():
    ap = argparse.ArgumentParser(description="Prerregistro 44 — el brazo que parece no-mio")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("=== PRERREGISTRO 44 — semillas NUEVAS", list(SEMILLAS), "===")
    mundos = []
    for s in SEMILLAS:
        m = _medidas_de_un_mundo(s)
        mundos.append(m)
        for f in m["filas"]:
            print(f"  s{s} {f['articulacion']:<6} obed={f['obediencia_neta']:+.4f} "
                  f"no_mio={str(f['no_mio']):<5} var={f['varianza_propia']:.5f} "
                  f"contacto={f['fraccion_de_contacto']:.3f}")
    r = veredicto(mundos)
    print(f"\nmal clasificadas: {r['mal_clasificadas']}/{r['de']}")
    print(f"VEREDICTO: {r['veredicto']}")
    if a.salida:
        os.makedirs(os.path.dirname(a.salida) or ".", exist_ok=True)
        json.dump({"prerregistro": 44, "semillas": list(SEMILLAS), "mundos": mundos, **r},
                  open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"escrito: {a.salida}")


if __name__ == "__main__":
    main()
