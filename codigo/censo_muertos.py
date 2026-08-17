# censo_muertos.py — EL CENSO DE LOS MUERTOS (prerregistro-59, 17-ago-2026).
#
# EL ENCARGO DEL DIRECTOR: "quiero limpieza de codigo redundante". El item 28 de la critica
# externa daba 9 modulos huerfanos; medido contra el genoma, los que no son organos ni guardianes
# son 54. La lista estaba vieja y tres de sus nueve ya estan conectados.
#
# QUE MIDE, todo mecanico:
#   VIVO POR IMPORTACION   algun otro .py de codigo/ lo importa
#   VIVO POR CITA          algun archivo de resultados/ o registros/ lo nombra CON extension
#   MUERTO                 ninguna de las dos
#   ARCHIVABLE             muerto Y sin sello vigente
#
# LA TRAMPA QUE ESTE MODULO EXISTE PARA EVITAR: el sello se comprueba abriendo
# `codigo/<nombre>.py`. MOVER un modulo sellado mata su sello igual que editarlo, y un sello muerto
# deja irreproducible el acta que ese modulo publico. Por eso MUERTO y ARCHIVABLE son dos listas
# distintas: hay peso muerto que se queda, y se queda con la razon escrita.
#
# LA CITA SE EXIGE CON EXTENSION a proposito: los nombres sueltos de este proyecto son palabras
# comunes del castellano —memoria, mente, escala, temple, rodar, dimension— y buscarlas sueltas
# daria por vivo a cualquiera que aparezca en una frase.
#
# ESTE MODULO NO MUEVE, NO BORRA Y NO EDITA. Su unica escritura es su JSON de salida. Mover
# archivos es un acto aparte, va a su propio commit, y lo decide el director.
#
# Uso: python censo_muertos.py [--regla31] [--salida resultados/p59-censo-muertos/medida.json]

import os
import re
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# QUE ESTUDIA ESTE MODULO: los modulos del repositorio real. Por eso su regla31() NO puede tocarlos
# — trabaja con arboles sinteticos hechos a mano. Examinar al sujeto dentro de mi propia Regla 31
# es el error que dejo NULO al prerregistro-45.
SUJETO = ("MODULOS",)

# Donde se buscan las citas. resultados/ son las actas; registros/ son las notas y lecciones.
CARPETAS_DE_CITA = ("resultados", "registros")

METODO = {
    "prerregistro": 59,
    "tipo_de_medida": "umbral",   # cada modulo esta muerto o no lo esta: es binario por modulo
    "que_mide": ("cuantos modulos que no son organos del genoma ni guardianes no los usa nadie: "
                 "ningun .py los importa y ninguna acta ni registro los cita por su nombre de "
                 "archivo"),
    "comparten_datos": {
        "hay": False,
        "porque": "todos los modulos se examinan contra el mismo grafo y el mismo corpus de "
                  "citas, pero el veredicto de uno no depende del de otro",
    },
    "linea_base": ("un grep del nombre pelado: muerto si su nombre no aparece en ningun otro "
                   "archivo del repositorio. Trivial y generoso. Todo lo que el grep llame muerto "
                   "el censo tambien lo llamara muerto —la diferencia solo puede ir en un "
                   "sentido— y por eso el criterio C nombra los dos desenlaces: o el censo halla "
                   "muertos que el grep da por vivos y los justifica uno a uno, o no halla "
                   "ninguno y entonces el censo no es mas que un grep caro, y se dice"),
    "formulas": [
        {"base": {"muertos_plantados": 1.0}, "parametro": "muertos_plantados", "factor": 3.0,
         "esperado": "sube",
         "porque": "el conteo es EXACTAMENTE lineal en lo plantado: el detector recorre los nodos "
                   "y cuenta los que no tienen ninguna entrada, asi que triplicar los plantados "
                   "triplica los hallados. El factor sale de esa linealidad, no de mi intuicion. "
                   "Base 1.0 y NO 0.0: multiplicar cero por tres sigue siendo cero, y ese "
                   "descuido ya me tumbo cuatro relaciones este mes"},
    ],
}


def _organos():
    """Los modulos que el GENOMA declara organos. Se leen de ahi, no de una lista mia."""
    g = json.load(open(os.path.join(BASE, "arbol", "GENOMA.json"), encoding="utf-8"))["genes"]
    return sorted({m[:-3] for v in g.values()
                   for m in re.findall(r"([\w_]+\.py)", v.get("modulo") or "")})


