# atencion.py — GEN G8: LA ATENCIÓN — elegir solo importa cuando no puedes con todo.
# Construido el 8-ago-2026 por orden del director. REPARTE UN PRESUPUESTO, NO ELIGE OBJETIVOS:
# qué estudiar lo sigue diciendo la curiosidad (G2); la atención dice CUÁNTO de un presupuesto
# finito recibe cada frente. Sin escasez no hay atención — un bebé tiene fóvea estrecha y
# memoria de trabajo de 3-4 ítems, y ESA restricción es la que lo obliga a elegir bien.
#
# LA ECUACIÓN (compuesta de genes ya validados, no inventada aquí):
#
#     prioridad(region) = epistemica(region) · max(poder(region), piso)
#     reparto            ∝ prioridad, con cuota mínima de exploración
#
#   · epistemica (G14): ignorancia CURABLE — donde más se puede aprender.
#   · poder (G13): control real — donde además se puede INTERVENIR para aprender más rápido
#     (la lección del INFORME-30: mirar no basta; el que puede empujar, desambigua).
#   · La ALEATORIA no entra: gastar fóvea en azar es el televisor ruidoso. Ese canal queda
#     cerrado por construcción, no por parche.
#
# Regla 31: el televisor (varianza máxima, todo aleatorio) debe recibir ~cuota mínima; la región
# curable-y-controlable debe recibir la mayor parte; y con presupuesto sobrado NO se inventa
# escasez (todo recibe lo que necesita).

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def repartir(regiones, presupuesto, cuota_exploracion=0.05, piso_poder=0.05):
    """regiones: [{'id', 'epistemica', 'aleatoria', 'poder', 'coste'}]. Devuelve el reparto.
    'coste' = lo que consumiría atender la región del todo. Si el presupuesto alcanza para
    todos los costes, se asigna completo (la escasez no se finge)."""
    total_coste = sum(r["coste"] for r in regiones)
    if presupuesto >= total_coste:
        return [{"id": r["id"], "asignado": r["coste"], "fraccion": 1.0,
                 "nota": "sin escasez: atencion plena"} for r in regiones]
    prioridad = np.array([r["epistemica"] * max(r["poder"], piso_poder) for r in regiones])
    if prioridad.sum() <= 0:
        prioridad = np.ones(len(regiones))
    base = cuota_exploracion * presupuesto / len(regiones)     # nadie queda ciego del todo
    resto = presupuesto - base * len(regiones)
    pesos = prioridad / prioridad.sum()
    out = []
    for r, w in zip(regiones, pesos):
        asignado = min(base + resto * w, r["coste"])
        out.append({"id": r["id"], "asignado": round(float(asignado), 4),
                    "fraccion": round(float(asignado / r["coste"]), 4)})
    return out


def regla31(verbose=True):
    fallos = []
    regiones = [
        {"id": "curable_y_controlable", "epistemica": 0.8, "aleatoria": 0.1, "poder": 0.6, "coste": 10},
        {"id": "curable_sin_control",   "epistemica": 0.8, "aleatoria": 0.1, "poder": 0.0, "coste": 10},
        {"id": "televisor",             "epistemica": 0.05, "aleatoria": 2.0, "poder": 0.0, "coste": 10},
        {"id": "ya_aprendida",          "epistemica": 0.02, "aleatoria": 0.1, "poder": 0.7, "coste": 10},
    ]
    rep = {r["id"]: r["asignado"] for r in repartir(regiones, presupuesto=12)}
    c1 = rep["curable_y_controlable"] == max(rep.values())
    c2 = rep["televisor"] < rep["curable_y_controlable"] * 0.25
    c3 = rep["curable_sin_control"] > rep["televisor"]      # mirar sin manos > mirar ruido
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} la región curable Y controlable recibe lo máximo ({rep})")
        print(f"  {'ok  ' if c2 else 'FALLO'} el televisor recibe migajas aunque tenga la varianza máxima")
        print(f"  {'ok  ' if c3 else 'FALLO'} curable-sin-control > televisor (mirar aún vale algo)")
    for c, n in ((c1, "maximo"), (c2, "televisor"), (c3, "orden")):
        if not c:
            fallos.append(n)

    rep2 = repartir(regiones, presupuesto=100)
    c4 = all(r["fraccion"] == 1.0 for r in rep2)
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} con presupuesto sobrado NO finge escasez (todos al 100%)")
    if not c4:
        fallos.append("escasez_fingida")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la fóvea va donde se aprende y se puede actuar."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G8: atención — reparto de presupuesto finito")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (su cableado real a las corridas lo define un prerregistro)")
