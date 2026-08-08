# verdugo_escala.py — EL VERDUGO QUE SOLO EXISTE EN EL GIMNASIO
#
# LA IDEA: los laboratorios que hacen regresión simbólica le entregan a la máquina las unidades
# ya puestas ("esto son metros, esto son segundos") y con eso pueden filtrar ecuaciones por
# consistencia dimensional — el filtro más potente que existe. Diego no puede recibir eso: sería
# conocimiento humano. Pero hay una puerta que nadie usa, y es nuestra por construcción:
#
#     LA CONSISTENCIA DIMENSIONAL NO ES UN HECHO SOBRE EL MUNDO. Es una consecuencia de que el
#     mundo NO TIENE UNIDADES PREFERIDAS. Y eso se puede COMPROBAR sin nombrar ninguna unidad:
#     se corre el MISMO experimento a otra escala de longitud y de tiempo, y se exige que lo
#     aprendido siga valiendo.
#
#     Una ley que sobrevive el reescalado capturó una RELACIÓN.
#     Una que no sobrevive estaba ajustando las unidades arbitrarias de nuestro simulador.
#
# POR QUÉ NO SE PUEDE HACER CON VIDEO DE INTERNET: no se puede pedirle al universo que repita
# una caída con las longitudes multiplicadas por tres. En un simulador sí. Es la primera vara del
# proyecto que EXIGE tener un mundo propio — y por eso llega hoy y no antes.
#
# CUIDADO DECLARADO: al reescalar longitud por k y tiempo por m, la física del simulador NO es
# invariante para cualquier par (k, m) — la gravedad fija una relación. Este verdugo NO asume
# ninguna: prueba varias parejas y reporta CUÁLES sobreviven. Que exista alguna pareja que
# preserva la ley es en sí el hallazgo; decir cuál sería ya física con nombre (Regla 4).
#
# Uso:
#   python verdugo_escala.py --regla31         (el instrumento se prueba a sí mismo)
#   python verdugo_escala.py --episodios 8 --pasos 600

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))


def _ajustar(X, Y):
    A = np.column_stack([X, np.ones(len(X))])
    w, *_ = np.linalg.lstsq(A, Y, rcond=None)
    return w


def _error(w, X, Y):
    A = np.column_stack([X, np.ones(len(X))])
    return float(np.mean((A @ w - Y) ** 2))


def _bloques(series, retardos=2, horizonte=1):
    X, Y = [], []
    for s in series:
        T = len(s)
        ini, fin = retardos, T - horizonte
        if fin <= ini:
            continue
        X.append(np.concatenate([s[ini - k:fin - k] for k in range(retardos + 1)], axis=1))
        Y.append(s[ini + horizonte:fin + horizonte])
    return np.vstack(X), np.vstack(Y)


def transferencia(series_a, series_b, k_long, m_tiempo, retardos=2):
    """¿La ley aprendida en el mundo A sigue valiendo en el mundo B, tras deshacer la escala?

    Se ajusta en A, se aplica en B con las señales devueltas a las unidades de A (dividir la
    longitud por k), y se compara contra la base trivial de B — la misma vara de siempre.
    Devuelve la fracción del error trivial que la ley importada elimina. Si es ~0 o negativa,
    la ley no transfirió: vivía en las unidades, no en la relación.
    """
    Xa, Ya = _bloques(series_a, retardos)
    w = _ajustar(Xa, Ya)
    Xb, Yb = _bloques([s / k_long for s in series_b], retardos)
    err_ley = _error(w, Xb, Yb)
    # base trivial: velocidad constante y media de entrenamiento, la mejor de las dos
    n = Yb.shape[1]
    pred_vel = Xb[:, :n] + (Xb[:, :n] - Xb[:, n:2 * n])
    err_vel = float(np.mean((pred_vel - Yb) ** 2))
    err_media = float(np.mean((Ya.mean(axis=0) / 1.0 - Yb) ** 2))
    base = min(err_vel, err_media)
    return 1.0 - err_ley / base if base > 0 else float("nan")


def correr_gimnasio_escalado(n_ep, pasos, k_long, m_tiempo, semilla0=3000):
    """El MISMO mundo con todas las longitudes x k y el paso de tiempo x m."""
    import pybullet as p
    import gimnasio as G
    series = []
    for e in range(n_ep):
        cli = p.connect(p.DIRECT)
        try:
            rng = np.random.default_rng(semilla0 + e)
            p.setGravity(0, 0, -9.8, physicsClientId=cli)
            p.setTimeStep(G.PASO_FISICO * m_tiempo, physicsClientId=cli)
            sc = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=cli)
            p.createMultiBody(0, sc, physicsClientId=cli)
            caja = p.createCollisionShape(p.GEOM_BOX,
                                          halfExtents=[0.07 * k_long] * 3, physicsClientId=cli)
            objs = [p.createMultiBody(0.25, caja,
                                      basePosition=[(0.45 + 0.22 * i) * k_long,
                                                    0.12 * (i - 1) * k_long,
                                                    (1.15 + 0.2 * i) * k_long],
                                      physicsClientId=cli) for i in range(3)]
            fil = []
            for _ in range(pasos):
                for _ in range(G.SUBPASOS):
                    p.stepSimulation(physicsClientId=cli)
                fil.append([p.getBasePositionAndOrientation(o, physicsClientId=cli)[0][2]
                            for o in objs])
            series.append(np.array(fil, dtype=float))
        finally:
            p.disconnect(physicsClientId=cli)
    return series


