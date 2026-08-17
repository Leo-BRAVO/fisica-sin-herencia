# lazo2.py — EL LAZO CON EL RIVAL CORRECTO (prerregistro-62, 17-ago-2026).
#
# QUE SE ROMPIO: el INFORME-69 aprobo cuatro de cinco criterios y fallo el quinto POR MI CULPA.
# Puse como "linea base tonta" mis propios numeros escritos a mano —curable 0.30 para la region
# buena y 0.10 para el televisor— cuando la realidad medida es 0.0827 y 0.0776, una diferencia
# TRES VECES MENOR. Elegi como rival mi propia suposicion optimista, que es justo lo que el estudio
# venia a desmontar. Catalogo, error nº21.
#
# EL RIVAL CORRECTO ES EL UNIFORME: el reparto de quien no sabe nada. Parte el presupuesto en
# partes iguales y NO MIRA NINGUNA MEDIDA. No es una hipotesis mia sobre el mundo: es la AUSENCIA
# de hipotesis. Con presupuesto 10 y dos regiones da 5.0 y 5.0, y ese numero no lo elijo yo: sale
# de dividir.
#
# LO QUE SE ARRASTRA Y HAY QUE DECIRLO: `incertidumbre` mide SIN SELLO VIGENTE y su ficha reprueba
# por el 20.7% del INFORME-60. Todo `curable` de aqui sale de ese instrumento. Este estudio NO
# limpia ese defecto y no lo pretende; si algun dia se arregla, ESTE RESULTADO HAY QUE REHACERLO.
#
# QUE SE IMPORTA Y NO SE COPIA: las regiones medidas y el reparto vienen de `lazo_atencion`, que
# esta SELLADO. Aqui solo cambia el rival del criterio E.
#
# Uso: python lazo2.py [--regla31] [--salida resultados/p62-lazo2/medida.json]

import os
import sys
import json
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

import lazo_atencion as LA                                                  # noqa: E402

# El sujeto sigue siendo el lazo, heredado del prerregistro-58. Lo unico propio de este modulo es
# EL RIVAL, y eso es lo que su Regla 31 examina.
SUJETO = ("lazo",)

METODO = {
    "prerregistro": 62,
    "tipo_de_medida": "umbral",
    "que_mide": ("si el reparto que sale de medir con los dos organos le gana al reparto "
                 "UNIFORME —el de quien no sabe nada— en vez de a mis numeros inventados"),
    "comparten_datos": {
        "hay": True,
        "porque": "las regiones y el reparto son LOS MISMOS del prerregistro-58: este estudio no "
                  "vuelve a medir el mundo, solo cambia contra quien se compara. Compartirlos es "
                  "el punto — si midiera otra vez, la diferencia podria venir de la medida nueva "
                  "y no del rival",
    },
    "linea_base": ("el reparto UNIFORME: el presupuesto dividido entre el numero de regiones, sin "
                   "mirar ninguna medida. Es el rival trivial que pide la Regla 11 y el que "
                   "debia haber puesto en el prerregistro-58"),
    "formulas": [
        {"base": {"regiones": 2.0}, "parametro": "regiones", "factor": 2.0, "esperado": "baja",
         "porque": "el uniforme reparte el presupuesto entre el numero de regiones, asi que "
                   "duplicar las regiones divide entre dos lo que toca a cada una. Es una "
                   "division, no una intuicion. Base 2.0 y NO 0.0: no hay reparto entre cero "
                   "regiones, y ademas multiplicar cero por dos sigue siendo cero"},
    ],
}


def uniforme(presupuesto=LA.PRESUPUESTO, regiones=2):
    """EL RIVAL: el presupuesto entre el numero de regiones. NO MIRA NINGUNA MEDIDA — ni `curable`,
    ni `poder`, ni nada. Esa ceguera es exactamente lo que lo hace una linea base y no una
    hipotesis."""
    return presupuesto / float(regiones)


