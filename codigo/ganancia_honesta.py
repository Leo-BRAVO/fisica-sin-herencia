# ganancia_honesta.py — LA VARA QUE NADIE USA: cuanto del rendimiento es DINAMICA
# y cuanto es solo TEXTURA. (Nace el 8-ago-2026 de un fracaso convertido en instrumento.)
#
# DE DONDE VIENE (la historia importa): el nulo surrogado IAAFT "fallo" al no poder falsificar
# los latentes de Diego — daba el mismo mundo con otro nombre. Parecia un test roto. Pero el
# IAAFT conserva el espectro de cada senal (la TEXTURA: suavidad, autocorrelacion) y destruye
# fases y acoples (la DINAMICA). Entonces lo que el motor logra en el mundo surrogado ES, POR
# CONSTRUCCION, la parte de su rendimiento explicable por textura. No era un juez roto: era un
# MEDIDOR que nadie habia leido como tal.
#
#     GANANCIA_HONESTA = reduccion_en_datos_REALES  −  reduccion_en_datos_SURROGADOS
#
# ambas medidas SOBRE LOS JUECES CONGELADOS (auditoria sellada). Lo que queda es la parte del
# poder predictivo que la textura NO puede explicar.
#
# POR QUE ES NUESTRA Y NO DE ELLOS: los laboratorios eligen representaciones por error de
# reconstruccion o de prediccion — y la textura satisface AMBOS. Nadie corre surrogados como
# parte rutinaria del aprendizaje de representaciones, porque nadie tiene jueces sellados ni
# la disciplina de nulos. Nosotros si. Primera medicion (INFORME-27): Mendeley 91.5% honesto;
# los latentes de Diego -0.1% — todo su poder era textura.
#
# Uso:
#   python ganancia_honesta.py --comparar <campana_real> <campana_nula>   (lee resumenes ya corridos)
#   python ganancia_honesta.py --medir <carpeta_datos> [--jueces 3 6 9] [--suavizar N] [--retardos N]
#         (medicion RAPIDA con el rival lineal como sonda: sirve para elegir representacion
#          sin gastar el motor simbolico — el veredicto oficial siempre lo dan las campanas)
#   python ganancia_honesta.py --regla31    (el instrumento se prueba a si mismo)

import os
import sys
import json
import glob
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))
from descubrir import preparar, error_linea_base, error_rival_lineal


def reduccion(base, mejor):
    """Fraccion del error trivial que la ley elimina. Negativa si la ley es peor que lo trivial."""
    return 1.0 - (mejor / base) if base > 0 else float("nan")


def comparar(campana_real, campana_nula):
    """Ganancia honesta a partir de dos campanas YA corridas (la via oficial)."""
    def leer(c):
        d = json.load(open(os.path.join(BASE, "resultados", c, "resumen.json"), encoding="utf-8"))
        return d["mse_base"], min(v["mse_total"] for v in d["semillas"].values()), d.get("nulo")
    br, mr, nr = leer(campana_real)
    bn, mn, nn = leer(campana_nula)
    if nr:
        raise SystemExit(f"{campana_real} es una corrida NULA — el primer argumento debe ser la real")
    if nn != "surrogado":
        print(f"AVISO: la corrida nula usa '{nn}', no 'surrogado'. La ganancia honesta EXIGE surrogado: "
              "es el unico nulo que conserva la textura y destruye solo los acoples.")
    rr, rn = reduccion(br, mr), reduccion(bn, mn)
    return {"real": campana_real, "nula": campana_nula,
            "reduccion_real": round(rr, 5), "reduccion_falsa": round(rn, 5),
            "ganancia_honesta": round(rr - rn, 5)}


