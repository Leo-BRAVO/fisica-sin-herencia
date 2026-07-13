# conservada.py — cantidades conservadas: combinaciones de las señales cuyo VALOR casi no
# cambia en el tiempo (invariantes), con control negativo (barajado) integrado.
#
# Método (Regla 2: matemática genérica, sin física con nombre) — variante de Análisis de
# Rasgos Lentos (Slow Feature Analysis) generalizado: sobre una base de funciones (las
# variables de X y, si --grado 2, sus productos), se busca la combinación lineal c que
# MINIMIZA la razón (c^T D c)/(c^T C c), con C = covarianza de los valores de la base y
# D = covarianza de sus diferencias temporales (dentro de cada réplica, sin cruzar
# fronteras entre réplicas). Razón chica -> la combinación casi no cambia en el tiempo ->
# candidata a cantidad conservada. Se resuelve por blanqueo de Cholesky (sin scipy, para
# no añadir dependencias): L = chol(C), M = L^-1 D L^-T, eigh(M) da (lambda, w), y se
# transforma de vuelta c = L^-T w.
#
# Control negativo (misma lógica de la Regla 11 que usa descubrir.py): se repite
# EXACTAMENTE el mismo cálculo con el orden temporal de cada réplica de entrenamiento
# permutado al azar (independiente por réplica, rng semilla fija 0), --barajados veces, y
# se guarda el autovalor MÍNIMO de cada corrida. El score de cada candidata real es su
# lambda dividido por la mediana de esos mínimos barajados: si una candidata real no es al
# menos 5 veces más constante que el piso del azar (score < 0.2), no se considera seria.
#
# Validación en jueces (réplicas fuera del entrenamiento): para las candidatas serias se
# compara, réplica por réplica, la varianza de la candidata evaluada en los datos reales
# contra su varianza evaluada en una reconstrucción barajada de ESA MISMA réplica (usando
# el propio mecanismo nulo="barajado" de preparar(), que permuta las señales ANTES de
# calcular los cambios — así los cambios barajados quedan hechos de pares al azar y dejan
# de ser derivadas reales, lo que rompe cualquier candidata que dependa de ellos).
#
# Uso: python conservada.py <carpeta_csvs> [--jueces 3 7 11] [--grado 2] [--barajados 20]
#      [--centrar] [--top 3]

import os
import glob
import json
import argparse

import numpy as np

from descubrir import preparar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def construir_base(X, grado):
    """Construye la base de funciones de una sola réplica: v_i (grado 1) y, si grado>=2,
    todos los productos v_i*v_j con i<=j (incluye los cuadrados v_i*v_i). Devuelve
    (matriz T x F, nombres). Variables base = TODAS las columnas de X (señales+cambios)."""
    k = X.shape[1]
    columnas = [X[:, i] for i in range(k)]
    nombres = [f"v{i+1}" for i in range(k)]
    if grado >= 2:
        for i in range(k):
            for j in range(i, k):
                columnas.append(X[:, i] * X[:, j])
                nombres.append(f"v{i+1}*v{j+1}")
    return np.column_stack(columnas), nombres


def diffs_dentro_de_replica(matrices):
    """Diferencia fila t+1 - fila t POR SEPARADO en cada réplica (lista de matrices) y
    concatena el resultado; nunca resta entre el final de una réplica y el comienzo de
    la siguiente."""
    return np.vstack([np.diff(m, axis=0) for m in matrices])


def cov_reg(M):
    F = M.shape[1]
    return np.cov(M, rowvar=False) + 1e-9 * np.eye(F)


def resolver_generalizado(C, D):
    """Minimiza (c^T D c)/(c^T C c) sin scipy: blanqueo de Cholesky + eigh de numpy.
    Devuelve autovalores ascendentes (menor = más conservado) y sus vectores c (columnas),
    normalizados a norma 1 (la normalización no cambia ninguna razón, solo hace legibles
    los coeficientes al imprimir)."""
    L = np.linalg.cholesky(C)
    Linv = np.linalg.inv(L)
    M = Linv @ D @ Linv.T
    lam, W = np.linalg.eigh(M)
    Cvec = Linv.T @ W
    Cvec = Cvec / np.linalg.norm(Cvec, axis=0, keepdims=True)
    return lam, Cvec


