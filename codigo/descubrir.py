# descubrir.py — Fase 0, proyecto Física sin herencia
# Regresión simbólica sobre posiciones extraídas de video. Parámetros fijados en CIMIENTOS.md sección 3b.
# Uso:  python descubrir.py <posiciones.csv> <carpeta_resultados> [--semillas 10] [--nulo barajado|ruido]
#
# Reglas que este script implementa y NO deben relajarse:
#  - Regla 1/4: al descubridor solo se le dan números (x, y, vx, vy). Sin nombres físicos, sin constantes con nombre.
#  - División 70/30 POR TIEMPO (sección 3b): jamás al azar.
#  - Regla 12: línea base = velocidad constante; éxito = error < 50% del error base en el 30% oculto.
#  - Regla 7: correr con --semillas N (por defecto 10), todas registradas.
#  - Regla 11: --nulo barajado (orden temporal aleatorizado) y --nulo ruido deben FALLAR el umbral.

import os
import sys
import json
import argparse

import numpy as np
import pandas as pd


def preparar(csv_path, nulo=None, rng=None, suavizar=0, retardos=0):
    """suavizar: ventana de promedio móvil centrado (0/1 = sin suavizado) — filtro GENÉRICO
    documentado, permitido por la Regla 2. retardos: nº de valores PASADOS de cada señal
    añadidos como variables (inmersión por retardos de Takens — pura historia, cero física).
    Mejoras de la AUDITORIA-OBSERVACION, aprobadas por el director el 11-jul-2026."""
    df = pd.read_csv(csv_path).dropna()
    # Acepta extracción propia (x_px, y_px) o cualquier número de señales neutras s1..sN
    if "x_px" in df.columns:
        cols = ["x_px", "y_px"]
    else:
        import re as _re
        cols = sorted([c for c in df.columns if _re.fullmatch(r"s\d+", c)],
                      key=lambda c: int(c[1:]))
    señales = [df[c].to_numpy(float) for c in cols]

    if suavizar and suavizar > 1:
        k = np.ones(suavizar) / suavizar
        señales = [np.convolve(s, k, mode="valid") for s in señales]

    if nulo == "barajado":
        perm = rng.permutation(len(señales[0]))
        señales = [s[perm] for s in señales]
    elif nulo == "ruido":
        señales = [rng.uniform(s.min(), s.max(), size=len(s)) for s in señales]

    # Velocidades por diferencia entre cuadros (operación matemática neutra)
    cambios = [np.diff(s) for s in señales]
    # Estado en t → estado en t+1, con t desde 'ini' para dar espacio a los retardos
    ini = max(1, retardos)
    fin = len(señales[0]) - 1
    columnas = [s[ini:fin] for s in señales] + [c[ini - 1:fin - 1] for c in cambios]
    for k in range(1, retardos + 1):
        columnas += [s[ini - k:fin - k] for s in señales]
    X = np.column_stack(columnas)
    Y = np.column_stack([s[ini + 1:fin + 1] for s in señales])
    return X, Y


def dividir_por_tiempo(X, Y, frac=0.70):
    n = int(len(X) * frac)
    return X[:n], Y[:n], X[n:], Y[n:]


def _mse_suma(pred, Y):
    # Unidad estándar del proyecto (prerregistro-02): suma de los MSE por señal.
    return float(np.sum(np.mean((pred - Y) ** 2, axis=0)))


def error_linea_base(X_te, Y_te, Y_tr=None):
    # Vara honesta (enmienda-01): el mejor de DOS predictores triviales (velocidad y media).
    n_sig = Y_te.shape[1]  # X = [señales..., cambios...]: posición i + cambio i+n_sig
    pred_vel = np.column_stack([X_te[:, i] + X_te[:, i + n_sig] for i in range(n_sig)])
    mse_vel = _mse_suma(pred_vel, Y_te)
    if Y_tr is None:
        return mse_vel
    mse_media = _mse_suma(np.broadcast_to(Y_tr.mean(axis=0), Y_te.shape), Y_te)
    return min(mse_vel, mse_media)


def error_rival_lineal(X_tr, Y_tr, X_te, Y_te):
    # Rival digno (mejora aprobada 9-jul-2026): regresión lineal por mínimos cuadrados.
    # Si el descubrimiento simbólico no vence a esto, no descubrió estructura no lineal.
    A_tr = np.column_stack([X_tr, np.ones(len(X_tr))])
    A_te = np.column_stack([X_te, np.ones(len(X_te))])
    W, *_ = np.linalg.lstsq(A_tr, Y_tr, rcond=None)
    return _mse_suma(A_te @ W, Y_te)


