# reflejos.py — GEN G12: la politica rapida, DESTILADA de deliberaciones (prerregistro-40).
#
# QUE ES UN REFLEJO, y esta definicion es todo el gen: NO es una regla que le escribimos a Diego.
# Es una deliberacion suya, comprimida hasta que corre sin pensar.
#
# LA INVESTIGACION QUE LO RESPALDA. La arquitectura de LeCun separa dos modos:
#   MODO 2 — razonar: predecir consecuencias, evaluar costes, planificar. Lento.
#   MODO 1 — reaccionar: una politica que computa la accion directa desde la percepcion. Rapido.
# Y la pieza que hace esto construible: "el agente puede entrenar la politica para APROXIMAR las
# acciones optimas que salen del razonamiento de Modo-2; asi adquiere destrezas que quedan
# COMPILADAS en una politica reactiva".
#
# Eso da criterios comprobables en vez de adjetivos. Un reflejo legitimo:
#   (a) es MAS RAPIDO que la deliberacion que lo origino — si no, es una copia lenta;
#   (b) COINCIDE con ella donde ella opinaba;
#   (c) CALLA donde ella no actuaria — un reflejo que dispara siempre no es un reflejo;
#   (d) no puede nacer de ruido.
#
# EL RIESGO REAL DE ESTE GEN, dicho antes que nada: un reflejo es la PUERTA TRASERA PERFECTA para
# meter fisica humana. Si yo escribiera "si el objeto cae, retira la mano", le estaria enseñando
# gravedad disfrazada de instinto. Por eso NINGUN reflejo se escribe a mano: todos se destilan de
# decisiones que Diego ya tomo, y `sanidad.politica_limpia()` comprueba que ninguna funcion de este
# modulo nombre masa, gravedad, caida ni nada del mundo.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

PISO_ACUERDO = 0.35      # ganancia MINIMA sobre la linea base tonta (Regla 12), no
                         # acierto crudo: con clases desiguales el acierto crudo miente
TECHO_DISPARO = 0.85     # ...y no puede disparar en mas de esta fraccion de los casos
MINIMO_EJEMPLOS = 40     # guarda de potencia: destilar de menos es copiar ruido

_BASE_MET = {"n": 200.0, "senal": 1.0, "ruido": 0.30}
METODO = {
    "tipo_de_medida": "umbral",   # el reflejo DECIDE actuar o no: clasifica
    "comparten_datos": {
        "hay": True,
        "porque": "el reflejo se entrena sobre las MISMAS decisiones que la deliberacion produjo — "
                  "esa es su definicion. Lo que los separa NO son los datos sino el TIEMPO: el "
                  "reflejo no puede mirar el futuro ni evaluar costes, solo el estado presente. "
                  "Se comprueba en el caso 1 (velocidad) y en el 2 (acuerdo por encima del azar).",
    },
    "formulas": [
        {"base": dict(_BASE_MET), "parametro": "ruido", "factor": 5.0, "esperado": "baja",
         "porque": "mas ruido en las decisiones de origen = menos estructura que destilar, luego "
                   "menos acuerdo. Se declara como DESIGUALDAD porque el acuerdo de una "
                   "aproximacion lineal a una frontera curva bajo ruido no tiene forma cerrada: "
                   "poner un factor exacto seria inventarselo"},
        {"base": dict(_BASE_MET), "parametro": "senal", "factor": 0.02, "esperado": "baja",
         "porque": "sin señal en el origen las decisiones las manda el ruido y no queda nada que "
                   "destilar: el acuerdo cae"},
    ],
}


HORIZONTE = 8      # cuantos pasos hacia adelante mira el Modo 2
ACCIONES = (0, 1)  # las dos que hay: actuar o no


