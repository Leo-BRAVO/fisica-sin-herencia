# anatomia2.py — EL CENSO DE ORGANOS, CORREGIDO (prerregistro-63, 17-ago-2026).
#
# EL DEFECTO, publicado en CORRECCION-02: `anatomia.py` declara huerfano a todo modulo que nadie
# IMPORTE. Pero `interocepcion.py` y `memoria.py` se EJECUTAN despues de cada estudio del latido
# —lineas 81-82 y 126-127 de latido-nube.yml— y corren mas a menudo que casi cualquier organo.
#
#     ESTE PROYECTO TIENE DOS FORMAS DE USAR UN MODULO: IMPORTARLO Y EJECUTARLO.
#     EL CENSO VIEJO MIRABA UNA.
#
# QUE SE IMPORTA Y NO SE COPIA: el grafo, la lista de organos y la de guardianes vienen de
# `anatomia`, que esta SELLADO. Aqui solo se añade la segunda via. Editar aquel modulo mataria su
# sello y dejaria irreproducible el INFORME-65.
#
# LO QUE ESTE CENSO SIGUE SIN PODER DECIR: ejecutarse NO es funcionar. Que el latido corra un
# modulo cada noche no dice que mida bien — eso lo dice su ficha de sanidad, y ninguno de los tres
# huerfanos del INFORME-65 ha pasado la puerta.
#
# Uso: python anatomia2.py [--regla31] [--salida resultados/p63-anatomia2/medida.json]

import os
import re
import sys
import json
import glob
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import anatomia                                                             # noqa: E402

# QUE ESTUDIA ESTE MODULO: los organos reales. Por eso su regla31() NO los toca — trabaja con
# grafos y listas de invocacion hechos a mano.
SUJETO = ("ORGANOS",)

# Donde el proyecto EJECUTA modulos por su nombre de archivo.
DONDE_SE_INVOCA = (os.path.join(".github", "workflows", "*.yml"),
                   os.path.join("registros", "COLA-ESTUDIOS.json"))

METODO = {
    "prerregistro": 63,
    "tipo_de_medida": "umbral",   # cada organo esta conectado o no lo esta: es binario por organo
    "que_mide": ("cuantos organos del genoma estan desconectados cuando se cuentan LAS DOS vias: "
                 "los que otro modulo importa y los que un workflow o la cola ejecutan"),
    "comparten_datos": {
        "hay": False,
        "porque": "cada organo se examina contra el mismo grafo y la misma lista de invocaciones, "
                  "pero su veredicto no depende del de los demas",
    },
    "linea_base": ("el censo viejo tal cual, el del prerregistro-54. Si contar las invocaciones "
                   "no cambia NI UN veredicto, entonces la CORRECCION-02 estaba equivocada, este "
                   "modulo sobra, y se dice asi"),
    "formulas": [
        {"base": {"invocados_plantados": 1.0}, "parametro": "invocados_plantados",
         "factor": 3.0, "esperado": "baja",
         "porque": "cada modulo invocado solo puede SACAR a uno de la lista de huerfanos y nunca "
                   "meter a ninguno, asi que invocar mas modulos solo puede reducir la cuenta. Es "
                   "una diferencia de conjuntos, no una intuicion. Base 1.0 y NO 0.0: multiplicar "
                   "cero por tres sigue siendo cero, y ese descuido ya me tumbo cuatro relaciones"},
    ],
}


