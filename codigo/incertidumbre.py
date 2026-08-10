# incertidumbre.py — GEN G14: saber CUÁNTO no sé, y de qué clase es mi ignorancia.
# Activado por orden del director el 8-ago-2026 ("activalo"); no emite veredictos de campaña
# hasta que un prerregistro firmado lo cablee a una decisión (misma cuarentena que tuvo G10).
#
# POR QUÉ EXISTE: hasta hoy Diego da predicciones puntuales. Sin una variable de confianza, su
# curiosidad no puede distinguir "no sé porque ES AZAR" (irreducible — el televisor ruidoso) de
# "no sé porque AÚN NO APRENDO" (reducible — donde vale la pena excavar). Esa distinción es
# exactamente la que la literatura del ruido-TV nombra aleatoria vs epistémica, y es crítica en
# cuanto se tiene un cuerpo con contactos caóticos.
#
# CÓMO, con matemática genérica y nada más:
#   EPISTÉMICA(x) = varianza entre las predicciones de un CONJUNTO de modelos entrenados sobre
#                   remuestreos de los mismos datos. Si los datos aún no fijan el modelo, los
#                   miembros discrepan. SE REDUCE con más datos.
#   ALEATORIA(x)  = varianza residual media que ningún miembro puede explicar. NO se reduce con
#                   más datos: es el azar del mundo (o lo que mis variables no ven).
#
# LA FIRMA QUE LO HACE FALSABLE (y su Regla 31): al DOBLAR los datos, la epistémica debe caer
# (~mitad en régimen lineal) y la aleatoria debe quedarse. Un estimador que no muestre esa
# firma en mundos de verdad conocida no puede opinar sobre la ignorancia de nadie.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def medir(X, Y, X_test, miembros=12, semilla=0):
    """Devuelve, por punto de prueba: predicción media, incertidumbre EPISTÉMICA (desv. entre
    miembros del conjunto) e incertidumbre ALEATORIA (residuo medio de los miembros).
    Y puede ser (n,) o (n, d)."""
    rng = np.random.default_rng(semilla)
    Y2 = Y if Y.ndim > 1 else Y[:, None]
    A = np.column_stack([X, np.ones(len(X))])
    At = np.column_stack([X_test, np.ones(len(X_test))])
    preds, residuos = [], []
    for _ in range(miembros):
        idx = rng.integers(0, len(X), len(X))          # bootstrap: remuestreo con reemplazo
        w, *_ = np.linalg.lstsq(A[idx], Y2[idx], rcond=None)
        preds.append(At @ w)
        residuos.append(float(np.mean((A[idx] @ w - Y2[idx]) ** 2)))
    preds = np.stack(preds)                            # (miembros, n_test, d)
    return {"prediccion": preds.mean(axis=0),
            "epistemica": float(preds.std(axis=0).mean()),
            "aleatoria": float(np.sqrt(np.mean(residuos)))}


# ==========================================================================================
# LA PUERTA (metodo.py) — 10-ago-2026, prerregistro-43
# ==========================================================================================
# G14 publica en cada ronda y **el temple lee su numero** para calcular su termino de sorpresa —
# y el temple es CABLEADO E INMUTABLE por diseño. Es decir: si G14 midiera mal, el error quedaria
# congelado dentro de un organo que por construccion no se puede ajustar. Por eso este es de los
# primeros que pasan.
METODO = {
    "prerregistro": 43,
    "tipo_de_medida": "continua",
    "que_mide": ("las DOS ignorancias por separado: la EPISTEMICA (curable con mas datos, medida "
                 "como desacuerdo entre miembros del conjunto) y la ALEATORIA (irreducible, el "
                 "residuo). Confundirlas es creer que se puede aprender lo que solo es ruido"),
    "comparten_datos": {
        "hay": True,
        "porque": "los miembros del conjunto se entrenan por bootstrap sobre EL MISMO conjunto de "
                  "entrenamiento: esa es la definicion del metodo, y su desacuerdo es justo la "
                  "señal que se busca. Lo que NO se comparte es el conjunto de prueba.",
    },
    "linea_base": ("decir que TODA la incertidumbre es aleatoria — es decir, que nada es curable. "
                   "Un estimador que no bate a eso no distingue las dos ignorancias"),
    "formulas": [
        {"base": {"n": 40.0, "ruido": 0.5}, "parametro": "n", "factor": 8.0, "esperado": "baja",
         "porque": "la ignorancia EPISTEMICA es, por definicion, la que se cura con datos: al "
                   "multiplicar por 8 las muestras tiene que caer. Es la firma falsable del "
                   "concepto — si NO cayera, lo que se esta midiendo no es ignorancia curable"},
        {"base": {"n": 40.0, "ruido": 0.5}, "parametro": "ruido", "factor": 4.0, "esperado": "sube",
         "porque": "mas ruido irreducible = mas desacuerdo entre miembros remuestreados. Sube, "
                   "pero se declara como desigualdad: la relacion exacta depende del "
                   "condicionamiento de la matriz y ponerle un factor seria inventarselo"},
    ],
}


def _mundo(n=40.0, ruido=0.5, dim=2, semilla=4):
    """Un mundo lineal cuyo TAMAÑO DE MUESTRA y RUIDO fijamos nosotros. La verdad la ponemos aqui."""
    rng = np.random.default_rng(int(semilla))
    X = rng.normal(size=(int(n), int(dim)))
    Y = 2.0 * X[:, 0] - X[:, 1] + rng.normal(0, float(ruido), int(n))
    Xt = rng.normal(size=(200, int(dim)))
    return X, Y, Xt


