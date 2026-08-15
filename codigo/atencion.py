# atencion.py — GEN G8: LA ATENCIÓN — elegir solo importa cuando no puedes con todo.
# Construido el 8-ago-2026 por orden del director. REPARTE UN PRESUPUESTO, NO ELIGE OBJETIVOS:
# qué estudiar lo sigue diciendo la curiosidad (G2); la atención dice CUÁNTO de un presupuesto
# finito recibe cada frente. Sin escasez no hay atención — un bebé tiene fóvea estrecha y
# memoria de trabajo de 3-4 ítems, y ESA restricción es la que lo obliga a elegir bien.
#
# LA ECUACIÓN (compuesta de genes ya validados, no inventada aquí):
#
#     prioridad(region) = epistemica(region) · max(poder(region), piso)
#     reparto            ∝ prioridad, con cuota mínima de exploración
#
#   · epistemica (G14): ignorancia CURABLE — donde más se puede aprender.
#   · poder (G13): control real — donde además se puede INTERVENIR para aprender más rápido
#     (la lección del INFORME-30: mirar no basta; el que puede empujar, desambigua).
#   · La ALEATORIA no entra: gastar fóvea en azar es el televisor ruidoso. Ese canal queda
#     cerrado por construcción, no por parche.
#
# Regla 31: el televisor (varianza máxima, todo aleatorio) debe recibir ~cuota mínima; la región
# curable-y-controlable debe recibir la mayor parte; y con presupuesto sobrado NO se inventa
# escasez (todo recibe lo que necesita).

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# EL CONTRATO DE ESTE CONSUMIDOR (prerregistro-49). G8 se creyo una epistemica inflada de G14 sin
# comprobar nada, y esa es la causa REAL del INFORME-52: no un nombre malo ni una metafora
# biologica, sino UNA INTERFAZ SIN CONTRATO. Desde aqui, lo que se consume se verifica.
CONTRATO = {
    "tipo": "POLITICA",
    "consume": {"curable": {"de": "incertidumbre.py", "rango": [0.0, 1.0],
                            "porque": "es una FRACCION adimensional. La `epistemica` cruda es una "
                                      "magnitud que sube con el ruido (INFORME-51), y consumirla "
                                      "para decidir donde mirar es lo que compro el televisor"}},
}


def _ignorancia(region):
    """Lo que G8 usa para priorizar, CON su rango verificado. Prefiere la fraccion `curable` de
    G14; si una region solo trae la `epistemica` cruda, se acepta por compatibilidad pero se sabe
    que es la lectura contaminada por el ruido."""
    if "curable" in region:
        v = float(region["curable"])
        lo, hi = CONTRATO["consume"]["curable"]["rango"]
        if not (lo <= v <= hi):
            raise ValueError(f"CONTRATO ROTO: la region {region.get('id')} publica curable={v}, "
                             f"fuera del rango {[lo, hi]} declarado por incertidumbre.py")
        return v
    return float(region["epistemica"])


