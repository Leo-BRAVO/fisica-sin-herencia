# intermodal.py — EL ESPEJO DEL BEBÉ: reconocerse cruzando los sentidos (prerregistro-26, FIRMADO).
#
# LA IDEA BIOLÓGICA: un bebé frente al espejo se reconoce porque lo que SIENTE (propiocepción)
# coincide, instante a instante, con lo que VE. Nadie le enseña qué imagen es suya: la coherencia
# entre sus sentidos LO ES. Esa es la ecuación que faltaba entre los ojos y el cuerpo:
#
#     ESPEJO = correlación canónica máxima entre [latentes visuales] y [propiocepción],
#              medida en episodios-juez retenidos, MENOS su nulo (propiocepción de OTRO episodio).
#
# Si la vista lleva dentro al cuerpo, alguna dirección de sus latentes debe moverse CON el cuerpo
# sentido. Si el espejo neto es ~0, la vista no contiene al cuerpo — y eso convierte en NÚMERO el
# diagnóstico que el prereg-25 dio por tres vías.
#
# Regla 31: (1) visión construida DESDE la propiocepción → espejo alto; (2) visión independiente →
# espejo neto ~0; (3) el nulo de otro-episodio debe matar el espejo aunque las estadísticas
# marginales sean idénticas.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _cca_max(A, B):
    """Correlación canónica máxima entre dos bloques (matemática pura, vía SVD blanqueada)."""
    A = A - A.mean(0)
    B = B - B.mean(0)
    Ua, Sa, _ = np.linalg.svd(A, full_matrices=False)
    Ub, Sb, _ = np.linalg.svd(B, full_matrices=False)
    ra = (Sa > 1e-8 * Sa[0]).sum()
    rb = (Sb > 1e-8 * Sb[0]).sum()
    s = np.linalg.svd(Ua[:, :ra].T @ Ub[:, :rb], compute_uv=False)
    return float(s[0])


def espejo(vision, cuerpo, jueces, nulos=10, semilla=0):
    """vision/cuerpo: listas por episodio (T, d). El espejo se mide SOLO en episodios-juez;
    el nulo empareja la visión de un juez con el cuerpo de OTRO episodio (mismas estadísticas,
    cero coincidencia instante a instante)."""
    rng = np.random.default_rng(semilla)
    jidx = sorted({j - 1 for j in jueces})
    real = float(np.mean([_cca_max(vision[i], cuerpo[i]) for i in jidx]))
    falsas = []
    for _ in range(nulos):
        otros = [int(rng.choice([k for k in range(len(cuerpo)) if k != i])) for i in jidx]
        falsas.append(float(np.mean([_cca_max(vision[i], cuerpo[o][:len(vision[i])])
                                     for i, o in zip(jidx, otros)])))
    techo = float(np.max(falsas))
    return {"espejo": round(real, 4), "nulo_techo": round(techo, 4),
            "neto": round(real - techo, 4), "se_reconoce": bool(real > techo)}


def regla31(verbose=True):
    rng = np.random.default_rng(37)
    T, n_ep = 400, 8
    k9 = np.ones(9) / 9
    fallos = []

    def episodios(acoplada):
        vis, cue = [], []
        for _ in range(n_ep):
            prop = np.column_stack([np.convolve(rng.normal(size=T + 8), k9, mode="valid")[:T]
                                    for _ in range(4)])
            if acoplada:
                M = rng.normal(size=(4, 6))
                v = prop @ M + rng.normal(0, 0.4, (T, 6))     # la vista LLEVA al cuerpo dentro
            else:
                v = np.column_stack([np.convolve(rng.normal(size=T + 8), k9, mode="valid")[:T]
                                     for _ in range(6)])       # misma textura, cero cuerpo
            vis.append(v); cue.append(prop)
        return vis, cue

    v1, c1_ = episodios(True)
    r1 = espejo(v1, c1_, [7, 8])
    ok1 = r1["se_reconoce"] and r1["neto"] > 0.1
    if verbose:
        print(f"  {'ok  ' if ok1 else 'FALLO'} VISTA CON CUERPO DENTRO: espejo {r1['espejo']:.3f} "
              f"(nulo {r1['nulo_techo']:.3f}) — se reconoce")
    if not ok1:
        fallos.append("acoplada")

    v2, c2_ = episodios(False)
    r2 = espejo(v2, c2_, [7, 8])
    ok2 = not r2["se_reconoce"] or r2["neto"] < 0.05
    if verbose:
        print(f"  {'ok  ' if ok2 else 'FALLO'} VISTA AJENA: espejo neto {r2['neto']:+.3f} — "
              f"no se inventa un yo en un espejo que no lo refleja")
    if not ok2:
        fallos.append("independiente")

    # 3) el nulo es de OTRO episodio con estadisticas identicas: si el estimador confundiera
    # textura con coincidencia, este numero seria alto. Debe ser CLARAMENTE menor que el real.
    ok3 = r1["nulo_techo"] < r1["espejo"] - 0.1
    if verbose:
        print(f"  {'ok  ' if ok3 else 'FALLO'} EL NULO MUERDE: mismas estadísticas, otro episodio "
              f"→ {r1['nulo_techo']:.3f} vs real {r1['espejo']:.3f}")
    if not ok3:
        fallos.append("nulo")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el espejo refleja al que se mueve, no al que se parece."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="El espejo del bebé: coherencia visión-propiocepción")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (la corrida oficial la define el prerregistro-26)")
