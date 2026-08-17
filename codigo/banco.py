# banco.py — EL CARRIL RAPIDO (crítica externa 01, item 29; 11-ago-2026).
#
# POR QUE EXISTE, y nace de una critica al proyecto que es en parte acertada: "la burocracia
# interna del codigo ha comenzado a frenar la velocidad de experimentacion".
#
# DONDE LA CRITICA NO TIENE RAZON: los guardianes se han pagado solos. Encontraron los dos
# defectos del motor, la cadena G14->G8, los cuatro organos desconectados y tres falsos positivos
# de mis propios detectores en un solo dia. Quitarlos no acelerar√≠a: nos devolveria a publicar
# resultados falsos mas deprisa.
#
# DONDE SI TIENE RAZON, y es un fallo de diseño mio: NO EXISTE UN CARRIL RAPIDO. Hoy, probar una
# tasa de aprendizaje distinta obliga a pasar por la puerta como si fuera un estudio. Eso no
# protege nada —una prueba de concepto no publica— y cuesta horas.
#
# LA SALIDA NO ES AFLOJAR LOS GUARDIANES: ES DECLARAR DOS CARRILES, y poner la frontera donde de
# verdad esta el riesgo, que no es "tocar codigo" sino "AFIRMAR ALGO".
#
#   CARRIL RAPIDO (aqui)      : tantear, ajustar, romper, tirar. SIN sello, SIN prerregistro.
#   CARRIL DE PRODUCCION      : LA PUERTA entera, prerregistro firmado antes, acta con datos.
#
# LAS TRES REGLAS DEL BANCO, y son lo unico que lo hace seguro:
#   1. NADA DEL BANCO PRODUCE UNA AFIRMACION. Sus numeros son tanteos, no evidencia, y este modulo
#      los marca como tales en cada salida que escribe.
#   2. NADA DEL BANCO ENTRA EN arbol/ NI EN resultados/. Se comprueba a maquina, y bloquea.
#   3. LO QUE SOBREVIVE AL BANCO NO SE ASCIENDE: SE REESCRIBE COMO ESTUDIO. Un tanteo que funciona
#      no es un hallazgo — es una razon para escribir un prerregistro. Y las semillas usadas en el
#      banco QUEDAN QUEMADAS, porque tantear sobre ellas es haber mirado los datos.
#
# Uso: python banco.py [--regla31] [--listar]

import os
import re
import sys
import json
import glob
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TALLER = os.path.join(BASE, "banco")             # aqui vive lo que se tantea
BITACORA = os.path.join(TALLER, "BITACORA.json")  # que se probo, con que semillas, y que salio

# Las carpetas donde vive lo que SI afirma. El banco no puede escribir en ninguna.
PROHIBIDO_ESCRIBIR = ("arbol", "resultados", "registros")

SELLO_DE_TANTEO = ("TANTEO DEL BANCO — NO ES EVIDENCIA. Sin prerregistro previo y sin sello, "
                   "este numero no puede citarse en ningun acta ni sostener ninguna afirmacion. "
                   "Si el tanteo funciona, el paso siguiente NO es ascenderlo: es escribir un "
                   "prerregistro y volver a medirlo con semillas nuevas.")

# QUE ESTUDIA ESTE MODULO: nada externo. Vigila SUS PROPIAS reglas, y su regla31() las ejercita
# con rutas y registros sinteticos. Declararlo vacio obliga a escribir esta linea; no declararlo
# reprueba, que es lo que `disciplina.py` comprueba desde hoy.
SUJETO = ()

METODO = {
    "prerregistro": 55,
    "tipo_de_medida": "umbral",   # cada intento de escritura se permite o se bloquea: es binario
    "que_mide": ("cuantos intentos de escritura fuera del taller bloquea, y si toda salida del "
                 "banco lleva el sello de tanteo que impide citarla como evidencia"),
    "comparten_datos": {
        "hay": False,
        "porque": "cada intento de escritura se juzga por su ruta, sin relacion con los demas; "
                  "lo unico comun es el propio guardia",
    },
    "linea_base": ("dejar escribir donde sea — el tonto de la Regla 11. Un banco sin frontera no "
                   "es un carril rapido: es el mismo carril sin guardianes, que es exactamente lo "
                   "que la critica NO pedia"),
    "formulas": [
        {"base": {"intentos_prohibidos": 1.0}, "parametro": "intentos_prohibidos", "factor": 4.0,
         "esperado": "sube",
         "porque": "mas intentos de escribir fuera del taller = mas bloqueos, porque el guardia "
                   "examina cada ruta por separado y es determinista. Es lo unico que se sabe A "
                   "PRIORI de esta medida. Base 1.0 y NO 0.0: multiplicar cero por cuatro sigue "
                   "siendo cero, y ese descuido ya me tumbo cuatro relaciones este mes"},
    ],
}


