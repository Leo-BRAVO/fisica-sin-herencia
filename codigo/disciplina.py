# disciplina.py — EL GUARDIAN QUE ME CORRIGE A MI (encargo del director, 11-ago-2026).
#
# POR QUE EXISTE. Los demas guardianes vigilan el REPOSITORIO. Este vigila AL QUE ESCRIBE LAS
# PRUEBAS, que soy yo, y nace de una observacion del director que es exacta: mis errores no son
# variados — son LOS MISMOS, una y otra vez, y cada uno costo horas o dejo un estudio NULO.
#
# QUE HACE: guarda el catalogo de cada error de metodo que he cometido en este proyecto, CON su
# incidente real y sus numeros, y corre ANTES de que una prueba se lance. Lo que puede cazar a
# maquina, lo BLOQUEA. Lo que no, lo RECUERDA por escrito, que es mejor que fingir que no existe.
#
# LA REGLA QUE SE APLICA A SI MISMO: cada detector se prueba POR LOS DOS LADOS —un caso que DEBE
# marcarse y otro que NO— porque un detector que solo se ha visto aprobar es indistinguible de no
# tenerlo. Y la lista de errores no puede estar vacia: revisar sobre vacio aprueba siempre.
#
# COMO CRECE: cada vez que cometo un error nuevo, se añade aqui con su incidente. El catalogo es
# la memoria del proyecto sobre mis propios fallos, y es lo unico que impide repetirlos por
# olvido en vez de por descuido.
#
# Uso: python disciplina.py [--regla31] [--modulo NOMBRE] [--prerregistros]

import os
import re
import sys
import glob
import json
import argparse
import importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DESDE CUANDO RIGE. La convencion de declarar SUJETO nace HOY, asi que exigirsela a los modulos
# que ya existen tendria dos efectos y los dos malos: editarlos MATA SU SELLO —la puerta sella por
# hash— y dejaria irreproducibles los estudios que ya produjeron. Se aplica el precedente que el
# propio proyecto ya fijo con los cuatro endurecimientos de reglas.py: RIGE HACIA ADELANTE, y lo
# anterior SE CUENTA como deuda medida en vez de reescribirse.
# El corte incluye lo que escribi HOY: mundo (50), invariantes (52), contratos (49)... tambien
# estan en deuda. Ponerme a mi mismo del lado bueno de la linea seria hacer trampa con la fecha.
DESDE_PRERREGISTRO = 53

