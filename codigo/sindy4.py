# sindy4.py — EL MOTOR CON CORTE ADIMENSIONAL (prerregistro-47, FIRMADO 11-ago-2026).
#
# POR QUE EXISTE (dos defectos MEDIDOS, no supuestos):
#   1. AGUJEROS DE ESCALA (INFORME-55). `sindy3` ve, deja de ver y vuelve a ver — tres tramos
#      separados en dos sistemas independientes, con la zona muerta en el MISMO sitio. La causa
#      esta localizada en el DIAGNOSTICO-MOTOR-01: `umbral=0.05` es un corte por MAGNITUD, y bajo
#      un cambio de escala s los pesos se multiplican por s (termino constante), por 1 (lineales)
#      y por 1/s (cuadraticos). Un solo numero comparado contra tres escalas que se mueven en
#      direcciones opuestas. No es un parametro mal puesto: es un error DIMENSIONAL.
#   2. ALUCINACION (INFORME-54). Sobre señal casi constante `sindy3` declara leyes de seis
#      terminos con confianza 1.0 en 20 de 25 casos. La matriz esta casi degenerada (condicion
#      7e9 frente a 10.5 del oscilador sano) y el algebra devuelve una mezcla cualquiera con pesos
#      enormes que superan el umbral sin esfuerzo.
#
# POR QUE ES UN ARCHIVO NUEVO Y NO UNA EDICION DE sindy3.py. Tres razones, y la tercera es la
# importante:
#   - LA PUERTA sella por HASH del archivo: editar sindy3 mataria su sello.
#   - Las 67 corridas ya hechas se hicieron con sindy3; editarlo las volveria irreproducibles.
#   - La Fase 2 del plan consiste en correr lo mismo con LOS DOS motores y comparar veredictos.
#     Con un solo motor no hay comparacion posible. Los dos tienen que seguir vivos.
#
# LOS CUATRO CAMBIOS, y NINGUNO MAS (un cambio a la vez o no se sabe cual actuo):
#   1. CORTE ADIMENSIONAL. En vez de "borra lo menor que 0.05", se pregunta si el peso esta lejos
#      de cero EN UNIDADES DE SU PROPIA DISPERSION: CP = |media| / desviacion entre remuestreos.
#      Una razon no tiene unidades, luego NO CAMBIA si el mundo se mide en otra escala. Es la
#      propiedad entera por la que se eligio.
#   2. ADIMENSIONALIZACION. Las columnas se normalizan por las escalas de LOS PROPIOS DATOS antes
#      de ajustar, y los pesos vuelven a unidades al final. Con las escalas de los datos y no con
#      unidades humanas: los kilogramos son un descubrimiento humano, no un hecho del mundo, y
#      meterlos aqui seria herencia por la puerta de atras.
#   3. GUARDA DE CONDICION. Si la matriz esta demasiado degenerada, EL MOTOR CALLA. El tope es
#      aritmetico, no empirico: la doble precision lleva ~16 cifras significativas y con condicion
#      1e6 se conservan 10 buenas.
#   4. PODER PREDICTIVO FUERA DE MUESTRA. Se ajusta en el 70% de las ventanas y se mide en el 30%
#      restante contra la LINEA BASE TONTA. Le exigimos Regla 12 a cada prerregistro y el corazon
#      del proyecto no la tenia: nunca comprobaba que la ley PREDIJERA nada.
#
# LO QUE NO CAMBIA: la forma debil (integrar en vez de derivar) se reutiliza LITERALMENTE de
# sindy3 —se importa su funcion, no se copia— para que la unica diferencia entre los dos motores
# sea la REGLA DE DECISION. Si la copiara, cualquier diferencia podria venir de la copia. Y el
# diccionario sigue teniendo las mismas seis piezas: ampliarlo es otro estudio.

import os
import sys
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sindy3                                                               # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOMBRES = sindy3.NOMBRES
MUESTRAS_MINIMAS = sindy3.MUESTRAS_MINIMAS   # el mismo minimo: sin potencia no se opina

PISO_CP = 3.0            # un peso entra solo si esta a 3 desviaciones o mas de cero
PISO_PESO = 0.01         # ...Y si aporta al menos el 1% de la magnitud del objetivo. VER ABAJO.
TOPE_CONDICION = 1e6     # por encima de esto la matriz no tiene cifras que dar: se calla
FRACCION_AJUSTE = 0.7    # 70% de ventanas para ajustar, 30% para medir lo que no vio
MARGEN_R2 = 0.10         # cuanto debe ganarle la ley a la linea base tonta, fuera de muestra


