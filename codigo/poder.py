# poder.py — GEN G13: el PODER (empowerment) — cuánto control tengo sobre mi futuro, en bits de R².
# Activado por orden del director el 8-ago-2026 ("activalo"). BLINDAJE DE ACTIVACIÓN: mide pero
# NO decide — no entra a la ecuación de curiosidad ni elige nada hasta que un prerregistro
# firmado lo cablee (la misma cuarentena que tuvo G10 y que evitó un Goodhart).
#
# QUÉ ES: donde la curiosidad (G2) pregunta "¿dónde estoy MEJORANDO?", el poder pregunta
# "¿desde dónde puedo HACER más?". La literatura lo llama empowerment: información mutua entre
# mis acciones y mis estados futuros. Un bebé que gateó hasta el centro del cuarto tiene más
# futuros alcanzables que uno atrapado en una esquina — sin que nadie le dé recompensa alguna.
#
# POR QUÉ ES LEGAL: mide SU control sobre SU futuro. Cero contenido del mundo.
#
# CÓMO, con la matemática de la casa: PODER(región) = R² con que MIS COMANDOS explican el cambio
# de mis variables a horizonte h, dado el estado, DENTRO de esa región del estado — en réplicas
# retenidas, jamás en las de ajuste. Es información mutua bajo supuesto gaussiano-lineal, en la
# misma moneda (varianza explicada) que todo el proyecto.
#
# EL GOODHART PROPIO, DECLARADO ANTES DE USARLO (ECUACIONES-COMPARADAS nos enseñó a hacerlo así):
# un agente que maximiza poder puede preferir controlar VARIABLES TRIVIALES. Por eso el gen nace
# MEDIDOR y el día que decida, decidirá sobre la MISMA auditoría sellada que la curiosidad.
#
# Su Regla 31 exige TRES separaciones, incluida la del televisor ruidoso (el canal que mató a
# la ganancia honesta): ruido causado por mi comando NO es control — es varianza, no información.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))


def _r2_control(eps, jidx, horizonte=8, retardos=2, filtro=None):
    """R² con que los comandos explican el futuro DADO el estado (modelos anidados, la forma que
    el INFORME-31 validó: un mundo, dos conjuntos de entradas, mismas filas)."""
    def bloques(ee):
        Xs, As, Ys = [], [], []
        for com, sen in ee:
            T = len(sen)
            ini, fin = retardos, T - horizonte
            if fin <= ini:
                continue
            X = np.concatenate([sen[ini - k:fin - k] for k in range(retardos + 1)], axis=1)
            A_ = np.concatenate([com[ini - k:fin - k] for k in range(retardos + 1)], axis=1)
            Y = sen[ini + horizonte:fin + horizonte]
            if filtro is not None:
                m = filtro(sen[ini:fin])
                X, A_, Y = X[m], A_[m], Y[m]
            Xs.append(X); As.append(A_); Ys.append(Y)
        return np.vstack(Xs), np.vstack(As), np.vstack(Ys)

    tren = [e for i, e in enumerate(eps) if i not in jidx]
    test = [e for i, e in enumerate(eps) if i in jidx]
    Xtr, Atr, Ytr = bloques(tren)
    Xte, Ate, Yte = bloques(test)
    if len(Xte) < 40:
        return None                                    # sin potencia no se opina (leccion INF-32)

    def mse(Xa, Ya, Xb, Yb):
        A = np.column_stack([Xa, np.ones(len(Xa))])
        B = np.column_stack([Xb, np.ones(len(Xb))])
        w, *_ = np.linalg.lstsq(A, Ya, rcond=None)
        return float(np.mean((B @ w - Yb) ** 2))

    sin_ = mse(Xtr, Ytr, Xte, Yte)
    con_ = mse(np.column_stack([Xtr, Atr]), Ytr, np.column_stack([Xte, Ate]), Yte)
    return 1.0 - con_ / sin_ if sin_ > 0 else 0.0


def medir(episodios, jueces, region_var=0, cortes=(0.0,), horizonte=8, retardos=2):
    """El mapa de poder: R² de control por REGIÓN del estado (regiones definidas por cortes de
    una variable). Devuelve una fila por región. MEDIDOR, no motor."""
    jidx = {j - 1 for j in jueces}
    bordes = [-np.inf] + sorted(cortes) + [np.inf]
    filas = []
    for lo, hi in zip(bordes[:-1], bordes[1:]):
        filtro = lambda S, lo=lo, hi=hi: (S[:, region_var] >= lo) & (S[:, region_var] < hi)
        r = _r2_control(episodios, jidx, horizonte, retardos, filtro)
        filas.append({"region": f"[{lo:.2g}, {hi:.2g})", "poder": None if r is None
                      else round(float(r), 4)})
    return filas