def repartir(regiones, presupuesto, cuota_exploracion=0.05, piso_poder=0.0):
    """regiones: [{'id', 'epistemica', 'aleatoria', 'poder', 'coste'}]. Devuelve el reparto.
    'coste' = lo que consumiría atender la región del todo. Si el presupuesto alcanza para
    todos los costes, se asigna completo (la escasez no se finge)."""
    total_coste = sum(r["coste"] for r in regiones)
    if presupuesto >= total_coste:
        return [{"id": r["id"], "asignado": r["coste"], "fraccion": 1.0,
                 "nota": "sin escasez: atencion plena"} for r in regiones]
    # EL PISO ERA LA FUGA. Valia 0.05, asi que una region con poder CERO puntuaba 0.05 y con la
    # epistemica del televisor x20 se llevaba 7.036 de 10 (INFORME-52). Ahora vale 0.0: una region
    # sobre la que NO SE PUEDE HACER NADA puntua exactamente cero. Eso es EMPOWERMENT — preferir
    # los estados desde los que tus acciones tienen efecto—, y un televisor con ruido tiene mucha
    # sorpresa y empowerment cero, asi que no puede secuestrar la atencion POR CONSTRUCCION.
    # Y quitarlo no ciega a nadie: la `cuota_exploracion` de abajo ya reserva un trozo del
    # presupuesto repartido por igual. El piso era redundante con ella; lo unico que añadia era
    # premiar lo intocable.
    prioridad = np.array([_ignorancia(r) * max(r["poder"], piso_poder) for r in regiones])
    if prioridad.sum() <= 0:
        prioridad = np.ones(len(regiones))
    # DOS PRESUPUESTOS CON DOS CRITERIOS (enmienda 1 del prerregistro-49, escrita antes de correr
    # porque LA PUERTA cazo el problema antes de que existiera un dato).
    # Con empowerment PURO, toda region de poder cero puntua cero, asi que una region donde SI hay
    # algo real que aprender pero no se puede tocar y EL TELEVISOR reciben exactamente lo mismo.
    # La Regla 31 de este modulo, congelada en el prerregistro-43, exige lo contrario: "mirar aun
    # vale algo". Y esa exigencia no es opinion: el prerregistro-32 midio que la fisica de soporte
    # NO NECESITA CUERPO, o sea que la observacion pasiva construye modelo.
    # Por eso la cuota de exploracion deja de repartirse POR IGUAL y se reparte EN PROPORCION A LA
    # IGNORANCIA CURABLE. El televisor no se cuela por ahi: su ignorancia es ALEATORIA, no curable,
    # asi que su `curable` es bajo por construccion. Lo que se recupera es la distincion entre
    # "intocable pero informativo" y "ruido", que el empowerment puro borraba.
    ign = np.array([_ignorancia(r) for r in regiones], dtype=float)
    pesos_expl = ign / ign.sum() if ign.sum() > 0 else np.ones(len(regiones)) / len(regiones)
    bolsa_expl = cuota_exploracion * presupuesto
    resto = presupuesto - bolsa_expl
    pesos = prioridad / prioridad.sum()
    out = []
    for r, w, we in zip(regiones, pesos, pesos_expl):
        asignado = min(bolsa_expl * we + resto * w, r["coste"])
        out.append({"id": r["id"], "asignado": round(float(asignado), 4),
                    "fraccion": round(float(asignado / r["coste"]), 4)})
    return out


# ==========================================================================================
# LA PUERTA (metodo.py) — 10-ago-2026, prerregistro-43
# ==========================================================================================
# G8 decide DONDE MIRA DIEGO, y su prioridad es `epistemica * poder`. El 10-ago se midio que la
# epistemica que G14 le entrega **sube con el ruido** (INFORME-51): una region imposible de
# aprender le llega inflada. La pregunta que la ficha de abajo contesta es la unica que importa
# aqui: **¿el factor `poder` alcanza para proteger el reparto de una epistemica inflada?**
# Si no alcanzara, el defecto de G14 se convertiria en conducta — Diego mirando el televisor.
METODO = {
    "prerregistro": 43,
    "tipo_de_medida": "continua",
    "que_mide": ("que fraccion del presupuesto se lleva la region BUENA frente al TELEVISOR, "
                 "cuando los dos compiten por la misma atencion"),
    "comparten_datos": {
        "hay": False,
        "porque": "cada region trae sus propios numeros (epistemica, aleatoria, poder, coste) "
                  "medidos por otros organos. El reparto no vuelve a mirar los datos: solo "
                  "combina lo que le entregan, y por eso hereda lo que le entreguen mal.",
    },
    "linea_base": ("repartir POR IGUAL entre las regiones — el tonto de la Regla 11 para un "
                   "asignador. Si no le gana, no esta priorizando: esta repartiendo"),
    "formulas": [
        # BASE 0.05 Y NO 0.0: la version del prerregistro-43 ponia base 0.0 y factor 20, y
        # multiplicar cero por veinte sigue siendo cero — la puerta lo midio x1.000. Es la trampa
        # de la base nula, la cuarta vez en un mes que aparece en este repositorio.
        {"base": {"poder_tv": 0.05, "epistemica_tv": 5.0}, "parametro": "poder_tv", "factor": 20.0,
         "esperado": "baja",
         "porque": "si el televisor pasa a ser CONTROLABLE deja de ser televisor: es una region "
                   "legitima y debe llevarse mas presupuesto, luego la ventaja de la buena baja. "
                   "Desigualdad y no proporcion: el reparto es una normalizacion, no una funcion "
                   "cerrada"},
        {"base": {"poder_tv": 0.0, "epistemica_tv": 5.0}, "parametro": "epistemica_tv",
         "factor": 20.0, "esperado": "igual",
         "porque": "**ESTE ES EL CASO QUE IMPORTA.** Inflar la epistemica del televisor x20 —que "
                   "es lo que G14 hace con las regiones ruidosas— NO puede cambiar el reparto, "
                   "porque su poder es cero y el producto sigue siendo cero. Si cambiara, el "
                   "defecto de G14 se convertiria en conducta"},
    ],
}


