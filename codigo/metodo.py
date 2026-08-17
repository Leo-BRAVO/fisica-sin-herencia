# metodo.py — LA PUERTA. Ningun estudio se encola si su modulo no pasa por aqui.
#
# POR QUE EXISTE, y es una idea del director (10-ago-2026): "primero escribes la prueba, luego pasa
# por el metodo, te explica que esta mal en cada paso y lo arreglas, y UNICAMENTE despues de que
# pasen todas las validaciones puedes correr una prueba".
#
# Tenia razon y su version es mejor que la mia. Yo habia escrito el metodo como un DOCUMENTO — ocho
# pasos que prometia seguir. Y el mismo dia que lo escribi me salte el paso 2: use `>>` para añadir
# al final de un archivo sin leer que ahi vivia el bloque de arranque, y el modulo quedo llamando a
# funciones que aun no existian. Era la SEGUNDA vez que cometia ese error exacto.
#
# UN DOCUMENTO NO ES UNA PUERTA. Esto si:
#   - se corre sobre un modulo y dice, paso por paso, que esta mal;
#   - si algo falla, NO deja sello;
#   - `coherencia.py` exige sello VALIDO para todo estudio pendiente en la cola;
#   - el sello guarda la HUELLA del archivo: si toco el modulo despues de pasar, el sello muere.
# Resultado: no puedo encolar un estudio sin pasar, ni editar el modulo despues de pasar.
#
# FRONTERA (Regla 27), y el director lo subrayo: DIEGO NO VE NADA DE ESTO. Estas son reglas del
# ORQUESTADOR, no del ente. La puerta vive en codigo/ porque es codigo, pero su sello vive en
# registros/ (lado humano) y ningun gen la lee ni la ejecuta. `coherencia.py` lo comprueba.

import ast
import os
import sys
import json
import time
import hashlib
import argparse
import importlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

SELLOS = os.path.join(BASE, "registros", "METODO-SELLOS.json")


def huella(ruta):
    return hashlib.sha256(open(ruta, "rb").read()).hexdigest()[:16]


# ------------------------------------------------------------------ los pasos mecanizables
def paso2_arranque_al_final(ruta):
    """PASO 2 — el bloque `if __name__ == "__main__"` debe ser lo ULTIMO del archivo.

    Este caso existe por un error mio, cometido DOS VECES: añadir al final de un archivo con `>>`
    sin mirar que ahi estaba el arranque. El modulo quedaba llamando a funciones definidas mas
    abajo, y reventaba al ejecutarse. El metodo escrito no lo impidio; esto si."""
    lineas = open(ruta, encoding="utf-8").read().rstrip().split("\n")
    idx = [i for i, l in enumerate(lineas) if l.startswith('if __name__ ==')]
    if not idx:
        return {"aprueba": True, "nota": "el modulo no tiene bloque de arranque"}
    resto = [l for l in lineas[idx[0] + 1:] if l.strip() and not l.startswith((" ", "\t"))]
    if resto:
        return {"aprueba": False,
                "fallos": [f"hay {len(resto)} definiciones DESPUES del bloque de arranque "
                           f"(primera: '{resto[0][:60]}') — el modulo llamara a funciones que aun "
                           f"no existen. Añadiste al final sin leer el final."]}
    return {"aprueba": True}


