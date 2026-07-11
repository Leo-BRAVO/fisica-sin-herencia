# descubrir_pool.py — descubrimiento sobre MÚLTIPLES réplicas del mismo experimento (prereg-08).
# Entrena agrupando las transiciones de varios videos y juzga sobre VIDEOS COMPLETOS nunca vistos
# (réplicas fuera de muestra — la forma más dura de validación disponible con réplicas).
# Las transiciones jamás cruzan la frontera entre videos.
# Uso: python descubrir_pool.py <carpeta_con_csvs> <outdir> [--semillas 5] [--jueces 3 7 11]

import os
import sys
import json
import glob
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descubrir import preparar, error_linea_base, error_rival_lineal, correr_semilla


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("outdir")
    ap.add_argument("--semillas", type=int, default=5)
    ap.add_argument("--semilla-inicial", type=int, default=1)
    ap.add_argument("--maxsize", type=int, default=25)
    ap.add_argument("--niter", type=int, default=200)
    ap.add_argument("--jueces", nargs="+", type=int, default=[3, 7, 11],
                    help="posiciones (1-indexadas) de los videos juez en la lista ordenada")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    csvs = sorted(glob.glob(os.path.join(args.carpeta, "*.csv")))
    if len(csvs) < 2:
        sys.exit("Se necesitan al menos 2 réplicas (1 para entrenar, 1 juez).")
    jueces_idx = {j - 1 for j in args.jueces if j - 1 < len(csvs)}
    print(f"{len(csvs)} réplicas | jueces (fuera de muestra): "
          + ", ".join(os.path.basename(csvs[i]) for i in sorted(jueces_idx)))

    Xtr, Ytr, Xte, Yte = [], [], [], []
    for i, c in enumerate(csvs):
        X, Y = preparar(c)  # las transiciones no cruzan videos: cada CSV se prepara por separado
        (Xte if i in jueces_idx else Xtr).append(X)
        (Yte if i in jueces_idx else Ytr).append(Y)
    X_tr, Y_tr = np.vstack(Xtr), np.vstack(Ytr)
    X_te, Y_te = np.vstack(Xte), np.vstack(Yte)

    base = error_linea_base(X_te, Y_te, Y_tr)
    umbral = 0.5 * base
    rival = error_rival_lineal(X_tr, Y_tr, X_te, Y_te)
    print(f"Entrenamiento: {len(X_tr)} transiciones | juicio: {len(X_te)} | "
          f"base trivial={base:.4f} | umbral={umbral:.4f} | rival lineal={rival:.4f} (reportado, no exigido — ver prereg-08)")

    resumen = {"replicas": [os.path.basename(c) for c in csvs], "jueces": sorted(jueces_idx),
               "mse_base": base, "umbral": umbral, "mse_rival_lineal": rival, "semillas": {}}
    for s in range(args.semilla_inicial, args.semilla_inicial + args.semillas):
        ya = os.path.join(args.outdir, f"semilla_{s}.json")
        if os.path.exists(ya):
            r = json.load(open(ya))
            print(f"— semilla {s}: previa, se reutiliza.")
        else:
            print(f"— semilla {s} …")
            r = correr_semilla(X_tr, Y_tr, X_te, Y_te, s, args.outdir,
                               niterations=args.niter, maxsize=args.maxsize)
        resumen["semillas"][s] = {"mse_total": r["mse_total"],
                                  "supera_umbral": bool(r["mse_total"] < umbral),
                                  "ecuaciones": {k: v["ecuacion"] for k, v in r.items() if k != "mse_total"}}
        with open(os.path.join(args.outdir, "resumen.json"), "w") as f:
            json.dump(resumen, f, indent=2)
    print("Listo. Resumen en", os.path.join(args.outdir, "resumen.json"))


if __name__ == "__main__":
    main()