# ==========================================================================================
# LA PUERTA (metodo.py) — 10-ago-2026, prerregistro-43
# ==========================================================================================
# G13 publica en cada ronda y **el temple lee su `subestima` como termino de error**. El temple es
# CABLEADO E INMUTABLE por diseño, asi que un error aqui quedaria congelado dentro de un organo que
# por construccion no se puede ajustar. Es la misma razon por la que G14 se examino antes que los
# demas — y G14 REPROBO (INFORME-51). Este es el otro que alimenta al temple.
METODO = {
    "prerregistro": 43,
    "tipo_de_medida": "continua",
    "que_mide": ("el R2 de CONTROL por region: cuanto explican los comandos del futuro DADO el "
                 "estado. Modelos anidados sobre las mismas filas — un mundo y dos conjuntos de "
                 "entradas, no dos mundos (la forma que el INFORME-31 valido)"),
    "comparten_datos": {
        "hay": True,
        "porque": "el modelo CON comandos y el modelo SIN comandos se ajustan sobre exactamente "
                  "las mismas filas: esa es justo la propiedad que cierra el canal de mentira que "
                  "tumbo a la ganancia honesta (INFORME-30), donde se comparaban dos mundos "
                  "distintos. Lo que NO se comparte son los episodios juez.",
    },
    "linea_base": ("el modelo SIN comandos, que ya va dentro de la resta: el poder ES una ganancia "
                   "sobre el, no un R2 crudo (Regla 11)"),
    "formulas": [
        {"base": {"fuerza": 0.6, "ruido": 0.3}, "parametro": "fuerza", "factor": 0.02,
         "esperado": "baja",
         "porque": "si el comando casi no mueve nada, lo que explica del futuro tiene que caer. "
                   "Desigualdad y no proporcion: el R2 de un modelo anidado no es funcion cerrada "
                   "de la fuerza del actuador"},
        {"base": {"fuerza": 0.6, "ruido": 0.3}, "parametro": "ruido", "factor": 10.0,
         "esperado": "baja",
         "porque": "ruido que ningun comando explica se lleva la varianza a un sitio donde el "
                   "comando no llega: el poder baja. Si NO bajara, estaria midiendo la escala de "
                   "la señal y no el control"},
    ],
}


def _mundo_con_poder(fuerza=0.6, ruido=0.3, T=1200, n_ep=6, semilla=13):
    """Un mundo donde YO fijo cuanto poder tienen los comandos. La verdad la ponemos nosotros."""
    rng = np.random.default_rng(int(semilla))
    k = np.ones(9) / 9
    eps = []
    for _ in range(int(n_ep)):
        a = np.column_stack([np.convolve(rng.normal(size=T + 8), k, mode="valid")[:T]
                             for _ in range(3)])
        s = np.zeros((T, 3))
        for t in range(1, T):
            s[t, 0] = 0.85 * s[t - 1, 0] + float(fuerza) * a[t - 1, 0] + rng.normal(0, float(ruido))
            s[t, 1] = 0.90 * s[t - 1, 1] + rng.normal(0, 1.0)          # nadie la manda
            s[t, 2] = 0.80 * s[t - 1, 2] + rng.normal(0, 1.0)          # nadie la manda
        eps.append((a, s))
    return eps