def _dentro_del_taller(ruta):
    """¿Esta ruta cae dentro del taller? Se compara por camino real, no por texto: '../' es la
    forma obvia de saltarse una frontera escrita a base de prefijos."""
    r = os.path.realpath(os.path.join(TALLER, ruta) if not os.path.isabs(ruta) else ruta)
    return os.path.commonpath([r, os.path.realpath(TALLER)]) == os.path.realpath(TALLER)


def guardia(ruta):
    """LA FRONTERA. Devuelve la lista de motivos por los que esa escritura NO se permite."""
    if _dentro_del_taller(ruta):
        return []
    r = os.path.realpath(os.path.join(BASE, ruta) if not os.path.isabs(ruta) else ruta)
    rel = os.path.relpath(r, BASE)
    cima = rel.split(os.sep)[0]
    if cima in PROHIBIDO_ESCRIBIR:
        return [f"el banco NO puede escribir en '{cima}/': ahi vive lo que AFIRMA, y un tanteo no "
                f"afirma. Si el tanteo funciona, escribe un prerregistro y vuelve a medirlo"]
    return [f"'{rel}' esta fuera del taller: el banco solo escribe en banco/"]


def escribir(ruta, datos, semillas=(), que_se_tanteaba=""):
    """Guarda un tanteo DENTRO del taller, con su sello y sus semillas quemadas."""
    motivos = guardia(ruta)
    if motivos:
        raise PermissionError(motivos[0])
    destino = os.path.join(TALLER, ruta)
    os.makedirs(os.path.dirname(destino) or TALLER, exist_ok=True)
    envuelto = {"_sello": SELLO_DE_TANTEO,
                "_semillas_quemadas": sorted(int(s) for s in semillas),
                "_que_se_tanteaba": que_se_tanteaba,
                "tanteo": datos}
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(envuelto, f, indent=2, ensure_ascii=False)
    _anotar(ruta, semillas, que_se_tanteaba)
    return destino


def _anotar(ruta, semillas, que):
    """LA BITACORA: que se tanteo y con que semillas. Existe por una razon concreta — las semillas
    usadas para tantear QUEDAN QUEMADAS, porque tantear sobre ellas es haber mirado los datos, y
    volver a usarlas en el estudio formal seria elegir las que salieron bien."""
    os.makedirs(TALLER, exist_ok=True)
    b = json.load(open(BITACORA, encoding="utf-8")) if os.path.exists(BITACORA) else {"tanteos": []}
    b["tanteos"].append({"salida": ruta, "semillas_quemadas": sorted(int(s) for s in semillas),
                         "que_se_tanteaba": que})
    b["semillas_quemadas_en_total"] = sorted({s for t in b["tanteos"]
                                              for s in t["semillas_quemadas"]})
    with open(BITACORA, "w", encoding="utf-8") as f:
        json.dump(b, f, indent=2, ensure_ascii=False)


def semillas_quemadas():
    """Las semillas que el banco ha gastado. Un estudio formal NO puede usar ninguna."""
    if not os.path.exists(BITACORA):
        return []
    return json.load(open(BITACORA, encoding="utf-8")).get("semillas_quemadas_en_total", [])


def fugas_del_taller():
    """¿Se ha colado algun archivo del banco donde vive lo que afirma? Se comprueba buscando el
    sello de tanteo fuera del taller: si aparece ahi, un numero sin prerregistro esta sosteniendo
    una afirmacion."""
    # SI ESTA LISTA SE VACIARA, este detector recorreria cero carpetas y devolveria "sin fugas"
    # sobre nada — el error `not []` que reglas.py ya cometio una vez. Lo cazo disciplina.py en la
    # primera corrida de este archivo, y es un verdadero positivo: sin esta guarda, vaciar una
    # constante desactivaria la frontera EN SILENCIO.
    if not PROHIBIDO_ESCRIBIR:
        raise RuntimeError("PROHIBIDO_ESCRIBIR esta VACIA: el detector de fugas no vigilaria "
                           "ninguna carpeta y aprobaria sobre nada")
    fugas = []
    for carpeta in PROHIBIDO_ESCRIBIR:
        for p in glob.glob(os.path.join(BASE, carpeta, "**", "*.json"), recursive=True):
            try:
                if "TANTEO DEL BANCO" in open(p, encoding="utf-8").read():
                    fugas.append(os.path.relpath(p, BASE))
            except Exception:
                continue
    return fugas