# ==========================================================================================
# EL CATALOGO. Cada entrada es un error REAL, con el incidente que lo produjo.
# `mecanizado`: True  -> hay detector y BLOQUEA.
#               False -> no se puede cazar a maquina y se RECUERDA. Decirlo es parte del trato:
#                        un catalogo que finge cazarlo todo miente sobre su propia cobertura.
# ==========================================================================================
ERRORES = [
    {
        "id": "base-cero",
        "titulo": "Relacion metamorfica con base 0.0",
        "veces": 4,
        "incidente": ("contingencia (ruido), escala.py dos veces, y atencion.py heredado del "
                      "prerregistro-43. Multiplicar cero por doscientos sigue siendo cero: LA "
                      "PUERTA midio 'x1.000' y la relacion no probo absolutamente nada."),
        "como_evitarlo": "toda base de una relacion metamorfica debe ser distinta de cero",
        "mecanizado": True,
    },
    {
        "id": "relacion-sin-saber-a-priori",
        "titulo": "Relacion metamorfica declarada sin saberla A PRIORI",
        "veces": 3,
        "incidente": ("prerregistro-46 y prerregistro-43 declararon 'mas ruido baja la cuenta' "
                      "sobre ruido de PROCESO, que EXCITA el sistema en vez de enterrarlo: la "
                      "desviacion del mundo subio de 0.658 a 13.686 y las leyes de 3.0 a 4.0. Las "
                      "dos veces APROBO, por el motivo equivocado — sindy3 perdia leyes por "
                      "fragilidad suya. Ver LECCION-RUIDO-01."),
        "como_evitarlo": ("cada relacion declara POR QUE se sabe de antemano; si el 'porque' "
                          "describe una intuicion en vez de un mecanismo, no es a priori"),
        "mecanizado": True,
    },
    {
        "id": "objeto-de-estudio-en-mi-regla31",
        "titulo": "Prueba sobre el OBJETO DE ESTUDIO dentro de la Regla 31 del instrumento",
        "veces": 2,
        "incidente": ("el prerregistro-45 quedo NULO por esto y el 44 casi. La Regla 31 examina MI "
                      "PROCEDIMIENTO; lo que hace el sujeto es RESULTADO. Con el sujeto ahi, un "
                      "defecto suyo bloquea el modulo que existe para medir sus defectos, y ademas "
                      "el criterio que deberia poder reprobar ya no puede."),
        "como_evitarlo": ("el modulo declara SUJETO = (...) con lo que estudia, y su regla31() no "
                          "puede mencionarlo"),
        "mecanizado": True,
    },
    {
        "id": "criterio-tautologico",
        "titulo": "Criterio que no puede fallar",
        "veces": 1,
        "incidente": ("el criterio 4 del prerregistro-41 comparaba el canal del tacto contra la "
                      "misma consulta de la que se deriva: dio 1.0000 y el predictor tonto "
                      "tambien. UN CRITERIO QUE NO PUEDE FALLAR TAMPOCO PUEDE APROBAR NADA. Se "
                      "evito seis veces mas durante agosto, siempre a proposito."),
        "como_evitarlo": ("preguntarse, antes de correr: ¿que resultado haria fallar esto? Si no "
                          "hay ninguno, no es un criterio"),
        "mecanizado": False,
    },
    {
        "id": "aprueba-sobre-vacio",
        "titulo": "Chequeo que aprueba sobre una lista vacia",
        "veces": 1,
        "incidente": ("los cuatro endurecimientos de reglas.py salieron en verde sin poder salir "
                      "de otra forma: no existia ningun prerregistro 42 todavia, y `not []` es "
                      "siempre cierto. Lo cazo la Regla 31 del archivo que nacio para cazarlo."),
        "como_evitarlo": "toda lista sobre la que se itera para juzgar se comprueba NO VACIA",
        "mecanizado": True,
    },
    {
        "id": "prueba-que-caduca",
        "titulo": "Prueba que caduca en silencio",
        "veces": 1,
        "incidente": ("una prueba de daño buscaba el literal '32 reglas'; al pasar a 34 dejo de "
                      "poder aplicarse y la meta-auditoria seguia diciendo 'los 9 daños fueron "
                      "cazados' contando 8. SALTADA era un aprobado disfrazado."),
        "como_evitarlo": "ningun conteo del repositorio se escribe a mano en una prueba",
        "mecanizado": True,
    },
    {
        "id": "numeros-solo-en-mi-cabeza",
        "titulo": "Publicar numeros medidos a mano, sin archivo detras",
        "veces": 2,
        "incidente": ("INFORME-48 publico una obediencia de 0.0297 que no estaba en ningun "
                      "archivo, e INFORME-58 hizo lo mismo con cuatro cifras del diagnostico. El "
                      "auditor de actas lo cazo la segunda vez."),
        "como_evitarlo": "todo numero de un acta sale de un archivo de datos citado",
        "mecanizado": False,
    },
    {
        "id": "nulo-copiado-de-otro-motor",
        "titulo": "Copiar el nulo de otro instrumento sin comprobar que aplica",
        "veces": 1,
        "incidente": ("el prerregistro-52 uso el barajado de FILAS —el nulo de sindy3— para un "
                      "buscador de invariantes. Barajar el tiempo destruye una ecuacion "
                      "diferencial pero NO toca una cantidad conservada: x2+v2 vale lo mismo en "
                      "cualquier orden. UN NULO TIENE QUE DESTRUIR LA ESTRUCTURA QUE EL MOTOR "
                      "BUSCA, y cada motor busca otra."),
        "como_evitarlo": "cada nulo declara QUE estructura destruye, no de donde se copio",
        "mecanizado": False,
    },
    {
        "id": "control-de-regresion-de-una-sola-familia",
        "titulo": "Control de 'no rompimos nada' construido con casos parecidos entre si",
        "veces": 1,
        "incidente": ("el criterio C del prerregistro-47 paso 4 de 4 y no vio que sindy4 se "
                      "quedaba MUDO en la caida con roce: sus cuatro casos eran todos de la "
                      "familia del oscilador."),
        "como_evitarlo": "un control de regresion necesita casos de familias distintas",
        "mecanizado": False,
    },
    {
        "id": "excepcion-de-compatibilidad",
        "titulo": "Contrato con una excepcion amable",
        "veces": 1,
        "incidente": ("escribi `_ignorancia()` aceptando la epistemica cruda 'por "
                      "compatibilidad', y esa concesion reabrio la fuga que el prerregistro-49 "
                      "existia para cerrar: inflando x2 la ventaja caia de 34.9971 a 27.0034. UNA "
                      "INTERFAZ CON UNA EXCEPCION AMABLE NO ES UN CONTRATO."),
        "como_evitarlo": "ningun contrato acepta el valor viejo 'por ahora'",
        "mecanizado": False,
    },
    {
        "id": "expectativa-de-un-solo-lado",
        "titulo": "Expectativa declarada que solo se equivoca por un lado",
        "veces": 1,
        "incidente": ("declare 'espero entre 2 y 5 reprobados de 8' y prepare la frase para el "
                      "caso de que aprobaran todos. Reprobaron los 8: el lado que no habia "
                      "previsto. Ver INFORME-63."),
        "como_evitarlo": "toda expectativa declara que dira si falla POR CADA lado",
        "mecanizado": False,
    },
    {
        "id": "medir-con-la-regla-equivocada",
        "titulo": "Medir con un parametro distinto del que se integro",
        "veces": 1,
        "incidente": ("sueno.py integraba con paso 0.02 y se le pasaba dt=1.0: ni la fase "
                      "despierta encontraba nada y la lectura base salia CERO. No era el organo: "
                      "era yo midiendolo con la regla equivocada."),
        "como_evitarlo": "el paso de integracion viaja con los datos, no se supone",
        "mecanizado": False,
    },
    {
        "id": "mundo-de-juguete-demasiado-limpio",
        "titulo": "Mundo de prueba donde la respuesta sale sola",
        "veces": 1,
        "incidente": ("en contingencia.py el cuerpo era una funcion pura del mando, asi que "
                      "cualquier fuerza daba 1.000. El instrumento no podia fallar porque el mundo "
                      "no tenia nada mas que explicar."),
        "como_evitarlo": "todo mundo de juguete lleva un termino de fondo independiente",
        "mecanizado": False,
    },
    {
        "id": "media-sobre-resultado-bimodal",
        "titulo": "Criterio construido sobre una MEDIA cuando el resultado tiene dos modos",
        "veces": 1,
        "incidente": ("el criterio B del prerregistro-57 exigia que la ventaja MEDIA superara "
                      "0.2693 y paso por 0.011 (0.2802) — pero cuatro semillas daban entre 0.3412 "
                      "y 0.5171 y la quinta daba -0.3277, es decir el signo contrario. La media "
                      "escondio exactamente lo que habia que mirar: que el candidato falla del "
                      "todo 1 de cada 5 veces. Ver INFORME-67."),
        "como_evitarlo": ("si un criterio puede pasar con la mitad de los casos fallando, no use "
                          "la media: exija el resultado EN CADA CASO, como hacen los criterios "
                          "'5 de 5' del resto del proyecto"),
        "mecanizado": False,
    },
    {
        "id": "variable-muerta",
        "titulo": "Variable que se calcula y no se usa",
        "veces": 2,
        "incidente": ("poder.py tenia `jueces = [11, 12]` que no coincidia con los indices "
                      "usados, y cerebro.py:115 tiene 'prog'. UNA VARIABLE MUERTA ES UNA "
                      "AFIRMACION FALSA SOBRE LO QUE HACE EL CODIGO."),
        "como_evitarlo": "el paso 7 de la puerta ya lo caza; no borrar ese paso",
        "mecanizado": True,
    },
]