def correr_semilla(X_tr, Y_tr, X_te, Y_te, semilla, outdir, niterations=200, maxsize=25):
    from pysr import PySRRegressor
    # Guardado parcial por señal (lección de dos apagones, 11-jul-2026): si existe un
    # parcial de esta semilla, las señales ya ajustadas se reutilizan.
    parcial = os.path.join(outdir, f"semilla_{semilla}_parcial.json")
    resultados = json.load(open(parcial)) if os.path.exists(parcial) else {}
    nombres = [f"v{j+1}_sig" for j in range(Y_tr.shape[1])]  # Regla 4: sin nombres físicos
    for j, nombre in enumerate(nombres):
        if nombre in resultados:
            continue
        modelo = PySRRegressor(
            niterations=niterations,
            binary_operators=["+", "-", "*", "/"],
            unary_operators=["sin", "cos", "exp", "sqrt", "square"],
            maxsize=maxsize,
            random_state=semilla,
            deterministic=True,
            parallelism="serial",
            progress=False,
            temp_equation_file=True,
        )
        modelo.fit(X_tr, Y_tr[:, j], variable_names=[f"v{i+1}" for i in range(X_tr.shape[1])])
        pred = modelo.predict(X_te)
        mse = float(np.mean((pred - Y_te[:, j]) ** 2))
        resultados[nombre] = {"ecuacion": str(modelo.get_best()["equation"]), "mse_test": mse}
        with open(parcial, "w") as f:
            json.dump(resultados, f, indent=2)
    resultados["mse_total"] = sum(resultados[n]["mse_test"] for n in nombres)
    if os.path.exists(parcial):
        os.remove(parcial)
    with open(os.path.join(outdir, f"semilla_{semilla}.json"), "w") as f:
        json.dump(resultados, f, indent=2)
    return resultados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("outdir")
    ap.add_argument("--semillas", type=int, default=10)
    ap.add_argument("--nulo", choices=["barajado", "ruido"], default=None)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    rng = np.random.default_rng(0)
    X, Y = preparar(args.csv, nulo=args.nulo, rng=rng)
    X_tr, Y_tr, X_te, Y_te = dividir_por_tiempo(X, Y)
    base = error_linea_base(X_te, Y_te, Y_tr)
    umbral = 0.5 * base  # éxito exige: < 50% de la base trivial Y ADEMÁS vencer al rival lineal
    rival = error_rival_lineal(X_tr, Y_tr, X_te, Y_te)
    print(f"Datos: {len(X)} transiciones | entrenamiento: {len(X_tr)} | prueba oculta: {len(X_te)}")
    print(f"Base trivial (MSE suma): {base:.4f} | umbral: < {umbral:.4f} | rival lineal: {rival:.4f}")

    resumen = {"nulo": args.nulo, "mse_base": base, "umbral": umbral, "mse_rival_lineal": rival, "semillas": {}}
    exitos = 0
    for s in range(1, args.semillas + 1):
        # Reanudación tras apagón: si esta semilla ya tiene resultado en disco, se carga y no se recalcula
        ya = os.path.join(args.outdir, f"semilla_{s}.json")
        if os.path.exists(ya):
            with open(ya) as f:
                r = json.load(f)
            print(f"— semilla {s}/{args.semillas}: resultado previo encontrado, se reutiliza.")
        else:
            print(f"— semilla {s}/{args.semillas} …")
            r = correr_semilla(X_tr, Y_tr, X_te, Y_te, s, args.outdir)
        exito = r["mse_total"] < umbral and r["mse_total"] < rival
        exitos += exito
        resumen["semillas"][s] = {"mse_total": r["mse_total"], "supera_umbral": bool(r["mse_total"] < umbral),
                                  "vence_rival_lineal": bool(r["mse_total"] < rival), "exito": bool(exito)}
        print(f"   mse={r['mse_total']:.4f}  {'EXITO' if exito else 'no supera'}")

    resumen["exitos"] = exitos
    with open(os.path.join(args.outdir, "resumen.json"), "w") as f:
        json.dump(resumen, f, indent=2)
    print(f"\nSemillas que superan el umbral: {exitos}/{args.semillas}")
    if args.nulo:
        print("PRUEBA NULA: si alguna semilla superó el umbral, el pipeline está roto (Regla 11).")


if __name__ == "__main__":
    main()
