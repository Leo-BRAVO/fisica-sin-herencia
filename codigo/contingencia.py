# contingencia.py — GEN G4: el detector de "¿esto respondió a MI comando?"
#
# Es el órgano del que nace la frontera yo/mundo. NADIE le programa a Diego qué parte del vector
# de estado es su cuerpo: se lo gana midiendo, variable por variable, cuánta de su dinámica
# explican sus propios comandos motores recientes.
#
#     CONTINGENCIA(d) = reducción del error al predecir la variable d
#                       CUANDO se le añaden los comandos como entrada
#
# medida sobre EPISODIOS-JUEZ CONGELADOS que el detector jamás vio (prerregistro-19, FIRMADO).
#
# ===================== POR QUÉ ESTA VARA NO ES LA QUE SE NOS CAYÓ AYER =====================
# El INFORME-30 tumbó la ganancia honesta: comparaba el mundo REAL contra un mundo SURROGADO —
# dos conjuntos de datos distintos — y la no estacionariedad del real fabricaba ventaja.
# Aquí NO hay dos mundos: hay UN mundo y DOS CONJUNTOS DE ENTRADAS (con comandos y sin comandos),
# evaluados sobre exactamente las mismas filas. Es una comparación de modelos ANIDADOS, y por
# construcción cierra el canal que nos mordió: la deriva está en AMBOS lados de la resta.
#
# PERO hereda un peligro propio, y por eso el nulo se elige con cuidado (enmienda de la Regla 31):
#   Si los comandos están autocorrelacionados (un balbuceo suave lo estará), los comandos
#   codifican "CUÁNDO", y una variable con tendencia es predecible desde "cuándo". Eso fabricaría
#   contingencia donde solo hay deriva.
#   EL NULO CORRECTO ES EL DESPLAZAMIENTO CIRCULAR de los comandos: conserva ENTERA la estructura
#   temporal propia del comando y destruye SOLO su alineación con las señales. Barajarlos sería
#   demasiado destructivo (les quita su autocorrelación) — el error espejo que ya cometimos.
# ==========================================================================================
#
# Uso:
#   python contingencia.py --regla31          (el instrumento se prueba a sí mismo: 4 mundos)
#   python contingencia.py --episodios <carpeta_npz> [--jueces 8 9 10]

import os
import sys
import json
import glob
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lstsq_mse(X_tr, y_tr, X_te, y_te):
    """Rival lineal con término independiente — la misma vara del proyecto desde el día uno."""
    A_tr = np.column_stack([X_tr, np.ones(len(X_tr))])
    A_te = np.column_stack([X_te, np.ones(len(X_te))])
    w, *_ = np.linalg.lstsq(A_tr, y_tr, rcond=None)
    return float(np.mean((A_te @ w - y_te) ** 2))


def _armar(episodios, retardos=2):
    """De episodios (comandos, señales) a matrices. El estado en t predice la señal en t+1.
    Los comandos entran con sus 'retardos' últimos valores: un efecto motor puede tardar."""
    Xs, As, Ys = [], [], []
    for com, sen in episodios:
        T = len(sen)
        ini, fin = retardos, T - 1
        if fin <= ini:
            continue
        estado = [sen[ini - k:fin - k] for k in range(retardos + 1)]
        acc = [com[ini - k:fin - k] for k in range(retardos + 1)]
        Xs.append(np.concatenate(estado, axis=1))
        As.append(np.concatenate(acc, axis=1))
        Ys.append(sen[ini + 1:fin + 1])
    return Xs, As, Ys


