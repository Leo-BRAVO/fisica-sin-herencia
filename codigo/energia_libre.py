# energia_libre.py — LA UNIFICACIÓN: una sola cantidad debajo de la curiosidad, la incertidumbre
# y el poder. Implementada el 8-ago-2026.
#
# LA ECUACIÓN (es la de Friston, escrita en la moneda que la casa ya usaba — MDL, Regla 6):
#
#     F(modelo, datos) = bits(residuos) + bits(modelo)
#                      = n/2·log2(2πe·mse)  +  k/2·log2(n)
#
# y con ella, TODO lo que Diego siente es la misma cantidad vista desde ángulos distintos:
#   · CURIOSIDAD (G2)      = −ΔF esperada / coste     (bits que espero liberar por esfuerzo)
#   · INCERTIDUMBRE (G14)  = la parte de F que MÁS DATOS bajan (epistémica) vs la que no (aleatoria)
#   · PODER (G13)          = la ΔF que puedo causar INTERVINIENDO (no solo mirando)
#   · PARSIMONIA (Regla 6) = el término bits(modelo), que castiga la complejidad
# No adoptamos a Friston por autoridad: la ecuación del impulso YA ERA esto (ΔC/coste con C en
# MDL). Aquí solo queda ejecutable y con verdugos — que es lo que su programa no tiene.
#
# Regla 31: (1) la ley simple verdadera vence al polinomio sobreajustado (el término de
# complejidad muerde); (2) en ruido puro, el modelo nulo vence a cualquier ajuste; (3) la mejora
# de F por más datos es EPISTÉMICA — en un mundo ya aprendido, más datos no liberan bits.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def bits(mse, n, k):
    """F en bits: descripción de los residuos + descripción del modelo (forma BIC/MDL)."""
    return float(n / 2 * np.log2(2 * np.pi * np.e * max(mse, 1e-300)) + k / 2 * np.log2(n))


def F(X, Y, grado=1):
    """Energía libre de un ajuste polinómico de 'grado' sobre (X→Y), con mse honesto (por mitad
    retenida) y k = parámetros. grado=0 es el modelo nulo (la media)."""
    n = len(Y)
    mitad = n // 2
    if grado == 0:
        pred = np.full(n - mitad, Y[:mitad].mean())
        k = 1
    else:
        A = np.column_stack([X[:mitad] ** g for g in range(1, grado + 1)] + [np.ones(mitad)])
        w, *_ = np.linalg.lstsq(A, Y[:mitad], rcond=None)
        At = np.column_stack([X[mitad:] ** g for g in range(1, grado + 1)] + [np.ones(n - mitad)])
        pred = At @ w
        k = grado + 1
    mse = float(np.mean((pred - Y[mitad:]) ** 2))
    return bits(mse, n - mitad, k)


def regla31(verbose=True):
    rng = np.random.default_rng(31)
    fallos = []
    X = rng.uniform(-2, 2, 400)
    Y = 1.5 * X + rng.normal(0, 0.3, 400)          # mundo con ley lineal y ruido moderado

    f_simple = F(X, Y, grado=1)
    f_sobre = F(X, Y, grado=9)
    c1 = f_simple < f_sobre
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} PARSIMONIA: la ley simple ({f_simple:.0f} bits) vence "
              f"al polinomio grado 9 ({f_sobre:.0f} bits)")
    if not c1:
        fallos.append("parsimonia")

    Yr = rng.normal(0, 1.0, 400)                    # ruido puro
    c2 = F(X, Yr, grado=0) < min(F(X, Yr, grado=g) for g in (1, 3, 9))
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} RUIDO PURO: el modelo nulo vence a todo ajuste")
    if not c2:
        fallos.append("ruido")

    # 3) en un mundo YA aprendido, mas datos no liberan bits POR MUESTRA (la F por muestra
    # se estanca); en uno a medio aprender, si.
    def f_por_muestra(n):
        Xa = rng.uniform(-2, 2, n)
        Ya = 1.5 * Xa + rng.normal(0, 0.3, n)
        return F(Xa, Ya, grado=1) / (n // 2)
    mejora_chico = f_por_muestra(60) - f_por_muestra(120)
    mejora_grande = abs(f_por_muestra(4000) - f_por_muestra(8000))
    c3 = mejora_chico > 3 * mejora_grande
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} EPISTÉMICA: doblar datos libera {mejora_chico:.3f} "
              f"bits/muestra cuando falta aprender y {mejora_grande:.3f} cuando ya se aprendió")
    if not c3:
        fallos.append("epistemica")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — una sola moneda debajo de todos los impulsos."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Energía libre en MDL: la unificación ejecutable")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31")
