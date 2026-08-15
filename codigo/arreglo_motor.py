# arreglo_motor.py — PRERREGISTRO 47: ¿arregla el corte adimensional los dos defectos del motor?
#
# QUE MIDE. Los cuatro criterios congelados del prerregistro-47, sobre CINCO SEMILLAS NUEVAS
# (43, 47, 53, 59, 61) y los DOS motores:
#   A  agujeros cerrados     — un solo tramo contiguo, >=5 de 6 decadas, en los dos sistemas
#   B  alucinacion muerta    — 0 leyes declaradas en 25 de 25 casos de señal casi constante
#   C  no se rompio nada     — sindy4 recupera lo que sindy3 recuperaba, y calla donde callaba
#   D  es del motor          — sindy3, con ESTAS MISMAS semillas nuevas, SIGUE fallando A y B
#
# POR QUE EXISTE EL CRITERIO D, que es el que me deja peor. Sin el, un arreglo que no arregla nada
# podria aprobar solo porque las semillas nuevas fueran mas faciles que las del prerregistro-46.
# Con el, si sindy3 sale limpio sobre estas semillas, la conclusion no es "sindy4 funciona" sino
# "el INFORME-55 estaba equivocado", y se escribe asi.
#
# LO QUE ESTE MODULO NO HACE: no arregla el motor —eso es sindy4.py, ya escrito y sellado aparte—
# y no dice que resultados nuestros quedan tocados, que es la Fase 2 y exige medir campaña por
# campaña. Aqui solo se mide si los dos defectos concretos siguen ahi.
#
# LA REGLA 31 DE ESTE ARCHIVO EXAMINA MI PROCEDIMIENTO DE MEDIDA, NUNCA EL MOTOR. Lo escribo
# arriba del todo porque este mismo error mato al prerregistro-45 y casi al 44, el mismo dia: si
# metiera aqui una prueba sobre lo que hace sindy4, un defecto del motor bloquearia el modulo que
# existe para medir defectos del motor, y ademas el criterio que el estudio debe poder reprobar
# no podria reprobar nunca.
#
# Uso: python arreglo_motor.py [--regla31] [--salida resultados/p47-arreglo/medida.json]

import os
import sys
import json
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sindy3                                                               # noqa: E402
import sindy4                                                               # noqa: E402
import escala                                                               # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# El barrido es IDENTICO al del prerregistro-46 para que la comparacion sea legitima: mismas
# escalas, mismos dos sistemas, mismo ruido relativo. Lo unico que cambia son las semillas y el
# motor. Se importan de `escala` en vez de copiarse, por la misma razon que sindy4 importa la
# forma debil de sindy3: una copia introduce diferencias que luego no se sabe de donde salieron.
EXPONENTES = escala.EXPONENTES
SISTEMAS = escala.SISTEMAS
DT = escala.DT
RUIDO_REL = escala.RUIDO_REL
MINIMOS_VE = escala.MINIMOS_VE

# NUEVAS. Quemadas: 2,3,5,7,11 / 23,29,31,37,41 / 7 (las sondas) / 43 (ver enmienda 4: la abri
# para diagnosticar por que la puerta reprobaba la relacion metamorfica, y por eso sale).
SEMILLAS = (47, 53, 59, 61, 67)
DECADAS_MINIMAS = 5.0             # criterio A: el tramo unico debe cubrir >=5 de las 6 decadas
CASOS_CONSTANTE = 25              # criterio B: 5 semillas x 5 amplitudes de señal casi constante
MOTORES = {"sindy3": sindy3.descubrir, "sindy4": sindy4.descubrir}