def _desplazar(com, rng):
    """NULO: desplazamiento circular. Conserva entera la estructura temporal del comando y
    destruye solo su alineación con las señales (ver cabecera)."""
    k = int(rng.integers(len(com) // 8, len(com) - len(com) // 8))
    return np.roll(com, k, axis=0)


def medir(episodios, jueces, retardos=2, nulos=12, semilla=0,
          horizonte=8, ventana=150, piso_ventana=0.02, fraccion=0.5):
    """Contingencia por variable, medida como CONSISTENCIA a través de ventanas.

    ===================== LO QUE CORRER ESTO NOS ENSEÑÓ (8-ago-2026) =====================
    La primera versión medía la contingencia AGREGADA a un cuadro vista. Falló los cuatro
    controles del Gimnasio, y las dos razones son ciencia, no bugs:

    1. EL HORIZONTE. Un brazo es un sistema de segundo orden casi determinista: a un cuadro
       vista, tres retardos del ángulo ya extrapolan casi perfecto y el par solo aporta un
       empujón minúsculo, enterrado bajo los contactos. El efecto de una aceleración sobre una
       POSICIÓN crece con el tiempo. Medido: v0 pasa de +0.002 (h=1) a +0.141 (h=32).
       A un cuadro vista, un cuerpo es casi invisible para su propio dueño.

    2. LA CONTINGENCIA PERFECTA. El brazo GOLPEA las cajas — así que la altura de una caja SÍ
       responde a sus comandos. Contingencia binaria no separa cuerpo de mundo, porque un
       objeto manipulable también es contingente. Lo que los separa es la CONSISTENCIA:
       el cuerpo obedece SIEMPRE; el mundo solo en las ventanas donde hubo contacto.
       (La literatura de contingencia sensomotora ya lo llamaba "contingencia perfecta"; el
       prerregistro-19 lo pasó por alto y por eso su criterio está subespecificado — ver
       INFORME-31 y la enmienda propuesta al director.)

    ADVERTENCIA HONESTA: `piso_ventana` y `fraccion` son constantes que este código NO puede
    fijar por su cuenta sin caer en el vicio que llevamos toda la semana cazando (ajustar la
    vara hasta que el resultado salga). Quedan expuestas y SIN AJUSTAR, y deben fijarse en un
    prerregistro firmado antes de que este detector emita ningún veredicto sobre un hito.
    ======================================================================================
    """
    jidx = {j - 1 for j in jueces}
    tren = [e for i, e in enumerate(episodios) if i not in jidx]
    test = [e for i, e in enumerate(episodios) if i in jidx]
    if not tren or not test:
        raise SystemExit("hacen falta episodios de entrenamiento Y de juez")

    def bloques(eps, rot, rng):
        Xs, As, Ys = [], [], []
        for com, sen in eps:
            c = _desplazar(com, rng) if rot else com
            T = len(sen)
            ini, fin = retardos, T - horizonte
            if fin <= ini:
                continue
            Xs.append(np.concatenate([sen[ini - k:fin - k] for k in range(retardos + 1)], axis=1))
            As.append(np.concatenate([c[ini - k:fin - k] for k in range(retardos + 1)], axis=1))
            Ys.append(sen[ini + horizonte:fin + horizonte])
        return np.vstack(Xs), np.vstack(As), np.vstack(Ys)

    def ajustar(X, y):
        A = np.column_stack([X, np.ones(len(X))])
        w, *_ = np.linalg.lstsq(A, y, rcond=None)
        return w

    def error(w, X, y):
        A = np.column_stack([X, np.ones(len(X))])
        return float(np.mean((A @ w - y) ** 2))

    def fracciones(rot, semilla_):
        rng = np.random.default_rng(semilla_)
        Xtr, Atr, Ytr = bloques(tren, rot, rng)
        Xte, Ate, Yte = bloques(test, rot, rng)
        XAte = np.column_stack([Xte, Ate])
        out = []
        for d in range(Ytr.shape[1]):
            w_sin = ajustar(Xtr, Ytr[:, d])
            w_con = ajustar(np.column_stack([Xtr, Atr]), Ytr[:, d])
            buenas = total = 0
            for a in range(0, len(Xte) - ventana, ventana):
                sl = slice(a, a + ventana)
                e_sin = error(w_sin, Xte[sl], Yte[sl, d])
                e_con = error(w_con, XAte[sl], Yte[sl, d])
                total += 1
                if e_sin > 0 and 1.0 - e_con / e_sin > piso_ventana:
                    buenas += 1
            out.append(buenas / max(total, 1))
        return np.array(out)

    real = fracciones(False, semilla)
    falsas = np.array([fracciones(True, semilla + 1 + i) for i in range(nulos)])
    techo = falsas.max(axis=0)
    return [{"variable": d,
             "obedece_en": round(float(real[d]), 4),
             "nulo_media": round(float(falsas[:, d].mean()), 4),
             "nulo_techo": round(float(techo[d]), 4),
             "es_mia": bool(real[d] > techo[d] and real[d] > fraccion),
             "margen": round(float(real[d] - max(techo[d], fraccion)), 4),
             "horizonte": horizonte}
            for d in range(len(real))]


# ============================== REGLA 31: cuatro mundos con verdad conocida ==============================

def _mundos_regla31(n_ep=12, T=600, semilla=7):
    """Cuatro mundos donde YO sé la respuesta. Si el detector falla en alguno, no puede opinar
    sobre Diego. Cada mundo: 3 grados de libertad de 'cuerpo' + 2 variables de 'mundo'."""
    rng = np.random.default_rng(semilla)
    k = np.ones(9) / 9

    def balbuceo(T_, A):
        """Comandos SUAVES y autocorrelacionados — como sería un balbuceo real, y por eso el
        caso difícil: un comando suave codifica 'cuándo'."""
        return np.column_stack([np.convolve(rng.normal(size=T_ + 8), k, mode="valid")[:T_]
                                for _ in range(A)])

    def deriva(T_):
        return np.cumsum(rng.normal(0, 0.05, T_))

    mundos = {}

    # 1) SIN AGENCIA — los comandos se emiten pero NO actúan. Nada debe ser "mío".
    eps = []
    for _ in range(n_ep):
        a = balbuceo(T, 3)
        s = np.column_stack([np.convolve(np.cumsum(rng.normal(size=T + 8)), k, mode="valid")[:T]
                             for _ in range(5)])
        eps.append((a, s))
    mundos["1 SIN AGENCIA (motores desconectados)"] = (eps, set())

    # 2) CONTROL POSITIVO — SOLO el grado de libertad 0 mueve la variable 0.
    eps = []
    for _ in range(n_ep):
        a = balbuceo(T, 3)
        cols = []
        cuerpo = np.zeros(T)
        for t in range(1, T):
            cuerpo[t] = 0.85 * cuerpo[t - 1] + 0.6 * a[t - 1, 0]
        cols.append(cuerpo)
        for _ in range(4):
            cols.append(np.convolve(np.cumsum(rng.normal(size=T + 8)), k, mode="valid")[:T])
        eps.append((a, np.column_stack(cols)))
    mundos["2 CONTROL POSITIVO (solo la var 0 obedece)"] = (eps, {0})

    # 3) TELEVISOR RUIDOSO CORPORAL — una variable RESPONDE a un comando... con RUIDO PURO.
    #    Su cuerpo se vuelve su propio distractor. Debe clasificarse MUNDO, no YO.
    eps = []
    for _ in range(n_ep):
        a = balbuceo(T, 3)
        cuerpo = np.zeros(T)
        for t in range(1, T):
            cuerpo[t] = 0.85 * cuerpo[t - 1] + 0.6 * a[t - 1, 0]
        tv = np.array([rng.normal(0, 1.0 + 2.0 * abs(a[t, 1])) for t in range(T)])
        resto = [np.convolve(np.cumsum(rng.normal(size=T + 8)), k, mode="valid")[:T]
                 for _ in range(3)]
        eps.append((a, np.column_stack([cuerpo, tv] + resto)))
    mundos["3 TELEVISOR RUIDOSO CORPORAL"] = (eps, {0})

    # 4) DERIVA + COMANDOS SUAVES — el canal que nos mordió en el INFORME-30, trasplantado:
    #    señales integradas con tendencia y comandos autocorrelacionados que codifican 'cuándo'.
    #    NADA obedece. Cualquier contingencia aquí es mentira fabricada.
    eps = []
    for _ in range(n_ep):
        a = balbuceo(T, 3)
        s = np.column_stack([np.convolve(np.cumsum(rng.normal(size=T + 8)), k, mode="valid")[:T]
                             + 3.0 * deriva(T) for _ in range(5)])
        eps.append((a, s))
    mundos["4 DERIVA FUERTE, CERO AGENCIA (la trampa del INF-30)"] = (eps, set())
    return mundos


def regla31(verbose=True):
    """El detector se prueba a sí mismo antes de tocar a Diego (Regla 31)."""
    jueces = [10, 11, 12]
    fallos = []
    if verbose:
        print("=== REGLA 31 sobre contingencia.py — el detector de la frontera yo/mundo ===")
        print("   (jueces 10/11/12 congelados; nulo = desplazamiento circular; se mide la\n    FRACCION DE VENTANAS en que la variable obedece — la contingencia perfecta)\n")
    for nombre, (eps, mias_reales) in _mundos_regla31().items():
        res = medir(eps, jueces, nulos=10, horizonte=4, ventana=120)
        halladas = {r["variable"] for r in res if r["es_mia"]}
        ok = halladas == mias_reales
        if verbose:
            det = " ".join(f"v{r['variable']}={r['obedece_en']:.2f}"
                           f"{'*' if r['es_mia'] else ''}" for r in res)
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}")
            print(f"        esperado={sorted(mias_reales) or 'ninguna'} "
                  f"hallado={sorted(halladas) or 'ninguna'}")
            print(f"        {det}")
        if not ok:
            fallos.append(nombre)
    if verbose:
        print()
        print("REGLA 31: APRUEBA — el detector encuentra el cuerpo donde lo hay y NO lo inventa"
              if not fallos else f"REGLA 31: REPRUEBA en {fallos} — NO puede producir nodos")
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G4: detector de contingencia sensomotora")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--episodios", default=None, help="carpeta con episodio_*.npz")
    ap.add_argument("--jueces", nargs="+", type=int, default=[10, 11, 12])
    ap.add_argument("--nulos", type=int, default=12)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    if a.episodios:
        eps = []
        for f in sorted(glob.glob(os.path.join(a.episodios, "episodio_*.npz"))):
            d = np.load(f)
            eps.append((d["comandos"], d["senales"]))
        print(json.dumps(medir(eps, a.jueces, nulos=a.nulos), indent=2, ensure_ascii=False))