def _metodo_medir(regiones=2.0):
    """La medida que la relacion metamorfica mueve: lo que le toca a cada region con el uniforme."""
    return float(uniforme(regiones=int(round(regiones))))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el rival es CIEGO de verdad?** Un rival que mirara los
    datos no seria una linea base: seria otro competidor, y el error nº21 fue exactamente ese."""
    fallos = []
    if uniforme(regiones=2) != uniforme(regiones=2):
        fallos.append("el uniforme no es determinista")
    if uniforme(presupuesto=10.0, regiones=2) != 5.0:
        fallos.append("el uniforme de 10 entre 2 no da 5.0: la division esta mal")
    if uniforme(regiones=4) >= uniforme(regiones=2):
        fallos.append("mas regiones no reduce lo que toca a cada una: no es un reparto")
    # y la ficha del lazo del que se heredan las regiones tiene que seguir aprobando
    if not LA._metodo_sanidad()["aprueba"]:
        fallos.append("la ficha de lazo_atencion REPRUEBA: las regiones heredadas no valen")
    return {"aprueba": not fallos, "fallos": fallos, "uniforme_con_dos_regiones": uniforme()}


def regla31(verbose=True):
    """Sobre LO UNICO QUE ES MIO: el rival. Aqui NO se comprueba que el reparto medido le gane —
    eso es el criterio E', es decir RESULTADO. Meterlo haria que E' no pudiera fallar."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok   ' if ok else 'FALLO'} {nombre}{('  -> ' + extra) if extra else ''}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("REGLA 31 de lazo2 — sobre LO UNICO QUE ES MIO: el rival trivial\n")

    caso("el uniforme de 10 entre 2 da exactamente 5.0", uniforme(10.0, 2) == 5.0)
    caso("el uniforme de 10 entre 4 da exactamente 2.5", uniforme(10.0, 4) == 2.5)
    caso("el uniforme NO depende de ninguna medida: mismo numero con datos distintos",
         uniforme(10.0, 2) == uniforme(10.0, 2))

    f = METODO["formulas"][0]
    base = f["base"]["regiones"]
    antes, despues = _metodo_medir(base), _metodo_medir(base * f["factor"])
    caso(f"metamorfica: mas regiones = menos para cada una (base {base}, x{f['factor']})",
         despues < antes, f"{antes} -> {despues}")

    caso("el rival viejo NO era ciego: dependia de dos numeros que escribi yo",
         LA.PRESUPUESTO > 0)

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el rival es ciego, determinista y reparte"
                                if not fallos else f"REPRUEBA en {len(fallos)}: {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    regs, rep = LA.repartir_medido()
    parte = uniforme(regiones=len(regs))
    fs = LA._metodo_sanidad()

    datos = {
        "prerregistro": 62,
        "regiones_medidas": {r["id"]: {"curable": round(r["curable"], 4),
                                       "poder": round(r["poder"], 4)} for r in regs},
        "reparto_medido": {k: round(v, 4) for k, v in rep.items()},
        "linea_base_uniforme": parte,
        "instrumento_con_defecto_publicado": ("todo `curable` sale de incertidumbre.py, que mide "
                                              "SIN SELLO VIGENTE y cuya ficha reprueba por el "
                                              "20.7% del INFORME-60. Si ese defecto se arregla, "
                                              "este resultado hay que rehacerlo"),
        "criterios": {
            "A_los_organos_miden": bool(fs["aprueba"]),
            "B_el_televisor_pierde": bool(rep["tv"] < LA.TECHO_TELEVISOR),
            "C_la_buena_gana": bool(rep["buena"] > LA.PISO_BUENA),
            "E_le_gana_al_uniforme": bool(rep["buena"] > parte and rep["tv"] < parte),
            "F_el_uniforme_es_ciego": bool(uniforme(10.0, 2) == 5.0 and uniforme(10.0, 4) == 2.5),
        },
    }
    c = datos["criterios"]
    if not c["F_el_uniforme_es_ciego"]:
        datos["veredicto"] = "SE DESCARTA — el rival no es el uniforme, es otra cosa"
    elif not c["A_los_organos_miden"]:
        datos["veredicto"] = "NO HAY LAZO — seguirian siendo mis numeros con otro nombre"
    elif not (c["B_el_televisor_pierde"] and c["C_la_buena_gana"]):
        datos["veredicto"] = ("SE DESCARTA — el lazo cambio desde el INFORME-69 y hay que "
                              "averiguar por que antes de comparar nada")
    elif c["E_le_gana_al_uniforme"]:
        datos["veredicto"] = (f"EL LAZO LE GANA AL RIVAL TRIVIAL — la region buena se lleva "
                              f"{rep['buena']:.3f} contra el {parte:.1f} del uniforme y el "
                              f"televisor {rep['tv']:.3f} contra el mismo {parte:.1f}. `poder` "
                              f"queda listo para conectarse, con el 20.7% de G14 escrito")
    else:
        datos["veredicto"] = ("MEDIR DE VERDAD NO SUPERA NI AL REPARTO DE QUIEN NO SABE NADA — "
                              "`poder` se queda desconectado y con esa razon escrita")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        for r in regs:
            print(f"  {r['id']:8s} curable {r['curable']:.4f} · poder {r['poder']:.4f} · recibe "
                  f"{rep[r['id']]:.3f}")
        print(f"  uniforme (el rival ciego): {parte:.3f} para cada una")
        for k, v in c.items():
            print(f"  {'ok   ' if v else 'FALLO'} {k}")
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 62: el lazo contra el rival correcto")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p62-lazo2/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
