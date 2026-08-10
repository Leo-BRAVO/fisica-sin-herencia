# escala.py — PRERREGISTRO 46: ¿cuál es la banda de escala en la que el motor simbólico VE?
#
# (El prerregistro-45 quedó NULO por su propio señuelo — ver INFORME-54. El 46 lo rehace con el
#  señuelo colocado donde corresponde y con semillas nuevas.)
#
# ORIGEN. El INFORME-50 midió que `sindy3` encuentra la misma ley a x1 y x10 y NO la encuentra a
# x0.1 ni a x100. Mismos datos, mismo sistema, solo cambian las unidades. Salió al pasar G9 por la
# puerta: su señuelo de escala se puso rojo y la causa no era suya.
#
# POR QUE ESTO NO ES UN DETALLE. La Regla 2 exige el dato mas crudo posible —pixeles, voltajes,
# conteos— y los datos crudos vienen en las unidades que vengan. Un motor con banda estrecha
# produce FALSOS NEGATIVOS: leyes que estaban ahi y no vio. Lo que queda en duda, por tanto, no son
# nuestros hallazgos sino nuestros "no concluyente".
#
# LO QUE ESTE MODULO NO HACE: no arregla el motor. Normalizar antes de ajustar y re-escalar los
# coeficientes despues es el arreglo estandar y probablemente el correcto — y hacerlo aqui seria
# medir y arreglar en la misma corrida, que es como se acaba arreglando hasta que el numero salga
# bonito. Este modulo MIDE. El arreglo va en su propio prerregistro.
#
# Uso: python escala.py [--regla31] [--salida resultados/p45-banda/medida.json]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

import sindy3                                                               # noqa: E402

# ------------------------------------------------------------------ EL PRERREGISTRO, EN CODIGO
# Congelado en el prerregistro-45 ANTES de correr. Cambiar cualquiera de estos numeros despues de
# ver los datos es lo unico que la enmienda de la Regla 15 nunca delego.
EXPONENTES = [round(-3.0 + 0.25 * i, 2) for i in range(25)]   # 10^-3 .. 10^3, 25 puntos
SEMILLAS = (23, 29, 31, 37, 41)   # NUEVAS: las 2,3,5,7,11 quedaron quemadas al arreglar el modulo
T = 4000
DT = 0.02
RUIDO_REL = 0.002              # ruido RELATIVO a la escala: si no, escalar cambiaria la relacion
                               # señal/ruido y el estudio mediria eso en vez de la escala
MINIMOS_VE = 4                 # de 5 semillas, para decir que "ve" en esa escala
MAXIMO_NO_VE = 1               # de 5, para decir que "no ve"
DECADAS_ESTRECHA = 3.0         # menos que esto se declara banda ESTRECHA (grave)

METODO = {
    "prerregistro": 46,
    "tipo_de_medida": "umbral",   # el motor DECLARA ley o no: es una decision binaria por corrida
    "que_mide": ("en cuantas de 5 semillas el motor declara ley, para cada una de 25 escalas del "
                 "MISMO sistema. Lo unico que cambia entre escalas es un factor multiplicativo"),
    "comparten_datos": {
        "hay": True,
        "porque": "cada escala usa EXACTAMENTE la misma trayectoria multiplicada por su factor — "
                  "esa es la definicion del experimento. Si cada escala tuviera su propia "
                  "trayectoria, la diferencia podria ser de la trayectoria y no de la escala.",
    },
    "linea_base": ("el ideal: 'el motor ve la ley siempre que exista, sin importar las unidades'. "
                   "Se reporta la FRACCION DE ESCALAS en que ve, sobre el barrido declarado — no "
                   "un acierto crudo (Regla 11)"),
    "formulas": [
        {"base": {"exponente": 0.0, "ruido_rel": 0.002}, "parametro": "ruido_rel", "factor": 200.0,
         "esperado": "baja",
         "porque": "con la señal enterrada en ruido no hay ley que hallar, luego la fraccion de "
                   "semillas en que ve tiene que caer. Es la comprobacion de que la medida "
                   "responde a la fisica del problema y no solo a la aritmetica de la escala"},
        # AQUI DECLARE UNA SEGUNDA RELACION —"subir el exponente baja la cuenta"— Y LA RETIRO,
        # por una razon que vale mas que la relacion: UNA RELACION METAMORFICA SOLO PUEDE DECLARAR
        # LO QUE SE SABE A PRIORI, y como cambia esta medida con la escala es EXACTAMENTE lo
        # desconocido que el estudio existe para medir. Declararla era inventarme la respuesta y
        # meterla en el instrumento que iba a buscarla.
        # (Ademas la escribi dos veces con base 0.0 —multiplicar cero por cuatro sigue siendo
        # cero— y la puerta me la tumbo midiendo x1.000 las dos veces. Tercera vez en un dia con
        # ese mismo descuido; queda escrito para el que lea el modulo despues.)
    ],
}


