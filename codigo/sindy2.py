# sindy2.py — SINDy: EL SEGUNDO MOTOR DE DESCUBRIMIENTO, rival interno de PySR.
# Implementado el 8-ago-2026. Dos motores INDEPENDIENTES que llegan a la misma ley valen más que
# uno — y uno que descubre donde el otro calla es una alarma de método en cualquiera de los dos.
#
# CÓMO (regresión dispersa, matemática pura): la derivada de cada señal se ajusta como combinación
# LINEAL de un diccionario de términos (1, x, v, x², xv, ...), y se PODAN los coeficientes chicos
# iterativamente (STLSQ). Queda una ecuación RALA y legible — el mismo idioma composicional de la
# casa (G5), por otro camino.
#
# EL CRITERIO DE LA CASA que SINDy de fábrica no trae: un término solo cuenta si REPLICA — el
# soporte (qué términos sobreviven) debe ser IDÉNTICO al ajustar sobre dos mitades independientes
# de los datos. Sin replicación no hay ley, hay ajuste (la lección de N-002 aplicada al nacer).
#
# Regla 31: recupera un oscilador amortiguado conocido término a término; en datos barajados y en
# ruido puro NO debe replicar soporte alguno.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOMBRES = ["1", "x", "v", "x2", "xv", "v2"]


def _diccionario(X):
    x, v = X[:, 0], X[:, 1]
    return np.column_stack([np.ones(len(x)), x, v, x * x, x * v, v * v])


def _stlsq(Theta, dX, umbral=0.05, pasadas=8):
    W, *_ = np.linalg.lstsq(Theta, dX, rcond=None)
    for _ in range(pasadas):
        chicos = np.abs(W) < umbral
        W[chicos] = 0.0
        for j in range(dX.shape[1]):
            act = ~chicos[:, j]
            if act.sum() == 0:
                continue
            W[act, j], *_ = np.linalg.lstsq(Theta[:, act], dX[:, j], rcond=None)
    return W


def descubrir(X, umbral=0.05, dt=1.0):
    """X: (T, 2). Devuelve la ley SOLO si el soporte replica entre mitades Y no es vacío.
    LECCIONES DE LA PRIMERA CORRIDA (8-ago-2026), cazadas por su propia Regla 31:
      1. sin `dt`, la derivada queda multiplicada por el paso y la poda se come coeficientes
         reales (la ley dx=v con dt=0.05 aparece como 0.05·v < umbral → 'nada');
      2. dos mitades con soporte VACÍO "replicaban": una ley vacía no es una ley replicada.
    """
    dX = np.gradient(X, axis=0) / dt
    mitad = len(X) // 2
    Wa = _stlsq(_diccionario(X[:mitad]), dX[:mitad], umbral)
    Wb = _stlsq(_diccionario(X[mitad:]), dX[mitad:], umbral)
    sop_a, sop_b = (np.abs(Wa) > 0), (np.abs(Wb) > 0)
    if not np.array_equal(sop_a, sop_b) or sop_a.sum() == 0:
        return None
    W = _stlsq(_diccionario(X), dX, umbral)
    if not np.array_equal(np.abs(W) > 0, sop_a):
        return None            # el ajuste final debe confirmar el MISMO soporte de las mitades
    terminos = {f"d{var}/dt": [(NOMBRES[i], round(float(W[i, j]), 4))
                               for i in range(len(NOMBRES)) if abs(W[i, j]) > 0]
                for j, var in enumerate(["x", "v"])}
    return terminos


def regla31(verbose=True):
    rng = np.random.default_rng(19)
    fallos = []
    # oscilador amortiguado: dx=v, dv=-0.4x-0.1v (verdad conocida)
    T, dt = 3000, 0.05
    x, v = 1.5, 0.0
    tray = []
    for _ in range(T):
        tray.append([x, v])
        x, v = x + v * dt, v + (-0.4 * x - 0.1 * v) * dt
    X = np.array(tray)
    ley = descubrir(X, dt=dt)
    c1 = (ley is not None
          and [t for t, _ in ley["dx/dt"]] == ["v"]
          and sorted(t for t, _ in ley["dv/dt"]) == ["v", "x"])
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} OSCILADOR: recupera la ley rala termino a termino "
              f"({ley if ley else 'nada'})")
    if not c1:
        fallos.append("oscilador")

    ley2 = descubrir(X[rng.permutation(len(X))], dt=dt)
    c2 = ley2 is None
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} BARAJADO: sin replicacion no hay ley "
              f"({'callo' if c2 else ley2})")
    if not c2:
        fallos.append("barajado")

    ruido = np.column_stack([rng.normal(size=3000), rng.normal(size=3000)])
    ley3 = descubrir(ruido)
    c3 = ley3 is None
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} RUIDO PURO: calla ({'callo' if c3 else ley3})")
    if not c3:
        fallos.append("ruido")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — segundo motor listo para ser rival de PySR."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="SINDy con replicacion obligatoria: el segundo motor")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (su uso como rival oficial exige prerregistro)")
