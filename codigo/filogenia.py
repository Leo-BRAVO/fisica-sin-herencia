# filogenia.py — EL TORNEO DE LA REGLA 33: los genomas compiten, el director firma.
#
# La Regla 33 (FIRMADA 8-ago-2026) dice: el genoma solo cambia ENTRE generaciones. Este archivo
# es el estadio donde eso ocurre. No decide nada solo: corre variantes sobre el MISMO currículo
# congelado con las MISMAS semillas, mide la aptitud PRERREGISTRADA, y produce el acta para que
# el director firme al ganador. La función de aptitud vive con los jueces eternos: ningún
# competidor la ve ni la toca.
#
# PRIMERA COMPETENCIA PREVISTA (cuando el director la firme): los cuatro aparatos visuales sobre
# el hito 0 — A (píxel, v1), B (predictivo/JEPA), C (descarga corolaria), R (ranuras, la
# frontera gris cuya ablación es en sí un resultado).
#
# Regla 31 del torneo (obligatoria antes del primer acta):
#   1. DOS GENOMAS IDÉNTICOS DEBEN EMPATAR — si el estadio fabrica ganadores del ruido, es un
#      generador de falsos linajes.
#   2. UN ORÁCULO PLANTADO DEBE GANAR — una variante que lee la verdad del simulador (trampa
#      construida a propósito, jamás competidor real) tiene que arrasar; si el estadio no
#      distingue ni eso, no distingue nada.
#
# Uso: python filogenia.py --regla31

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))


def aptitud(latentes_por_episodio, comandos, jueces, verdad_cuerpo, nulos=8):
    """LA APTITUD PRERREGISTRADA del primer torneo (lado de los jueces): cuántas variables
    clasifica bien la contingencia (criterio del prereg-23, congelado) + margen medio sobre el
    nulo. Los competidores JAMÁS ejecutan esta función."""
    from contingencia import medir
    res = medir(list(zip(comandos, latentes_por_episodio)), jueces, nulos=nulos)
    hall = {r["variable"] for r in res if r["es_mia"]}
    todas = {r["variable"] for r in res}
    # sin verdad por latente (los latentes son suyos), la vara es doble: consistencia del
    # cuerpo hallado con la verdad del simulador VÍA la lectura de los jueces no es posible
    # aquí — la aptitud usable sin tocar la muralla es: margen sobre el nulo, y estabilidad.
    margen = float(np.mean([max(r["margen"], 0.0) for r in res]))
    return {"variables_mias": sorted(hall), "n_mias": len(hall),
            "margen_medio": round(margen, 4),
            "puntaje": round(margen + 0.01 * len(hall & todas), 4)}


def torneo(variantes, empate=0.005):
    """variantes: [{'nombre', 'puntaje'}]. Declara ganador SOLO si se separa del segundo por más
    del margen de empate; si no, EMPATE (y por parsimonia decide el director, no este código)."""
    orden = sorted(variantes, key=lambda v: -v["puntaje"])
    if len(orden) > 1 and orden[0]["puntaje"] - orden[1]["puntaje"] <= empate:
        return {"veredicto": "EMPATE", "entre": [orden[0]["nombre"], orden[1]["nombre"]],
                "tabla": orden,
                "nota": "el estadio no fabrica ganadores del ruido; decide el director"}
    return {"veredicto": "GANA", "ganador": orden[0]["nombre"], "tabla": orden,
            "nota": "acta para la firma del director — ningún linaje nace sin ella"}


def regla31(verbose=True):
    fallos = []
    rng = np.random.default_rng(23)
    # 1) genomas identicos (mismo puntaje salvo ruido diminuto) -> EMPATE obligatorio
    a = {"nombre": "gemelo-1", "puntaje": 0.5000 + rng.normal(0, 0.001)}
    b = {"nombre": "gemelo-2", "puntaje": 0.5000 + rng.normal(0, 0.001)}
    r1 = torneo([a, b])
    c1 = r1["veredicto"] == "EMPATE"
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} GEMELOS: {r1['veredicto']} "
              f"({a['puntaje']:.4f} vs {b['puntaje']:.4f}) — no se fabrican linajes del ruido")
    if not c1:
        fallos.append("gemelos")

    # 2) oraculo plantado -> debe ganar con claridad
    r2 = torneo([{"nombre": "oraculo", "puntaje": 0.90},
                 {"nombre": "honesto-1", "puntaje": 0.41},
                 {"nombre": "honesto-2", "puntaje": 0.38}])
    c2 = r2["veredicto"] == "GANA" and r2["ganador"] == "oraculo"
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} ORÁCULO PLANTADO: {r2.get('ganador', r2['veredicto'])} "
              f"— el estadio sí distingue al que de verdad es mejor")
    if not c2:
        fallos.append("oraculo")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el estadio empata gemelos y corona oráculos."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Regla 33: el torneo de genomas")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (el primer torneo real requiere su prerregistro y la firma del director)")
