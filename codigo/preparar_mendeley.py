# preparar_mendeley.py — convierte los datos de rastreo del dataset Mendeley 7yd2ntbh3w
# al formato de descubrir.py: CSV con columnas t, s1, s2 (nombres NEUTROS — Regla 4).
# s1 = señal del marcador del cuerpo 0; s2 = señal del marcador del cuerpo 1. Nada más se le dice al descubridor.
# Uso: python preparar_mendeley.py <carpeta_trial> <salida.csv>

import sys
import csv

import numpy as np


def main():
    carpeta, salida = sys.argv[1], sys.argv[2]
    rb0 = np.load(f"{carpeta}/DPmean_data_RB0.npy")  # fila 0: tiempo, fila 1: señal
    rb1 = np.load(f"{carpeta}/DPmean_data_RB1.npy")
    t = rb0[0]
    if not np.allclose(rb0[0], rb1[0]):
        sys.exit("Las dos señales no comparten la misma base de tiempo — revisar antes de continuar.")
    with open(salida, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "s1", "s2"])
        for i in range(len(t)):
            w.writerow([t[i], rb0[1][i], rb1[1][i]])
    print(f"{salida}: {len(t)} muestras | paso medio: {np.mean(np.diff(t)):.6f} | "
          f"s1 rango [{rb0[1].min():.3f}, {rb0[1].max():.3f}] | s2 rango [{rb1[1].min():.3f}, {rb1[1].max():.3f}]")


if __name__ == "__main__":
    main()