def _metodo_medir(fuerza=0.6, ruido=0.3):
    """PASO 1 — la medida escalar: el poder global sobre un mundo de poder conocido."""
    eps = _mundo_con_poder(fuerza=fuerza, ruido=ruido)
    filas = medir(eps, jueces=[5, 6], region_var=0, cortes=())
    val = [f["poder"] for f in filas if f["poder"] is not None]
    return float(val[0]) if val else 0.0


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el poder medido sigue a la fuerza real del actuador, o
    se lo lleva el ruido?** Un mapa de poder que sube con el ruido le diria a Diego que manda
    justo donde no manda — y G13 es el organo del que sale su sentido de agencia.
    """
    import sanidad as S
    rng = np.random.default_rng(37)
    fuerzas, lect = [], []
    for _ in range(8):
        f = float(rng.uniform(0.05, 1.5))
        fuerzas.append(f)
        lect.append(_metodo_medir(fuerza=f, ruido=0.3))
    r = S.correlaciones({"fuerza": lect}, {"fuerza": fuerzas})
    fallos = list(r["fallos"])
    # Señuelo de escala: multiplicar el mundo entero por 10 no puede cambiar el poder, porque el
    # poder es una RAZON de errores. Si cambiara, estaria leyendo amplitud.
    a = _metodo_medir(fuerza=0.6, ruido=0.3)
    eps = [(c, s * 10.0) for c, s in _mundo_con_poder(fuerza=0.6, ruido=0.3)]
    filas = medir(eps, jueces=[5, 6], region_var=0, cortes=())
    b = float([f["poder"] for f in filas if f["poder"] is not None][0])
    if abs(a - b) > 0.05:
        fallos.append(f"ESCALA: con el mundo x10 el poder pasa de {a:.4f} a {b:.4f} — lee amplitud")
    return {"aprueba": not fallos, "fallos": fallos,
            "sin_escalar": round(a, 4), "escalado_x10": round(b, 4)}


def regla31(verbose=True):
    """Tres mundos con verdad conocida:
      SIN AGENCIA        -> poder ~0 en todas partes (no inventa control).
      COMPUERTA          -> el comando solo actúa cuando la variable 0 es positiva:
                            el poder debe ser ALTO en esa región y ~0 en la otra.
      TELEVISOR RUIDOSO  -> mi comando CAUSA varianza pero no información: poder ~0.
                            (El canal exacto que mató a la ganancia honesta, INFORME-30.)"""
    rng = np.random.default_rng(17)
    T, n_ep = 900, 12
    k9 = np.ones(9) / 9
    # 10-ago-2026: aqui habia un `jueces = [11, 12]` que no usaba nadie — y que ademas NO coincidia
    # con los indices que la prueba usa de verdad (`{10, 11}`, que en base cero son los episodios
    # 11 y 12). Leerlo hacia creer que los jueces de esta prueba eran otros. Lo caza el paso 7 de
    # la puerta al pasar el modulo por primera vez. Una variable muerta no es solo basura: es una
    # afirmacion falsa sobre lo que el codigo hace.

    def balbuceo():
        return np.column_stack([np.convolve(rng.normal(size=T + 8), k9, mode="valid")[:T]
                                for _ in range(2)])

    def mundo(tipo):
        eps = []
        for _ in range(n_ep):
            a = balbuceo()
            s = np.zeros((T, 3))
            s[:, 2] = np.convolve(np.cumsum(rng.normal(size=T + 8)), k9, mode="valid")[:T]
            for t in range(1, T):
                s[t, 1] = 0.9 * s[t - 1, 1] + rng.normal(0, 0.05)
                if tipo == "sin_agencia":
                    s[t, 0] = 0.9 * s[t - 1, 0] + rng.normal(0, 0.05)
                elif tipo == "compuerta":
                    efecto = 0.8 * a[t - 1, 0] if s[t - 1, 0] > 0 else 0.0
                    s[t, 0] = 0.9 * s[t - 1, 0] + efecto + rng.normal(0, 0.05)
                elif tipo == "televisor":
                    s[t, 0] = rng.normal(0, 0.3 + 2.0 * abs(a[t - 1, 0]))
            eps.append((a, s))
        return eps

    # HORIZONTE = 1 en estos mundos, y la razon va escrita: son mundos de PRIMER ORDEN (el
    # comando actua en el paso siguiente). El h=8 del Gimnasio nacio de un cuerpo de SEGUNDO
    # orden donde el efecto tarda en verse (INFORME-31). El horizonte no es una constante
    # universal: se corresponde con la dinamica del mundo que se mide — usar h=8 aqui enterro
    # una compuerta real bajo el estado ya integrado (medido: +0.048 antes, +0.435 despues).
    H = 1
    fallos = []
    r_sin = _r2_control(mundo("sin_agencia"), {10, 11}, horizonte=H)
    c = abs(r_sin) < 0.05
    if verbose:
        print(f"  {'ok  ' if c else 'FALLO'} SIN AGENCIA: poder {r_sin:+.4f} (debe ser ~0)")
    if not c:
        fallos.append("sin_agencia")

    eps = mundo("compuerta")
    jidx = {10, 11}
    r_pos = _r2_control(eps, jidx, horizonte=H, filtro=lambda S: S[:, 0] > 0)
    r_neg = _r2_control(eps, jidx, horizonte=H, filtro=lambda S: S[:, 0] <= 0)
    c = r_pos is not None and r_neg is not None and r_pos > 0.2 and r_pos > 4 * max(r_neg, 0.01)
    if verbose:
        print(f"  {'ok  ' if c else 'FALLO'} COMPUERTA: poder donde el comando actúa {r_pos:+.3f} "
              f"vs donde no {r_neg:+.3f} — el mapa señala DÓNDE se puede hacer más")
    if not c:
        fallos.append("compuerta")

    r_tv = _r2_control(mundo("televisor"), {10, 11}, horizonte=H)
    c = abs(r_tv) < 0.05
    if verbose:
        print(f"  {'ok  ' if c else 'FALLO'} TELEVISOR RUIDOSO: poder {r_tv:+.4f} — causar ruido "
              f"NO es control (varianza sin información)")
    if not c:
        fallos.append("televisor")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — mide control real, no varianza ni casualidad."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G13: poder (empowerment) — mide, no decide")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (el gen mide; no decide hasta ser cableado por prerregistro firmado)")
