# forense.py — F2: "la ley como detective de datos" (planos de construccion, 13-jul-2026)
# Cuando las ecuaciones REPLICADAS de varias semillas fallan JUNTAS en los mismos cuadros,
# la fisica no cambio: el INSTRUMENTO mintio (desenfoque, oclusion, salto del rastreador).
# El detective marca esos cuadros con evidencia auditable — jamas borra ni modifica datos.
#
# Uso: python forense.py <outdir_con_semillas> <carpeta_csvs> [--jueces 3 7 11]
#      [--suavizar 0] [--retardos 0] [--centrar] [--umbral-sigma 4.0] [--consenso 0.8]
#
# Regla del detective (gobernanza): fallo CONJUNTO de varias semillas = instrumento;
# fallo de una sola semilla = idiosincrasia del modelo (no se marca).

import os
import json
import glob
import argparse

import numpy as np

from descubrir import preparar
from autopsia import evaluar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def es_semilla_completa(ruta):
    # semilla_N.json exacto; descarta semilla_N_parcial.json y semilla_N_canonica.json
    nombre = os.path.basename(ruta)
    if not (nombre.startswith("semilla_") and nombre.endswith(".json")):
        return False
    medio = nombre[len("semilla_"):-len(".json")]
    return medio.isdigit()


def cargar_semillas(outdir):
    archivos = sorted(f for f in glob.glob(os.path.join(outdir, "semilla_*.json")) if es_semilla_completa(f))
    semillas = []
    for f in archivos:
        with open(f) as fh:
            d = json.load(fh)
        señales = sorted((k for k in d if k != "mse_total"), key=lambda k: int(k.split("_")[0][1:]))
        semillas.append({"nombre": os.path.basename(f), "señales": señales, "datos": d})
    return semillas


def elegir_csvs(carpeta, jueces):
    csvs = sorted(glob.glob(os.path.join(carpeta, "*.csv")))
    if not jueces:
        return csvs
    jidx = {j - 1 for j in jueces}
    elegidos = [c for i, c in enumerate(csvs) if i in jidx]
    return elegidos or csvs


def residuo_semilla(semilla, X, Y):
    # suma de |residuos| por fila, sobre todas las señales de esta semilla
    r = np.zeros(len(X))
    for j, sig in enumerate(semilla["señales"]):
        eq = semilla["datos"][sig]["ecuacion"]
        pred = evaluar(eq, X)
        r += np.abs(pred - Y[:, j])
    return r


def puntuar_z(r):
    # normalizacion robusta: mediana y MAD (Regla del detective: robusta a idiosincrasias)
    mediana = np.median(r)
    mad = np.median(np.abs(r - mediana))
    return (r - mediana) / (1.4826 * mad + 1e-12)


def agrupar_rangos(indices):
    # agrupa indices contiguos t en rangos [(a, b), ...]
    if len(indices) == 0:
        return []
    rangos = []
    ini = prev = indices[0]
    for t in indices[1:]:
        if t == prev + 1:
            prev = t
            continue
        rangos.append((ini, prev))
        ini = prev = t
    rangos.append((ini, prev))
    return rangos


def analizar_replica(csv_path, semillas, umbral_sigma, consenso, suavizar, retardos, centrar):
    X, Y = preparar(csv_path, suavizar=suavizar, retardos=retardos, centrar=centrar)
    total = len(X)
    n = len(semillas)
    zs = np.array([puntuar_z(residuo_semilla(s, X, Y)) for s in semillas])
    votos = (zs > umbral_sigma).sum(axis=0)
    umbral_votos = consenso * n
    sospechoso = votos >= (umbral_votos - 1e-9)
    z_consenso = zs.mean(axis=0)
    idx_sosp = np.where(sospechoso)[0].tolist()
    rangos = []
    for a, b in agrupar_rangos(idx_sosp):
        etiqueta = f"{a}-{b}" if a != b else str(a)
        rangos.append({"rango": etiqueta, "z_medio": round(float(np.mean(z_consenso[a:b + 1])), 3)})
    return {
        "total_cuadros": int(total),
        "cuadros_sospechosos": int(len(idx_sosp)),
        "porcentaje": round(100.0 * len(idx_sosp) / total, 2) if total else 0.0,
        "pico_z_consenso": round(float(np.max(z_consenso)), 3) if total else 0.0,
        "rangos_sospechosos": rangos,
    }


def parsear_args():
    ap = argparse.ArgumentParser(description="Detective forense: marca cuadros sospechosos por consenso de semillas")
    ap.add_argument("outdir")
    ap.add_argument("datos")
    ap.add_argument("--jueces", nargs="+", type=int, default=None)
    ap.add_argument("--suavizar", type=int, default=0)
    ap.add_argument("--retardos", type=int, default=0)
    ap.add_argument("--centrar", action="store_true")
    ap.add_argument("--umbral-sigma", type=float, default=4.0)
    ap.add_argument("--consenso", type=float, default=0.8)
    return ap.parse_args()


def main():
    args = parsear_args()
    semillas = cargar_semillas(args.outdir)
    if not semillas:
        print("No se encontraron semillas completas (semilla_N.json) en", args.outdir)
        return
    csvs = elegir_csvs(args.datos, args.jueces)
    nombre_outdir = os.path.basename(os.path.normpath(args.outdir))

    print("=== FORENSE ===")
    print(f"Semillas completas: {len(semillas)} ({', '.join(s['nombre'] for s in semillas)})")
    print(f"Replicas analizadas: {len(csvs)} ({', '.join(os.path.basename(c) for c in csvs)})")
    print(f"Umbral: z > {args.umbral_sigma} | consenso >= {args.consenso*100:.0f}% "
          f"de {len(semillas)} semillas (>= {args.consenso*len(semillas):.2f} votos)")

    reporte = {
        "parametros": {
            "outdir": nombre_outdir,
            "datos": args.datos,
            "jueces": args.jueces,
            "suavizar": args.suavizar,
            "retardos": args.retardos,
            "centrar": bool(args.centrar),
            "umbral_sigma": args.umbral_sigma,
            "consenso": args.consenso,
            "n_semillas": len(semillas),
            "semillas_usadas": [s["nombre"] for s in semillas],
        },
        "replicas": {},
    }

    for c in csvs:
        nombre = os.path.basename(c)
        info = analizar_replica(c, semillas, args.umbral_sigma, args.consenso, args.suavizar, args.retardos, args.centrar)
        reporte["replicas"][nombre] = info
        print(f"\n{nombre}: {info['total_cuadros']} cuadros | sospechosos: {info['cuadros_sospechosos']} "
              f"({info['porcentaje']:.1f}%) | pico z consenso: {info['pico_z_consenso']:.2f}")
        if info["rangos_sospechosos"]:
            for r in info["rangos_sospechosos"]:
                print(f"   cuadros {r['rango']}  z medio={r['z_medio']:.2f}")
        else:
            print("   sin cuadros sospechosos")

    destino = os.path.join(BASE, "resultados", f"forense-{nombre_outdir}")
    os.makedirs(destino, exist_ok=True)
    with open(os.path.join(destino, "reporte.json"), "w") as f:
        json.dump(reporte, f, indent=2)
    print("\nReporte guardado en", os.path.join(destino, "reporte.json"))
    print("El detective marca; la exclusion la decide un prerregistro.")


if __name__ == "__main__":
    main()