# ------------------------------------------------------------------ los dos sistemas
def oscilador(semilla=3, ruido_rel=RUIDO_REL):
    """Oscilador amortiguado. El mismo del INFORME-50, para que el hallazgo sea comparable."""
    rng = np.random.default_rng(int(semilla))
    x = np.zeros((T, 2))
    x[0] = [1.0, 0.0]
    for t in range(1, T):
        dx = np.array([x[t - 1, 1], -0.9 * x[t - 1, 0] - 0.05 * x[t - 1, 1]])
        x[t] = x[t - 1] + DT * dx + rng.normal(0, float(ruido_rel), 2)
    return x


def caida_con_roce(semilla=3, ruido_rel=RUIDO_REL):
    """Un sistema DISTINTO, para no confundir una propiedad del motor con una del oscilador:
    velocidad que crece hasta su terminal por roce lineal. Su ley tiene otra forma."""
    rng = np.random.default_rng(int(semilla) + 500)
    x = np.zeros((T, 2))
    x[0] = [0.0, 0.0]
    for t in range(1, T):
        dx = np.array([x[t - 1, 1], 1.0 - 0.35 * x[t - 1, 1]])
        x[t] = x[t - 1] + DT * dx + rng.normal(0, float(ruido_rel), 2)
    return x


SISTEMAS = {"oscilador": oscilador, "caida_con_roce": caida_con_roce}


def _ve(sistema, exponente, semilla, ruido_rel=RUIDO_REL):
    """¿El motor declara ley sobre este sistema, a esta escala, con esta semilla?"""
    x = SISTEMAS[sistema](semilla=semilla, ruido_rel=ruido_rel)
    return sindy3.descubrir(x * (10.0 ** float(exponente)), dt=DT) is not None