def paso2_sin_pisar_nombres(ruta, texto=None):
    """PASO 2 — ninguna funcion puede reusar un nombre que ya significa otra cosa en su bucle.

    Nace del bug de `soporte.py`: llame `w` al diccionario del mundo, y dentro del bucle `w` ya era
    la velocidad de la articulacion. Reventaba en tiempo de ejecucion."""
    # `texto` permite probar el detector con codigo hecho a mano, sin inventar archivos falsos en
    # el repositorio. pruebas.py lo usa para congelar la distincion entre un INICIALIZADOR y un
    # valor calculado y pisado (ver mas abajo).
    arbol = ast.parse(texto if texto is not None else open(ruta, encoding="utf-8").read())
    fallos = []
    for fn in [n for n in ast.walk(arbol) if isinstance(n, ast.FunctionDef)]:
        # EL PATRON EXACTO DEL BUG, no "cualquier nombre repetido". Cazado por esta misma puerta
        # en su primera corrida: marcaba `m` asignado en las dos ramas de un if/else, que es
        # Python normal y corriente. Una alarma falsa hace desconfiar de lo que funciona.
        # El bug real de soporte.py fue otro: un nombre asignado FUERA de un bucle y vuelto a
        # asignar DENTRO del bucle con otro significado. Ahi el de dentro pisa al de fuera y el
        # resto de la funcion usa el equivocado.
        fuera, dentro = {}, {}
        bucles = [n for n in ast.walk(fn) if isinstance(n, (ast.For, ast.While))]
        en_bucle = set()
        for b in bucles:
            for n in ast.walk(b):
                if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                        and isinstance(n.targets[0], ast.Name):
                    en_bucle.add((n.targets[0].id, n.lineno))
                    dentro.setdefault(n.targets[0].id, n.lineno)
        # UN INICIALIZADOR NO ES UN VALOR PISADO — 11-ago-2026, segunda correccion de este mismo
        # detector. La primera quito la alarma sobre `m` asignado en las dos ramas de un if/else.
        # Esta quita la que salta sobre `ultima = None` antes de un bucle: eso es un INICIALIZADOR,
        # y el bucle lo rellena, que es la forma normal de escribir un acumulador. El INFORME-63 ya
        # lo identifico como falso positivo —marcaba `_iaaft` y `coste_de`, dos algoritmos
        # perfectamente correctos— y se dejo sin arreglar a proposito: aflojar un detector JUSTO
        # despues de verlo dispararme en contra es lo que este proyecto prohibe. Se arregla ahora,
        # con la distincion escrita y probada por los dos lados en pruebas.py.
        #
        # LA DISTINCION, y NO afloja el criterio: el bug real de soporte.py asignaba fuera del
        # bucle un valor CALCULADO —una llamada, una operacion— y el de dentro lo pisaba. Un
        # literal (None, 0, "", [], {}) no calcula nada: no hay valor que perder.
        def _es_inicializador(nodo):
            return isinstance(nodo.value, ast.Constant) or (
                isinstance(nodo.value, (ast.List, ast.Dict, ast.Tuple, ast.Set))
                and not getattr(nodo.value, "elts", None)
                and not getattr(nodo.value, "keys", None))

        for n in ast.walk(fn):
            if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                    and isinstance(n.targets[0], ast.Name):
                v = n.targets[0].id
                if (v, n.lineno) not in en_bucle and not _es_inicializador(n):
                    fuera.setdefault(v, n.lineno)
        for v, ln_dentro in dentro.items():
            if v in fuera and fuera[v] < ln_dentro:
                fallos.append(f"{fn.name}: '{v}' se asigna FUERA del bucle (linea {fuera[v]}) y "
                              f"vuelve a asignarse DENTRO (linea {ln_dentro}) — el de dentro pisa "
                              f"al de fuera y el resto de la funcion usa el equivocado")
    return {"aprueba": not fallos, "fallos": fallos}


def paso0_manifiesto(mod):
    """PASO 0 — el modulo debe DECLARAR que clase de prueba es. Sin esto no se sabe que
    comprobacion aplica, y aplicar la equivocada produce alarmas falsas (paso 0 del METODO)."""
    m = getattr(mod, "METODO", None)
    if not isinstance(m, dict):
        return {"aprueba": False,
                "fallos": ["el modulo no declara METODO = {...}: no dice que clase de prueba es, "
                           "ni sus formulas, ni si hay condiciones que comparten datos"]}
    fallos = []
    if m.get("tipo_de_medida") not in ("continua", "umbral", "mixta"):
        fallos.append("METODO['tipo_de_medida'] debe ser 'continua', 'umbral' o 'mixta'")
    if not m.get("formulas"):
        fallos.append("METODO['formulas'] vacio: sin formula escrita no entiendo la medida "
                      "(paso 1) y no debo programarla")
    if "comparten_datos" not in m:
        fallos.append("METODO['comparten_datos'] ausente: hay que decir SI o NO, no omitirlo — "
                      "compartir datos es legitimo, compartirlos sin declararlo es tautologia")
    return {"aprueba": not fallos, "fallos": fallos, "manifiesto": m}