def calcular_lambdas(bases):
    """bases: lista de matrices YA ESTANDARIZADAS por réplica (grupo de entrenamiento).
    Arma B y dB, calcula C=cov(B) y D=cov(dB), y resuelve el problema generalizado."""
    B = np.vstack(bases)
    dB = diffs_dentro_de_replica(bases)
    C = cov_reg(B)
    D = cov_reg(dB)
    return resolver_generalizado(C, D)


def barajar_minimos(bases, barajados):
    """Control negativo: permuta el orden temporal de cada réplica (independiente por
    réplica, mismo rng con semilla fija 0 avanzando entre corridas) y repite EXACTAMENTE
    el mismo cálculo --barajados veces. Devuelve la lista de autovalores MÍNIMOS."""
    rng = np.random.default_rng(0)
    minimos = []
    for _ in range(barajados):
        barajadas = [b[rng.permutation(len(b))] for b in bases]
        lam, _ = calcular_lambdas(barajadas)
        minimos.append(float(lam.min()))
    return minimos


def expresion_top6(c, nombres, n=6):
    orden = np.argsort(-np.abs(c))[:n]
    return " ".join(f"{c[i]:+.3f}*{nombres[i]}" for i in orden)


def main():
    ap = argparse.ArgumentParser(
        description="Busca combinaciones de senales que casi no cambian en el tiempo "
                     "(cantidades conservadas), con control negativo integrado.")
    ap.add_argument("carpeta", help="carpeta con los CSV de las replicas (preparadas, sin suavizar/retardos)")
    ap.add_argument("--jueces", nargs="+", type=int, default=[3, 7, 11],
                     help="posiciones 1-indexadas (lista ordenada de CSVs) usadas como jueces, no en el entrenamiento")
    ap.add_argument("--grado", type=int, default=2,
                     help="1 = solo v_i ; 2 (o mas) = agrega tambien los productos v_i*v_j")
    ap.add_argument("--barajados", type=int, default=20,
                     help="numero de corridas del control negativo (orden temporal permutado)")
    ap.add_argument("--centrar", action="store_true",
                     help="centra cada replica en su propia media antes de construir las variables")
    ap.add_argument("--top", type=int, default=3,
                     help="cuantas candidatas serias (score < 0.2) validar en los jueces")
    args = ap.parse_args()
    if args.barajados < 1:
        raise SystemExit("--barajados debe ser >= 1 (se necesita al menos una corrida de control negativo)")

    csvs = sorted(glob.glob(os.path.join(args.carpeta, "*.csv")))
    if not csvs:
        print("sin CSVs en la carpeta:", args.carpeta)
        return

    jidx_bruto = {j - 1 for j in args.jueces}
    for j in jidx_bruto:
        if j < 0 or j >= len(csvs):
            print(f"AVISO: indice de juez {j + 1} fuera de rango (hay {len(csvs)} csvs); se ignora")
    jidx = {j for j in jidx_bruto if 0 <= j < len(csvs)}
    idx_tr = [i for i in range(len(csvs)) if i not in jidx]
    idx_te = [i for i in range(len(csvs)) if i in jidx]
    if not idx_tr:
        print("no quedan replicas de entrenamiento (todas quedaron como jueces)")
        return

    # Paso 2: cargar cada CSV crudo — sin suavizar, sin retardos (leccion INFORME-18)
    Xs = [preparar(c, centrar=args.centrar)[0] for c in csvs]
    k = Xs[0].shape[1]
    for X in Xs:
        assert X.shape[1] == k, "todas las replicas deben tener el mismo numero de columnas en X"

    # Paso 3: base de funciones por replica (grado 1 o 2), sobre variables CRUDAS
    bases_crudas, nombres = [], None
    for X in Xs:
        b, nombres = construir_base(X, args.grado)
        bases_crudas.append(b)
    F = len(nombres)

    # Paso 4: estandarizar con media/desvio SOLO del grupo de entrenamiento, aplicado a todas
    cat_tr = np.vstack([bases_crudas[i] for i in idx_tr])
    mu = cat_tr.mean(axis=0)
    sd = cat_tr.std(axis=0)
    sd[sd == 0] = 1.0
    bases_std = [(b - mu) / sd for b in bases_crudas]
    bases_tr = [bases_std[i] for i in idx_tr]

    # Pasos 5-6: B, dB, C, D y el problema generalizado sobre el entrenamiento agrupado
    lam, Cvec = calcular_lambdas(bases_tr)

    # Paso 7: control negativo (barajado) y score
    minimos = barajar_minimos(bases_tr, args.barajados)
    piso = float(np.median(minimos))
    score = lam / piso if piso > 0 else np.full(F, np.inf)
    seria = score < 0.2

    print("=== CANTIDADES CONSERVADAS (control negativo integrado) ===")
    print(f"carpeta: {args.carpeta}")
    print(f"replicas: {len(csvs)} total | entrenamiento: {len(idx_tr)} | jueces (1-indexado): {sorted(j + 1 for j in idx_te)}")
    print(f"variables base v1..v{k} (columnas de X: senales + cambios) | grado={args.grado} -> {F} funciones en la base")
    print(f"piso del azar (mediana de {args.barajados} autovalores minimos barajados): {piso:.6g}")
    print()
    print(f"{'idx':>4} {'lambda':>12} {'score':>10} {'seria':>6}  expresion (6 terminos de mayor |coef|)")
    tope = min(F, 30)
    for i in range(tope):
        print(f"{i:>4} {lam[i]:>12.6g} {score[i]:>10.4f} {'SI' if seria[i] else 'no':>6}  {expresion_top6(Cvec[:, i], nombres)}")
    if F > tope:
        print(f"... ({F - tope} funciones mas en el archivo de resultados)")

    # Paso 8: validacion en jueces para las --top candidatas serias
    serias_idx = [i for i in range(F) if seria[i]][:args.top]
    print()
    print(f"=== VALIDACION EN JUECES (top {args.top} candidatas serias, score < 0.2) ===")
    if not serias_idx:
        print("ninguna candidata fue seria (score < 0.2); no hay nada que validar en jueces")

    validaciones = []
    rng_juez = np.random.default_rng(0)
    for i in serias_idx:
        c = Cvec[:, i]
        ratios = {}
        for pos in idx_te:
            csv_j = csvs[pos]
            bj_real = bases_std[pos]  # ya construida y estandarizada arriba
            Xj_baraj = preparar(csv_j, nulo="barajado", rng=rng_juez, centrar=args.centrar)[0]
            bj_baraj_cruda, _ = construir_base(Xj_baraj, args.grado)
            bj_baraj = (bj_baraj_cruda - mu) / sd
            f_real = bj_real @ c
            f_baraj = bj_baraj @ c
            v_real = float(np.var(f_real))
            v_baraj = float(np.var(f_baraj))
            ratio = v_real / v_baraj if v_baraj > 0 else float("inf")
            ratios[os.path.basename(csv_j)] = ratio
        validaciones.append({"indice": int(i), "expresion": expresion_top6(c, nombres),
                              "lambda": float(lam[i]), "score": float(score[i]), "ratios_jueces": ratios})
        print(f"candidata {i} (lambda={lam[i]:.6g}, score={score[i]:.4f}): {expresion_top6(c, nombres)}")
        for nombre_csv, r in ratios.items():
            print(f"   juez {nombre_csv}: ratio_juez = {r:.4f}")

    # Paso 9: guardar todo
    nombre_carpeta = os.path.basename(os.path.normpath(args.carpeta))
    outdir = os.path.join(BASE, "resultados", f"conservadas-{nombre_carpeta}")
    os.makedirs(outdir, exist_ok=True)
    resumen = {
        "carpeta": args.carpeta,
        "csvs": [os.path.basename(c) for c in csvs],
        "jueces_1indexado": sorted(args.jueces),
        "grado": args.grado,
        "barajados": args.barajados,
        "centrar": bool(args.centrar),
        "top": args.top,
        "n_variables_base_X": k,
        "n_funciones_base": F,
        "nombres_base": nombres,
        "n_entrenamiento": len(idx_tr),
        "n_jueces": len(idx_te),
        "lambdas_barajados_minimos": minimos,
        "piso_barajado": piso,
        "candidatas": [
            {"indice": i, "lambda": float(lam[i]), "score": float(score[i]), "seria": bool(seria[i]),
             "expresion_top6": expresion_top6(Cvec[:, i], nombres),
             "coeficientes": {nombres[j]: float(Cvec[j, i]) for j in range(F)}}
            for i in range(F)
        ],
        "validacion_jueces": validaciones,
    }
    with open(os.path.join(outdir, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)
    print()
    print("guardado en:", os.path.join(outdir, "resumen.json"))


if __name__ == "__main__":
    main()