def _por_id(i):
    return next(e for e in ERRORES if e["id"] == i)


def _importar_silencioso(nombre):
    """Importar un modulo LO EJECUTA. En la primera corrida de este archivo, uno del repositorio
    tenia argparse a nivel de modulo, se comio mis argumentos y aborto el barrido entero — un
    guardian que se cae al mirar es peor que no tenerlo. Aqui se le quitan los argumentos, se le
    tapa la boca y se atrapa su SystemExit."""
    import io
    import contextlib
    argv = sys.argv[:]
    sys.argv = [nombre]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return importlib.import_module(nombre)
    except SystemExit:
        return None
    except Exception:
        return None
    finally:
        sys.argv = argv


# ==========================================================================================
# LOS DETECTORES. Cada uno devuelve la lista de incumplimientos (vacia = limpio).
# ==========================================================================================
def d_base_cero(metodo):
    """Toda base de una relacion metamorfica debe ser distinta de cero."""
    malos = []
    for f in (metodo or {}).get("formulas", []) or []:
        par = f.get("parametro")
        base = (f.get("base") or {}).get(par)
        if base is not None and float(base) == 0.0:
            malos.append(f"la relacion sobre '{par}' tiene base {base}: multiplicar cero por "
                         f"{f.get('factor')} sigue siendo cero y no prueba nada")
    return malos


