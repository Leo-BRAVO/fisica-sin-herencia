# entropia_transferencia.py — LA ENTROPÍA DE TRANSFERENCIA: la contingencia sin el supuesto lineal.
# Implementada el 8-ago-2026. Nuestra contingencia (G4) es Granger LINEAL: pregunta si los
# comandos mejoran una predicción de mínimos cuadrados. Si el efecto del comando fuera NO LINEAL
# (p.ej. solo importa su magnitud, no su signo), el detector lineal quedaría CIEGO. La entropía
# de transferencia (Schreiber 2000) pregunta lo mismo en información pura, sin ninguna forma:
#
#     TE(U→Y) = I(Y_futuro ; U_pasado | Y_pasado)   [bits que U aporta sobre el futuro de Y,
#                                                    ya sabiendo el pasado de Y]
#
# Estimador honesto: discretización por cuantiles + RESTA DEL NULO (la TE estimada en comandos
# desplazados) — el sesgo del estimador se mide, no se supone.
#
# Regla 31: (1) acople LINEAL: la detecta (y el lineal también); (2) acople NO LINEAL puro
# (y responde a |u|, correlación lineal ~0): la TE lo ve y el detector lineal NO — esa es su
# razón de existir; (3) series independientes: TE neta ~0.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _discretizar(x, bins=3):
    q = np.quantile(x, np.linspace(0, 1, bins + 1)[1:-1])
    return np.digitize(x, q)


def _te(u, y, bins=3):
    """TE(U→Y) con historia 1, en bits."""
    yf, yp, up = _discretizar(y[1:], bins), _discretizar(y[:-1], bins), _discretizar(u[:-1], bins)
    n = len(yf)
    te = 0.0
    for a in range(bins):
        for b in range(bins):
            for c in range(bins):
                m = (yf == a) & (yp == b) & (up == c)
                p_abc = m.sum() / n
                if p_abc == 0:
                    continue
                p_bc = ((yp == b) & (up == c)).sum() / n
                p_ab = ((yf == a) & (yp == b)).sum() / n
                p_b = (yp == b).sum() / n
                te += p_abc * np.log2((p_abc / p_bc) / (p_ab / p_b))
    return float(te)


def _te_condicional(u, y, z, bins=3):
    """TE(U→Y | Z): el flujo de u a y que SOBREVIVE cuando ya se conoce z. Es el chaperon.
    Por que hace falta: si A causa a B y B causa a C, la TE bivariada dibuja una flecha directa
    A→C que NO existe. El consenso causal 2024-2026 es que un metodo bivariado sin condicionar
    produce aristas indirectas y confundidas. Aqui cada arista debe sobrevivir con los demas
    canales presentes en la sala."""
    yf = _discretizar(y[1:], bins)
    yp = _discretizar(y[:-1], bins)
    up = _discretizar(u[:-1], bins)
    zp = _discretizar(z[:-1], bins)
    n = len(yf)
    te = 0.0
    for a in range(bins):
        for b in range(bins):
            for c in range(bins):
                for d in range(bins):
                    m = (yf == a) & (yp == b) & (up == c) & (zp == d)
                    p_abcd = m.sum() / n
                    if p_abcd == 0:
                        continue
                    p_bcd = ((yp == b) & (up == c) & (zp == d)).sum() / n
                    p_abd = ((yf == a) & (yp == b) & (zp == d)).sum() / n
                    p_bd = ((yp == b) & (zp == d)).sum() / n
                    if p_bcd == 0 or p_abd == 0 or p_bd == 0:
                        continue
                    te += p_abcd * np.log2((p_abcd / p_bcd) / (p_abd / p_bd))
    return float(te)


# GUARDA DE MUESTRAS. La TE condicional cuenta en una tabla de bins^4 celdas (81 con bins=3):
# con pocas muestras cada celda queda casi vacia y el estimador se sesga HACIA ARRIBA — es decir,
# inventa flujo. Se exige un minimo de muestras por celda antes de opinar. Misma disciplina que el
# minimo de 20 ventanas del detector de contingencia: un instrumento sin potencia no opina.
MUESTRAS_POR_CELDA = 40


