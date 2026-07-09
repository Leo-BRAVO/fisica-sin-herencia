# preparar_zenodo.py — convierte los archivos del dataset Zenodo 15569631 (péndulo simple,
# app Pendulum Tracker de SimuFísica sobre péndulos reales) al formato del descubridor.
# Solo se toma la señal de posición angular como s1 (nombre neutro, Regla 4). La columna
# omega del archivo es derivada por la app — la descartamos y recalculamos cambios nosotros.
# Uso: python preparar_zenodo.py <archivo.txt> <salida.csv>

import sys

import pandas as pd


def main():
    origen, salida = sys.argv[1], sys.argv[2]
    df = pd.read_csv(origen, sep=r"\s+", skiprows=2, names=["t", "s1", "omega"], usecols=[0, 1, 2])
    df = df.dropna(subset=["t", "s1"])
    dt = df["t"].diff().dropna()
    df[["t", "s1"]].to_csv(salida, index=False)
    print(f"{salida}: {len(df)} muestras | paso medio {dt.mean():.4f}s (min {dt.min():.4f}, max {dt.max():.4f}) "
          f"| s1 rango [{df['s1'].min():.2f}, {df['s1'].max():.2f}]")


if __name__ == "__main__":
    main()