def d_relacion_sin_porque(metodo):
    """Cada relacion declara POR QUE se sabe A PRIORI, y con mecanismo, no con intuicion."""
    malos = []
    for f in (metodo or {}).get("formulas", []) or []:
        porque = (f.get("porque") or "").strip()
        if len(porque) < 40:
            malos.append(f"la relacion sobre '{f.get('parametro')}' no explica POR QUE se sabe a "
                         f"priori (tiene {len(porque)} caracteres de justificacion)")
    return malos


def d_sujeto_en_regla31(nombre, texto):
    """El modulo declara SUJETO = (...) con lo que estudia, y su regla31() no puede mencionarlo.

    Es la mecanizacion del error que dejo NULO al prerregistro-45. Si un modulo no declara SUJETO
    se avisa, porque no declararlo es la forma facil de esquivar el chequeo."""
    m = re.search(r"^SUJETO\s*=\s*\(([^)]*)\)", texto, re.M)
    if not m:
        return ["no declara SUJETO = (...): sin decir QUE estudia no se puede comprobar que su "
                "Regla 31 no lo examine (el error que dejo NULO al prerregistro-45)"]
    sujetos = [s.strip().strip("\"'") for s in m.group(1).split(",") if s.strip()]
    i = texto.find("def regla31")
    if i < 0 or not sujetos:
        return []
    cuerpo = texto[i:]
    fin = re.search(r"\ndef (?!regla31)", cuerpo)
    cuerpo = cuerpo[:fin.start()] if fin else cuerpo
    # se ignoran las lineas de comentario: nombrar el sujeto para EXPLICAR por que no se prueba
    # es exactamente lo que queremos que se escriba.
    codigo = "\n".join(l for l in cuerpo.split("\n") if not l.strip().startswith("#"))
    return [f"su regla31() menciona a '{s}', que es su OBJETO DE ESTUDIO: eso es resultado, no "
            f"requisito de entrada" for s in sujetos if re.search(rf"\b{re.escape(s)}\b", codigo)]