def _metodo_medir(intentos_prohibidos=1.0):
    """PASO 1 — la medida escalar: cuantos intentos de escribir fuera del taller bloquea."""
    rutas = ["../arbol/x.json", "../resultados/y.json", "../registros/z.json",
             "../codigo/w.py"][:int(intentos_prohibidos)]
    return float(sum(1 for r in rutas if guardia(r)))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿la frontera se sostiene contra el atajo obvio?** Una
    frontera escrita a base de prefijos de texto se salta con '../', y entonces no es una
    frontera: es un cartel."""
    fallos = []
    if not guardia("../resultados/colado.json"):
        fallos.append("la frontera se salta con '../': no es una frontera, es un cartel")
    if guardia("prueba/rapida.json"):
        fallos.append("no deja escribir DENTRO del taller: entonces no hay carril rapido")
    if not guardia(os.path.join(BASE, "arbol", "x.json")):
        fallos.append("una ruta absoluta a arbol/ no se bloquea")
    return {"aprueba": not fallos, "fallos": fallos,
            "taller": os.path.relpath(TALLER, BASE)}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados, con rutas hechas a mano.

    NO se prueba aqui si un tanteo concreto es buena idea: eso no lo juzga una maquina y no es de
    este modulo. Se prueba que la FRONTERA se sostiene."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del banco: la frontera, no los tanteos ==")

    caso("CONTROL POSITIVO: deja escribir dentro del taller", guardia("tanteo/x.json") == [])
    caso("SEÑUELO: bloquea escribir en resultados/", len(guardia("../resultados/x.json")) == 1)
    caso("SEÑUELO: bloquea escribir en arbol/", len(guardia("../arbol/x.json")) == 1)
    caso("SEÑUELO: bloquea escribir en registros/", len(guardia("../registros/x.json")) == 1)
    caso("la frontera NO se salta con una ruta absoluta",
         len(guardia(os.path.join(BASE, "resultados", "x.json"))) == 1)

    # el sello viaja SIEMPRE con el dato: sin el, un tanteo se puede citar como si fuera evidencia
    d = escribir("regla31/tanteo.json", {"x": 1}, semillas=(101, 103), que_se_tanteaba="la propia Regla 31")
    guardado = json.load(open(d, encoding="utf-8"))
    caso("todo lo que escribe lleva el sello de TANTEO", "TANTEO DEL BANCO" in guardado["_sello"])
    caso("y deja constancia de las semillas QUEMADAS", guardado["_semillas_quemadas"] == [101, 103])
    caso("la bitacora acumula las semillas quemadas", 101 in semillas_quemadas())

    # intentar escribir fuera DEBE levantar error, no avisar
    try:
        escribir("../resultados/colado.json", {"x": 1})
        caso("escribir fuera del taller LEVANTA error", False)
    except PermissionError:
        caso("escribir fuera del taller LEVANTA error", True)

    caso("no hay ningun tanteo colado donde vive lo que afirma", fugas_del_taller() == [],
         str(fugas_del_taller()))

    # Y EL DETECTOR DE FUGAS NO PUEDE APROBAR SOBRE VACIO: si alguien vaciara la lista de carpetas
    # vigiladas, la frontera se desactivaria en silencio. Se prueba vaciandola a proposito.
    global PROHIBIDO_ESCRIBIR
    _guardado = PROHIBIDO_ESCRIBIR
    try:
        PROHIBIDO_ESCRIBIR = ()
        fugas_del_taller()
        caso("el detector de fugas SE NIEGA a aprobar sobre una lista vacia", False)
    except RuntimeError:
        caso("el detector de fugas SE NIEGA a aprobar sobre una lista vacia", True)
    finally:
        PROHIBIDO_ESCRIBIR = _guardado

    b, s = _metodo_medir(1.0), _metodo_medir(4.0)
    caso("la medida RESPONDE (y la base no es cero)", b > 0 and s > b, f"{b:.0f} -> {s:.0f}")

    fs = _metodo_sanidad()
    caso("la ficha aprueba", fs["aprueba"], str(fs["fallos"]))

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — hay carril rapido y sigue habiendo frontera."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="El carril rapido, con su frontera")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--listar", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    if a.listar:
        print(json.dumps(json.load(open(BITACORA, encoding="utf-8"))
                         if os.path.exists(BITACORA) else {"tanteos": []},
                         ensure_ascii=False, indent=2))
        sys.exit(0)
    fugas = fugas_del_taller()
    print("=== EL BANCO: carril rapido con frontera ===")
    print(f"taller: banco/ · semillas quemadas: {semillas_quemadas()}")
    if fugas:
        print(f"FUGA: {len(fugas)} tanteo(s) colado(s) donde vive lo que afirma: {fugas}")
        sys.exit(1)
    print("ok    ningun tanteo se ha colado donde vive lo que afirma")
    sys.exit(0)
