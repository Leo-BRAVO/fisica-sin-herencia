# dimension.py — DIMENSION INTRINSECA: la primera pregunta de todo sistema nuevo
# (AUDITORIA-PENDULO-DOBLE, replanteo #3, aprobado por el director el 8-ago-2026).
# Antes de buscar leyes, preguntar: ¿cuantas variables esconde este sistema?
# (Es el primer paso del metodo de Columbia/Lipson 2022 — nosotros lo saltabamos.)
#
# Dos estimadores, ambos matematica generica (Regla 2 — cero fisica):
#  1. TwoNN (razon de distancias a los 2 vecinos mas cercanos): estima la dimension
#     del conjunto de estados visitados, robusto a curvatura. Referencia del metodo:
#     razon mu = r2/r1 sigue una ley de potencia cuyo exponente ES la dimension.
#  2. Razon de participacion (PCA): cuantas direcciones lineales concentran la varianza.
#     Cota superior lineal — util como contraste (TwoNN <= participacion, usualmente).
#
# La estimacion se hace sobre el espacio de estados observado (senales + cambios,
# como los ve el motor), POR REPLICA y agrupado, con submuestreo determinista.
#
# Uso: python dimension.py <carpeta_csvs_o_csv> [--centrar] [--max-puntos 2000]

import os
import glob
import json
import argparse

import numpy as np

from descubrir import preparar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def twonn(X, rng=None):
    """Estimador TwoNN de dimension intrinseca. X: (n, d) puntos.
    Devuelve la dimension estimada (float) o None si hay muy pocos puntos."""
    n = len(X)
    if n < 20:
        return None
    # distancias a 1er y 2do vecino (excluyendo el propio punto y duplicados exactos)
    d2 = np.sum((X[:, None, :] - X[None, :, :]) ** 2, axis=2)
    np.fill_diagonal(d2, np.inf)
    orden = np.sort(d2, axis=1)
    r1 = np.sqrt(orden[:, 0])
    r2 = np.sqrt(orden[:, 1])
    ok = r1 > 0
    if ok.sum() < 20:
        return None
    mu = r2[ok] / r1[ok]
    mu = mu[mu > 1.0]
    if len(mu) < 20:
        return None
    # ajuste por maxima verosimilitud del exponente: d = n / sum(log mu)
    return float(len(mu) / np.sum(np.log(mu)))


def participacion(X):
    """Razon de participacion de PCA: (sum lambda)^2 / sum(lambda^2) — cuantas
    direcciones lineales 'trabajan'. Cota lineal de la dimension."""
    Xc = X - X.mean(axis=0)
    lam = np.linalg.eigvalsh(np.cov(Xc, rowvar=False))
    lam = np.clip(lam, 0, None)
    s = lam.sum()
    return float(s * s / np.sum(lam ** 2)) if s > 0 else 0.0


def submuestrear(X, max_puntos, rng):
    if len(X) <= max_puntos:
        return X
    idx = rng.choice(len(X), size=max_puntos, replace=False)
    return X[idx]


def main():
    ap = argparse.ArgumentParser(description="Dimension intrinseca del sistema: cuantas variables esconde")
    ap.add_argument("datos")
    ap.add_argument("--centrar", action="store_true")
    ap.add_argument("--max-puntos", type=int, default=2000)
    args = ap.parse_args()

    csvs = sorted(glob.glob(os.path.join(args.datos, "*.csv"))) \
        if os.path.isdir(args.datos) else [args.datos]
    rng = np.random.default_rng(0)

    print("=== DIMENSION INTRINSECA (la primera pregunta de todo sistema nuevo) ===")
    reporte = {"datos": args.datos, "centrar": bool(args.centrar), "replicas": {}, "agrupado": {}}
    Xs = []
    for c in csvs:
        X, _ = preparar(c, centrar=args.centrar)
        Xs.append(X)
        Xi = submuestrear(X, args.max_puntos, rng)
        d_nn = twonn(Xi, rng)
        d_pr = participacion(Xi)
        reporte["replicas"][os.path.basename(c)] = {
            "puntos": int(len(X)), "twonn": round(d_nn, 2) if d_nn else None,
            "participacion_pca": round(d_pr, 2)}
        print(f"  {os.path.basename(c)}: {len(X)} estados | TwoNN ~ "
              f"{d_nn:.2f}" if d_nn else f"  {os.path.basename(c)}: pocos puntos",
              f"| participacion PCA ~ {d_pr:.2f}" if d_nn else "")

    Xall = submuestrear(np.vstack(Xs), args.max_puntos, rng)
    d_nn = twonn(Xall, rng)
    d_pr = participacion(Xall)
    reporte["agrupado"] = {"puntos": int(sum(len(X) for X in Xs)),
                           "twonn": round(d_nn, 2) if d_nn else None,
                           "participacion_pca": round(d_pr, 2)}
    print(f"\nAGRUPADO: TwoNN ~ {d_nn:.2f} | participacion PCA ~ {d_pr:.2f}")
    print("Lectura: TwoNN estima cuantas variables NECESITA el sistema; si es mucho menor")
    print("que el numero de senales observadas, hay redundancia (ojos mas simples posibles);")
    print("si se acerca o supera, faltan variables (estado incompleto — retardos o mas ojos).")

    nombre = os.path.basename(os.path.normpath(args.datos))
    outdir = os.path.join(BASE, "resultados", f"dimension-{nombre}")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "reporte.json"), "w") as f:
        json.dump(reporte, f, indent=2)
    print("Reporte guardado en", os.path.join(outdir, "reporte.json"))


if __name__ == "__main__":
    main()