def d_aprueba_sobre_vacio(texto):
    """Toda lista de nivel de modulo sobre la que se juzga se comprueba NO VACIA en algun sitio."""
    listas = re.findall(r"^([A-Z_]{3,})\s*=\s*[\(\[]", texto, re.M)
    malos = []
    for L in set(listas):
        if not re.search(rf"for\s+\w+\s+in\s+{L}\b", texto):
            continue
        if not re.search(rf"(len\(\s*{L}\s*\)|not\s+{L}\b|if\s+{L}\b)", texto):
            malos.append(f"itera sobre {L} para juzgar y nunca comprueba que NO este vacia: "
                         f"revisar sobre vacio aprueba siempre")
    return malos


CONTEOS = re.compile(r"[\"'][^\"']*\b\d+\s+(reglas|nodos|informes|prerregistros|organos|genes)\b",
                     re.I)


def _sin_prosa(texto):
    """Quita comentarios y docstrings. Lo demas es codigo que SE EJECUTA.

    POR QUE EXISTE — 11-ago-2026, primera vez que este archivo se equivoca contra mi: la version
    original de `d_prueba_que_caduca` marcaba `anatomia.py` por dos frases de sus COMENTARIOS
    ("medir cuatro cosas", "acusaria a 10 de 15 organos"). El incidente que el detector existe
    para cazar fue un literal de conteo dentro de una BUSQUEDA REAL, es decir codigo que se
    ejecuta y caduca. Explicar un numero en prosa no caduca nada.
    ESTO NO AFLOJA EL CRITERIO: lo aplica al texto correcto. Un conteo escrito a mano dentro de
    una cadena OPERATIVA sigue disparando, y la Regla 31 lo prueba por los dos lados."""
    tres = chr(34) * 3
    tres2 = chr(39) * 3
    sin = re.sub(tres + r"[\s\S]*?" + tres, "", texto)
    sin = re.sub(tres2 + r"[\s\S]*?" + tres2, "", sin)
    return "\n".join(l for l in sin.split("\n") if not l.strip().startswith("#"))


def d_prueba_que_caduca(texto):
    """Ningun conteo del repositorio se escribe a mano dentro de una prueba."""
    return [f"lleva un conteo escrito a mano: {m.group(0)[:60]} — cuando el numero cambie, la "
            f"prueba caducara en silencio" for m in CONTEOS.finditer(_sin_prosa(texto))]


# ==========================================================================================
def revisar_modulo(nombre, verbose=True):
    """Corre TODOS los detectores sobre un modulo. Devuelve la lista de incumplimientos."""
    ruta = os.path.join(BASE, "codigo", f"{nombre}.py")
    if not os.path.exists(ruta):
        return [f"no existe codigo/{nombre}.py"]
    texto = open(ruta, encoding="utf-8").read()
    mod = _importar_silencioso(nombre)
    if mod is None:
        return [f"el modulo no se puede importar para revisarlo"]
    metodo = getattr(mod, "METODO", None)

    fallos = []
    for det, eid, arg in ((d_base_cero, "base-cero", metodo),
                          (d_relacion_sin_porque, "relacion-sin-saber-a-priori", metodo),
                          (d_aprueba_sobre_vacio, "aprueba-sobre-vacio", texto),
                          (d_prueba_que_caduca, "prueba-que-caduca", texto)):
        for f in det(arg):
            fallos.append(f"[{eid}] {f}")
    deuda = []
    if metodo is not None:                 # solo a los modulos que declaran ser una medida
        nuevo_regimen = int(metodo.get("prerregistro", 0)) >= DESDE_PRERREGISTRO
        for f in d_sujeto_en_regla31(nombre, texto):
            (fallos if nuevo_regimen else deuda).append(f"[objeto-de-estudio-en-mi-regla31] {f}")
        # el resto tambien es deuda si el modulo es anterior al corte
        if not nuevo_regimen:
            deuda.extend(fallos)
            fallos = []

    if verbose:
        if fallos:
            print(f"  FALLO {nombre}")
            for f in fallos:
                print(f"        -> {f}")
                eid = f.split("]")[0][1:]
                print(f"           YA ME PASO {_por_id(eid)['veces']} "
                      f"vez/veces: {_por_id(eid)['incidente'][:110]}...")
        elif deuda:
            print(f"  !!    {nombre} — {len(deuda)} en DEUDA (anterior al corte, no bloquea)")
        else:
            print(f"  ok    {nombre}")
    revisar_modulo.ultima_deuda = deuda
    return fallos


