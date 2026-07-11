# autopsia.py — Mejoras #1 y #2 (aprobadas 11-jul-2026): tras cada corrida, diagnosticar
# DÓNDE falla la mejor fórmula y contra qué piso de ruido compite.
# Uso: python autopsia.py <outdir_con_semillas> <carpeta_csvs_o_csv> [--jueces 3 7 11]
#
# Produce autopsia.json en el outdir y un parte en español llano:
#   - piso de ruido por señal (estimado ANTES de mirar la fórmula, con segundas diferencias)
#   - error de la mejor semilla por señal y por video juez
#   - dónde falla: correlación del error con la magnitud del cambio, y por tercios temporales

import os
import re
import sys
import json
import glob
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descubrir import preparar


def evaluar(eq, X):
    ns = {f"v{i+1}": X[:, i] for i in range(X.shape[1])}
    ns.update({"sin": np.sin, "cos": np.cos, "exp": np.exp, "sqrt": np.sqrt,
               "square": lambda x: x * x})
    return eval(eq, {"__builtins__": {}}, ns)


def piso_de_ruido(y):
    # Estimador por segundas diferencias: para señal suave + ruido iid, var(Δ²y) ≈ 6·var(ruido)
    d2 = np.diff(y, n=2)
    return float(np.var(d2) / 6.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("datos")
    ap.add_argument("--jueces", nargs="+", type=int, default=None)
    args = ap.parse_args()

    if os.path.isdir(args.datos):
        csvs = sorted(glob.glob(os.path.join(args.datos, "*.csv")))
        jidx = {j - 1 for j in (args.jueces or [])}
        jueces = [(os.path.basename(c), *preparar(c)) for i, c in enumerate(csvs) if i in jidx] \
            or [(os.path.basename(c), *preparar(c)) for c in csvs]
    else:
        jueces = [(os.path.basename(args.datos), *preparar(args.datos))]

    semillas = sorted(glob.glob(os.path.join(args.outdir, "semilla_*.json")))
    mejor = min((json.load(open(f)) for f in semillas), key=lambda r: r["mse_total"])
    señales = [k for k in mejor if k != "mse_total"]

    parte = {"mejor_mse_total": mejor["mse_total"], "señales": {}, "videos": {}}
    print("=== AUTOPSIA ===")
    for j, sig in enumerate(señales):
        eq = mejor[sig]["ecuacion"]
        pisos, errores = [], []
        for nombre, X, Y in jueces:
            piso = piso_de_ruido(Y[:, j])
            pred = evaluar(eq, X)
            res = pred - Y[:, j]
            mse = float(np.mean(res ** 2))
            pisos.append(piso); errores.append(mse)
            # dónde falla dentro del video
            n = len(res)
            tercios = [float(np.mean(res[i * n // 3:(i + 1) * n // 3] ** 2)) for i in range(3)]
            vel = np.abs(X[:, j + len(señales)])
            corr = float(np.corrcoef(np.abs(res), vel)[0, 1]) if np.std(vel) > 0 else 0.0
            parte["videos"].setdefault(nombre, {})[sig] = {
                "mse": mse, "piso_ruido": piso, "mse_sobre_piso": mse / piso if piso > 0 else None,
                "mse_por_tercios": tercios, "corr_error_vs_cambio": corr}
        parte["señales"][sig] = {"ecuacion": eq, "mse_medio": float(np.mean(errores)),
                                 "piso_medio": float(np.mean(pisos)),
                                 "veces_sobre_el_piso": float(np.mean(errores) / np.mean(pisos)) if np.mean(pisos) > 0 else None}
        v = parte["señales"][sig]
        print(f"[{sig}] error medio {v['mse_medio']:.1f} | piso de ruido {v['piso_medio']:.1f} "
              f"| la fórmula está a {v['veces_sobre_el_piso']:.1f}× del piso "
              f"({'cerca del límite físico de estos datos' if v['veces_sobre_el_piso'] and v['veces_sobre_el_piso'] < 3 else 'hay margen de mejora real'})")
    for nombre, d in parte["videos"].items():
        for sig, v in d.items():
            t = v["mse_por_tercios"]
            peor = ["inicio", "medio", "final"][int(np.argmax(t))]
            print(f"  {nombre} · {sig}: {v['mse']:.1f} ({v['mse_sobre_piso']:.1f}× piso) | "
                  f"falla más al {peor} | corr(error, cambio)={v['corr_error_vs_cambio']:+.2f}")

    with open(os.path.join(args.outdir, "autopsia.json"), "w") as f:
        json.dump(parte, f, indent=2)
    print("Parte guardado en", os.path.join(args.outdir, "autopsia.json"))


if __name__ == "__main__":
    main()