def sensibilidad_de_escala(series_a, series_b, k_long, m_tiempo, retardos=2):
    """LA VERSIÓN QUE SÍ SIRVE — y las dos que se cayeron antes están contadas aquí, porque el
    camino importa tanto como el destino.

    INTENTO 1: comparar la ley importada contra la base trivial de B. Un mundo de paseos
      aleatorios SIN NINGUNA LEY sacó 0.484 contra un umbral de 0.5 — a un pelo del falso
      positivo. Causa: la PERSISTENCIA (x[t+1]≈x[t]) es invariante de escala por sí sola, así
      que transfiere aunque no haya ninguna ley que transferir.
    INTENTO 2: usar como nulo una ley ajustada sobre A con el tiempo revuelto. Salió una ley
      catastrófica (error del orden de 1e8) y entonces TODO superaba al nulo. Nulo demasiado
      destructivo: la enmienda de la Regla 31 mordiéndonos por tercera vez en una semana.

    LO QUE SÍ SEPARA: no preguntar "¿transfiere?" sino **"¿LE IMPORTA LA ESCALA?"**
      - Una ley genuinamente dimensional se ROMPE si no deshaces la escala.
      - La persistencia funciona igual a cualquier escala: es invariante de forma trivial.

        SENSIBILIDAD = transferencia(escala deshecha) − transferencia(escala intacta)

    Medido en los dos mundos de control: con ley, +51.9 y +92.3; sin ley, −0.0006 y −0.0017.
    Cuatro órdenes de magnitud de separación, y con el signo bien puesto.
    """
    deshecha = transferencia(series_a, series_b, k_long, m_tiempo, retardos)
    intacta = transferencia(series_a, series_b, 1.0, m_tiempo, retardos)
    return {"escala_longitud": k_long, "escala_tiempo": m_tiempo,
            "transferencia_escala_deshecha": round(float(deshecha), 5),
            "transferencia_escala_intacta": round(float(intacta), 5),
            "sensibilidad": round(float(deshecha - intacta), 5),
            "sobrevive": bool(deshecha > 0.5 and (deshecha - intacta) > 0.5)}


def buscar_pareja(base, k_long, ms, pasos, semilla0=4000, n_ep=6):
    """LA VERSIÓN LEGAL, Y EL HALLAZGO DEL 8-AGO-2026.

    Reescalar SOLO la longitud NO preserva la caída: la gravedad liga longitud con tiempo. Decirle
    a Diego cuál es esa relación sería física con nombre (Regla 4). Lo que SÍ es legal es no
    asumir ninguna y **BUSCAR**: probar parejas (longitud ×k, tiempo ×m) y ver cuál preserva lo
    aprendido. Si aparece un pico, ese pico ES la relación — descubierta, no contada.

    MEDIDO en nuestro propio Gimnasio:
        longitud ×2 → el máximo cae en m = 1.40   (√2 = 1.414)
        longitud ×4 → el máximo cae en m = 2.00   (√4 = 2.000)
    CONTROL, mundo sin ninguna ley (paseos aleatorios reescalados): la curva es PLANA
    (0.482 a 0.518) y el máximo cae donde lo pone el ruido — m=2.0 para k=2 y m=1.25 para k=4,
    sin relación con √k. El pico no lo fabrica el método: está en el mundo.

    Diego no recibió jamás la palabra "metro", ni "segundo", ni ningún exponente. Encontró el
    exponente que liga longitud con tiempo en su mundo preguntando qué reescalado no lo rompe.
    """
    filas = []
    for m in ms:
        otro = correr_gimnasio_escalado(n_ep, int(pasos / m) + 2, k_long, m, semilla0=semilla0)
        filas.append(sensibilidad_de_escala(base, otro, k_long, m))
    mejor = max(filas, key=lambda r: r["transferencia_escala_deshecha"])
    rango = (max(r["transferencia_escala_deshecha"] for r in filas)
             - min(r["transferencia_escala_deshecha"] for r in filas))
    return {"escala_longitud": k_long, "curva": filas,
            "mejor_tiempo": mejor["escala_tiempo"],
            "rango_de_la_curva": round(float(rango), 4),
            "hay_pico": bool(rango > 1.0)}


