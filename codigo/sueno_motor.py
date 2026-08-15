# sueno_motor.py — PRERREGISTRO 48: ¿se recupera el organo del sueño con el motor nuevo?
#
# QUE MIDE. La ficha de sanidad que YA TIENE `sueno.py` —declarada en el prerregistro 43, no hoy—
# corrida con los dos motores sobre el mismo mundo y las mismas semillas. El criterio decisivo es
# el señuelo de escala del propio organo: "multiplicar el mundo por 10 no puede cambiar cuantas
# leyes pasan".
#
# LA PROPIEDAD MAS IMPORTANTE DE ESTE MODULO: yo no escribo el criterio. Estaba congelado desde el
# prerregistro 43 y reprobo el 10-ago-2026 (INFORME-50). Aqui se cambia el INSTRUMENTO y se vuelve
# a correr la MISMA prueba. No hay ningun umbral que yo pueda ajustar para que salga bien.
#
# LO QUE ESTE MODULO NO HACE: no cambia el motor por defecto de `sueno.py` —sigue siendo sindy3,
# de modo que el comportamiento del organo no cambia mientras este estudio corre— y no dice si
# sindy4 es buen motor: solo si este organo concreto se recupera.
#
# LA REGLA 31 DE ESTE ARCHIVO EXAMINA MI PROCEDIMIENTO, NO EL MOTOR NI EL ORGANO. Su control
# positivo es reproducir el REPROBADO ya publicado con sindy3: si mi montaje no lo reprodujera, no
# estaria midiendo lo mismo que el INFORME-50 y no habria nada que comparar.
#
# Uso: python sueno_motor.py [--regla31] [--salida resultados/p48-sueno/medida.json]

import os
import sys
import json
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sueno                                                                # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTORES = ("sindy3", "sindy4")

METODO = {
    "prerregistro": 48,
    "tipo_de_medida": "continua",
    "que_mide": ("cuantas leyes soñadas sobreviven al filtro de vigilia, con cada motor, y si el "
                 "señuelo de escala del propio organo (mundo x1 contra mundo x10) da el mismo "
                 "numero. El criterio viene del prerregistro 43 y no se toca aqui"),
    "comparten_datos": {
        "hay": True,
        "porque": "los dos motores se corren sobre EXACTAMENTE el mismo mundo y las mismas "
                  "semillas — esa es la definicion de la comparacion. Si cada motor tuviera su "
                  "propio mundo, la diferencia podria ser del mundo.",
    },
    "linea_base": ("la que ya tiene el organo desde el prerregistro 43: soñar sobre un modelo "
                   "ajustado a RUIDO PURO. Cuantas leyes sobreviven al filtro alli es el suelo y "
                   "debe ser cero, con los dos motores"),
    "formulas": [
        {"base": {"estructura": 1.0}, "parametro": "estructura", "factor": 0.0, "esperado": "baja",
         "porque": "sin estructura en el mundo vivido no hay ley que soñar que coincida con la "
                   "vigilia, luego la cuenta que sobrevive al filtro tiene que caer. Es lo unico "
                   "que se sabe A PRIORI sobre esta medida. La base es estructura=1.0, que da una "
                   "lectura distinta de cero: comparar un cero con otro cero no prueba nada, y ese "
                   "descuido ya me tumbo tres relaciones en un dia."},
    ],
}


def _metodo_medir(estructura=1.0, motor="sindy3"):
    """PASO 1 — la medida escalar: cuantas leyes soñadas sobreviven al filtro, con ese motor.

    POR QUE EL MOTOR POR DEFECTO ES sindy3: este paso examina MI PROCEDIMIENTO, y para eso hace
    falta el motor cuyo comportamiento ya esta publicado. sindy4 es parte de lo que se mide."""
    return float(sueno._metodo_medir(estructura=float(estructura), ruido=0.02, motor=motor))


def _linea_base_ruido(motor):
    """La linea base tonta del prerregistro 43: soñar sobre un modelo ajustado a RUIDO PURO."""
    rng = np.random.default_rng(48)
    eps = [rng.normal(size=(4000, 2)) for _ in range(5)]
    modelo = sueno._modelo_del_mundo(eps)
    suenos = sueno.sonar_episodios(modelo, eps[0], semilla=48)
    return len(sueno.mineria_en_suenos(suenos, dt=sueno.DT_JUGUETE, motor=motor))