def deliberar(estados, senal=1.0, ruido=0.30, semilla=3):
    """MODO 2 — la version LENTA de verdad: para cada estado y cada accion posible, RUEDA el mundo
    hacia adelante HORIZONTE pasos, acumula el coste, y elige la accion mas barata.

    POR QUE ES ASI Y NO UNA COMPARACION. La primera version de este modulo "deliberaba" con un
    `coste < umbral`, y su Regla 31 lo cazo al instante: el reflejo salia MAS LENTO que la
    deliberacion (0.77 ms contra 0.38 ms). No era un bug del reflejo — era que mi Modo 2 no estaba
    deliberando. Comparar no es planificar. Modo 2 significa PREDECIR CONSECUENCIAS y EVALUAR
    COSTES, y eso cuesta caro por definicion; si no costara, no haria falta destilar nada.
    """
    x = np.asarray(estados, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    rng = np.random.default_rng(int(semilla))
    n, d = x.shape
    # modelo del mundo, fijo: el estado deriva y la accion lo empuja
    A = np.eye(d) * 0.92
    empuje = np.zeros(d)
    empuje[0] = 0.06   # calibrado para que la decision quede REPARTIDA (ver caso 7)
    ruidos = ruido * rng.normal(size=(n, len(ACCIONES), HORIZONTE))
    total = np.zeros((n, len(ACCIONES)))
    for k, a in enumerate(ACCIONES):
        e = x.copy()
        for h in range(HORIZONTE):
            e = e @ A.T + a * empuje
            # EL COSTE ES CUADRATICO ALREDEDOR DE UN OBJETIVO, no lineal. Cazado por el caso 7 de
            # esta misma Regla 31: con un coste lineal, empujar SIEMPRE convenia, la deliberacion
            # elegia actuar en el 100% de los casos y el reflejo "acertaba" el 100% imitando una
            # constante. Un mundo donde la respuesta es siempre la misma no prueba ninguna
            # politica — es el mismo fallo que "el presupuesto no ata" del prereg-39, con otra cara.
            # Con coste cuadratico, empujar ayuda si el estado esta por debajo del objetivo y
            # ESTORBA si esta por encima: la decision depende del estado, que es el punto.
            # LA FRONTERA OPTIMA ES CURVA (lleva un producto e0*e1), asi que un reflejo LINEAL
            # solo puede aproximarla. Es a proposito: un reflejo es una compresion CON PERDIDA. Si
            # pudiera copiar la deliberacion sin perder nada, no habria nada que medir — y eso fue
            # lo que paso en la version anterior, con acuerdo clavado en 0.90 pasara lo que pasara.
            total[:, k] += senal * ((e[:, 0] - 0.5 * e[:, 1]) ** 2
                                    + 0.8 * e[:, 0] * e[:, 1]) + ruidos[:, k, h]
    return np.argmin(total, axis=1).astype(int)


def destilar(estados, decisiones):
    """MODO 1 — comprime las decisiones en una politica que solo mira el estado presente.
    Un ajuste lineal con umbral: deliberadamente pobre. Un reflejo tiene que ser TONTO y rapido;
    si necesitara ser listo, no seria un reflejo."""
    x = np.asarray(estados, dtype=float)
    y = np.asarray(decisiones, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    if len(y) < MINIMO_EJEMPLOS:
        return {"listo": False,
                "motivo": f"solo {len(y)} decisiones; hacen falta {MINIMO_EJEMPLOS}. Destilar de "
                          f"menos es copiar ruido y llamarlo instinto"}
    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return {"listo": True, "coef": coef.tolist()}


def reaccionar(politica, estados):
    """Aplica el reflejo. Sin planificar, sin mirar el futuro, sin evaluar costes: solo el estado."""
    if not politica.get("listo"):
        return None
    x = np.asarray(estados, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    X = np.column_stack([np.ones(len(x)), x])
    return (X @ np.asarray(politica["coef"]) > 0.5).astype(int)


def examinar(politica, estados, decisiones_lentas):
    """Las cuatro cifras que deciden si un reflejo se adopta o se tira."""
    r = reaccionar(politica, estados)
    if r is None:
        return {"adoptable": False, "motivo": "la politica no esta lista"}
    y = np.asarray(decisiones_lentas, dtype=int)
    crudo = float(np.mean(r == y))
    # LA LINEA BASE TONTA (Regla 12), que es lo que me faltaba. Medido el 10-ago: con la
    # deliberacion disparando solo el 2% de las veces, un reflejo que dijera SIEMPRE "no" acertaba
    # el 88.7%, y el mio sacaba 90.7%. Llamar "acuerdo 0.907" a eso era un numero que no significaba
    # nada. Mi propio METODO me cazo violando una regla del proyecto que existe desde el principio.
    trivial = float(max(np.mean(y == 0), np.mean(y == 1)))
    ganancia = (crudo - trivial) / max(1.0 - trivial, 1e-9)   # 0 = igual que el tonto, 1 = perfecto
    dispara = float(np.mean(r))
    return {"acuerdo_crudo": round(crudo, 4),
            "linea_base_tonta": round(trivial, 4),
            "acuerdo_con_la_deliberacion": round(max(0.0, ganancia), 4),
            "fraccion_en_que_dispara": round(dispara, 4),
            "adoptable": bool(ganancia >= PISO_ACUERDO and dispara <= TECHO_DISPARO),
            "nota": "el acuerdo es GANANCIA sobre la linea base tonta (Regla 12), no acierto crudo: "
                    "con clases desiguales, acertar mucho puede no significar nada"}


# ------------------------------------------------------ lo que LA PUERTA ejecuta
def _mundo_de_prueba(n=200, senal=1.0, ruido=0.30, semilla=7):
    """Un mundo sintetico con verdad conocida: la decision correcta depende de una combinacion
    lineal del estado, mas ruido. Sirve para medir si el destilado recupera lo que habia."""
    rng = np.random.default_rng(int(semilla))
    n = int(n)
    x = rng.normal(size=(n, 3))
    return x, deliberar(x, senal=senal, ruido=ruido, semilla=semilla + 1)


def _metodo_medir(n=200.0, senal=1.0, ruido=0.30):
    x, y = _mundo_de_prueba(n=n, senal=senal, ruido=ruido)
    p = destilar(x, y)
    if not p["listo"]:
        return 0.0
    return float(examinar(p, x, y)["acuerdo_con_la_deliberacion"])


def _metodo_sanidad():
    """PASO 3 — la ficha. Aqui la verdad es cuanta señal habia en el origen: el acuerdo del reflejo
    debe seguirla, y no seguir al ruido."""
    import sanidad as S
    # UNA lectura, UNA verdad. Declarar una verdad sin lectura que la acompañe hace que la ficha
    # avise "no hay lectura", y tiene razon: no puede comprobar lo que no le das. Que el acuerdo NO
    # siga al ruido lo cubre el paso 1, con su relacion metamorfica declarada en METODO.
    senales = [0.2, 0.5, 0.8, 1.2, 1.6, 2.0, 2.6, 3.2]
    acuerdos = [_metodo_medir(n=300.0, senal=v, ruido=0.30) for v in senales]
    r = S.correlaciones({"senal": acuerdos}, {"senal": senales})
    return {"aprueba": not r["fallos"], "fallos": r["fallos"], "tabla": r["tabla"]}


def regla31(verbose=True):
    import time
    fallos = []
    x, y = _mundo_de_prueba(n=400)
    pol = destilar(x, y)

    # 5) MAS RAPIDO que la deliberacion. Si no lo es, no es un reflejo: es una copia lenta.
    t0 = time.perf_counter()
    for _ in range(50):
        deliberar(x)
    t_lento = time.perf_counter() - t0
    t0 = time.perf_counter()
    for _ in range(50):
        reaccionar(pol, x)
    t_rapido = time.perf_counter() - t0
    c5 = t_rapido < t_lento
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} MAS RAPIDO: reflejo {t_rapido*1000:.2f} ms vs "
              f"deliberacion {t_lento*1000:.2f} ms")
    if not c5:
        fallos.append("velocidad")

    # 6) COINCIDE con la deliberacion por encima del azar
    ex = examinar(pol, x, y)
    c6 = ex["acuerdo_con_la_deliberacion"] >= PISO_ACUERDO
    if verbose:
        print(f"  {'ok  ' if c6 else 'FALLO'} COINCIDE: acuerdo "
              f"{ex['acuerdo_con_la_deliberacion']:.3f} (piso {PISO_ACUERDO})")
    if not c6:
        fallos.append("acuerdo")

    # 7) CALLA donde la deliberacion no actuaria. Un reflejo que dispara siempre es un boton
    #    encendido, no un instinto.
    c7 = ex["fraccion_en_que_dispara"] <= TECHO_DISPARO
    if verbose:
        print(f"  {'ok  ' if c7 else 'FALLO'} NO DISPARA SIEMPRE: dispara en "
              f"{ex['fraccion_en_que_dispara']:.3f} de los casos (techo {TECHO_DISPARO})")
    if not c7:
        fallos.append("dispara-siempre")

    # 8) SEÑUELO: una deliberacion de PURO RUIDO no puede parir un reflejo adoptable. Es el hermano
    #    de los cuatro señuelos que ya cazaron fallos reales en su primera corrida.
    rng = np.random.default_rng(99)
    x_r = rng.normal(size=(400, 3))
    y_r = rng.integers(0, 2, 400)
    pol_r = destilar(x_r, y_r)
    ex_r = examinar(pol_r, x_r, y_r)
    c8 = not ex_r["adoptable"]
    if verbose:
        print(f"  {'ok  ' if c8 else 'FALLO'} SEÑUELO DE RUIDO: de decisiones al azar NO sale "
              f"reflejo adoptable (acuerdo {ex_r['acuerdo_con_la_deliberacion']:.3f})")
    if not c8:
        fallos.append("senuelo-ruido")

    # 9) GUARDA DE POTENCIA: destilar de pocas decisiones debe NEGARSE, no improvisar.
    c9 = not destilar(x[:10], y[:10])["listo"]
    if verbose:
        print(f"  {'ok  ' if c9 else 'FALLO'} GUARDA DE POTENCIA: con 10 decisiones se NIEGA a "
              f"destilar (minimo {MINIMO_EJEMPLOS})")
    if not c9:
        fallos.append("guarda-potencia")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el reflejo es mas rapido, coincide, calla donde debe y "
                                "no nace del ruido." if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="G12 reflejos: la politica destilada (prereg-40)")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    x, y = _mundo_de_prueba()
    print(examinar(destilar(x, y), x, y))


if __name__ == "__main__":
    main()
