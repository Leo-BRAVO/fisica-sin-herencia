# sindy3.py — SINDy EN FORMA DEBIL + BOOTSTRAP (prerregistro-28, FIRMADO 9-ago-2026).
#
# POR QUE EXISTE (el problema medido, no supuesto): sindy2.py calcula la derivada restando
# posiciones consecutivas (np.gradient). Esa resta AMPLIFICA el ruido: el error relativo de la
# derivada crece como sigma/dt, asi que con sensores encarnados —ruidosos por construccion, como
# los de cualquier cuerpo— la ley real queda enterrada bajo el ruido de su propia derivada.
#
# LA CURA (matematica pura, cero fisica heredada): no restar. Integrar.
#   Se elige una funcion de prueba phi que vale cero en los bordes de su ventana. Entonces
#       integral( phi * dx/dt ) = -integral( phi' * x )        [integracion por partes]
#   El lado derecho NO tiene ninguna derivada de los datos: solo pesa x contra una curva conocida.
#   El ruido, al integrarse contra phi', se cancela solo (promedia a cero). Es la diferencia entre
#   pesar el arroz grano a grano con pulso tembloroso y pesar el saco entero.
#
# LA SEGUNDA MEJORA — BOOTSTRAP en vez de dos mitades: sindy2 exige que el soporte replique entre
# DOS mitades. Es la idea correcta con el musculo minimo. Aqui se remuestrean las ventanas cientos
# de veces y cada termino recibe una PROBABILIDAD DE INCLUSION: "aparecio en 287 de 300 remuestreos"
# dice mucho mas que "aparecio dos veces". Un termino solo entra a la ley si supera el piso
# prerregistrado de inclusion.
#
# Regla 31 (cuatro casos, uno de ellos imposible para sindy2):
#   1. OSCILADOR LIMPIO: recupera dx=v, dv=-0.4x-0.1v termino a termino.
#   2. OSCILADOR CON RUIDO REAL: recupera la MISMA ley donde la derivada numerica ya fracasa
#      — es el control positivo que justifica la existencia de este modulo.
#   3. BARAJADO: calla.
#   4. RUIDO PURO: calla (y una ley vacia jamas cuenta como ley replicada — la leccion de sindy2).

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOMBRES = ["1", "x", "v", "x2", "xv", "v2"]


def _diccionario(X):
    x, v = X[:, 0], X[:, 1]
    return np.column_stack([np.ones(len(x)), x, v, x * x, x * v, v * v])


def _prueba(m, p=6):
    """La funcion de prueba phi(s)=(1-s^2)^p sobre m muestras, y su derivada. Vale CERO en ambos
    bordes (por eso no hay termino de frontera al integrar por partes) y es suave por dentro."""
    s = np.linspace(-1.0, 1.0, m)
    phi = (1.0 - s ** 2) ** p
    dphi = -2.0 * p * s * (1.0 - s ** 2) ** (p - 1)
    return phi, dphi


def _sistema_debil(X, dt, ventana, salto, p=6):
    """Construye (A, b) SIN derivar los datos ni una sola vez.
       b[k, j] = integral( phi * d(x_j)/dt )  =  -integral( phi' * x_j )   <- solo pesa los datos
       A[k, i] = integral( phi * theta_i )
    Cada fila es una VENTANA de tiempo. El ruido se promedia dentro de cada integral."""
    T = len(X)
    if T < ventana + 1:
        return None, None
    phi, dphi = _prueba(ventana, p)
    Theta = _diccionario(X)
    filas_A, filas_b = [], []
    for ini in range(0, T - ventana + 1, salto):
        seg = slice(ini, ini + ventana)
        # el integrando se acumula por trapecios; dt cancela al dividir b entre A salvo el factor
        # de la derivada de phi respecto al tiempo real de la ventana
        escala = 2.0 / (ventana * dt)          # ds/dt: la ventana [-1,1] dura ventana*dt segundos
        filas_b.append(-np.trapezoid(dphi[:, None] * X[seg], dx=dt, axis=0) * escala)
        filas_A.append(np.trapezoid(phi[:, None] * Theta[seg], dx=dt, axis=0))
    return np.array(filas_A), np.array(filas_b)


def _stlsq(A, b, umbral=0.05, pasadas=8):
    W, *_ = np.linalg.lstsq(A, b, rcond=None)
    for _ in range(pasadas):
        chicos = np.abs(W) < umbral
        W[chicos] = 0.0
        for j in range(b.shape[1]):
            act = ~chicos[:, j]
            if act.sum() == 0:
                continue
            W[act, j], *_ = np.linalg.lstsq(A[:, act], b[:, j], rcond=None)
    return W


# GUARDA DE MUESTRAS. HALLAZGO DEL 9-ago-2026, encontrado al construir el sueño en dos fases:
# con series cortas el bootstrap declara leyes sobre RUIDO PURO. Medido, 6 semillas de ruido:
#   n=600 -> 2/6 leyes falsas | n=1000 -> 1/6 | n=1500 -> 1/6 | n=2000 -> 0/6 | n=3000 -> 0/6
# El remuestreo con reemplazo repite ventanas, y con pocas ventanas distintas la "replicacion"
# se vuelve un eco de si misma. Por debajo del minimo el motor NO OPINA: es la misma disciplina
# que el minimo de 20 ventanas del detector de contingencia.
MUESTRAS_MINIMAS = 2000