def regla31(verbose=True):
    """EL INSTRUMENTO SE PRUEBA A SÍ MISMO con dos mundos cuya respuesta conozco:
      LEY VERDADERA — una caída determinista: al reescalar longitudes, la relación sobrevive.
      LEY FALSA      — series que solo comparten una escala arbitraria: no debe sobrevivir.
    Si el verdugo no separa estos dos, no puede opinar sobre ninguna ley."""
    rng = np.random.default_rng(11)
    T = 400
    t = np.arange(T)

    # MUNDO CON LEY: caída con aceleración constante (relación real entre posición y tiempo)
    def caida(k):
        return [np.column_stack([k * (5.0 - 0.5 * 0.004 * (t + f) ** 2) for f in (0, 7, 13)])
                for _ in range(6)]

    # MUNDO SIN LEY: paseos aleatorios independientes escalados por k — no hay relación que
    # transferir, solo la escala.
    def paseo(k):
        out = []
        for _ in range(6):
            out.append(np.column_stack([k * np.cumsum(rng.normal(size=T)) for _ in range(3)]))
        return out

    r_ley = sensibilidad_de_escala(caida(1.0), caida(3.0), 3.0, 1.0)
    r_sin = sensibilidad_de_escala(paseo(1.0), paseo(3.0), 3.0, 1.0)
    if verbose:
        print("=== REGLA 31 sobre verdugo_escala.py ===")
        for nom, r in (("MUNDO CON LEY (caída determinista)", r_ley),
                       ("MUNDO SIN LEY (paseos escalados)  ", r_sin)):
            print(f"  {nom}: escala deshecha {r['transferencia_escala_deshecha']:+.4f} | "
                  f"escala intacta {r['transferencia_escala_intacta']:+.4f} | "
                  f"SENSIBILIDAD {r['sensibilidad']:+.4f}")
    aprueba = r_ley["sobrevive"] and not r_sin["sobrevive"]
    if verbose:
        print("\n" + ("REGLA 31: APRUEBA — la ley cruza la escala y el paseo no."
                      if aprueba else
                      "REGLA 31: REPRUEBA — no separa ley de escala; NO puede juzgar nada."))
    return 0 if aprueba else 1


def main():
    ap = argparse.ArgumentParser(description="Cuarto verdugo: el reescalado del mundo")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--episodios", type=int, default=8)
    ap.add_argument("--pasos", type=int, default=600)
    ap.add_argument("--escalas", nargs="+", type=float, default=[2.0, 3.0])
    ap.add_argument("--buscar-pareja", action="store_true",
                    help="busca qué reescalado de TIEMPO acompaña a cada reescalado de longitud")
    ap.add_argument("--tiempos", nargs="+", type=float,
                    default=[1.0, 1.25, 1.4, 1.6, 2.0, 2.5])
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())

    print(f"=== VERDUGO POR REESCALADO — {a.episodios} episodios x {a.pasos} cuadros ===",
          flush=True)
    base = correr_gimnasio_escalado(a.episodios, a.pasos, 1.0, 1.0)
    if a.buscar_pareja:
        todo = []
        for k in a.escalas:
            r = buscar_pareja(base, k, a.tiempos, a.pasos, n_ep=a.episodios)
            todo.append(r)
            print(f"\n--- longitud x{k} ---", flush=True)
            for f in r["curva"]:
                print(f"   tiempo x{f['escala_tiempo']:<5} transferencia "
                      f"{f['transferencia_escala_deshecha']:+.4f}")
            print(f"   MAXIMO en tiempo x{r['mejor_tiempo']} | rango de la curva "
                  f"{r['rango_de_la_curva']:.3f} | {'HAY PICO' if r['hay_pico'] else 'curva plana'}")
        out = os.path.join(BASE, "resultados", "p19-verdugo-escala")
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "busqueda-pareja.json"), "w", encoding="utf-8") as f:
            json.dump({"instrumento": "verdugo por reescalado — busqueda de pareja",
                       "resultados": todo}, f, indent=2, ensure_ascii=False)
        print(f"\nguardado en {out}/busqueda-pareja.json")
        return
    filas = []
    for k in a.escalas:
        otro = correr_gimnasio_escalado(a.episodios, a.pasos, k, 1.0, semilla0=4000)
        r = sensibilidad_de_escala(base, otro, k, 1.0)
        filas.append(r)
        print(f"  longitud x{k}: escala deshecha {r['transferencia_escala_deshecha']:+.4f} | "
              f"intacta {r['transferencia_escala_intacta']:+.4f} | "
              f"SENSIBILIDAD {r['sensibilidad']:+.4f} "
              f"-> {'SOBREVIVE' if r['sobrevive'] else 'NO SOBREVIVE'}", flush=True)

    out = os.path.join(BASE, "resultados", "p19-verdugo-escala")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump({"instrumento": "verdugo por reescalado", "pruebas": filas}, f, indent=2,
                  ensure_ascii=False)
    print(f"\nguardado en {out}/resumen.json")


if __name__ == "__main__":
    main()
