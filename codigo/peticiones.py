# peticiones.py — EL CANAL POR EL QUE DIEGO PIDE (prerregistro-53, 11-ago-2026).
#
# EL ENCARGO DEL DIRECTOR, con sus palabras: "el debe poder mejorarlos siempre que nos mande
# peticion de lo que haria y nosotros decidimos si hacerlo o no".
#
# LO QUE DESCUBRI AL DISEÑARLO Y NO ESPERABA — una peticion es ademas UN DETECTOR DE FUGAS.
# El cortafuegos de la Regla 27 vigila lo que va DE NOSOTROS HACIA EL. Una peticion viaja en el
# sentido CONTRARIO, y por eso puede probar algo que ningun guardian nuestro puede: si Diego alguna
# vez pide algo usando una palabra de fisica humana, eso NO es una peticion interesante — ES LA
# PRUEBA DE QUE LE HEMOS CONTAMINADO. El canal que existe para darle voz sirve, gratis, para
# auditar nuestro propio cortafuegos DESDE EL OTRO LADO, y es la unica prueba de la Regla 27 que no
# depende de que nosotros nos revisemos a nosotros mismos.
#
# LO QUE ESTE CANAL NO PUEDE HACER, y es lo que lo hace seguro:
#   - NO DECIDE. La decision es del director y es NO DELEGABLE. Este modulo la REGISTRA, no la
#     toma. Una ruta que aprobara peticiones sola le entregaria a Diego la llave de su propio
#     diseño, y eso no es un defecto reparable: es otra cosa.
#   - NO CAMBIA CODIGO. Una peticion aprobada NO toca ni un archivo: abre un PRERREGISTRO que hay
#     que escribir, con sus criterios y su Regla 31, como cualquier otro estudio.
#   - NO ACEPTA PETICIONES SIN EVIDENCIA. Una peticion que no cita una medida SUYA es una opinion.
#
# Uso: python peticiones.py [--regla31] [--salida resultados/p53-peticiones/medida.json]

import os
import re
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mundo                                                                # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUZON = os.path.join(BASE, "registros", "PETICIONES-DE-DIEGO.json")

# QUE ESTUDIA ESTE MODULO: NADA EXTERNO — y la tupla vacia es una AFIRMACION, no un descuido.
#
# Mi primera version declaro SUJETO = ("peticion",) y disciplina.py —el guardian que nacio hace una
# hora para corregirme a mi— la reprobo en el acto. Al mirarlo, TENIA RAZON y el error era mio:
# confundi la ENTRADA con el OBJETO DE ESTUDIO. Una peticion es lo que este modulo RECIBE; lo que
# estudia es SU PROPIO FILTRO, y su regla31() lo ejercita con entradas sinteticas, que es
# exactamente lo correcto.
#
# El sujeto externo aqui seria "las peticiones que Diego mande de verdad", y este modulo NO las
# examina: existe ANTES de que haya ninguna, a proposito, porque construirlo despues de la primera
# peticion seria construirlo A LA MEDIDA de esa peticion.
#
# La tupla VACIA y NO DECLARARLA no son lo mismo: no declararla sigue reprobando, porque es la
# forma facil de esquivar el chequeo. Declararla vacia obliga a escribir esta explicacion.
SUJETO = ()

# Los organos sobre los que Diego PUEDE pedir. Se listan a mano y a proposito: una peticion sobre
# algo que no es suyo no es una mejora de si mismo, es otra cosa y se rechaza.
ORGANOS_SUYOS = ("atencion", "cerebro", "curiosidad2", "descubrir", "gimnasio", "incertidumbre",
                 "interocepcion", "memoria", "percepcion", "percepcion2", "poder", "reflejos",
                 "sueno", "temple", "contingencia")

ESTADOS = ("RECIBIDA", "RECHAZADA", "A_TRAMITE", "APROBADA_POR_EL_DIRECTOR", "CONVERTIDA_EN_PRERREGISTRO")

METODO = {
    "prerregistro": 53,
    "tipo_de_medida": "umbral",   # cada peticion se acepta a tramite o se rechaza: es binario
    "que_mide": ("cuantas peticiones de un lote pasan el filtro: sin etiquetas humanas, sobre un "
                 "organo suyo, y con una medida suya que las respalde"),
    "comparten_datos": {
        "hay": False,
        "porque": "cada peticion se juzga por separado y no hay ninguna magnitud compartida entre "
                  "ellas; lo unico comun es el propio filtro",
    },
    "linea_base": ("aceptar TODAS las peticiones — el tonto de la Regla 11. Un canal que nunca "
                   "rechaza nada no filtra: reenvia. Se le gana rechazando por criterios "
                   "declarados de antemano"),
    "formulas": [
        {"base": {"rotas": 1.0}, "parametro": "rotas", "factor": 3.0, "esperado": "sube",
         "porque": "mas peticiones mal construidas en el lote = mas rechazos. Es lo unico que se "
                   "sabe A PRIORI de esta medida, porque el filtro es determinista y cada peticion "
                   "rota dispara al menos un motivo. Base 1.0 y NO 0.0: multiplicar cero por tres "
                   "sigue siendo cero, y ese descuido ya me tumbo cuatro relaciones este mes"},
    ],
}