def descubrir(X, dt=1.0, umbral=0.05, ventana=None, salto=None,
              remuestreos=200, piso_inclusion=0.9, semilla=28):
    """La ley SOLO si cada termino supera el piso de inclusion del bootstrap Y el ajuste final
    sobre todas las ventanas confirma ese mismo soporte. Devuelve tambien las probabilidades,
    porque un numero que no se puede auditar no sirve de evidencia."""
    T = len(X)
    if T < MUESTRAS_MINIMAS:
        return None            # sin potencia no se opina (ver MUESTRAS_MINIMAS)
    ventana = ventana or max(20, T // 25)
    salto = salto or max(1, ventana // 4)
    A, b = _sistema_debil(X, dt, ventana, salto)
    if A is None or len(A) < 12:
        return None                     # sin ventanas suficientes no hay estadistica: se calla
    rng = np.random.default_rng(semilla)
    n = len(A)
    cuenta = np.zeros((len(NOMBRES), b.shape[1]))
    for _ in range(remuestreos):
        idx = rng.integers(0, n, n)     # remuestreo CON reemplazo de ventanas completas
        cuenta += (np.abs(_stlsq(A[idx], b[idx], umbral)) > 0).astype(float)
    prob = cuenta / remuestreos
    soporte = prob >= piso_inclusion
    if soporte.sum() == 0:
        return None                     # ley vacia NO es ley (leccion congelada de sindy2)
    W = _stlsq(A, b, umbral)
    if not np.array_equal(np.abs(W) > 0, soporte):
        return None                     # el ajuste completo debe confirmar lo que voto el bootstrap
    return {"terminos": {f"d{var}/dt": [(NOMBRES[i], round(float(W[i, j]), 4),
                                         round(float(prob[i, j]), 3))
                                        for i in range(len(NOMBRES)) if soporte[i, j]]
                         for j, var in enumerate(["x", "v"])},
            "ventanas": int(n), "remuestreos": int(remuestreos),
            "piso_inclusion": piso_inclusion}


def _oscilador(T=4000, dt=0.02, ruido=0.0, semilla=7):
    """Verdad conocida: dx/dt = v ; dv/dt = -0.4x - 0.1v. El ruido se agrega a lo MEDIDO
    (como un sensor real), no a la dinamica."""
    rng = np.random.default_rng(semilla)
    x, v, tray = 1.5, 0.0, []
    for _ in range(T):
        tray.append([x, v])
        x, v = x + v * dt, v + (-0.4 * x - 0.1 * v) * dt
    X = np.array(tray)
    if ruido > 0:
        X = X + rng.normal(0, ruido, X.shape)
    return X, dt


def _es_la_ley(ley):
    if ley is None:
        return False
    t = ley["terminos"]
    return ([n for n, _, _ in t["dx/dt"]] == ["v"]
            and sorted(n for n, _, _ in t["dv/dt"]) == ["v", "x"])


def regla31(verbose=True):
    fallos = []
    rng = np.random.default_rng(28)

    X, dt = _oscilador()
    ley = descubrir(X, dt=dt)
    c1 = _es_la_ley(ley)
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} OSCILADOR LIMPIO: recupera la ley rala "
              f"({ley['terminos'] if ley else 'nada'})")
    if not c1:
        fallos.append("oscilador-limpio")

    # EL CASO QUE JUSTIFICA ESTE MODULO: mismo mundo, sensor ruidoso. La derivada numerica de
    # sindy2 se ahoga aqui; la forma debil no deberia.
    Xr, dtr = _oscilador(ruido=0.02)
    ley_r = descubrir(Xr, dt=dtr)
    c2 = _es_la_ley(ley_r)
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} OSCILADOR CON SENSOR RUIDOSO: la forma debil "
              f"sobrevive ({ley_r['terminos'] if ley_r else 'nada'})")
    if not c2:
        fallos.append("oscilador-ruidoso")

    ley_b = descubrir(X[rng.permutation(len(X))], dt=dt)
    c3 = ley_b is None
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} BARAJADO: calla "
              f"({'callo' if c3 else ley_b['terminos']})")
    if not c3:
        fallos.append("barajado")

    puro = rng.normal(size=(4000, 2))
    ley_n = descubrir(puro, dt=dt)
    c4 = ley_n is None
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} RUIDO PURO: calla "
              f"({'callo' if c4 else ley_n['terminos']})")
    if not c4:
        fallos.append("ruido-puro")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — forma debil + bootstrap listos."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def comparar_con_sindy2(verbose=True):
    """La medida honesta de cuanto se gano: misma verdad, mismo ruido, los dos motores.
    No es un juez de nada — es el numero que justifica (o no) haber escrito este modulo."""
    import sindy2
    filas = []
    for ruido in (0.0, 0.005, 0.01, 0.02, 0.05):
        X, dt = _oscilador(ruido=ruido)
        viejo = sindy2.descubrir(X, dt=dt)
        ok_viejo = (viejo is not None
                    and [n for n, _ in viejo["dx/dt"]] == ["v"]
                    and sorted(n for n, _ in viejo["dv/dt"]) == ["v", "x"])
        ok_nuevo = _es_la_ley(descubrir(X, dt=dt))
        filas.append((ruido, ok_viejo, ok_nuevo))
        if verbose:
            print(f"  ruido {ruido:<6}: derivada numerica {'SI' if ok_viejo else 'no'}   "
                  f"forma debil {'SI' if ok_nuevo else 'no'}")
    return filas


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="SINDy en forma debil + bootstrap (prereg-28)")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--comparar", action="store_true",
                    help="mide cuanto aguanta cada motor al subir el ruido del sensor")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    if a.comparar:
        comparar_con_sindy2()
        sys.exit(0)
    print("uso: --regla31 | --comparar")