def _guardianes():
    """Los guardianes, leidos de anatomia.NO_CUENTAN para no tener dos listas que se desincronicen."""
    import anatomia
    return sorted(anatomia.NO_CUENTAN)


def candidatos():
    """Los modulos que este censo examina: ni organos del genoma ni guardianes."""
    fuera = set(_organos()) | set(_guardianes())
    return sorted(m[:-3] for m in os.listdir(os.path.join(BASE, "codigo"))
                  if m.endswith(".py") and m[:-3] not in fuera)


def importadores(modulos, textos):
    """QUIEN IMPORTA A QUIEN. `textos` es {nombre: codigo}, para poder examinarlo con arboles
    sinteticos sin tocar el repositorio real."""
    usos = {m: set() for m in modulos}
    for quien, texto in textos.items():
        for m in usos:
            if quien == m:
                continue
            if re.search(rf"^\s*(import\s+{re.escape(m)}\b|from\s+{re.escape(m)}\s+import)",
                         texto, re.M):
                usos[m].add(quien)
    return usos


def citas(modulos, documentos):
    """QUIEN CITA A QUIEN, con extension. `documentos` es {ruta: contenido}."""
    hallado = {m: [] for m in modulos}
    for ruta, texto in documentos.items():
        for i, linea in enumerate(texto.splitlines(), 1):
            for m in hallado:
                if f"{m}.py" in linea:
                    hallado[m].append(f"{ruta}:{i}")
    return hallado


def _grep_pelado(modulos, textos, documentos):
    """LA LINEA BASE TONTA: el nombre pelado aparece o no aparece en algun otro archivo."""
    vivos = set()
    for quien, texto in textos.items():
        for m in modulos:
            if quien != m and re.search(rf"\b{re.escape(m)}\b", texto):
                vivos.add(m)
    for texto in documentos.values():
        for m in modulos:
            if re.search(rf"\b{re.escape(m)}\b", texto):
                vivos.add(m)
    return sorted(set(modulos) - vivos)


def _muertos(modulos, usos, citados):
    """Muerto = nadie lo importa Y nadie lo cita por su nombre de archivo."""
    return sorted(m for m in modulos if not usos.get(m) and not citados.get(m))


def _archivables(muertos, sellados):
    """ARCHIVABLE = muerto Y sin sello vigente. Un muerto SELLADO no se mueve: el sello se
    comprueba abriendo `codigo/<nombre>.py`, y moverlo lo mata igual que editarlo."""
    return [m for m in muertos if m not in sellados]


def _leer_codigo():
    d = os.path.join(BASE, "codigo")
    return {a[:-3]: open(os.path.join(d, a), encoding="utf-8").read()
            for a in sorted(os.listdir(d)) if a.endswith(".py")}


def _leer_documentos():
    docs = {}
    for carpeta in CARPETAS_DE_CITA:
        raiz = os.path.join(BASE, carpeta)
        if not os.path.isdir(raiz):
            continue
        for aqui, _, archivos in os.walk(raiz):
            for a in sorted(archivos):
                ruta = os.path.join(aqui, a)
                try:
                    docs[os.path.relpath(ruta, BASE)] = open(ruta, encoding="utf-8").read()
                except (UnicodeDecodeError, OSError):
                    continue     # un binario no cita a nadie
    return docs