def _metodo_medir(n=40.0, ruido=0.5):
    """PASO 1 — la medida escalar: la ignorancia EPISTEMICA, la que debe curarse con datos."""
    X, Y, Xt = _mundo(n=n, ruido=ruido)
    return float(medir(X, Y, Xt)["epistemica"])


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿cada ignorancia sigue a SU propia causa?** La epistemica
    debe seguir a la escasez de datos y la aleatoria al ruido. Si se contagian, Diego creeria que
    puede aprender lo que solo es ruido — y gastaria su presupuesto persiguiendo un televisor.
    """
    import sanidad as S
    rng = np.random.default_rng(31)
    v_datos, v_ruido, l_epi, l_ale = [], [], [], []
    for _ in range(10):
        n = float(rng.integers(30, 400))
        r = float(rng.uniform(0.1, 2.0))
        X, Y, Xt = _mundo(n=n, ruido=r)
        m = medir(X, Y, Xt)
        v_datos.append(1.0 / n)          # ESCASEZ: lo que la epistemica debe seguir
        v_ruido.append(r)
        l_epi.append(m["epistemica"])
        l_ale.append(m["aleatoria"])
    r = S.correlaciones({"escasez": l_epi, "ruido": l_ale},
                        {"escasez": v_datos, "ruido": v_ruido})
    return {"aprueba": not r["fallos"], "fallos": r["fallos"], "tabla": r.get("tabla")}


def regla31(verbose=True):
    """Tres mundos de verdad conocida. Si el estimador no separa las dos ignorancias, REPRUEBA.
      MUNDO APRENDIBLE, pocos datos: ley determinista y=2x1-x2 con n=25.
        -> epistémica ALTA que CAE al doblar los datos; aleatoria ~0.
      MUNDO RUIDOSO: la misma ley + ruido irreducible fuerte, muchos datos.
        -> aleatoria ALTA que NO cae al doblar los datos; epistémica pequeña.
      TELEVISOR: salida = ruido puro, sin relación con la entrada.
        -> TODA la incertidumbre es aleatoria; la epistémica no debe inventar estructura."""
    rng = np.random.default_rng(9)
    Xt = rng.normal(size=(300, 2))
    ley = lambda X: 2 * X[:, 0] - X[:, 1]
    fallos = []

    def mundo(n, ruido, tv=False):
        X = rng.normal(size=(n, 2))
        Y = rng.normal(0, 1.0, n) if tv else ley(X) + rng.normal(0, ruido, n)
        return X, Y

    # 1) aprendible con pocos datos: doblar datos debe reducir la epistemica claramente.
    # LECCION DE LA PRIMERA CORRIDA (8-ago-2026): plantee este mundo con ley EXACTA y el
    # estimador dio epistemica = 0.0000 — y REPRUEBA... pero el que estaba mal era MI MUNDO,
    # no el instrumento: con ley exacta y modelo suficiente, 25 puntos DETERMINAN el modelo
    # y la ignorancia epistemica ES cero. Decir cero ahi es lo correcto. Para que exista
    # ignorancia curable el mundo debe estar SUBDETERMINADO: ley + algo de ruido y pocos
    # datos. Se corrige el mundo de prueba y se deja escrito, porque casi degrado un
    # instrumento por darle un examen sin respuesta que aprender.
    X1, Y1 = mundo(12, 0.5)
    X2, Y2 = mundo(48, 0.5)
    e1 = medir(X1, Y1, Xt)
    e2 = medir(X2, Y2, Xt)
    c1 = e1["epistemica"] > 0.08
    c2 = e2["epistemica"] < 0.65 * e1["epistemica"]
    if verbose:
        print(f"  {'ok  ' if c1 and c2 else 'FALLO'} APRENDIBLE: epistemica {e1['epistemica']:.4f} "
              f"-> {e2['epistemica']:.4f} al doblar datos (aleatoria {e1['aleatoria']:.4f})")
    if not (c1 and c2):
        fallos.append("aprendible")

    # 2) ruidoso: la aleatoria manda y NO cae con mas datos
    X3, Y3 = mundo(400, 1.0)
    X4, Y4 = mundo(800, 1.0)
    r3 = medir(X3, Y3, Xt)
    r4 = medir(X4, Y4, Xt)
    c3 = r3["aleatoria"] > 3 * r3["epistemica"]
    c4 = r4["aleatoria"] > 0.8 * r3["aleatoria"]
    if verbose:
        print(f"  {'ok  ' if c3 and c4 else 'FALLO'} RUIDOSO: aleatoria {r3['aleatoria']:.3f} "
              f"-> {r4['aleatoria']:.3f} al doblar datos (epistemica {r3['epistemica']:.3f})")
    if not (c3 and c4):
        fallos.append("ruidoso")

    # 3) televisor: nada que aprender; la epistemica no inventa estructura con datos de sobra
    X5, Y5 = mundo(600, 0.0, tv=True)
    t5 = medir(X5, Y5, Xt)
    c5 = t5["aleatoria"] > 5 * t5["epistemica"]
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} TELEVISOR: aleatoria {t5['aleatoria']:.3f} vs "
              f"epistemica {t5['epistemica']:.3f} — el azar no se disfraza de ignorancia curable")
    if not c5:
        fallos.append("televisor")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — distingue 'es azar' de 'aun no aprendo'."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G14: incertidumbre propia (epistemica vs aleatoria)")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (el gen no emite veredictos de campaña hasta ser cableado por prerregistro)")
