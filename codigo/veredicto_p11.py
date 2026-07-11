# veredicto_p11.py — evaluación del prerregistro-11 (péndulo doble Morpheus)
# Nivel A: por señal, umbral = max(50% base trivial de la señal, 3× piso mediano)
# Nivel B: acople canónico — gradientes de las ecuaciones de un cuerpo respecto a señales del otro
import os
import sys
import json
import glob

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))
from descubrir import preparar
from autopsia import evaluar, piso_de_ruido
from canonizar import tarjeta

DATOS = os.path.join(BASE, "datos", "procesados", "dp_morpheus")
OUT = os.path.join(BASE, "resultados", "dp-morpheus")

csvs = sorted(glob.glob(os.path.join(DATOS, "*.csv")))
jidx = {2, 5, 8}
Xtr, Ytr, Xte, Yte = [], [], [], []
pisos = [[] for _ in range(4)]
for i, c in enumerate(csvs):
    X, Y = preparar(c)
    df = pd.read_csv(c)
    for j in range(4):
        pisos[j].append(piso_de_ruido(df[f"s{j+1}"].to_numpy(float)))
    (Xte if i in jidx else Xtr).append(X)
    (Yte if i in jidx else Ytr).append(Y)
X_tr, Y_tr = np.vstack(Xtr), np.vstack(Ytr)
X_te, Y_te = np.vstack(Xte), np.vstack(Yte)

print("=== NIVEL A (por señal, umbral informado por piso) ===")
umbrales = []
for j in range(4):
    vel = float(np.mean((X_te[:, j] + X_te[:, j + 4] - Y_te[:, j]) ** 2))
    med = float(np.mean((Y_tr[:, j].mean() - Y_te[:, j]) ** 2))
    piso = float(np.median(pisos[j]))
    u = max(0.5 * min(vel, med), 3 * piso)
    umbrales.append(u)
    print(f"  s{j+1}: base={min(vel,med):.1f} piso={piso:.1f} -> umbral={u:.1f}")

exitosas = []
for f in sorted(glob.glob(os.path.join(OUT, "semilla_*.json"))):
    r = json.load(open(f))
    sigs = [k for k in r if k != "mse_total"]
    oks = [r[s]["mse_test"] < umbrales[j] for j, s in enumerate(sigs)]
    ok = all(oks)
    if ok:
        exitosas.append(f)
    print(f"  {os.path.basename(f)}: " + " ".join(f"s{j+1}={r[s]['mse_test']:.0f}{'✓' if o else '✗'}"
          for j, (s, o) in enumerate(zip(sigs, oks))) + f"  -> {'EXITO' if ok else 'no'}")
print(f"Nivel A: {len(exitosas)}/5 (exigido 3/5) -> {'CUMPLIDO' if len(exitosas) >= 3 else 'FRACASO'}")

print("\n=== NIVEL B (acople canónico entre cuerpos) ===")
# cuerpo 1 = s1,s2 (vars v1,v2 + cambios v5,v6); cuerpo 2 = s3,s4 (v3,v4 + v7,v8)
otro = {0: [2, 3, 6, 7], 1: [2, 3, 6, 7], 2: [0, 1, 4, 5], 3: [0, 1, 4, 5]}
con_acople = 0
for f in exitosas:
    r = json.load(open(f))
    sigs = [k for k in r if k != "mse_total"]
    acoples = []
    for j, s in enumerate(sigs):
        t = tarjeta(r[s]["ecuacion"], 8)
        g = t.get("gradiente", [0] * 8)
        cruzados = [abs(g[i]) for i in otro[j]]
        acoples.append(max(cruzados) if cruzados else 0.0)
    tiene = any(a > 0.001 for a in acoples)
    con_acople += tiene
    print(f"  {os.path.basename(f)}: max acople cruzado por señal = {[round(a,4) for a in acoples]} "
          f"-> {'ACOPLE' if tiene else 'sin acople'}")
print(f"Nivel B: {con_acople}/{len(exitosas)} semillas exitosas con acople canónico")
