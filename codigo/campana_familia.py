# campana_familia.py — Etapa 1 del prerregistro-07: correr el descubridor sobre las
# 14+ longitudes del dataset Zenodo y registrar las constantes descubiertas por longitud.
# Uso: python campana_familia.py

import os
import re
import json
import glob

import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEN = os.path.join(BASE, "datos", "crudos", "zenodo-pendulo-simple")
PROCESADOS = os.path.join(BASE, "datos", "procesados", "familia")
RESULTADOS = os.path.join(BASE, "resultados", "familia")

import sys
sys.path.insert(0, os.path.join(BASE, "codigo"))
from descubrir import preparar, dividir_por_tiempo, error_linea_base, error_rival_lineal, correr_semilla


def longitud_de(nombre):
    m = re.search(r"(\d+(?:\.\d+)?)\s*cm", nombre)
    return float(m.group(1)) if m else None


def main():
    os.makedirs(PROCESADOS, exist_ok=True)
    os.makedirs(RESULTADOS, exist_ok=True)
    familia = {}

    for txt in sorted(glob.glob(os.path.join(ORIGEN, "*.txt"))):
        nombre = os.path.basename(txt).replace(".txt", "")
        L = longitud_de(nombre)
        if L is None:
            print(f"[{nombre}] sin longitud en el nombre — se omite"); continue

        csv = os.path.join(PROCESADOS, nombre.replace("=", "_") + ".csv")
        df = pd.read_csv(txt, sep=r"\s+", skiprows=2, names=["t", "s1", "omega"], usecols=[0, 1, 2]).dropna(subset=["t", "s1"])
        df[["t", "s1"]].to_csv(csv, index=False)

        outdir = os.path.join(RESULTADOS, nombre.replace("=", "_"))
        os.makedirs(outdir, exist_ok=True)
        X, Y = preparar(csv)
        X_tr, Y_tr, X_te, Y_te = dividir_por_tiempo(X, Y)
        base = error_linea_base(X_te, Y_te, Y_tr)
        rival = error_rival_lineal(X_tr, Y_tr, X_te, Y_te)
        entrada = {"longitud_cm": L, "muestras": int(len(X)), "mse_base": base, "mse_rival_lineal": rival, "semillas": {}}

        print(f"[{nombre}] L={L}cm, {len(X)} transiciones — corriendo 3 semillas…", flush=True)
        for s in (1, 2, 3):
            ya = os.path.join(outdir, f"semilla_{s}.json")
            if os.path.exists(ya):
                r = json.load(open(ya))
            else:
                r = correr_semilla(X_tr, Y_tr, X_te, Y_te, s, outdir)
            entrada["semillas"][s] = {"mse_total": r["mse_total"], "ecuacion": r["v1_sig"]["ecuacion"]}
        familia[nombre] = entrada
        with open(os.path.join(RESULTADOS, "familia_resumen.json"), "w") as f:
            json.dump(familia, f, indent=2)

    print(f"\nCampaña completa: {len(familia)} sistemas. Resumen en resultados/familia/familia_resumen.json")


if __name__ == "__main__":
    main()