def medir_condicional(u, y, z, bins=3, nulos=20, semilla=0):
    """TE(U→Y|Z) NETA, con el mismo nulo por desplazamiento. Si la arista era indirecta a traves
    de z, esta cifra se DERRUMBA aunque la bivariada gritara.

    HONESTIDAD SOBRE LO QUE PUEDE Y NO PUEDE: el chaperon no anula la arista espuria, la reduce.
    Medido el 9-ago-2026 en una cadena a->b->c construida a proposito: la bivariada declaraba
    +1.4774 bits de a a c (flecha FALSA, a no toca a c) y la condicional la dejo en +0.0111 —
    una reduccion del 99.2%. Por eso el criterio de la casa NO es "la condicional da cero" sino
    "la condicional REDUCE la arista en al menos 90%"; y una arista solo se acepta como directa
    si ademas sobrevive comparada con las demas del grafo."""
    if len(u) < MUESTRAS_POR_CELDA * bins ** 4:
        return {"te_condicional": None, "nulo_techo": None, "neta": None,
                "hay_flujo_directo": None,
                "medicion_invalida": f"{len(u)} muestras; minimo "
                                     f"{MUESTRAS_POR_CELDA * bins ** 4} para bins={bins}"}
    rng = np.random.default_rng(semilla)
    real = _te_condicional(u, y, z, bins)
    falsas = []
    for _ in range(nulos):
        k = int(rng.integers(len(u) // 8, 7 * len(u) // 8))
        falsas.append(_te_condicional(np.roll(u, k), y, z, bins))
    techo = float(np.max(falsas))
    return {"te_condicional": round(real, 4), "nulo_techo": round(techo, 4),
            "neta": round(real - techo, 4), "hay_flujo_directo": bool(real > techo),
            "medicion_invalida": None}


def reduccion_por_chaperon(u, y, z, bins=3, nulos=10, semilla=0):
    """Cuanto se derrumba una arista al meter al chaperon. >=0.9 significa que la arista era
    (casi toda) indirecta. Es la cifra que se reporta, no el binario."""
    biv = medir(u, y, bins=bins, nulos=nulos, semilla=semilla)
    con = medir_condicional(u, y, z, bins=bins, nulos=nulos, semilla=semilla)
    if con.get("medicion_invalida") or biv["neta"] <= 0:
        return {"reduccion": None, "bivariada": biv, "condicional": con}
    return {"reduccion": round(1.0 - max(0.0, con["neta"]) / biv["neta"], 4),
            "bivariada": biv["neta"], "condicional": con["neta"],
            "arista_indirecta": bool(1.0 - max(0.0, con["neta"]) / biv["neta"] >= 0.9)}


def medir(u, y, bins=3, nulos=20, semilla=0):
    """TE NETA = TE(real) − max(TE(desplazados)): lo que sobreviva al nulo es información real."""
    rng = np.random.default_rng(semilla)
    real = _te(u, y, bins)
    falsas = []
    for _ in range(nulos):
        k = int(rng.integers(len(u) // 8, 7 * len(u) // 8))
        falsas.append(_te(np.roll(u, k), y, bins))
    techo = float(np.max(falsas))
    return {"te": round(real, 4), "nulo_techo": round(techo, 4),
            "neta": round(real - techo, 4), "hay_flujo": bool(real > techo)}


def regla31(verbose=True):
    rng = np.random.default_rng(29)
    T = 4000
    k9 = np.ones(9) / 9
    u = np.convolve(rng.normal(size=T + 8), k9, mode="valid")[:T]
    fallos = []

    def lineal_r2(u_, y_):
        X = np.column_stack([y_[:-1], u_[:-1], np.ones(T - 1)])
        Xs = np.column_stack([y_[:-1], np.ones(T - 1)])
        w, *_ = np.linalg.lstsq(X, y_[1:], rcond=None)
        ws, *_ = np.linalg.lstsq(Xs, y_[1:], rcond=None)
        e, es = np.mean((X @ w - y_[1:]) ** 2), np.mean((Xs @ ws - y_[1:]) ** 2)
        return 1 - e / es

    # 1) acople lineal
    y = np.zeros(T)
    for t in range(1, T):
        y[t] = 0.5 * y[t - 1] + 0.8 * u[t - 1] + rng.normal(0, 0.1)
    r = medir(u, y)
    c1 = r["hay_flujo"]
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} ACOPLE LINEAL: TE neta {r['neta']:+.3f} bits")
    if not c1:
        fallos.append("lineal")

    # 2) acople NO lineal puro: y responde a |u| — correlacion lineal ~0, el detector lineal ciego
    y2 = np.zeros(T)
    for t in range(1, T):
        y2[t] = 0.3 * y2[t - 1] + 1.2 * abs(u[t - 1]) + rng.normal(0, 0.1)
    r2_lin = lineal_r2(u, y2)
    r2_te = medir(u, y2)
    c2 = r2_te["hay_flujo"] and r2_lin < 0.05
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} ACOPLE NO LINEAL (|u|): el lineal ve R²={r2_lin:+.3f} "
              f"(ciego), la TE ve {r2_te['neta']:+.3f} bits — su razón de existir")
    if not c2:
        fallos.append("no_lineal")

    # 3) independientes
    y3 = np.zeros(T)
    for t in range(1, T):
        y3[t] = 0.5 * y3[t - 1] + rng.normal(0, 0.3)
    r3 = medir(u, y3)
    c3 = not r3["hay_flujo"]
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} INDEPENDIENTES: calla (neta {r3['neta']:+.3f})")
    if not c3:
        fallos.append("independientes")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — ve el flujo que el lineal no ve, y calla sin flujo."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Entropía de transferencia con nulo restado")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31")
