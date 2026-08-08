# regla31_conservada.py — LA REGLA 31 aplicada a la herramienta F3 (conservada.py).
# "Toda herramienta de descubrimiento debe FALLAR en datos donde no hay nada."
#
# Genera dos mundos sinteticos deterministas (semillas fijas) y corre sobre ambos el
# MISMO calculo de conservada.py con el nulo elegido:
#   MUNDO VACIO — replicas independientes de caminatas aleatorias SUAVIZADAS: senales
#     con la textura de datos reales (suaves, autocorreladas) pero SIN ninguna cantidad
#     conservada ni relacion entre senales ni entre replicas, por construccion.
#   MUNDO LLENO — oscilador amortiguado ruidoso: s1 ~ A sin(wt+f), s2 ~ A cos(wt+f);
#     la combinacion s1^2 + s2^2 es genuinamente (casi) conservada dentro de cada replica.
#
# Veredicto de la herramienta bajo la Regla 31:
#   APRUEBA si (a) en el mundo VACIO ninguna candidata es seria (score >= 0.2), y
#             (b) en el mundo LLENO al menos una candidata es seria.
#   REPRUEBA en cualquier otro caso — y entonces la herramienta NO puede producir nodos.
#
# Historia (8-ago-2026, AUDITORIA-EXTERNA-01): con nulo "barajado" la herramienta
# REPRUEBA (a) — acepta el mundo vacio con score 0.0004 y jueces < 0.2, cumpliendo el
# criterio del prerregistro-16 sobre datos donde no hay nada. Con nulo "surrogado"
# (IAAFT) APRUEBA ambos. Por eso el surrogado es el unico nulo valido para veredictos.
#
# Uso: python regla31_conservada.py [--nulo surrogado|barajado] [--barajados 20]

import os
import sys
import shutil
import argparse
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descubrir import preparar
from conservada import construir_base, calcular_lambdas, nulos_minimos, ratio_juez


def escribir_replicas(carpeta, senales_por_replica):
    os.makedirs(carpeta, exist_ok=True)
    rutas = []
    for i, (s1, s2) in enumerate(senales_por_replica, start=1):
        ruta = os.path.join(carpeta, f"replica_{i}.csv")
        with open(ruta, "w") as f:
            f.write("t,s1,s2\n")
            for t in range(len(s1)):
                f.write(f"{t},{s1[t]:.6f},{s2[t]:.6f}\n")
        rutas.append(ruta)
    return rutas


def mundo_vacio(rng, n_replicas=6, T=600):
    """Caminatas aleatorias suavizadas e INDEPENDIENTES: suaves como datos reales,
    sin nada conservado por construccion."""
    k = np.ones(9) / 9
    reps = []
    for _ in range(n_replicas):
        s1 = np.convolve(np.cumsum(rng.normal(size=T + 8)), k, mode="valid")
        s2 = np.convolve(np.cumsum(rng.normal(size=T + 8)), k, mode="valid")
        reps.append((s1[:T], s2[:T]))
    return reps


def mundo_lleno(rng, n_replicas=6, T=600):
    """Oscilador con amplitud casi constante y ruido leve: s1^2+s2^2 se conserva
    genuinamente dentro de cada replica (amplitudes distintas entre replicas)."""
    reps = []
    for _ in range(n_replicas):
        A = rng.uniform(1.0, 3.0)
        w = rng.uniform(0.15, 0.35)
        f0 = rng.uniform(0, 2 * np.pi)
        t = np.arange(T)
        s1 = A * np.sin(w * t + f0) + rng.normal(0, 0.02, T)
        s2 = A * np.cos(w * t + f0) + rng.normal(0, 0.02, T)
        reps.append((s1, s2))
    return reps


def correr_mundo(csvs, nulo, barajados, grado=2):
    """El criterio COMPLETO que pare nodos (prerregistros 16-17): nivel A (candidata seria,
    score < 0.2 contra el piso del nulo) Y nivel B (mayoria de jueces con ratio < 0.2).
    Devuelve (mejor_score, n_serias, aprueba_jueces). Leccion registrada: en senales no
    estacionarias el nivel A puede sobreajustar; el verdugo DECISIVO es el nivel B."""
    jidx = {len(csvs) - 2, len(csvs) - 1}  # ultimas dos replicas como jueces
    idx_tr = [i for i in range(len(csvs)) if i not in jidx]
    Xs = [preparar(c)[0] for c in csvs]
    bases_crudas = [construir_base(X, grado)[0] for X in Xs]
    cat_tr = np.vstack([bases_crudas[i] for i in idx_tr])
    mu, sd = cat_tr.mean(axis=0), cat_tr.std(axis=0)
    sd[sd == 0] = 1.0
    bases_std = [(b - mu) / sd for b in bases_crudas]
    lam, Cvec = calcular_lambdas([bases_std[i] for i in idx_tr])
    minimos = nulos_minimos([csvs[i] for i in idx_tr], grado, mu, sd, barajados, nulo, False)
    piso = float(np.median(minimos))
    score = lam / piso if piso > 0 else np.full(len(lam), np.inf)
    serias = int((score < 0.2).sum())
    aprueba_jueces = False
    if serias:
        rng_j = np.random.default_rng(0)
        c = Cvec[:, int(np.argmin(score))]
        ratios = [ratio_juez(csvs[p], c, bases_std[p], mu, sd, grado, nulo, rng_j, False)
                  for p in sorted(jidx)]
        aprueba_jueces = sum(r < 0.2 for r in ratios) > len(ratios) / 2
    return float(score.min()), serias, aprueba_jueces


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nulo", choices=["surrogado", "barajado"], default="surrogado")
    ap.add_argument("--barajados", type=int, default=20)
    args = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="regla31_")
    try:
        vacio = escribir_replicas(os.path.join(tmp, "vacio"),
                                  mundo_vacio(np.random.default_rng(12345)))
        lleno = escribir_replicas(os.path.join(tmp, "lleno"),
                                  mundo_lleno(np.random.default_rng(54321)))

        print(f"=== REGLA 31 sobre conservada.py (criterio completo A+B) | nulo = {args.nulo} ===")
        sv, nv, jv = correr_mundo(vacio, args.nulo, args.barajados)
        pare_vacio = (nv > 0) and jv
        print(f"MUNDO VACIO (nada conservado): mejor score = {sv:.4g} | serias: {nv} | "
              f"jueces aprueban: {jv} -> {'FALSO POSITIVO (pariria nodo)' if pare_vacio else 'ok, rechazado'}")
        sl, nl, jl = correr_mundo(lleno, args.nulo, args.barajados)
        pare_lleno = (nl > 0) and jl
        print(f"MUNDO LLENO (s1^2+s2^2 conservada): mejor score = {sl:.4g} | serias: {nl} | "
              f"jueces aprueban: {jl} -> {'ok, encontrada' if pare_lleno else 'CIEGA: no encontro lo que existe'}")

        aprueba = (not pare_vacio) and pare_lleno
        print()
        if aprueba:
            print("REGLA 31: LA HERRAMIENTA APRUEBA — puede producir nodos con este nulo.")
            sys.exit(0)
        print("REGLA 31: LA HERRAMIENTA REPRUEBA — con este nulo NO puede producir nodos.")
        sys.exit(1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