# POR QUE HACEN FALTA DOS PISOS Y NO UNO (enmienda 3 del prerregistro-47, escrita antes de correr
# el estudio, despues de que LA PUERTA reprobara la primera version de este archivo):
# CP mide CONSISTENCIA, no RELEVANCIA. Sobre el oscilador sin ruido, el sesgo de discretizacion
# del integrador —magnitud 0.0059 contra 1.0— es diminuto pero PERFECTAMENTE consistente, asi que
# su CP sale 7e12, igual de alto que el de un termino verdadero. Un criterio de consistencia solo
# no puede separar "pequeño y sistematico" de "grande y real".
# El segundo piso NO reintroduce el defecto que este archivo arregla: el 0.05 de sindy3 cortaba
# PESOS CON UNIDADES y por eso se movia con la escala; este corta una FRACCION de la magnitud del
# objetivo, y una fraccion no cambia si el mundo se mide en otra escala. Es la diferencia entre
# "pesa menos de 50 gramos" y "es menos del 1% del total".


def _escalas(A, b):
    """Las escalas de los PROPIOS DATOS, columna a columna. Nunca unidades humanas."""
    ea = np.linalg.norm(A, axis=0)
    eb = np.linalg.norm(b, axis=0)
    ea[ea == 0] = 1.0
    eb[eb == 0] = 1.0
    return ea, eb


def _ols(A, b):
    W, *_ = np.linalg.lstsq(A, b, rcond=None)
    return W


def _cp(A_s, b_s, remuestreos, semilla):
    """LA PRESENCIA DE COEFICIENTE. Se remuestrean ventanas completas y se mira, para cada peso,
    cuantas desviaciones lo separan de cero. SIN umbral de magnitud en ninguna parte: el ajuste
    de cada remuestreo es minimos cuadrados puros sobre las seis piezas.

    POR QUE NO LLEVA EL FACTOR raiz(m) DE LA FORMULA ORIGINAL (enmienda 1 del prerregistro-47,
    escrita antes de que existiera este archivo): en el trabajo que la propone, `sigma` es la
    dispersion de una MUESTRA y raiz(m) la convierte en el error de la media. En un bootstrap la
    dispersion entre remuestreos YA ES el error estandar. Con 200 remuestreos el factor vale 14.1
    y multiplicaria por catorce la puntuacion de TODOS los terminos, tambien los falsos."""
    rng = np.random.default_rng(int(semilla))
    n = len(A_s)
    pesos = np.empty((remuestreos, A_s.shape[1], b_s.shape[1]))
    for k in range(remuestreos):
        idx = rng.integers(0, n, n)
        pesos[k] = _ols(A_s[idx], b_s[idx])
    mu, sd = pesos.mean(axis=0), pesos.std(axis=0)
    sd[sd == 0] = np.inf          # dispersion nula sin variacion no es certeza, es degeneracion
    return np.abs(mu) / sd


def _r2(y, pred):
    st = float(np.sum((y - y.mean()) ** 2))
    if st == 0:
        return 0.0
    return 1.0 - float(np.sum((y - pred) ** 2)) / st


def _gana_a_la_linea_base(A, b, soporte, corte):
    """PASO 4 — la Regla 12 aplicada al motor. Se ajusta en las primeras ventanas y se mide en las
    que NO VIO, contra la linea base tonta: el modelo que solo usa el termino constante, es decir
    "la derivada no depende de nada".

    POR QUE ESE RIVAL Y NO OTRO: es el que discrimina exactamente el defecto 2. Sobre una señal
    casi constante el modelo constante lo explica todo, asi que ninguna ley puede ganarle por el
    margen y el motor QUEDA OBLIGADO A CALLAR. Contra un rival mas debil, la alucinacion pasaria."""
    Atr, Ate, btr, bte = A[:corte], A[corte:], b[:corte], b[corte:]
    if len(Ate) < 3:
        return False, []
    margenes = []
    for j in range(b.shape[1]):
        act = soporte[:, j]
        if act.sum() == 0:
            return False, []
        w = _ols(Atr[:, act], btr[:, j])
        r2_ley = _r2(bte[:, j], Ate[:, act] @ w)
        w0 = _ols(Atr[:, :1], btr[:, j])                 # solo el termino constante
        r2_base = _r2(bte[:, j], Ate[:, :1] @ w0)
        margenes.append(round(float(r2_ley - r2_base), 4))
    return all(m >= MARGEN_R2 for m in margenes), margenes


