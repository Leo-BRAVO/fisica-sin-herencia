# veredicto_p09.py — evaluación por señal del prerregistro-09 (caída libre)
import os
import re
import json
import glob

import numpy as np
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))
from descubrir import preparar

CAIDA = os.path.join(BASE, "datos", "procesados", "caida")
OUT = os.path.join(BASE, "resultados", "caida-libre-p09")

csvs = sorted(glob.glob(os.path.join(CAIDA, "*.csv")))
jueces_idx = {2, 6, 10}
Xtr, Ytr, Xte, Yte = [], [], [], []
for i, c in enumerate(csvs):
    X, Y = preparar(c)
    (Xte if i in jueces_idx else Xtr).append(X)
    (Yte if i in jueces_idx else Ytr).append(Y)
X_tr, Y_tr = np.vstack(Xtr), np.vstack(Ytr)
X_te, Y_te = np.vstack(Xte), np.vstack(Yte)

# Base trivial POR SEÑAL v2 (columna 1): mejor entre velocidad y media, solo sobre v2
mse_vel_v2 = float(np.mean((X_te[:, 1] + X_te[:, 3] - Y_te[:, 1]) ** 2))
mse_med_v2 = float(np.mean((Y_tr[:, 1].mean() - Y_te[:, 1]) ** 2))
base_v2 = min(mse_vel_v2, mse_med_v2)
umbral_v2 = 0.5 * base_v2
print(f"Base v2 (vel={mse_vel_v2:.1f}, media={mse_med_v2:.1f}) -> base={base_v2:.1f} | umbral v2 < {umbral_v2:.1f}")

exitosas, constantes = 0, []
for f in sorted(glob.glob(os.path.join(OUT, "semilla_*.json"))):
    s = json.load(open(f))
    mse_v2 = s["v2_sig"]["mse_test"]
    eq = s["v2_sig"]["ecuacion"]
    ok = mse_v2 < umbral_v2
    exitosas += ok
    # constante aditiva: números al nivel superior de la expresión (heurística: candidatos 10-30 en valor absoluto)
    consts = [abs(float(c)) for c in re.findall(r"-?\d+\.\d+", eq) if 5 < abs(float(c)) < 40]
    if ok and consts:
        constantes.append(max(consts))
    print(f"{os.path.basename(f)}: mse_v2={mse_v2:.1f} {'EXITO' if ok else 'no'} | {eq[:80]}")

print(f"\nNivel A por señal: {exitosas}/5 (exigido 3/5) -> {'CUMPLIDO' if exitosas >= 3 else 'FRACASO'}")
if constantes:
    cv = np.std(constantes) / np.mean(constantes)
    print(f"Nivel B: constantes en semillas exitosas: {[round(c,3) for c in constantes]} | "
          f"media={np.mean(constantes):.3f} | variacion={cv*100:.1f}% (exigido <10%) -> "
          f"{'CUMPLIDO' if cv < 0.10 and exitosas >= 3 else 'no cumplido'}")