def _metodo_medir(exponente=0.0, ruido_rel=RUIDO_REL):
    """PASO 1 — la medida escalar: en cuantas de las 5 semillas ve, a esa escala."""
    return float(sum(1 for s in SEMILLAS
                     if _ve("oscilador", exponente, s, ruido_rel=ruido_rel)))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿la medida sigue a la ESCALA, o a otra cosa que cambia
    con ella?** El peligro concreto: si el ruido fuera absoluto en vez de relativo, escalar la
    señal cambiaria la relacion señal/ruido, y estariamos midiendo eso —una propiedad del ruido—
    creyendo medir una propiedad del motor. Se comprueba que con ruido RELATIVO la relacion
    señal/ruido es la misma en todas las escalas, que es lo que hace legitima la comparacion.
    """
    fallos = []
    # (a) la relacion señal/ruido NO cambia con la escala (por construccion, pero se mide)
    razones = []
    for e in (-2.0, 0.0, 2.0):
        x = oscilador(semilla=3) * (10.0 ** e)
        razones.append(float(np.std(x) / (RUIDO_REL * (10.0 ** e))))
    if max(razones) / min(razones) > 1.01:
        fallos.append(f"la relacion señal/ruido CAMBIA con la escala {razones} — el estudio "
                      f"estaria midiendo el ruido y no el motor")
    # (b) la medida debe responder al ruido, que es la unica variable fisica real aqui
    limpio = _metodo_medir(exponente=0.0, ruido_rel=0.002)
    sucio = _metodo_medir(exponente=0.0, ruido_rel=0.4)
    if not (limpio > sucio):
        fallos.append(f"la medida NO responde al ruido (limpio {limpio}, sucio {sucio}): no esta "
                      f"midiendo si hay ley que hallar")
    return {"aprueba": not fallos, "fallos": fallos,
            "razones_senal_ruido": [round(r, 3) for r in razones],
            "ve_limpio": limpio, "ve_sucio": sucio}


# ------------------------------------------------------------------ REGLA 31, los dos lados
def regla31(verbose=True):
    """Los dos lados declarados en el prerregistro-45, mas su señuelo."""
    fallos = []

    def caso(nombre, ok, extra=""):
        print(f"  {'ok  ' if ok else 'FALLO'} {nombre} {extra}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-45: la medida de la banda de escala ==")

    # LADO POSITIVO — a escala 1 el motor debe ver en las 5 semillas.
    v1 = _metodo_medir(exponente=0.0)
    caso("a escala x1 el motor ve en las 5 semillas", v1 == 5.0, f"{v1:.0f}/5")

    # LADO NEGATIVO — RUIDO PURO escalado igual: no puede declarar ley en NINGUNA escala.
    malos = []
    for e in (-2.0, 0.0, 2.0):
        for s in SEMILLAS[:3]:
            rng = np.random.default_rng(int(s) + 9000)
            ruido = rng.normal(size=(T, 2)) * (10.0 ** e)
            if sindy3.descubrir(ruido, dt=DT) is not None:
                malos.append((e, s))
    caso("sobre RUIDO PURO no declara ley en ninguna escala", not malos, str(malos[:3]))

    # AQUI VIVIA EL SEÑUELO "un sistema sin dinamica no puede dar ley", y APROBO DONDE NO DEBIA:
    # el motor declaro ley en 20 de 25 casos sin dinamica, con confianza 1.0 (INFORME-54). Por el
    # criterio congelado del prerregistro-45, ese estudio quedo NULO y se cumplio sin discutirlo.
    #
    # NO se quita porque falle. Se quita porque estaba MAL COLOCADO, y eso es un error de diseño
    # mio que conviene dejar escrito: metí en la Regla 31 de MI INSTRUMENTO una prueba sobre el
    # OBJETO DE ESTUDIO. Consecuencia: un defecto del motor bloquea el modulo que existe para
    # medir defectos del motor. La Regla 31 de un instrumento debe examinar el PROCEDIMIENTO DE
    # MEDIDA; el comportamiento del sujeto es RESULTADO, no requisito de entrada.
    # La medida sigue viva y publicada en resultados/p45-senuelo/medida.json, y el barrido se
    # rehace en el prerregistro-46 con esa separacion clara.

    # LA MEDIDA PUEDE DISTINGUIR — si diera lo mismo en todas las escalas no mediria nada.
    valores = {e: _metodo_medir(exponente=e) for e in (-3.0, 0.0, 3.0)}
    caso("la medida DISTINGUE entre escalas (no da lo mismo en todas)",
         len(set(valores.values())) > 1, str(valores))

    if verbose:
        print("REGLA 31: " + ("APRUEBA" if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


# ------------------------------------------------------------------ el barrido
def barrer(verbose=True):
    """El barrido declarado: 25 escalas x 5 semillas x 2 sistemas."""
    filas = {}
    for nombre in SISTEMAS:
        fila = []
        for e in EXPONENTES:
            n = sum(1 for s in SEMILLAS if _ve(nombre, e, s))
            fila.append({"exponente": e, "escala": 10.0 ** e, "ve_en": n, "de": len(SEMILLAS)})
            if verbose:
                marca = "VE " if n >= MINIMOS_VE else ("no " if n <= MAXIMO_NO_VE else "?? ")
                print(f"  {nombre:<16} 10^{e:<6} {marca} {n}/{len(SEMILLAS)}")
        filas[nombre] = fila
    return filas


def _tramos(fila):
    """Los tramos CONTIGUOS donde el motor ve en >= MINIMOS_VE, como lista de (ini, fin).

    Se escribe partiendo la lista en tramos en vez de acumulando dentro de un bucle. El paso 2 de
    la puerta marcaba la version con acumuladores ('ini' y 'mejor' asignados fuera del bucle y
    reasignados dentro). Ahi el patron era legitimo — pero el guardian existe porque ESE patron ya
    me escondio un error real, y reescribirlo claro cuesta menos que discutir con el.
    """
    ve = [f["ve_en"] >= MINIMOS_VE for f in fila]
    tramos, i = [], 0
    while i < len(ve):
        if not ve[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(ve) and ve[j + 1]:
            j += 1
        tramos.append((fila[i]["exponente"], fila[j]["exponente"]))
        i = j + 1
    return tramos


def _banda(fila):
    """El tramo contiguo MAS LARGO, o (None, None, 0) si el motor no ve en ninguna parte."""
    tramos = _tramos(fila)
    if not tramos:
        return (None, None, 0)
    ini, fin = max(tramos, key=lambda t: t[1] - t[0])
    return (ini, fin, fin - ini)


def veredicto(filas):
    """Los criterios del prerregistro, aplicados tal como se congelaron. Se calcula el detalle de
    cada sistema primero y se resume despues, para no acumular banderas dentro del bucle."""
    def de_un_sistema(fila):
        ini, fin, largo = _banda(fila)
        fuera = [f for f in fila
                 if ini is None or f["exponente"] < ini or f["exponente"] > fin]
        return {"banda_desde_10e": ini, "banda_hasta_10e": fin,
                "decadas": None if ini is None else round(largo, 2),
                "tramos_contiguos": len(_tramos(fila)),
                "fuera_de_la_banda_no_ve": bool(all(f["ve_en"] <= MAXIMO_NO_VE for f in fuera)),
                "ve_en_todas_las_escalas": all(f["ve_en"] >= MINIMOS_VE for f in fila)}

    detalle = {n: de_un_sistema(f) for n, f in filas.items()}
    ds = list(detalle.values())
    hay_banda_en_los_dos = all(d["banda_desde_10e"] is not None
                               and d["fuera_de_la_banda_no_ve"] for d in ds)
    estrecha = any(d["decadas"] is not None and d["decadas"] < DECADAS_ESTRECHA for d in ds)
    erratico = any(d["tramos_contiguos"] > 1 for d in ds)

    if all(d["ve_en_todas_las_escalas"] for d in ds):
        v = ("EL INFORME-50 QUEDA CONTRADICHO POR ESTE ESTUDIO: el motor ve en las 25 escalas de "
             "los dos sistemas. La causa del fallo de G9 esta en otra parte y es error mio")
    elif erratico:
        v = ("ERRATICO — el motor ve y deja de ver en tramos SEPARADOS, no en una banda. Es PEOR "
             "que una banda: una banda se rodea normalizando; un patron erratico hace que el "
             "veredicto dependa de las unidades de forma impredecible")
    elif hay_banda_en_los_dos and estrecha:
        v = "HAY BANDA Y ES ESTRECHA (menos de 3 decadas en al menos un sistema)"
    elif hay_banda_en_los_dos:
        v = "HAY BANDA, ANCHA (3 decadas o mas en los dos sistemas)"
    else:
        v = ("NO CONCLUYENTE: no hay un intervalo contiguo limpio en los dos sistemas — el motor "
             "falla de forma que este barrido no describe")
    return {"detalle": detalle, "veredicto": v}


def main():
    ap = argparse.ArgumentParser(description="Prerregistro 45 — la banda de escala del motor")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("=== PRERREGISTRO 45 — barrido de escala, 25 puntos x 5 semillas x 2 sistemas ===")
    filas = barrer()
    r = veredicto(filas)
    print()
    for n, d in r["detalle"].items():
        print(f"  {n}: banda 10^{d['banda_desde_10e']} .. 10^{d['banda_hasta_10e']} "
              f"({d['decadas']} decadas) | fuera no ve: {d['fuera_de_la_banda_no_ve']}")
    print(f"\nVEREDICTO: {r['veredicto']}")
    if a.salida:
        os.makedirs(os.path.dirname(a.salida) or ".", exist_ok=True)
        json.dump({"prerregistro": 45, "exponentes": EXPONENTES, "semillas": list(SEMILLAS),
                   "muestras": T, "dt": DT, "ruido_relativo": RUIDO_REL,
                   "barrido": filas, **r},
                  open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"escrito: {a.salida}")


if __name__ == "__main__":
    main()