def descubrir(X, dt=1.0, piso_cp=PISO_CP, ventana=None, salto=None, remuestreos=200,
              tope_condicion=TOPE_CONDICION, piso_peso=PISO_PESO, semilla=28):
    """Devuelve la ley o None. Firma compatible con sindy3.descubrir para que la Fase 2 pueda
    correr las mismas campañas con los dos motores sin tocar las campañas."""
    T = len(X)
    if T < MUESTRAS_MINIMAS:
        return None
    ventana = ventana or max(20, T // 25)
    salto = salto or max(1, ventana // 4)
    A, b = sindy3._sistema_debil(X, dt, ventana, salto)
    if A is None or len(A) < 12:
        return None

    condicion = float(np.linalg.cond(A))
    if not np.isfinite(condicion) or condicion > tope_condicion:
        return None                     # CAMBIO 3: sin cifras que dar, no se opina

    ea, eb = _escalas(A, b)             # CAMBIO 2: adimensionalizacion con las propias escalas
    A_s, b_s = A / ea, b / eb

    cp = _cp(A_s, b_s, remuestreos, semilla)          # CAMBIO 1: corte adimensional
    W_s = _ols(A_s, b_s)
    soporte = (cp >= piso_cp) & (np.abs(W_s) >= piso_peso)   # consistente Y relevante
    if soporte.sum() == 0:
        return None                     # ley vacia NO es ley (leccion congelada de sindy2)
    if not soporte.any(axis=0).all():
        return None                     # una ecuacion sin ni un termino no es una ley

    corte = max(3, int(len(A) * FRACCION_AJUSTE))
    gana, margenes = _gana_a_la_linea_base(A, b, soporte, corte)
    if not gana:
        return None                     # CAMBIO 4: una ley que no predice no es una ley

    W = np.zeros_like(cp)
    for j in range(b.shape[1]):
        act = soporte[:, j]
        W[act, j] = _ols(A_s[:, act], b_s[:, j])
    W = W * eb[None, :] / ea[:, None]                  # los pesos vuelven a sus unidades
    return {"terminos": {f"d{var}/dt": [(NOMBRES[i], round(float(W[i, j]), 4),
                                         round(float(cp[i, j]), 2))
                                        for i in range(len(NOMBRES)) if soporte[i, j]]
                         for j, var in enumerate(["x", "v"])},
            "ventanas": int(len(A)), "remuestreos": int(remuestreos),
            "piso_cp": piso_cp, "condicion": round(condicion, 2),
            "margen_sobre_linea_base": margenes}


def _es_la_ley(ley):
    if ley is None:
        return False
    t = ley["terminos"]
    return ([n for n, _, _ in t["dx/dt"]] == ["v"]
            and sorted(n for n, _, _ in t["dv/dt"]) == ["v", "x"])


def regla31(verbose=True):
    """LA REGLA 31 DE ESTE MODULO — y una decision de diseño que hay que leer antes de tocarla.

    AQUI **NO** SE PRUEBA QUE EL MOTOR CALLE SOBRE SEÑAL CASI CONSTANTE, y no es un olvido.
    Ese es el CRITERIO B del prerregistro-47, es decir, el resultado que el estudio existe para
    medir sobre 25 casos y semillas nuevas. Si lo exigiera aqui, el modulo no podria sellarse sin
    cumplirlo, y entonces el criterio B no podria fallar nunca: seria el cuarto criterio
    tautologico del mes (el criterio 4 del prerregistro-41, los chequeos sobre listas vacias, la
    confianza 1.0 del bootstrap sobre un sistema degenerado). UN CRITERIO QUE NO PUEDE FALLAR
    TAMPOCO PUEDE APROBAR NADA.

    Lo que si se prueba aqui es el MECANISMO: que cada guarda se dispara cuando debe, sobre
    entradas construidas a mano que no son el objeto del estudio."""
    fallos = []
    rng = np.random.default_rng(47)

    X, dt = sindy3._oscilador()
    c1 = _es_la_ley(descubrir(X, dt=dt))
    _di(verbose, c1, "CONTROL POSITIVO — oscilador limpio: recupera la ley rala")
    if not c1:
        fallos.append("oscilador-limpio")

    Xr, dtr = sindy3._oscilador(ruido=0.02)
    c2 = _es_la_ley(descubrir(Xr, dt=dtr))
    _di(verbose, c2, "CONTROL POSITIVO — sensor ruidoso: la forma debil sobrevive")
    if not c2:
        fallos.append("oscilador-ruidoso")

    c3 = descubrir(X[rng.permutation(len(X))], dt=dt) is None
    _di(verbose, c3, "CONTROL NEGATIVO — barajado: calla")
    if not c3:
        fallos.append("barajado")

    c4 = descubrir(rng.normal(size=(4000, 2)), dt=dt) is None
    _di(verbose, c4, "SEÑUELO — ruido puro: calla")
    if not c4:
        fallos.append("ruido-puro")

    # MECANISMO 1 — la guarda de condicion se dispara. Se le da al motor el MISMO oscilador sano
    # que acaba de resolver, bajando el tope hasta debajo de su condicion real: si la guarda
    # funciona, el mismo dato que daba ley ahora tiene que callar. Prueba la guarda, no al motor.
    c5 = descubrir(X, dt=dt, tope_condicion=1.0) is None
    _di(verbose, c5, "MECANISMO — con el tope de condicion por debajo del real, calla")
    if not c5:
        fallos.append("guarda-condicion-no-dispara")

    # MECANISMO 2 — el corte adimensional NO depende de la escala. Es la propiedad entera por la
    # que existe este archivo, y se comprueba sobre el control positivo, no sobre el barrido del
    # estudio: la MISMA trayectoria multiplicada por mil tiene que dar el MISMO soporte.
    ley_1 = descubrir(X, dt=dt)
    ley_k = descubrir(X * 1000.0, dt=dt)
    c6 = (_es_la_ley(ley_1) and _es_la_ley(ley_k))
    _di(verbose, c6, "MECANISMO — el soporte no cambia al multiplicar los datos por mil")
    if not c6:
        fallos.append("corte-no-adimensional")

    # MECANISMO 3 — el piso de CP separa por los DOS lados: con el piso en el suelo entran
    # terminos de mas, con el piso por las nubes no entra ninguno. Un filtro que da lo mismo con
    # cualquier piso no esta filtrando.
    # SE PRUEBA SOBRE EL OSCILADOR RUIDOSO, no sobre el limpio, y la razon es la de la enmienda 3:
    # sin ruido la dispersion entre remuestreos baja al ruido de coma flotante y el CP de los
    # terminos verdaderos llega a 1e14, asi que "un piso enorme" tendria que ser mayor que eso
    # para significar algo. Con ruido real el CP maximo se queda en cientos y la prueba discrimina.
    flojo = descubrir(Xr, dt=dtr, piso_cp=0.0, piso_peso=0.0)
    duro = descubrir(Xr, dt=dtr, piso_cp=1e9)
    n_flojo = sum(len(v) for v in flojo["terminos"].values()) if flojo else 0
    c7 = (n_flojo > 3) and (duro is None)
    _di(verbose, c7, f"MECANISMO — el piso de CP filtra por los dos lados "
                     f"(pisos a 0 -> {n_flojo} terminos, piso enorme -> {'calla' if duro is None else 'habla'})")
    if not c7:
        fallos.append("piso-cp-no-filtra")

    # MECANISMO 4 — el PISO DE PESO es el que hace el trabajo que CP no puede hacer, y se prueba
    # por los dos lados sobre el caso que lo hizo necesario: el oscilador SIN ruido.
    #   - con el piso quitado, el sesgo de discretizacion entra y la ley deja de ser la correcta;
    #   - con el piso por las nubes, no entra ningun termino y el motor calla.
    # Si las dos cosas no ocurrieran, el piso estaria de adorno.
    sin_piso = descubrir(X, dt=dt, piso_peso=0.0)
    con_piso_absurdo = descubrir(X, dt=dt, piso_peso=10.0)
    c8 = (sin_piso is not None) and (not _es_la_ley(sin_piso)) and (con_piso_absurdo is None)
    _di(verbose, c8, "MECANISMO — el piso de peso filtra por los dos lados "
                     f"(sin piso -> {'ley equivocada' if sin_piso and not _es_la_ley(sin_piso) else 'igual'}"
                     f", piso absurdo -> {'calla' if con_piso_absurdo is None else 'habla'})")
    if not c8:
        fallos.append("piso-peso-no-filtra")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — corte adimensional y guardas verificadas."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def _di(verbose, ok, texto):
    if verbose:
        print(f"  {'ok  ' if ok else 'FALLO'} {texto}")


def comparar_con_sindy3(verbose=True):
    """La medida honesta de que cambio: misma verdad, mismo ruido, los dos motores. No es un juez
    de nada — es lo que permitira, en la Fase 2, decir con cual se midio cada campaña."""
    filas = []
    for ruido in (0.0, 0.005, 0.01, 0.02, 0.05):
        X, dt = sindy3._oscilador(ruido=ruido)
        viejo = sindy3._es_la_ley(sindy3.descubrir(X, dt=dt))
        nuevo = _es_la_ley(descubrir(X, dt=dt))
        filas.append((ruido, viejo, nuevo))
        if verbose:
            print(f"  ruido {ruido:<6}: sindy3 {'SI' if viejo else 'no'}   "
                  f"sindy4 {'SI' if nuevo else 'no'}")
    return filas


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Motor con corte adimensional (prereg-47)")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--comparar", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    if a.comparar:
        comparar_con_sindy3()
        sys.exit(0)
    print("uso: --regla31 | --comparar")