def medir(carpeta, jueces, suavizar=0, retardos=0, centrar=False, semilla=0, surrogados=8):
    """Sonda RAPIDA con el rival lineal: no gasta el motor simbolico. Sirve para ELEGIR
    representacion (p.ej. que dimension latente merece existir) antes de invertir campanas."""
    csvs = sorted(glob.glob(os.path.join(carpeta, "*.csv")))
    if len(csvs) < 2:
        raise SystemExit(f"se necesitan >=2 replicas en {carpeta}")
    jidx = {j - 1 for j in jueces}

    def armar(nulo, s=None):
        rng = np.random.default_rng(semilla if s is None else s)
        Xtr, Ytr, Xte, Yte = [], [], [], []
        for i, c in enumerate(csvs):
            X, Y = preparar(c, nulo=nulo, rng=rng, suavizar=suavizar,
                            retardos=retardos, centrar=centrar)
            (Xte if i in jidx else Xtr).append(X)
            (Yte if i in jidx else Ytr).append(Y)
        return np.vstack(Xtr), np.vstack(Ytr), np.vstack(Xte), np.vstack(Yte)

    # UN SOLO SORTEO DE SURROGADO MIENTE (medido el 8-ago-2026): la ganancia varia +-0.015 entre
    # sorteos, y reportar uno solo equivale a elegir el que salio. Se promedian N y se reporta la
    # DESVIACION: un numero sin su dispersion no es una medicion, es una anecdota.
    X_tr, Y_tr, X_te, Y_te = armar(None)
    r_real = reduccion(error_linea_base(X_te, Y_te, Y_tr),
                       error_rival_lineal(X_tr, Y_tr, X_te, Y_te))
    falsas = []
    for s in range(surrogados):
        a, b, c, d = armar("surrogado", s)
        falsas.append(reduccion(error_linea_base(c, d, b), error_rival_lineal(a, b, c, d)))
    falsas = np.array(falsas)
    ganancias = r_real - falsas
    return {"carpeta": os.path.basename(os.path.normpath(carpeta)),
            "reduccion_real": round(float(r_real), 5),
            "reduccion_falsa": round(float(falsas.mean()), 5),
            "reduccion_falsa_desv": round(float(falsas.std()), 5),
            "ganancia_honesta": round(float(ganancias.mean()), 5),
            "ganancia_honesta_desv": round(float(ganancias.std()), 5),
            "surrogados": surrogados}


def regla31():
    """EL INSTRUMENTO SE PRUEBA A SI MISMO (Regla 31), con dos mundos deterministas:
      MUNDO TEXTURA — dos caminatas suavizadas INDEPENDIENTES: predecir funciona solo por
        autocorrelacion; no hay dinamica que descubrir -> ganancia honesta ~ 0.
      MUNDO ACOPLADO — s2 depende del PASADO de s1: hay dinamica real que el surrogado destruye
        -> ganancia honesta claramente > 0.
    Si el instrumento no separa estos dos mundos, no puede opinar sobre ninguna representacion."""
    import tempfile, shutil
    tmp = tempfile.mkdtemp(prefix="gh31_")
    try:
        def escribir(carpeta, reps):
            os.makedirs(carpeta, exist_ok=True)
            for i, (s1, s2) in enumerate(reps, 1):
                with open(os.path.join(carpeta, f"r{i}.csv"), "w") as f:
                    f.write("t,s1,s2\n")
                    for t in range(len(s1)):
                        f.write(f"{t},{s1[t]:.6f},{s2[t]:.6f}\n")
            return carpeta

        k = np.ones(9) / 9
        rng = np.random.default_rng(2026)
        textura, acoplado = [], []
        for _ in range(6):
            a = np.convolve(np.cumsum(rng.normal(size=608)), k, mode="valid")[:600]
            b = np.convolve(np.cumsum(rng.normal(size=608)), k, mode="valid")[:600]
            textura.append((a, b))                       # independientes
            c = np.roll(a, 3) * 0.9 + rng.normal(0, 0.01, 600)   # b depende del PASADO de a
            acoplado.append((a, c))
        gt = medir(escribir(os.path.join(tmp, "textura"), textura), [5, 6])
        ga = medir(escribir(os.path.join(tmp, "acoplado"), acoplado), [5, 6])
        print("=== REGLA 31 sobre ganancia_honesta ===")
        print(f"MUNDO TEXTURA  (nada que descubrir): ganancia honesta = {gt['ganancia_honesta']:+.4f}")
        print(f"MUNDO ACOPLADO (dinamica real)     : ganancia honesta = {ga['ganancia_honesta']:+.4f}")
        aprueba = gt["ganancia_honesta"] < 0.05 and ga["ganancia_honesta"] > 0.10
        print("\n" + ("REGLA 31: APRUEBA — el instrumento distingue dinamica de textura."
                      if aprueba else
                      "REGLA 31: REPRUEBA — no separa los dos mundos; NO puede opinar sobre representaciones."))
        return 0 if aprueba else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Ganancia honesta: dinamica menos textura")
    ap.add_argument("--comparar", nargs=2, metavar=("REAL", "NULA"))
    ap.add_argument("--medir", default=None)
    ap.add_argument("--jueces", nargs="+", type=int, default=[3, 6, 9])
    ap.add_argument("--suavizar", type=int, default=0)
    ap.add_argument("--retardos", type=int, default=0)
    ap.add_argument("--centrar", action="store_true")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    if a.comparar:
        print(json.dumps(comparar(*a.comparar), indent=2, ensure_ascii=False))
    if a.medir:
        print(json.dumps(medir(a.medir, a.jueces, a.suavizar, a.retardos, a.centrar),
                         indent=2, ensure_ascii=False))
