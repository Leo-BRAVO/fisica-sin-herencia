# transferir.py — prueba de transferencia (prerregistro-05)
# Evalúa las ecuaciones descubiertas en un trial sobre OTRO trial, sin re-entrenar.
# Uso: python transferir.py <semilla_origen.json> <datos_destino.csv>

import os
import sys
import json

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # portable (antes solo Windows)
from descubrir import preparar, dividir_por_tiempo, error_linea_base


def evaluar(ecuacion, X):
    ns = {
        "v1": X[:, 0], "v2": X[:, 1], "v3": X[:, 2], "v4": X[:, 3],
        "sin": np.sin, "cos": np.cos, "exp": np.exp, "sqrt": np.sqrt,
        "square": lambda x: x * x,
    }
    return eval(ecuacion, {"__builtins__": {}}, ns)  # ecuaciones propias del proyecto, sin entrada externa


def main():
    semilla_json, destino_csv = sys.argv[1], sys.argv[2]
    eqs = json.load(open(semilla_json))
    X, Y = preparar(destino_csv)
    X_tr, Y_tr, X_te, Y_te = dividir_por_tiempo(X, Y)
    base = error_linea_base(X_te, Y_te, Y_tr)
    umbral = 0.5 * base

    mse_total = 0.0
    for j, sig in enumerate(["v1_sig", "v2_sig"]):
        pred = evaluar(eqs[sig]["ecuacion"], X_te)
        mse = float(np.mean((pred - Y_te[:, j]) ** 2))
        mse_total += mse
        print(f"{sig}: mse transferido = {mse:.4f}")
    print(f"TOTAL transferido = {mse_total:.4f} | umbral del destino = {umbral:.4f} | "
          f"{'EXITO: la formula es del sistema' if mse_total < umbral else 'no supera: parte era de la corrida'}")
    return mse_total


if __name__ == "__main__":
    main()
