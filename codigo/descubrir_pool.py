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
    ap.add_argument("--paralelo", type=int, default=1,
                    help="procesos simultáneos (cada semilla sigue siendo determinista; 3 recomendado)")
    ap.add_argument("--maxsize", type=int, default=25)
    ap.add_argument("--niter", type=int, default=200)
    ap.add_argument("--jueces", nargs="+", type=int, default=[3, 7, 11],
                    help="posiciones (1-indexadas) de los videos juez en la lista ordenada")
    ap.add_argument("--suavizar", type=int, default=0,
                    help="ventana de promedio móvil centrado (filtro genérico, Regla 2)")
    ap.add_argument("--retardos", type=int, default=0,
                    help="valores pasados de cada señal como variables (Takens)")
    ap.add_argument("--rival-arbol", default=None,
                    help="semilla_N.json de un nodo del árbol: sus ecuaciones se evalúan como RIVAL adicional (el conocimiento propio sube la vara)")
    ap.add_argument("--heredar", default=None,
                    help="semilla_N.json de un nodo del árbol: sus predicciones se AÑADEN como variables de entrada (el motor puede construir sobre lo ya descubierto o ignorarlo)")
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
        X, Y = preparar(c, suavizar=args.suavizar, retardos=args.retardos)
        (Xte if i in jueces_idx else Xtr).append(X)
        (Yte if i in jueces_idx else Ytr).append(Y)
    X_tr, Y_tr = np.vstack(Xtr), np.vstack(Ytr)
    X_te, Y_te = np.vstack(Xte), np.vstack(Yte)

    base = error_linea_base(X_te, Y_te, Y_tr)
    umbral = 0.5 * base
    rival = error_rival_lineal(X_tr, Y_tr, X_te, Y_te)
    print(f"Entrenamiento: {len(X_tr)} transiciones | juicio: {len(X_te)} | "
          f"base trivial={base:.4f} | umbral={umbral:.4f} | rival lineal={rival:.4f} (reportado, no exigido — ver prereg-08)")

    # Interés compuesto del árbol (Regla 18, cableado 11-jul-2026): el conocimiento PROPIO
    # validado puede subir la vara (--rival-arbol) o servir de ladrillo (--heredar).
    # Jamás conocimiento humano — solo nodos del propio árbol (el cortafuegos no se toca).
    rival_arbol = None
    if args.rival_arbol:
        from autopsia import evaluar
        eqs = json.load(open(args.rival_arbol))
        sigs = [k for k in eqs if k != "mse_total"]
        pred = np.column_stack([evaluar(eqs[s]["ecuacion"], X_te) for s in sigs])
        rival_arbol = float(np.sum(np.mean((pred - Y_te) ** 2, axis=0)))
        print(f"rival del árbol ({os.path.basename(args.rival_arbol)}): {rival_arbol:.4f}")
    if args.heredar:
        from autopsia import evaluar
        eqs = json.load(open(args.heredar))
        sigs = [k for k in eqs if k != "mse_total"]
        her_tr = np.column_stack([evaluar(eqs[s]["ecuacion"], X_tr) for s in sigs])
        her_te = np.column_stack([evaluar(eqs[s]["ecuacion"], X_te) for s in sigs])
        X_tr = np.column_stack([X_tr, her_tr])
        X_te = np.column_stack([X_te, her_te])
        print(f"herencia del árbol: {her_tr.shape[1]} variables añadidas "
              f"(v{X_tr.shape[1]-her_tr.shape[1]+1}..v{X_tr.shape[1]}) — el motor decide si las usa")

    resumen = {"replicas": [os.path.basename(c) for c in csvs], "jueces": sorted(jueces_idx),
               "mse_base": base, "umbral": umbral, "mse_rival_lineal": rival,
               "mse_rival_arbol": rival_arbol, "herencia": args.heredar, "semillas": {}}
    rango = list(range(args.semilla_inicial, args.semilla_inicial + args.semillas))
    pendientes = [s for s in rango if not os.path.exists(os.path.join(args.outdir, f"semilla_{s}.json"))]

    if args.paralelo > 1 and len(pendientes) > 1:
        # Mejora #4 (11-jul-2026): semillas en procesos paralelos — cada una determinista por sí misma
        from concurrent.futures import ProcessPoolExecutor
        print(f"Corriendo {len(pendientes)} semillas en {args.paralelo} procesos paralelos…")
        with ProcessPoolExecutor(max_workers=args.paralelo) as ex:
            futs = {ex.submit(correr_semilla, X_tr, Y_tr, X_te, Y_te, s, args.outdir,
                              args.niter, args.maxsize): s for s in pendientes}
            for fut, s in futs.items():
                fut.result()
                print(f"— semilla {s}: completada.")
    else:
        for s in pendientes:
            print(f"— semilla {s} …")
            correr_semilla(X_tr, Y_tr, X_te, Y_te, s, args.outdir,
                           niterations=args.niter, maxsize=args.maxsize)

    for s in rango:
        r = json.load(open(os.path.join(args.outdir, f"semilla_{s}.json")))
        resumen["semillas"][s] = {"mse_total": r["mse_total"],
                                  "supera_umbral": bool(r["mse_total"] < umbral),
                                  "ecuaciones": {k: v["ecuacion"] for k, v in r.items() if k != "mse_total"}}
    with open(os.path.join(args.outdir, "resumen.json"), "w") as f:
        json.dump(resumen, f, indent=2)
    print("Listo. Resumen en", os.path.join(args.outdir, "resumen.json"))


if __name__ == "__main__":
    main()