def _metodo_sanidad():
    """PASO 3 — ¿es legitima la comparacion? El peligro concreto: que los dos motores no esten
    viendo el mismo mundo, en cuyo caso la diferencia seria del mundo y no del motor."""
    fallos = []
    a = sueno._mundo_soñable(estructura=1.0, ruido=0.02)
    b = sueno._mundo_soñable(estructura=1.0, ruido=0.02)
    if not all(np.array_equal(x, y) for x, y in zip(a, b)):
        fallos.append("el mundo de juguete NO es determinista: los dos motores no verian los "
                      "mismos datos y la comparacion no mediria el motor")
    if sueno.DT_JUGUETE != 0.02:
        fallos.append(f"el dt del juguete cambio a {sueno.DT_JUGUETE}: el organo integra a 0.02 y "
                      f"medirlo con otro paso fue un error real de este mismo modulo")
    return {"aprueba": not fallos, "fallos": fallos, "dt": sueno.DT_JUGUETE}


def regla31(verbose=True):
    """LA REGLA 31 DE ESTE MODULO — sobre MI PROCEDIMIENTO, los DOS lados, y nunca sobre sindy4.

    NO se prueba aqui que sindy4 arregle el señuelo de escala: eso es el RESULTADO. Meterlo aqui
    haria que el estudio no pudiera reprobar, que es el mal que ya cometi cinco veces este mes."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-48: la comparacion, no el motor ==")

    # CONTROL POSITIVO (debe aprobar): con sindy3 hay que REPRODUCIR el REPROBADO ya publicado.
    # Si no se reprodujera, mi montaje no mide lo mismo que el INFORME-50 y no hay comparacion.
    f3 = sueno._metodo_sanidad(motor="sindy3")
    escala_rota = any("ESCALA" in x for x in f3["fallos"])
    caso("CONTROL POSITIVO: con sindy3 se reproduce el REPROBADO por escala del INFORME-50",
         escala_rota, f"x1={f3.get('sin_escalar')} x10={f3.get('escalado_x10')}")

    # SEÑUELO / CONTROL NEGATIVO (debe fallar): la linea base tonta debe dar CERO con los dos.
    base = {m: _linea_base_ruido(m) for m in MOTORES}
    caso("SEÑUELO: soñar sobre un modelo de RUIDO PURO da 0 leyes con los dos motores",
         all(v == 0 for v in base.values()), str(base))

    # LA MEDIDA RESPONDE A LA ESTRUCTURA, que es lo unico que se sabe a priori. Base != 0.
    con = _metodo_medir(estructura=1.0, motor="sindy3")
    sin = _metodo_medir(estructura=0.0, motor="sindy3")
    caso("la medida RESPONDE a la estructura del mundo (y la base no es cero)",
         con > 0 and sin < con, f"estructura 1 -> {con:.0f} / estructura 0 -> {sin:.0f}")

    # LA FICHA del paso 3: los dos motores ven el mismo mundo
    fs = _metodo_sanidad()
    caso("los dos motores reciben EXACTAMENTE el mismo mundo", fs["aprueba"], str(fs["fallos"]))

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la comparacion es legitima."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    datos = {"prerregistro": 48, "criterio_viene_de": "prerregistro-43, no se toca aqui",
             "ficha": {}, "linea_base_ruido": {}}
    for m in MOTORES:
        if verbose:
            print(f"  ficha de sanidad con {m}...")
        f = sueno._metodo_sanidad(motor=m)
        datos["ficha"][m] = {"aprueba": bool(f["aprueba"]), "fallos": list(f["fallos"]),
                             "sin_escalar": f.get("sin_escalar"),
                             "escalado_x10": f.get("escalado_x10"),
                             "escala_ok": f.get("sin_escalar") == f.get("escalado_x10")}
        datos["linea_base_ruido"][m] = _linea_base_ruido(m)

    f4 = datos["ficha"]["sindy4"]
    base_cero = (f4["sin_escalar"] == 0 and f4["escalado_x10"] == 0)
    if base_cero:
        datos["veredicto"] = ("NO CONCLUYENTE POR INSTRUMENTO — con sindy4 la lectura base es 0 "
                              "leyes, asi que no hay nada que comparar")
    elif f4["aprueba"]:
        datos["veredicto"] = ("RECUPERADO — con sindy4 la ficha de sanidad aprueba entera y el "
                              "señuelo de escala da el mismo numero con el mundo x1 y x10")
    elif not f4["escala_ok"]:
        datos["veredicto"] = ("SIGUE REPROBADO POR LA ESCALA — la causa no era sindy3 y mi "
                              "diagnostico estaba equivocado")
    else:
        datos["veredicto"] = ("CAMBIA DE DEFECTO — el señuelo de escala pasa pero la ficha "
                              "reprueba por otra cosa que el primer defecto tapaba")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 48: el sueño con el motor nuevo")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p48-sueno/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