def _sellados():
    """Los modulos con sello VIGENTE. Se pregunta a la puerta, que es quien sabe."""
    import metodo
    vigentes = set()
    ruta = getattr(metodo, "SELLOS", None)
    if not ruta or not os.path.exists(ruta):
        return vigentes
    for nombre in json.load(open(ruta, encoding="utf-8")):
        ok, _ = metodo.sello_valido(nombre)
        if ok:
            vigentes.add(nombre)
    return vigentes


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el censo distingue 'muerto' de 'entrada del arbol'?**
    Casi todos los estudios de este repositorio son puntos de entrada: NADIE los importa, nunca.
    Si el censo mirara solo el grafo de importaciones, los mataria a todos de golpe. Lo que los
    salva es la CITA de un acta, y esta ficha comprueba que esa via funciona en los dos sentidos."""
    fallos = []
    # una entrada del arbol —no la importa nadie— con cita de acta esta VIVA...
    solo = {"entrada": "import otro\n", "otro": "x=1\n"}
    mods = sorted(solo)
    con_cita = citas(mods, {"resultados/I.md": "`entrada.py` lo mide"})
    if "entrada" in _muertos(mods, importadores(mods, solo), con_cita):
        fallos.append("una entrada del arbol citada por un acta se cuenta como muerta")
    # ...y sin cita ninguna, esta muerta: si no, el censo no encontraria jamas un muerto
    if "entrada" not in _muertos(mods, importadores(mods, solo), citas(mods, {})):
        fallos.append("una entrada del arbol sin cita ni importacion se cuenta como viva")
    # y ninguna de las dos listas de partida puede estar vacia: revisar sobre vacio aprueba siempre
    if not CARPETAS_DE_CITA:
        fallos.append("CARPETAS_DE_CITA esta VACIA: sin corpus de citas todo saldria muerto")
    if not candidatos():
        fallos.append("no hay ni un candidato que examinar: el censo aprobaria sobre nada")
    return {"aprueba": not fallos, "fallos": fallos,
            "carpetas_de_cita": len(CARPETAS_DE_CITA), "candidatos": len(candidatos())}


# ---------------------------------------------------------------- las autopruebas, los dos lados

def _arbol_sintetico(muertos_plantados=1.0):
    """Un arbol de mentira hecho a mano, y es una MINIATURA FIEL del repositorio real:
      `raiz`  es un estudio: no lo importa nadie y lo salva UNA CITA de un acta;
      `vivo`  lo importa `raiz`;   `usado`  lo importa `vivo`;
      y se plantan N muertos que ni se importan ni se citan.
    La primera version de este arbol no le daba cita a la raiz, y el detector la conto como muerta
    — con razon. El arbol estaba mal, no el detector."""
    n = int(round(muertos_plantados))
    textos = {"raiz": "import vivo\n", "vivo": "import usado\n", "usado": "x = 1\n"}
    for i in range(n):
        textos[f"muerto{i}"] = "y = 2\n"
    return textos, {"resultados/INFORME-DE-MENTIRA.md": "lo mide `raiz.py`"}


def _metodo_medir(muertos_plantados=1.0):
    """La medida que la relacion metamorfica mueve: cuantos muertos halla en un arbol sintetico."""
    textos, docs = _arbol_sintetico(muertos_plantados)
    mods = sorted(textos)
    return float(len(_muertos(mods, importadores(mods, textos), citas(mods, docs))))


def regla31(verbose=True, devolver_casos=False):
    fallos = []
    casos = {}

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok   ' if ok else 'FALLO'} {nombre}{('  -> ' + extra) if extra else ''}")
        casos[nombre[0]] = bool(casos.get(nombre[0], True)) and bool(ok)
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("REGLA 31 de censo_muertos — sobre MI PROCEDIMIENTO, con arboles hechos a mano\n")

    # A — control positivo: encuentra EXACTAMENTE lo plantado, ni uno mas
    textos, docs = _arbol_sintetico(2)
    mods = sorted(textos)
    hallados = _muertos(mods, importadores(mods, textos), citas(mods, docs))
    caso("A encuentra exactamente los muertos plantados",
         hallados == ["muerto0", "muerto1"], f"hallo {hallados}")

    # B — el señuelo: si TODOS estan importados, no puede inventarse un cadaver
    todos_vivos = {"a": "import b\nimport c\n", "b": "import c\n", "c": "import a\n"}
    mods = sorted(todos_vivos)
    caso("B senuelo: con todos importados no inventa ningun muerto",
         _muertos(mods, importadores(mods, todos_vivos), citas(mods, {})) == [])

    # C — una cita en un acta salva al modulo, y solo si lleva la extension
    solo = {"solitario": "x=1\n"}
    con_ext = citas(["solitario"], {"resultados/INFORME-X.md": "lo mide `solitario.py` hoy"})
    sin_ext = citas(["solitario"], {"resultados/INFORME-X.md": "el modulo solitario lo mide"})
    caso("C una cita CON extension lo declara vivo",
         _muertos(["solitario"], importadores(["solitario"], solo), con_ext) == [])
    caso("C el nombre suelto en prosa NO lo salva",
         _muertos(["solitario"], importadores(["solitario"], solo), sin_ext) == ["solitario"])

    # D — la relacion metamorfica, con base distinta de cero
    f = METODO["formulas"][0]
    base = f["base"]["muertos_plantados"]
    antes, despues = _metodo_medir(base), _metodo_medir(base * f["factor"])
    caso(f"D mas muertos plantados = mas muertos hallados (base {base}, x{f['factor']})",
         despues > antes, f"{antes} -> {despues}")

    # E — el censo distingue MUERTO de ARCHIVABLE, y se examina por los DOS lados con la misma
    # funcion que usa la corrida real: sin sellos los dos muertos se archivan; con `muerto0`
    # sellado, ese se queda fuera y el otro sigue dentro.
    caso("E sin sellos, todo muerto es archivable",
         _archivables(["muerto0", "muerto1"], set()) == ["muerto0", "muerto1"])
    caso("E un muerto con sello vigente NO entra en archivables",
         _archivables(["muerto0", "muerto1"], {"muerto0"}) == ["muerto1"])

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el censo encuentra lo plantado y no inventa cadaveres"
                                if not fallos else f"REPRUEBA en {len(fallos)}: {fallos}"))
    if devolver_casos:
        return casos
    return 0 if not fallos else 1


# ---------------------------------------------------------------------------------- la corrida

def correr(salida=None, verbose=True):
    mods = candidatos()
    textos = _leer_codigo()
    docs = _leer_documentos()

    usos = importadores(mods, textos)
    citados = citas(mods, docs)
    muertos = _muertos(mods, usos, citados)
    sellados = _sellados()
    archivables = _archivables(muertos, sellados)
    inmovibles = [m for m in muertos if m in sellados]

    base_tonta = _grep_pelado(mods, textos, docs)
    discrepancias = {}
    for m in muertos:
        if m in base_tonta:
            continue                       # los dos coinciden: no hay nada que justificar
        donde = [f"{q}.py (importa? no)" for q in sorted(textos)
                 if q != m and re.search(rf"\b{re.escape(m)}\b", textos[q])]
        donde += [f"{r}:{i}" for r, t in docs.items()
                  for i, l in enumerate(t.splitlines(), 1) if re.search(rf"\b{re.escape(m)}\b", l)]
        discrepancias[m] = donde[:6]

    autopruebas = regla31(verbose=False, devolver_casos=True)

    censo = {m: {"lo_importan": sorted(usos[m]), "lo_citan": citados[m][:6],
                 "muerto": m in muertos, "sellado": m in sellados,
                 "archivable": m in archivables} for m in mods}

    datos = {
        "prerregistro": 59,
        "candidatos": len(mods),
        "muertos": muertos,
        "archivables": archivables,
        "inmovibles_por_sello": inmovibles,
        "linea_base_tonta_grep": base_tonta,
        "discrepancias_con_la_linea_base": discrepancias,
        "censo": censo,
        "criterios": {
            "A_encuentra_lo_plantado": bool(autopruebas.get("A")),
            "B_no_acusa_a_quien_tiene_cita": bool(autopruebas.get("B") and autopruebas.get("C")),
            "C_le_gana_a_la_linea_base": bool(discrepancias),
            "D_ningun_sellado_entre_los_archivables": not (set(archivables) & sellados),
            "E_no_toca_nada": True,   # la unica escritura de este modulo es su --salida
        },
    }
    if not datos["criterios"]["A_encuentra_lo_plantado"]:
        datos["veredicto"] = "SE DESCARTA EL CENSO — reprueba sus propias autopruebas"
    elif not datos["criterios"]["D_ningun_sellado_entre_los_archivables"]:
        datos["veredicto"] = ("SE DESCARTA EL CENSO — propone mover un modulo SELLADO, que es "
                              "proponer romper el acta que ese modulo publico")
    elif not datos["criterios"]["C_le_gana_a_la_linea_base"]:
        datos["veredicto"] = ("EL CENSO NO APORTA NADA SOBRE UN grep — no halla ni un muerto que "
                              "el nombre pelado no hallara ya. Es una forma cara de hacer grep y "
                              "asi queda escrito")
    else:
        datos["veredicto"] = (f"{len(muertos)} MODULO(S) MUERTO(S) de {len(mods)}: "
                              f"{len(archivables)} archivable(s) y {len(inmovibles)} "
                              f"inmovible(s) por sello vigente")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"candidatos (ni organos ni guardianes): {len(mods)}")
        print(f"muertos: {len(muertos)} -> {muertos}")
        print(f"  archivables (sin sello vigente): {archivables}")
        print(f"  INMOVIBLES por sello vigente:    {inmovibles}")
        print(f"linea base tonta (grep del nombre pelado): {len(base_tonta)} -> {base_tonta}")
        print(f"discrepancias que el censo debe justificar: {len(discrepancias)}")
        for m, donde in sorted(discrepancias.items()):
            print(f"  {m}: aparece en {donde}")
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 59: el censo de los muertos")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p59-censo-muertos/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
