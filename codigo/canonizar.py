# canonizar.py — Mejora #5 (aprobada 11-jul-2026): la tarjeta de identidad canónica de una fórmula.
# Convierte cualquier ecuación descubierta en propiedades COMPARABLES entre sistemas
# (lección v7: comparar literales entre datasets pequeños no converge; comparar propiedades sí):
#   - desplazamiento: f(0)                  (el "término constante efectivo")
#   - gradiente: ∂f/∂vi en el origen        (los factores de pérdida/acople efectivos)
#   - curvatura: ∂²f/∂vi² en el origen      (no-linealidad local)
#   - estabilidad: ¿explota con entradas grandes? (bandera de fórmulas frágiles)
# Uso: python canonizar.py <semilla.json | outdir> [--estado v1 v2 ...] (punto de expansión opcional)

import os
import sys
import json
import glob
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autopsia import evaluar


def tarjeta(eq, n_vars, punto=None, h=1e-4):
    p = np.zeros(n_vars) if punto is None else np.array(punto, float)

    def f(v):
        return float(evaluar(eq, v.reshape(1, -1))[0])

    try:
        desplaz = f(p)
        grad, curv = [], []
        for i in range(n_vars):
            e = np.zeros(n_vars); e[i] = h
            g = (f(p + e) - f(p - e)) / (2 * h)
            c = (f(p + e) - 2 * desplaz + f(p - e)) / (h * h)
            grad.append(round(g, 6)); curv.append(round(c, 4))
        # estabilidad: sondear entradas grandes
        explota = False
        for esc in (1e3, 1e5):
            val = f(p + esc)
            if not np.isfinite(val) or abs(val) > 1e12:
                explota = True
                break
        return {"desplazamiento": round(desplaz, 6), "gradiente": grad,
                "curvatura": curv, "explota_con_entradas_grandes": explota}
    except Exception as e:
        return {"error": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("objetivo")
    ap.add_argument("--estado", nargs="+", type=float, default=None)
    args = ap.parse_args()

    archivos = sorted(glob.glob(os.path.join(args.objetivo, "semilla_*.json"))) \
        if os.path.isdir(args.objetivo) else [args.objetivo]

    for f in archivos:
        r = json.load(open(f))
        señales = [k for k in r if k != "mse_total"]
        n_vars = 2 * len(señales)
        print(f"=== {os.path.basename(f)} ===")
        salida = {}
        for sig in señales:
            t = tarjeta(r[sig]["ecuacion"], n_vars, punto=args.estado)
            salida[sig] = t
            print(f"  [{sig}] desplazamiento={t.get('desplazamiento')} | gradiente={t.get('gradiente')} "
                  f"| curvatura={t.get('curvatura')} | {'FRÁGIL (explota)' if t.get('explota_con_entradas_grandes') else 'estable'}")
        with open(f.replace(".json", "_canonica.json"), "w") as out:
            json.dump(salida, out, indent=2)


if __name__ == "__main__":
    main()