METODO = {
    "prerregistro": 47,
    "tipo_de_medida": "umbral",   # cada corrida es binaria: el motor declara ley o no la declara
    "que_mide": ("en cuantas de 5 semillas nuevas cada motor declara ley, para cada una de 25 "
                 "escalas y dos sistemas; y cuantas leyes declara cada motor sobre señal casi "
                 "constante, donde no hay ninguna que hallar"),
    "comparten_datos": {
        "hay": True,
        "porque": "los dos motores se corren sobre EXACTAMENTE las mismas trayectorias y las "
                  "mismas semillas — esa es la definicion de la comparacion. Si cada motor "
                  "tuviera sus propios datos, la diferencia podria ser de los datos.",
    },
    "linea_base": ("el ideal: 'el motor ve la ley siempre que exista, sin importar las unidades' "
                   "— 25 de 25 escalas en UN SOLO tramo. Se reporta la fraccion de escalas en que "
                   "ve y cuantos tramos contiguos hacen falta para describirla (Regla 11). La "
                   "linea base tonta interna del motor —el modelo que solo usa el termino "
                   "constante— vive dentro de sindy4 y no se mide aqui"),
    "formulas": [
        {"base": {"exponente": 0.0, "ruido_medida": 0.01}, "parametro": "ruido_medida",
         "factor": 200.0, "esperado": "baja",
         "porque": "el ruido de MEDIDA se suma a la trayectoria ya ocurrida, como el de un sensor: "
                   "entierra la señal sin cambiar la dinamica, luego con suficiente ruido no queda "
                   "ley que hallar y la cuenta tiene que caer. Es lo unico que se sabe A PRIORI "
                   "sobre esta medida. Base 0.01 y no 0.0, porque multiplicar cero por doscientos "
                   "sigue siendo cero y ese descuido ya me tumbo tres relaciones en un dia."},
        # AQUI DECLARE PRIMERO LA RELACION SOBRE `ruido_rel` —"subir el ruido del proceso baja la
        # cuenta"— Y LA RETIRO PORQUE ERA FALSA. El ruido de escala.py se añade DENTRO de la
        # integracion: no entierra la señal, la CONDUCE. La desviacion de la trayectoria sube de
        # 0.404 a 6.369 y la ley determinista sigue estando ahi; sindy4 la encuentra con margen
        # fuera de muestra de 0.71. Lo que la puerta midio como "x1.000" no era un fallo del
        # motor: era mi relacion inventada.
        # Y HAY MAS, que no me puedo callar: el prerregistro-46 declaro ESTA MISMA relacion falsa
        # y su Regla 31 la aprobo — pero por el motivo equivocado, porque sindy3 pierde la ley al
        # subir el ruido del proceso por FRAGILIDAD SUYA y no porque no hubiera ley que hallar.
        # Tercera vez que declaro una relacion metamorfica sin saberla de verdad a priori.
    ],
}


# ------------------------------------------------------------------ las medidas
def _ve(motor, sistema, exponente, semilla, ruido_rel=RUIDO_REL, ruido_medida=0.0):
    """¿Este motor declara ley sobre este sistema, a esta escala, con esta semilla?

    `ruido_rel` es ruido de PROCESO (dentro de la integracion: conduce el sistema y NO borra la
    ley). `ruido_medida` es ruido de SENSOR, sumado a la trayectoria ya ocurrida: ese si entierra
    la señal. Confundirlos fue el error de la enmienda 5."""
    x = SISTEMAS[sistema](semilla=semilla, ruido_rel=ruido_rel) * (10.0 ** float(exponente))
    if ruido_medida:
        rng = np.random.default_rng(int(semilla) + 31000)
        x = x + rng.normal(0, float(ruido_medida) * (10.0 ** float(exponente)), x.shape)
    return MOTORES[motor](x, dt=DT) is not None