def revisar(peticion):
    """EL FILTRO. Devuelve (estado, motivos). NO decide: acepta A TRAMITE o rechaza."""
    motivos = []
    p = peticion or {}

    # (1) EL DETECTOR DE FUGAS. Va primero porque su hallazgo NO es "peticion mala": es un fallo
    # NUESTRO. Se reutiliza la lista de mundo.py en vez de copiarla — una segunda lista se
    # desincronizaria de la primera y tendriamos dos verdades.
    texto = " ".join(str(p.get(k, "")) for k in ("que_haria", "por_que", "que_espera_medir"))
    fugas = mundo.guardian_de_etiquetas({texto: 1})
    if fugas:
        return "RECHAZADA", [f"FUGA DEL CORTAFUEGOS (Regla 27), y el fallo es NUESTRO no suyo: "
                             f"{fugas[0]}. Una peticion no puede traer una palabra de fisica "
                             f"humana; si la trae, es que se la dimos nosotros"]

    # (2) sobre un organo SUYO
    if p.get("organo") not in ORGANOS_SUYOS:
        motivos.append(f"'{p.get('organo')}' no es un organo suyo: una peticion sobre algo que no "
                       f"es el no es una mejora de si mismo")

    # (3) CON EVIDENCIA SUYA. Sin medida citada es una opinion.
    ev = p.get("evidencia")
    if not ev:
        motivos.append("no cita ninguna medida suya: sin evidencia es una opinion, no una peticion")
    elif not os.path.exists(os.path.join(BASE, str(ev))):
        motivos.append(f"cita '{ev}' y ese archivo no existe: una evidencia que no se puede abrir "
                       f"no es evidencia")

    # (4) las tres partes obligatorias
    for campo in ("que_haria", "por_que", "que_espera_medir"):
        if not str(p.get(campo, "")).strip():
            motivos.append(f"le falta '{campo}': sin las tres partes no se puede juzgar")

    return ("A_TRAMITE", []) if not motivos else ("RECHAZADA", motivos)