PASOS = ("0 manifiesto", "0.5 disciplina", "1 formulas", "2 arranque al final",
         "2 sin pisar nombres", "3 ficha de sanidad", "4 regla 31", "7 escritura limpia")


def revisar(nombre_modulo, verbose=True, correr_regla31=True):
    """Corre LA PUERTA sobre un modulo. Devuelve el veredicto y, si todo pasa, deja sello."""
    import sanidad as S
    ruta = os.path.join(BASE, "codigo", f"{nombre_modulo}.py")
    if not os.path.exists(ruta):
        return {"aprueba": False, "fallos": [f"no existe codigo/{nombre_modulo}.py"]}
    resultados, fallos = {}, []

    def _reg(paso, r):
        resultados[paso] = r
        if not r.get("aprueba"):
            for f in r.get("fallos", []) or [r.get("nota", "sin detalle")]:
                fallos.append(f"[paso {paso}] {f}")
        if verbose:
            print(f"  {'ok  ' if r.get('aprueba') else 'FALLO'} paso {paso}")
            if not r.get("aprueba"):
                for f in (r.get("fallos") or [])[:4]:
                    print(f"        -> {f}")

    # los pasos que NO necesitan importar el modulo van primero: si el modulo esta roto,
    # importarlo revienta y no sabriamos por que.
    _reg("2 arranque al final", paso2_arranque_al_final(ruta))
    _reg("2 sin pisar nombres", paso2_sin_pisar_nombres(ruta))
    _reg("7 escritura limpia", {"aprueba": S.homoglifos(ruta)["aprueba"]
                                and S.restos_de_versiones(ruta)["aprueba"],
                                "fallos": S.homoglifos(ruta)["fallos"]
                                + S.restos_de_versiones(ruta)["fallos"]})
    try:
        mod = importlib.import_module(nombre_modulo)
    except Exception as e:
        _reg("0 manifiesto", {"aprueba": False, "fallos": [f"el modulo no importa: {e}"]})
        return {"modulo": nombre_modulo, "aprueba": False, "fallos": fallos,
                "resultados": resultados}

    man = paso0_manifiesto(mod)
    _reg("0 manifiesto", man)

    # PASO 0.5 — EL GUARDIAN QUE ME CORRIGE A MI (disciplina.py, encargo del director).
    # Va AQUI y no al final porque su trabajo es pararme ANTES de lanzar mal una prueba, no
    # explicarme despues por que salio mal. Los demas pasos vigilan el modulo; este vigila los
    # errores que YO repito al escribirlo, y lleva el catalogo de cada uno con su incidente real.
    import disciplina as D
    _dis = D.revisar_modulo(nombre_modulo, verbose=False)
    # Y LA LECTURA PREVIA: el guardian tiene que haberse consultado ANTES de escribir, no despues.
    # "son demasiados errores", dijo el director, y llevaba razon: cazarlos al final es rehacer el
    # trabajo. La constancia CADUCA en cuanto se añade un error nuevo al catalogo.
    _ok_lect, _porque = D.lectura_valida(nombre_modulo)
    if not _ok_lect:
        _dis = list(_dis) + [f"[lectura-previa] {_porque}"]
    _reg("0.5 disciplina", {"aprueba": not _dis, "fallos": _dis})

    # PASO 1 — las formulas declaradas deben CUMPLIRSE. Es la unica comprobacion que seguira
    # valiendo el dia que Diego mida algo cuya respuesta nadie conoce.
    if man.get("aprueba") and hasattr(mod, "_metodo_medir"):
        rels = man["manifiesto"].get("formulas") or []
        _reg("1 formulas", S.relaciones_metamorficas(mod._metodo_medir, rels, verbose=False))
    else:
        _reg("1 formulas", {"aprueba": False,
                            "fallos": ["el modulo no expone _metodo_medir(**params): sin eso las "
                                       "formulas no se pueden comprobar, solo prometer"]}
             if man.get("aprueba") else {"aprueba": False, "fallos": ["sin manifiesto"]})

    # PASO 3 — la ficha propia del modulo, si la tiene
    if hasattr(mod, "_metodo_sanidad"):
        _reg("3 ficha de sanidad", mod._metodo_sanidad())
    else:
        _reg("3 ficha de sanidad", {"aprueba": False,
                                    "fallos": ["el modulo no expone _metodo_sanidad(): la Regla 31 "
                                               "comprueba que hace lo que quise, no que lo que "
                                               "quise fuera correcto"]})

    # PASO 4 — la Regla 31
    if correr_regla31 and hasattr(mod, "regla31"):
        ok = mod.regla31(verbose=False) == 0
        _reg("4 regla 31", {"aprueba": ok, "fallos": [] if ok else ["la Regla 31 del modulo reprueba"]})
    elif correr_regla31:
        _reg("4 regla 31", {"aprueba": False, "fallos": ["el modulo no tiene regla31()"]})

    aprueba = not fallos
    if aprueba:
        sellar(nombre_modulo, ruta)
    if verbose:
        print(f"\nLA PUERTA: {'ABIERTA — el modulo puede encolarse' if aprueba else 'CERRADA'}")
        if not aprueba:
            print(f"  {len(fallos)} cosas que arreglar antes de correr NADA.")
    return {"modulo": nombre_modulo, "aprueba": aprueba, "fallos": fallos,
            "resultados": resultados}