def _metodo_medir(exponente=0.0, ruido_medida=0.0, motor="sindy3"):
    """PASO 1 — la medida escalar que la puerta comprueba: en cuantas de las 5 semillas ve.

    POR QUE EL MOTOR POR DEFECTO ES sindy3 Y NO sindy4. Este paso examina MI PROCEDIMIENTO DE
    MEDIDA, y para eso hace falta un motor que sea cantidad conocida. `sindy4` es el OBJETO DE
    ESTUDIO: si lo pusiera aqui, una propiedad suya bloquearia el modulo que existe para medirlo
    —el error exacto que dejo NULO al prerregistro-45— y ademas los criterios A y B ya no podrian
    reprobar. `sindy3` es el ancla: su comportamiento esta publicado y no es lo que se mide aqui."""
    return float(sum(1 for s in SEMILLAS
                     if _ve(motor, "oscilador", exponente, s, ruido_medida=ruido_medida)))


def _tramos(ve_por_escala):
    """Cuantos TRAMOS CONTIGUOS de 've' hay, y cuantas decadas cubre el mas largo. Un solo tramo
    es una banda —se rodea normalizando—; mas de uno son agujeros, que no se rodean."""
    ve = [c >= MINIMOS_VE for c in ve_por_escala]
    tramos, dentro, ini = [], False, 0
    for i, v in enumerate(ve):
        if v and not dentro:
            dentro, ini = True, i
        elif not v and dentro:
            dentro = False
            tramos.append((ini, i - 1))
    if dentro:
        tramos.append((ini, len(ve) - 1))
    decadas = max((EXPONENTES[b] - EXPONENTES[a] for a, b in tramos), default=0.0)
    return len(tramos), round(float(decadas), 2), tramos


def barrido(motor):
    """Criterios A y D — el barrido de 25 escalas en los dos sistemas."""
    out = {}
    for sistema in SISTEMAS:
        cuentas = [sum(1 for s in SEMILLAS if _ve(motor, sistema, e, s)) for e in EXPONENTES]
        n, dec, tr = _tramos(cuentas)
        out[sistema] = {"ve_por_escala": cuentas, "tramos": n, "decadas_tramo_mayor": dec,
                        "tramos_indices": tr}
    return out