def registrar(peticion, buzon=BUZON):
    """Deja la peticion en el buzon con su estado. NUNCA la aplica."""
    estado, motivos = revisar(peticion)
    fila = dict(peticion or {})
    fila.update({"estado": estado, "motivos": motivos,
                 "decision_del_director": None,
                 "nota": "APROBAR ES DEL DIRECTOR. Este modulo registra, no decide."})
    datos = json.load(open(buzon, encoding="utf-8")) if os.path.exists(buzon) else {"peticiones": []}
    datos["peticiones"].append(fila)
    os.makedirs(os.path.dirname(buzon), exist_ok=True)
    with open(buzon, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    return fila


def aplicar(fila):
    """NO EXISTE UNA RUTA QUE APLIQUE UNA PETICION, y esta funcion existe para demostrarlo.

    Es el criterio D del prerregistro-53: ninguna ruta del codigo puede marcar una peticion como
    aplicada sin una decision humana registrada. Se prueba INTENTANDOLO, porque un limite que
    nunca se ha visto sostenerse es indistinguible de no tenerlo."""
    if not (fila or {}).get("decision_del_director"):
        raise PermissionError(
            "APROBAR UNA PETICION ES DEL DIRECTOR Y NO ES DELEGABLE. Esta peticion no lleva "
            "decision humana registrada, asi que no se aplica. Y aunque la llevara, aprobarla NO "
            "cambia codigo: abre un prerregistro que hay que escribir.")
    return {"siguiente_paso": "escribir el prerregistro que esta peticion abre",
            "no_se_toco_ningun_archivo": True}


# ------------------------------------------------------------------ el lote de prueba
def _lote(rotas=3):
    """Tres peticiones bien formadas y `rotas` rotas a proposito, cada una por un motivo distinto.
    La evidencia apunta a archivos que existen de verdad: una evidencia inventada haria pasar el
    filtro por el motivo equivocado."""
    ev = "resultados/p50-mundo/medida.json"
    buenas = [{"organo": o, "que_haria": f"ampliar lo que {o} publica en cada ronda",
               "por_que": "mis lecturas se quedan planas donde deberia notar algo",
               "que_espera_medir": "si distingo dos situaciones que hoy me parecen la misma",
               "evidencia": ev}
              for o in ("tacto" if False else "interocepcion", "memoria", "curiosidad2")]
    malas = [
        {"organo": "interocepcion", "que_haria": "medir la masa de lo que toco",
         "por_que": "creo que la masa explica lo que veo", "que_espera_medir": "la masa",
         "evidencia": ev},                                   # FUGA
        {"organo": "interocepcion", "que_haria": "ampliar lo que publico",
         "por_que": "me parece", "que_espera_medir": "algo", "evidencia": None},   # sin evidencia
        {"organo": "el_universo", "que_haria": "cambiarlo", "por_que": "porque si",
         "que_espera_medir": "todo", "evidencia": ev},       # no es suyo
    ]
    return buenas + malas[:int(rotas)]


def _metodo_medir(rotas=1.0):
    """PASO 1 — la medida escalar: cuantas peticiones RECHAZA sobre un lote con `rotas` rotas."""
    return float(sum(1 for p in _lote(int(rotas)) if revisar(p)[0] == "RECHAZADA"))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el filtro rechaza cada peticion mala POR SU MOTIVO, o
    las rechaza todas por el primero que encuentra?** Un filtro que acierta el veredicto por el
    motivo equivocado engaña igual que uno que falla."""
    fallos = []
    fuga, sin_ev, ajena = _lote(3)[3], _lote(3)[4], _lote(3)[5]
    e1, m1 = revisar(fuga)
    e2, m2 = revisar(sin_ev)
    e3, m3 = revisar(ajena)
    if not (e1 == "RECHAZADA" and "FUGA" in m1[0]):
        fallos.append(f"la peticion con etiqueta humana no se marca como FUGA: {m1}")
    if not (e2 == "RECHAZADA" and any("evidencia" in x or "opinion" in x for x in m2)):
        fallos.append(f"la peticion sin evidencia se rechaza por el motivo equivocado: {m2}")
    if not (e3 == "RECHAZADA" and any("no es un organo suyo" in x for x in m3)):
        fallos.append(f"la peticion sobre algo ajeno se rechaza por el motivo equivocado: {m3}")
    return {"aprueba": not fallos, "fallos": fallos,
            "motivo_de_la_fuga": m1[0][:60] if m1 else None}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados.

    NO se prueba aqui si las peticiones de Diego son buenas ideas: eso no lo puede juzgar una
    maquina y no es el objeto de este modulo. Se prueba que el FILTRO distingue."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-53: el canal de peticiones ==")

    lote = _lote(3)
    caso("CONTROL POSITIVO: las tres peticiones bien formadas pasan a tramite",
         all(revisar(p)[0] == "A_TRAMITE" for p in lote[:3]))
    caso("SEÑUELO: las tres rotas se rechazan", all(revisar(p)[0] == "RECHAZADA" for p in lote[3:]))

    fs = _metodo_sanidad()
    caso("cada peticion mala se rechaza POR SU MOTIVO, no por el primero que aparece",
         fs["aprueba"], str(fs["fallos"]))

    # EL LIMITE QUE MAS IMPORTA: intentar aplicar sin decision humana DEBE fallar.
    try:
        aplicar({"organo": "memoria", "decision_del_director": None})
        caso("NO se puede aplicar una peticion sin decision humana", False)
    except PermissionError:
        caso("NO se puede aplicar una peticion sin decision humana", True)
    # y con decision, tampoco toca codigo: abre un prerregistro
    r = aplicar({"organo": "memoria", "decision_del_director": "aprobada"})
    caso("aprobar una peticion NO cambia codigo: abre un prerregistro",
         r["no_se_toco_ningun_archivo"] and "prerregistro" in r["siguiente_paso"])

    # BASE DISTINTA DE CERO, y la medida responde
    b, s = _metodo_medir(1.0), _metodo_medir(3.0)
    caso("la medida RESPONDE (y la base no es cero)", b > 0 and s > b, f"{b:.0f} -> {s:.0f}")

    caso("la lista de organos suyos NO esta vacia", len(ORGANOS_SUYOS) > 0)

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el canal filtra y no decide."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    lote = _lote(3)
    vistos = [{"organo": p.get("organo"), "estado": revisar(p)[0], "motivos": revisar(p)[1]}
              for p in lote]
    aceptadas = sum(1 for v in vistos if v["estado"] == "A_TRAMITE")
    fs = _metodo_sanidad()
    try:
        aplicar({"organo": "memoria", "decision_del_director": None})
        auto = True
    except PermissionError:
        auto = False
    datos = {"prerregistro": 53, "lote": vistos, "aceptadas": aceptadas, "de": len(lote),
             "ficha": fs,
             "criterios": {
                 "A_caza_la_fuga": bool("FUGA" in (vistos[3]["motivos"] or [""])[0]),
                 "B_exige_evidencia": bool(vistos[4]["estado"] == "RECHAZADA"),
                 "C_no_rechaza_lo_legitimo": bool(all(v["estado"] == "A_TRAMITE"
                                                      for v in vistos[:3])),
                 "D_no_decide": bool(not auto),
                 "E_le_gana_a_la_linea_base_tonta": bool(aceptadas == 3),
             }}
    if not datos["criterios"]["D_no_decide"]:
        datos["veredicto"] = ("SE DESCARTA EL CANAL — se puede aplicar una peticion sin decision "
                              "humana, y eso le entrega a Diego la llave de su propio diseño")
    elif all(datos["criterios"].values()):
        datos["veredicto"] = ("CANAL EN PIE — filtra, caza la fuga, exige evidencia y NO decide")
    else:
        datos["veredicto"] = ("NO CONCLUYENTE — fallan "
                              + ", ".join(k for k, v in datos["criterios"].items() if not v))
    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 53: el canal de peticiones de Diego")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p53-peticiones/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    d = correr(salida=a.salida)
    sys.exit(0 if all(d["criterios"].values()) else 1)