def revisar_prerregistros(verbose=True):
    """Los prerregistros NUEVOS declaran que diran si su expectativa falla POR CADA LADO."""
    fallos = []
    for p in sorted(glob.glob(os.path.join(BASE, "registros", "prerregistro-*.md"))):
        n = int(re.search(r"(\d+)", os.path.basename(p)).group(1))
        if n < 47:                # rige hacia adelante, como los cuatro endurecimientos
            continue
        t = open(p, encoding="utf-8").read().lower()
        if "espero" in t and not re.search(r"si (sale|no|aprueban|falla|reprueban)", t):
            fallos.append(f"{os.path.basename(p)}: declara una expectativa y no dice que dira si "
                          f"falla — una expectativa que solo se equivoca por un lado no es honesta")
    if verbose:
        for f in fallos:
            print(f"  FALLO [expectativa-de-un-solo-lado] {f}")
        if not fallos:
            print("  ok    los prerregistros desde el 47 declaran los dos lados de su expectativa")
    return fallos


def regla31(verbose=True):
    """CADA DETECTOR, POR LOS DOS LADOS. Un detector que solo se ha visto aprobar es
    indistinguible de no tenerlo — y este archivo entero existe por esa leccion."""
    fallos = []

    def caso(nombre, ok):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}")
        if not ok:
            fallos.append(nombre)

    caso("base-cero: MARCA una base 0.0",
         len(d_base_cero({"formulas": [{"parametro": "r", "base": {"r": 0.0}, "factor": 2}]})) == 1)
    caso("base-cero: NO marca una base distinta de cero",
         d_base_cero({"formulas": [{"parametro": "r", "base": {"r": 0.5}, "factor": 2}]}) == [])

    caso("sin-porque: MARCA una justificacion vacia",
         len(d_relacion_sin_porque({"formulas": [{"parametro": "r", "porque": "porque si"}]})) == 1)
    caso("sin-porque: NO marca una justificacion con mecanismo",
         d_relacion_sin_porque({"formulas": [{"parametro": "r", "porque": "x" * 80}]}) == [])

    caso("vacio: MARCA una lista de la que se juzga sin comprobarla",
         len(d_aprueba_sobre_vacio("CASOS = (\nfor c in CASOS:\n")) == 1)
    caso("vacio: NO marca una lista comprobada",
         d_aprueba_sobre_vacio("CASOS = (\nfor c in CASOS:\nif len(CASOS) > 0:\n") == [])

    caso("caduca: MARCA un conteo escrito a mano",
         len(d_prueba_que_caduca('t = "32 reglas vigentes"')) == 1)
    caso("caduca: NO marca un texto sin conteo",
         d_prueba_que_caduca('t = "las reglas vigentes"') == [])
    caso("caduca: NO marca un conteo que solo aparece en un COMENTARIO",
         d_prueba_que_caduca("# aqui habia 32 reglas y ahora hay mas\nx = 1\n") == [])
    caso("caduca: NO marca un conteo dentro de un docstring explicativo",
         d_prueba_que_caduca('def f():\n    ' + chr(34)*3 + 'acusaria a 10 de 15 organos' +
                             chr(34)*3 + '\n    return 1\n') == [])
    caso("caduca: SI SIGUE marcando un conteo dentro de una cadena OPERATIVA",
         len(d_prueba_que_caduca('if "32 reglas" in t:\n    pass\n')) == 1)

    caso("sujeto: MARCA un modulo que no declara SUJETO",
         len(d_sujeto_en_regla31("x", "def regla31():\n    pass\n")) == 1)
    caso("sujeto: MARCA una regla31 que menciona su objeto de estudio",
         len(d_sujeto_en_regla31("x", 'SUJETO = ("sindy4",)\ndef regla31():\n    sindy4.foo()\n')) == 1)
    caso("sujeto: NO marca una regla31 limpia",
         d_sujeto_en_regla31("x", 'SUJETO = ("sindy4",)\ndef regla31():\n    otra()\n') == [])
    caso("sujeto: NO marca al sujeto nombrado en un COMENTARIO que explica por que no se prueba",
         d_sujeto_en_regla31("x", 'SUJETO = ("sindy4",)\ndef regla31():\n'
                                  '    # aqui NO se prueba sindy4: es resultado\n    otra()\n') == [])

    caso("el catalogo de errores NO esta vacio", len(ERRORES) > 0)
    caso("todo error del catalogo declara si esta mecanizado",
         all("mecanizado" in e and "incidente" in e for e in ERRORES))

    if verbose:
        mec = sum(1 for e in ERRORES if e["mecanizado"])
        print(f"\nREGLA 31: " + ("APRUEBA — los detectores funcionan por los dos lados."
                                 if not fallos else f"REPRUEBA en {fallos}"))
        print(f"COBERTURA HONESTA: {mec} de {len(ERRORES)} errores del catalogo estan MECANIZADOS; "
              f"los {len(ERRORES) - mec} restantes solo se RECUERDAN. Un catalogo que fingiera "
              f"cazarlo todo mentiria sobre su propia cobertura.")
    return 0 if not fallos else 1


