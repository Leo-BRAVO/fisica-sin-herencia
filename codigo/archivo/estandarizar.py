# estandarizar.py — z-score por dimension con estadisticas SOLO del entrenamiento.
# Uso: python estandarizar.py <src> <dst> [--jueces 3 6 9]  (posiciones 1-indexadas)
import os
import sys
import glob
import argparse

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--jueces", nargs="+", type=int, default=[3, 6, 9])
a = ap.parse_args()
os.makedirs(a.dst, exist_ok=True)
csvs = sorted(glob.glob(os.path.join(a.src, "*.csv")))
jidx = {j - 1 for j in a.jueces}
cols = [c for c in pd.read_csv(csvs[0]).columns if c.startswith("s")]
tren = pd.concat([pd.read_csv(c)[cols] for i, c in enumerate(csvs) if i not in jidx])
mu, sd = tren.mean(), tren.std().replace(0, 1)
for c in csvs:
    df = pd.read_csv(c)
    df[cols] = (df[cols] - mu) / sd
    df.to_csv(os.path.join(a.dst, os.path.basename(c)), index=False)
print("estandarizados:", len(csvs), "->", a.dst)