def sellar(nombre_modulo, ruta):
    sellos = json.load(open(SELLOS, encoding="utf-8")) if os.path.exists(SELLOS) else {}
    sellos[nombre_modulo] = {"huella": huella(ruta), "cuando": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(SELLOS, "w", encoding="utf-8") as f:
        json.dump(sellos, f, indent=2, ensure_ascii=False, sort_keys=True)


def sello_valido(nombre_modulo):
    """¿Este modulo paso la puerta, y sigue siendo el MISMO archivo que paso?
    La huella es lo que impide pasar la puerta y luego editar el modulo."""
    if not os.path.exists(SELLOS):
        return False, "no hay sellos: ningun modulo ha pasado la puerta"
    sellos = json.load(open(SELLOS, encoding="utf-8"))
    s = sellos.get(nombre_modulo)
    if not s:
        return False, f"{nombre_modulo} nunca paso la puerta"
    ruta = os.path.join(BASE, "codigo", f"{nombre_modulo}.py")
    if not os.path.exists(ruta):
        return False, f"codigo/{nombre_modulo}.py no existe"
    if huella(ruta) != s["huella"]:
        return False, (f"{nombre_modulo} paso la puerta el {s['cuando']} pero el archivo CAMBIO "
                       f"despues: el sello no vale")
    return True, f"sellado {s['cuando']}"


def main():
    ap = argparse.ArgumentParser(description="LA PUERTA del metodo (8 pasos)")
    ap.add_argument("--modulo", help="nombre sin .py, p.ej. experimentar2")
    ap.add_argument("--sin-regla31", action="store_true", help="salta el paso 4 (solo diagnostico)")
    ap.add_argument("--sellos", action="store_true", help="lista los sellos vigentes")
    a = ap.parse_args()
    if a.sellos:
        sellos = json.load(open(SELLOS, encoding="utf-8")) if os.path.exists(SELLOS) else {}
        for m in sorted(sellos):
            ok, por = sello_valido(m)
            print(f"  {'VALIDO ' if ok else 'CADUCO '} {m:<22} {por}")
        return
    if not a.modulo:
        print("uso: --modulo NOMBRE [--sin-regla31] | --sellos")
        return
    r = revisar(a.modulo, correr_regla31=not a.sin_regla31)
    sys.exit(0 if r["aprueba"] else 1)


if __name__ == "__main__":
    main()