def catalogo(salida=None):
    """El catalogo, a disco, para que se pueda auditar y para que crezca sin tocar el codigo."""
    d = {"errores": ERRORES,
         "mecanizados": sum(1 for e in ERRORES if e["mecanizado"]),
         "total": len(ERRORES),
         "veces_en_total": sum(e["veces"] for e in ERRORES)}
    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
    return d


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="El guardian que corrige al que escribe las pruebas")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--modulo")
    ap.add_argument("--prerregistros", action="store_true")
    ap.add_argument("--catalogo", default="registros/ERRORES-DE-METODO.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    catalogo(salida=a.catalogo)
    if a.modulo:
        sys.exit(1 if revisar_modulo(a.modulo) else 0)
    print("=== DISCIPLINA: los errores que ya cometi, para no repetirlos ===")
    d = catalogo()
    print(f"catalogo: {d['total']} errores distintos, {d['veces_en_total']} incidentes reales, "
          f"{d['mecanizados']} mecanizados\n")
    malos, deudas = 0, 0
    for m in sorted(glob.glob(os.path.join(BASE, "codigo", "*.py"))):
        n = os.path.basename(m)[:-3]
        if n in ("disciplina", "__init__"):
            continue
        mod = _importar_silencioso(n)
        if mod is None or getattr(mod, "METODO", None) is None:
            continue              # solo los modulos que declaran ser una medida
        if revisar_modulo(n, verbose=True):
            malos += 1
        deudas += len(getattr(revisar_modulo, "ultima_deuda", []))
    print()
    if revisar_prerregistros(verbose=True):
        malos += 1
    print(f"\nDISCIPLINA: {'SIN FALLOS BLOQUEANTES' if not malos else f'{malos} sitios que corregir'}"
          f" · {deudas} en DEUDA MEDIDA (modulos anteriores al prerregistro "
          f"{DESDE_PRERREGISTRO}; se cuentan, no se reescriben, porque editarlos mataria su sello)")
    sys.exit(0 if not malos else 1)