def casi_constante(motor, semillas=SEMILLAS):
    """Criterios B y D — la señal sin dinamica. NO hay ley que hallar: cualquier ley declarada es
    una alucinacion. Cinco amplitudes por semilla, 25 casos, igual que el prerregistro-45."""
    declaradas, total = 0, 0
    for s in semillas:
        rng = np.random.default_rng(int(s) + 9000)
        for amplitud in (1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
            x = np.column_stack([np.full(escala.T, 1.5), np.zeros(escala.T)])
            x = x + rng.normal(0, amplitud, x.shape)
            total += 1
            if MOTORES[motor](x, dt=DT) is not None:
                declaradas += 1
    return {"leyes_declaradas": declaradas, "casos": total}


def no_rompimos_nada():
    """Criterio C — sindy4 tiene que encontrar lo que sindy3 encontraba y callar donde callaba.
    Se corre sobre los cuatro casos que sindy3 declara en SU Regla 31, que son los que definen
    'lo que funcionaba'."""
    rng = np.random.default_rng(47)
    X, dt = sindy3._oscilador()
    Xr, dtr = sindy3._oscilador(ruido=0.02)
    barajado = X[rng.permutation(len(X))]
    puro = rng.normal(size=(escala.T, 2))
    casos = {
        "oscilador_limpio": (lambda m: MOTORES[m](X, dt=dt), True),
        "oscilador_ruidoso": (lambda m: MOTORES[m](Xr, dt=dtr), True),
        "barajado": (lambda m: MOTORES[m](barajado, dt=dt), False),
        "ruido_puro": (lambda m: MOTORES[m](puro, dt=dt), False),
    }
    out = {}
    for nombre, (corre, debe_ver) in casos.items():
        v3, v4 = corre("sindy3"), corre("sindy4")
        es3 = sindy3._es_la_ley(v3) if debe_ver else (v3 is None)
        es4 = sindy4._es_la_ley(v4) if debe_ver else (v4 is None)
        out[nombre] = {"debe_ver": debe_ver, "sindy3": bool(es3), "sindy4": bool(es4),
                       "sindy4_conserva": bool(es4 or not es3)}
    return out


# ------------------------------------------------------------------ Regla 31: MI procedimiento
def _metodo_sanidad():
    """PASO 3 — ¿es legitima la comparacion, o la estoy amañando con el diseño?

    El peligro concreto: si el ruido fuera absoluto en vez de relativo, escalar la señal cambiaria
    la relacion señal/ruido y estariamos midiendo el RUIDO creyendo medir la ESCALA. Se comprueba
    que con ruido relativo la relacion es la misma en las 25 escalas."""
    fallos = []
    razones = []
    for e in (-3.0, 0.0, 3.0):
        x = escala.oscilador(semilla=43) * (10.0 ** e)
        razones.append(float(np.std(x) / (RUIDO_REL * (10.0 ** e))))
    if max(razones) - min(razones) > 0.01 * max(razones):
        fallos.append(f"la relacion señal/ruido CAMBIA con la escala {razones}: el estudio "
                      f"estaria midiendo el ruido y no la escala")
    # los dos motores reciben EXACTAMENTE la misma trayectoria: si no, la comparacion no vale
    a = escala.oscilador(semilla=43)
    b = escala.oscilador(semilla=43)
    if not np.array_equal(a, b):
        fallos.append("la generacion de trayectorias no es determinista: los dos motores no "
                      "estarian viendo los mismos datos y la comparacion no mediria el motor")
    return {"aprueba": not fallos, "fallos": fallos,
            "razones_senal_ruido": [round(r, 3) for r in razones]}


def regla31(verbose=True):
    """LA REGLA 31 DE ESTE MODULO — sobre MI PROCEDIMIENTO, los DOS lados, y NUNCA sobre el motor.

    NO se prueba aqui que sindy4 cierre los agujeros ni que calle sobre señal constante: eso es
    el RESULTADO que este estudio existe para medir. Meterlo aqui haria que los criterios A y B
    no pudieran reprobar nunca, que es el mal que ya cometi cuatro veces este mes."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-47: la medida, no el motor ==")

    # CONTROL POSITIVO (debe aprobar): a escala x1 el barrido tiene anclaje con el motor VIEJO.
    # Se usa sindy3 a proposito: si usara sindy4, el ancla dependeria de lo que quiero medir.
    v1 = _metodo_medir(exponente=0.0, motor="sindy3")
    caso("CONTROL POSITIVO: a escala x1 el barrido encuentra ley con sindy3 en 5 de 5",
         v1 == 5.0, f"{v1:.0f}/5")

    # SEÑUELO / CONTROL NEGATIVO (debe fallar): sobre ruido puro escalado igual, la medida no
    # puede declarar ley en ninguna escala. Si declarase, la medida estaria rota.
    rng = np.random.default_rng(4747)
    puro = rng.normal(size=(escala.T, 2))
    declara = sum(1 for e in (-3.0, -1.5, 0.0, 1.5, 3.0)
                  if sindy3.descubrir(puro * (10.0 ** e), dt=DT) is not None)
    caso("SEÑUELO: sobre ruido puro la medida no declara ley en ninguna escala",
         declara == 0, f"{declara} de 5 escalas")

    # LA MEDIDA RESPONDE AL RUIDO DE MEDIDA: es lo unico que se sabe a priori sobre ella.
    # De SENSOR, no de proceso: el de proceso conduce el sistema sin borrar la ley (enmienda 5).
    limpio = _metodo_medir(ruido_medida=0.01, motor="sindy3")
    sucio = _metodo_medir(ruido_medida=2.0, motor="sindy3")
    caso("la medida RESPONDE al ruido de sensor (con la señal enterrada, la cuenta cae)",
         sucio < limpio, f"limpio {limpio:.0f}/5 -> sucio {sucio:.0f}/5")

    # LA MEDIDA DISTINGUE MOTORES: si diera lo mismo con los dos, no podria comparar nada, y el
    # estudio entero seria un espejo. Se comprueba sobre el caso degenerado del INFORME-54, que
    # YA ESTA PUBLICADO y no es resultado de este estudio.
    x = np.column_stack([np.full(escala.T, 1.5), np.zeros(escala.T)])
    x = x + np.random.default_rng(4748).normal(0, 1e-4, x.shape)
    distintos = (sindy3.descubrir(x, dt=DT) is not None) != (sindy4.descubrir(x, dt=DT) is not None)
    caso("la medida DISTINGUE los dos motores (si no, no podria comparar)", distintos)

    # LA FICHA DE SANIDAD del paso 3
    fs = _metodo_sanidad()
    caso("la relacion señal/ruido es identica en las 25 escalas (se mide, no se supone)",
         fs["aprueba"], str(fs.get("razones_senal_ruido")))

    # EL CONTADOR DE TRAMOS, probado por los DOS lados sobre listas hechas a mano: si contara mal,
    # el criterio A seria basura y no lo sabriamos.
    uno, dec_uno, _ = _tramos([5] * 25)
    tres, _, _ = _tramos([5] * 5 + [0] * 3 + [5] * 5 + [0] * 3 + [5] * 9)
    cero, _, _ = _tramos([0] * 25)
    caso("el contador de tramos acierta por los dos lados",
         uno == 1 and tres == 3 and cero == 0 and dec_uno == 6.0,
         f"todo->{uno} ({dec_uno} dec) / agujeros->{tres} / nada->{cero}")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la medida es legitima."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


# ------------------------------------------------------------------ el estudio
def correr(salida=None, verbose=True):
    datos = {"prerregistro": 47, "semillas": list(SEMILLAS), "exponentes": EXPONENTES,
             "barrido": {}, "casi_constante": {}, "no_rompimos_nada": {}}
    for motor in ("sindy3", "sindy4"):
        if verbose:
            print(f"  barrido con {motor}...")
        datos["barrido"][motor] = barrido(motor)
        datos["casi_constante"][motor] = casi_constante(motor)
    datos["no_rompimos_nada"] = no_rompimos_nada()

    b4 = datos["barrido"]["sindy4"]
    b3 = datos["barrido"]["sindy3"]
    crit_a = all(v["tramos"] == 1 and v["decadas_tramo_mayor"] >= DECADAS_MINIMAS
                 for v in b4.values())
    crit_b = datos["casi_constante"]["sindy4"]["leyes_declaradas"] == 0
    crit_c = all(v["sindy4_conserva"] for v in datos["no_rompimos_nada"].values())
    crit_d = (any(v["tramos"] > 1 for v in b3.values())
              or datos["casi_constante"]["sindy3"]["leyes_declaradas"] > 0)
    datos["criterios"] = {"A_agujeros_cerrados": bool(crit_a), "B_alucinacion_muerta": bool(crit_b),
                          "C_no_rompimos_nada": bool(crit_c),
                          "D_el_defecto_es_del_motor": bool(crit_d)}

    if not crit_d:
        datos["veredicto"] = ("EL INFORME-55 ESTABA MAL — sindy3 no reproduce sus defectos sobre "
                              "las semillas nuevas, asi que el defecto era de las semillas")
    elif not crit_c:
        datos["veredicto"] = ("SE DESCARTA sindy4 — arregla la escala pero pierde leyes que "
                              "sindy3 encontraba; el prerregistro manda descartarlo entero")
    elif crit_a and crit_b:
        datos["veredicto"] = "ARREGLADO — los dos defectos desaparecen y no se rompio nada"
    elif crit_a or crit_b:
        datos["veredicto"] = ("ARREGLA UNO SOLO — " + ("cierra los agujeros pero sigue alucinando"
                                                       if crit_a else
                                                       "deja de alucinar pero siguen los agujeros"))
    else:
        datos["veredicto"] = ("NO ERA LA CAUSA — el corte adimensional no cierra los agujeros ni "
                              "mata la alucinacion; el umbral no era el problema")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 47: el arreglo del motor")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p47-arreglo/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
