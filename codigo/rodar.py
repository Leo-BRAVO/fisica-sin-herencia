# rodar.py — Mejora #3 (aprobada 11-jul-2026): ¿la fórmula RUEDA?
# Desde el estado inicial real de un video, la fórmula predice SOLA muchos pasos hacia
# adelante (realimentando sus propias predicciones) y se mide el horizonte: cuántos pasos
# aguanta antes de que su error supere 3× la desviación del piso de ruido.
# Es la prueba que distingue una ley de un truco de un solo paso (pregunta P1 de N-001).
# Uso: python rodar.py <outdir_con_semillas> <csv_del_video> [--pasos 100]

import os
import sys
import json
import glob
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descubrir import preparar
from autopsia import evaluar, piso_de_ruido


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("csv")
    ap.add_argument("--pasos", type=int, default=100)
    args = ap.parse_args()

    semillas = sorted(glob.glob(os.path.join(args.outdir, "semilla_*.json")))
    mejor = min((json.load(open(f)) for f in semillas), key=lambda r: r["mse_total"])
    señales = [k for k in mejor if k != "mse_total"]
    n_sig = len(señales)

    X, Y = preparar(args.csv)
    if X.shape[1] != 2 * n_sig:
        raise SystemExit(f"rodar.py asume estado [señales, cambios] ({2*n_sig} columnas) y los datos "
                         f"traen {X.shape[1]} — con retardos u otras variables el rodado daría números "
                         f"en silencio. Preparar los datos sin retardos para rodar.")
    pasos = min(args.pasos, len(Y) - 1)
    tol = [3.0 * np.sqrt(max(piso_de_ruido(Y[:, j]), 1e-12)) for j in range(n_sig)]

    # estado inicial real: posiciones y cambios del primer punto
    estado = X[0].copy()
    horizonte = pasos
    errores = []
    for t in range(pasos):
        sig_pred = np.array([float(evaluar(mejor[señales[j]]["ecuacion"], estado.reshape(1, -1))[0])
                             for j in range(n_sig)])
        err = np.abs(sig_pred - Y[t])
        errores.append(err.tolist())
        if any(err[j] > tol[j] * 3 for j in range(n_sig)):  # 3σ de ruido ×3 = desmoronamiento claro
            horizonte = t + 1
            break
        # nuevo estado: posiciones predichas + cambios implicados
        cambios = sig_pred - estado[:n_sig]
        estado = np.concatenate([sig_pred, cambios])

    total = len(Y)
    print(f"Video: {os.path.basename(args.csv)} | pasos disponibles: {total}")
    print(f"HORIZONTE DE RODADO: {horizonte} pasos "
          f"({'rodó el video COMPLETO sin desmoronarse' if horizonte >= pasos else f'se desmoronó en el paso {horizonte}'})")
    err_fin = errores[-1] if errores else []
    print(f"Error final por señal: {[round(e,1) for e in err_fin]} | tolerancia (9σ ruido): {[round(t*3,1) for t in tol]}")

    with open(os.path.join(args.outdir, f"rodado_{os.path.basename(args.csv)}.json"), "w") as f:
        json.dump({"video": os.path.basename(args.csv), "horizonte": horizonte,
                   "pasos_disponibles": int(total), "errores": errores}, f, indent=2)


if __name__ == "__main__":
    main()