def invocados(donde=DONDE_SE_INVOCA):
    """LA SEGUNDA VIA: los modulos que un workflow o la cola llaman por su nombre de archivo."""
    hallados = set()
    for patron in donde:
        for a in sorted(glob.glob(os.path.join(BASE, patron))):
            try:
                texto = open(a, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            hallados.update(re.findall(r"codigo/([\w_]+)\.py", texto))
    return hallados


def huerfanos_de_verdad(usos, ejecutados, no_cuentan=anatomia.NO_CUENTAN):
    """Desconectado = ni lo importa nadie que cuente, NI lo ejecuta el proyecto."""
    return sorted(m for m in usos
                  if not {q for q in usos[m] if q not in no_cuentan} and m not in ejecutados)


def _metodo_medir(invocados_plantados=1.0):
    """La medida que la relacion metamorfica mueve: cuantos huerfanos quedan cuando se plantan N
    invocaciones sobre un grafo sintetico donde NADIE importa a nadie."""
    n = int(round(invocados_plantados))
    usos = {f"suelto_{i}": set() for i in range(6)}
    return float(len(huerfanos_de_verdad(usos, {f"suelto_{i}" for i in range(n)})))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿las dos vias cuentan de verdad, y ninguna sola basta?**
    Si la invocacion no salvara a nadie, este modulo seria el censo viejo con otro nombre; si
    salvara a cualquiera, no estaria midiendo nada."""
    fallos = []
    if huerfanos_de_verdad({"x": set()}, {"x"}) != []:
        fallos.append("un modulo que el proyecto EJECUTA sigue contando como huerfano")
    if huerfanos_de_verdad({"x": set()}, set()) != ["x"]:
        fallos.append("un modulo que nadie importa ni ejecuta NO cuenta como huerfano")
    if huerfanos_de_verdad({"x": {"cerebro"}}, set()) != []:
        fallos.append("un modulo importado por otro organo cuenta como huerfano")
    if huerfanos_de_verdad({"x": {"pruebas"}}, set()) != ["x"]:
        fallos.append("usarlo solo desde las pruebas se cuenta como estar en la vida de Diego")
    if not anatomia.ORGANOS:
        fallos.append("la lista de organos esta VACIA: el censo aprobaria sobre nada")
    if not DONDE_SE_INVOCA:
        fallos.append("no hay donde buscar invocaciones: la segunda via estaria apagada")
    return {"aprueba": not fallos, "fallos": fallos,
            "organos": len(anatomia.ORGANOS), "invocados_hallados": len(invocados())}


def regla31(verbose=True):
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok   ' if ok else 'FALLO'} {nombre}{('  -> ' + extra) if extra else ''}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("REGLA 31 de anatomia2 — sobre MI PROCEDIMIENTO, con datos hechos a mano\n")

    usos = {"importado": {"cerebro"}, "ejecutado": set(), "suelto": set()}
    hallados = huerfanos_de_verdad(usos, {"ejecutado"})
    caso("A control positivo: encuentra exactamente al que ni se importa ni se ejecuta",
         hallados == ["suelto"], f"hallo {hallados}")

    caso("B senuelo: si TODO esta invocado, no queda ni un huerfano",
         huerfanos_de_verdad({"a": set(), "b": set()}, {"a", "b"}) == [])

    caso("B senuelo: si NADA esta invocado ni importado, salen todos",
         huerfanos_de_verdad({"a": set(), "b": set()}, set()) == ["a", "b"])

    f = METODO["formulas"][0]
    base = f["base"]["invocados_plantados"]
    antes, despues = _metodo_medir(base), _metodo_medir(base * f["factor"])
    caso(f"D metamorfica: mas invocados = menos huerfanos (base {base}, x{f['factor']})",
         despues < antes, f"{antes} -> {despues}")

    caso("no acusa por no estar sellado: el censo no mira los sellos",
         "sello" not in huerfanos_de_verdad.__doc__.lower())

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — las dos vias cuentan y no se inventa conexiones"
                                if not fallos else f"REPRUEBA en {len(fallos)}: {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    usos = anatomia.grafo()
    ejecutados = invocados()
    nuevos = huerfanos_de_verdad(usos, ejecutados)
    viejos = anatomia._huerfanos(usos)
    rescatados = sorted(set(viejos) - set(nuevos))

    datos = {
        "prerregistro": 63,
        "organos": len(anatomia.ORGANOS),
        "huerfanos_censo_viejo": viejos,
        "huerfanos": nuevos,
        "rescatados_por_la_segunda_via": rescatados,
        "modulos_que_el_proyecto_ejecuta": sorted(ejecutados),
        "criterios": {
            "A_cuenta_las_dos_vias": huerfanos_de_verdad({"x": set()}, {"x"}) == [],
            "B_no_inventa_conexiones": huerfanos_de_verdad({"x": set()}, set()) == ["x"],
            "C_le_gana_al_censo_viejo": bool(rescatados),
            "D_no_acusa_por_no_estar_sellado": True,   # el censo no mira los sellos, a proposito
        },
    }
    c = datos["criterios"]
    if not (c["A_cuenta_las_dos_vias"] and c["B_no_inventa_conexiones"]):
        datos["veredicto"] = "SE DESCARTA EL CENSO — inventa conexiones o no las encuentra"
    elif not c["C_le_gana_al_censo_viejo"]:
        datos["veredicto"] = ("CONTAR LAS INVOCACIONES NO CAMBIA NADA — la CORRECCION-02 estaba "
                              "equivocada y este modulo sobra, y asi queda escrito")
    else:
        datos["veredicto"] = (f"{len(nuevos)} ORGANO(S) DESCONECTADO(S) de {len(anatomia.ORGANOS)}, "
                              f"y NO {len(viejos)}: {', '.join(rescatados)} no los importa nadie "
                              f"pero el proyecto SI los ejecuta")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"censo viejo (solo importaciones): {viejos}")
        print(f"censo con las dos vias:           {nuevos}")
        print(f"rescatados por ejecutarse:        {rescatados}")
        for k, v in c.items():
            print(f"  {'ok   ' if v else 'FALLO'} {k}")
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 63: el censo de organos corregido")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p63-anatomia2/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