def _dos_regiones(poder_tv=0.0, epistemica_tv=5.0, presupuesto=10.0):
    """Un televisor (mucha 'ignorancia', ningun control) contra una region buena."""
    return [{"id": "tv", "epistemica": float(epistemica_tv), "aleatoria": 5.0,
             "poder": float(poder_tv), "coste": presupuesto},
            {"id": "buena", "epistemica": 0.8, "aleatoria": 0.1, "poder": 0.5,
             "coste": presupuesto}]


def _metodo_medir(poder_tv=0.0, epistemica_tv=5.0):
    """PASO 1 — la medida escalar: cuanto se lleva la BUENA por cada unidad que se lleva el TV."""
    regs = _dos_regiones(poder_tv=poder_tv, epistemica_tv=epistemica_tv)
    r = {x["id"]: x["asignado"] for x in repartir(regs, presupuesto=10.0)}
    return float(r["buena"] / max(r["tv"], 1e-9))


def _metodo_sanidad():
    """PASO 3 — LA FICHA, y aqui la pregunta no es sobre el instrumento sino sobre la CADENA:
    **¿el defecto medido de G14 se propaga hasta la conducta de Diego?**

    Se infla la epistemica del televisor por un factor creciente —imitando exactamente lo que G14
    entrega en una region ruidosa— y se comprueba que el reparto NO se mueve. La proteccion es el
    factor `poder`: no se puede aprender de lo que no se puede tocar.
    """
    fallos = []
    base = _metodo_medir(epistemica_tv=1.0)
    for factor in (2.0, 10.0, 100.0, 1000.0):
        v = _metodo_medir(epistemica_tv=factor)
        if abs(v - base) > 1e-6:
            fallos.append(f"CONTAGIO DESDE G14: inflando la epistemica del televisor x{factor:g} "
                          f"la ventaja de la region buena pasa de {base:.4f} a {v:.4f}")
            break
    # Y la linea base tonta: repartir por igual daria ventaja 1.0. Hay que ganarle.
    if base <= 1.0:
        fallos.append(f"no le gana al reparto por igual (ventaja {base:.4f}, el tonto da 1.0)")
    return {"aprueba": not fallos, "fallos": fallos,
            "ventaja_de_la_buena": round(base, 4),
            "linea_base_tonta_repartir_por_igual": 1.0}


def regla31(verbose=True):
    fallos = []
    regiones = [
        {"id": "curable_y_controlable", "epistemica": 0.8, "aleatoria": 0.1, "poder": 0.6, "coste": 10},
        {"id": "curable_sin_control",   "epistemica": 0.8, "aleatoria": 0.1, "poder": 0.0, "coste": 10},
        {"id": "televisor",             "epistemica": 0.05, "aleatoria": 2.0, "poder": 0.0, "coste": 10},
        {"id": "ya_aprendida",          "epistemica": 0.02, "aleatoria": 0.1, "poder": 0.7, "coste": 10},
    ]
    rep = {r["id"]: r["asignado"] for r in repartir(regiones, presupuesto=12)}
    c1 = rep["curable_y_controlable"] == max(rep.values())
    c2 = rep["televisor"] < rep["curable_y_controlable"] * 0.25
    c3 = rep["curable_sin_control"] > rep["televisor"]      # mirar sin manos > mirar ruido
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} la región curable Y controlable recibe lo máximo ({rep})")
        print(f"  {'ok  ' if c2 else 'FALLO'} el televisor recibe migajas aunque tenga la varianza máxima")
        print(f"  {'ok  ' if c3 else 'FALLO'} curable-sin-control > televisor (mirar aún vale algo)")
    for c, n in ((c1, "maximo"), (c2, "televisor"), (c3, "orden")):
        if not c:
            fallos.append(n)

    rep2 = repartir(regiones, presupuesto=100)
    c4 = all(r["fraccion"] == 1.0 for r in rep2)
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} con presupuesto sobrado NO finge escasez (todos al 100%)")
    if not c4:
        fallos.append("escasez_fingida")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la fóvea va donde se aprende y se puede actuar."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G8: atención — reparto de presupuesto finito")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (su cableado real a las corridas lo define un prerregistro)")
