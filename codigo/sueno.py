# sueno.py — GEN G9: EL SUEÑO — consolidar lo vivido en menos bits, sin vivir nada nuevo.
# Construido el 8-ago-2026 por orden del director ("hagamos todo"). MIDE Y PROPONE, NO EJECUTA:
# sus propuestas van a la cola de estudios y las corre el latido — el sueño no toca el árbol.
#
# LA BIOLOGÍA (validada contra la literatura antes de escribir una línea):
#   1. REPETICIÓN PRIORIZADA: en el sueño se re-activan comprimidas las experiencias del día,
#      con probabilidad sesgada hacia lo más activado en vigilia (P(k|sueño) ∝ P(k|vigilia)^γ).
#   2. HOMEOSTASIS SINÁPTICA (Tononi): dormir REBAJA todas las sinapsis proporcionalmente —
#      se conserva lo relativo, se poda lo absoluto; sin eso la memoria satura.
#   Un humano sin sueño no consolida: acumula episodios que jamás se vuelven conocimiento.
#
# LA ADAPTACIÓN A DIEGO (la moneda de la casa es MDL — Regla 6):
#   El día de Diego produce CAMPAÑAS (episodios). Su sueño hace exactamente dos cosas:
#   1. RE-MINERÍA (repetición): busca pares (ley del conectoma, campaña vieja) donde una ley
#      MÁS SIMPLE descubierta después explicaría los mismos datos igual o mejor — y PROPONE el
#      re-análisis como item de cola. La prioridad = bits que se ahorrarían (γ nuestra: el
#      ahorro esperado, no la mera frecuencia).
#   2. PODA DECLARADA (homeostasis): señala redundancia — réplicas de memoria que dicen lo
#      mismo — para CONSOLIDAR en un resumen. El cuerpo es append-only: la poda es un resumen
#      añadido, jamás un borrado.
#
# Regla 31: sobre memorias sintéticas de verdad conocida — con una redundancia PLANTADA debe
# encontrarla; sobre una memoria sin nada que consolidar debe proponer NADA (un sueño que
# siempre sueña algo es un generador de trabajo falso, el televisor ruidoso de la gobernanza).

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mdl_ley(expr):
    """Bits aproximados de una expresión simbólica: longitud de su forma escrita.
    Es la vara de parsimonia de la casa (Regla 6), no una opinión."""
    return len(str(expr))


def sonar(leyes, campanas):
    """Una pasada de sueño. leyes: [{'id', 'expr', 'mse_en': {campana: mse}}] — lo que el
    conectoma sabe. campanas: [{'id', 'mejor_expr', 'mejor_mse'}] — lo vivido.
    Devuelve PROPUESTAS ordenadas por bits ahorrados. No ejecuta nada."""
    propuestas = []
    for c in campanas:
        for ley in leyes:
            mse_ahi = ley.get("mse_en", {}).get(c["id"])
            if mse_ahi is None:
                continue
            mas_simple = _mdl_ley(ley["expr"]) < _mdl_ley(c["mejor_expr"])
            no_peor = mse_ahi <= c["mejor_mse"] * 1.05
            if mas_simple and no_peor:
                ahorro = _mdl_ley(c["mejor_expr"]) - _mdl_ley(ley["expr"])
                propuestas.append({
                    "tipo": "re-analisis", "campana": c["id"], "ley_candidata": ley["id"],
                    "bits_ahorrados": ahorro,
                    "motivo": (f"la ley '{ley['id']}' ({_mdl_ley(ley['expr'])} bits) explicaría "
                               f"'{c['id']}' igual o mejor que su ley actual "
                               f"({_mdl_ley(c['mejor_expr'])} bits)")})
    propuestas.sort(key=lambda p: -p["bits_ahorrados"])
    return propuestas


def consolidar_memoria(registros, umbral=3):
    """Homeostasis: señala grupos de ≥umbral registros con el mismo (campana, tipo de hecho)
    para resumirlos en UNA línea de consolidación — que se AÑADE, no reemplaza."""
    from collections import Counter
    llaves = Counter((r.get("campana"), r.get("tipo", "registro")) for r in registros)
    return [{"campana": c, "tipo": t, "n": n,
             "propuesta": f"consolidar {n} registros de '{c}' ({t}) en un resumen añadido"}
            for (c, t), n in llaves.items() if n >= umbral]


def regla31(verbose=True):
    fallos = []
    # MUNDO 1: redundancia PLANTADA — la ley simple 'L1' explica la campaña 'c2' cuyo dueño
    # actual es una expresión largísima con el mismo error. El sueño DEBE encontrarla.
    leyes = [{"id": "L1", "expr": "v1*0.5", "mse_en": {"c2": 1.00}},
             {"id": "L2", "expr": "sin(v1*1.31)+cos(v2/0.77)*0.4412", "mse_en": {"c1": 9.9}}]
    campanas = [{"id": "c2", "mejor_expr": "sin(v1*1.31)+cos(v2/0.77)*0.4412-v3*0.0021",
                 "mejor_mse": 1.01},
                {"id": "c1", "mejor_expr": "v1*0.9", "mejor_mse": 0.5}]
    p = sonar(leyes, campanas)
    c1 = len(p) == 1 and p[0]["campana"] == "c2" and p[0]["ley_candidata"] == "L1"
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} REDUNDANCIA PLANTADA: la encuentra y solo esa "
              f"({[x['campana'] for x in p]})")
    if not c1:
        fallos.append("plantada")

    # MUNDO 2: nada que consolidar — leyes complejas o peores. Debe proponer NADA.
    leyes2 = [{"id": "L3", "expr": "sin(v1)*exp(v2)+v3*0.831", "mse_en": {"c3": 0.4}},
              {"id": "L4", "expr": "v1", "mse_en": {"c3": 99.0}}]     # simple pero PEOR
    p2 = sonar(leyes2, [{"id": "c3", "mejor_expr": "v1*0.5", "mejor_mse": 0.4}])
    c2 = len(p2) == 0
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} MEMORIA SANA: no inventa trabajo ({len(p2)} propuestas)")
    if not c2:
        fallos.append("inventa")

    # MUNDO 3: homeostasis — 5 registros repetidos deben señalarse; 2 sueltos no.
    regs = ([{"campana": "cX", "tipo": "medicion"}] * 5
            + [{"campana": "cY", "tipo": "medicion"}] * 2)
    cons = consolidar_memoria(regs)
    c3 = len(cons) == 1 and cons[0]["campana"] == "cX"
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} HOMEOSTASIS: consolida lo repetido y respeta lo suelto")
    if not c3:
        fallos.append("homeostasis")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — sueña donde hay algo y calla donde no."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G9: el sueño — consolidación por re-minería MDL")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (sus propuestas reales las cablea un prerregistro a la cola)")
