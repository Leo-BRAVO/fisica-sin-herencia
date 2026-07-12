# memoria.py — LA MEMORIA PROPIA DE LA MENTE (orden del director, 12-jul-2026).
# arbol/MEMORIA-MENTE.jsonl: registro de RECUERDOS en su idioma — que analizo, que ley
# encontro, cuanto le costo, que hueco le quedo. Append-only: los recuerdos no se borran.
# Uso:  python memoria.py --retro   (reconstruye recuerdos desde todos los resumenes existentes)
#       python memoria.py --ver     (muestra los ultimos recuerdos)

import os
import re
import json
import glob
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(BASE, "arbol", "MEMORIA-MENTE.jsonl")


def recordar(evento):
    with open(MEM, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")


def ya_recordado(campana):
    if not os.path.exists(MEM):
        return set()
    return {json.loads(l)["campana"] for l in open(MEM, encoding="utf-8") if l.strip()}


def retro():
    vistos = ya_recordado(None)
    nuevos = 0
    for res in sorted(glob.glob(os.path.join(BASE, "resultados", "*", "resumen.json")),
                      key=os.path.getmtime):
        campana = os.path.basename(os.path.dirname(res))
        if campana in vistos:
            continue
        r = json.load(open(res))
        try:
            mejor_id, mejor = min(r["semillas"].items(), key=lambda kv: kv[1]["mse_total"])
        except (KeyError, ValueError):
            continue
        base = r.get("mse_base")
        prop = (mejor["mse_total"] / base) if base else None
        leyes = mejor.get("ecuaciones", {})
        recuerdo = {
            "campana": campana,
            "replicas": len(r.get("replicas", [])) or None,
            "mi_mejor_esfuerzo": round(mejor["mse_total"], 6),
            "lo_trivial": round(base, 6) if base else None,
            "cuanto_mejore": round(1 - prop, 4) if prop is not None else None,
            "mis_frases": leyes if leyes else None,
            "hueco": bool(prop is not None and prop > 0.5),
        }
        recordar(recuerdo)
        nuevos += 1
    print(f"recuerdos nuevos: {nuevos} | memoria total: {sum(1 for _ in open(MEM, encoding='utf-8')) if os.path.exists(MEM) else 0}")


def ver(n=8):
    if not os.path.exists(MEM):
        print("sin recuerdos aun"); return
    lineas = [l for l in open(MEM, encoding="utf-8") if l.strip()][-n:]
    for l in lineas:
        r = json.loads(l)
        print(f"[{r['campana']}] mejora {r.get('cuanto_mejore')} | hueco: {r.get('hueco')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--retro", action="store_true")
    ap.add_argument("--ver", action="store_true")
    a = ap.parse_args()
    if a.retro:
        retro()
    if a.ver:
        ver()
