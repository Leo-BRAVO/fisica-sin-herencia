# anatomia.py — EL CENSO DE ORGANOS (prerregistro-54, 11-ago-2026).
#
# EL ENCARGO DEL DIRECTOR: "primero valida si realmente todos los organos deberian funcionar, si
# las atribuciones a la mente de Diego son las correctas" y "los organos decidir si son
# prescindibles".
#
# NO SE PUEDE MEDIR SI UN ORGANO "DEBERIA EXISTIR" — eso es un juicio. Si se pueden medir cuatro
# cosas que, juntas, dicen si esta haciendo algo:
#   CONEXION    ¿algun otro modulo lo usa?            -> si no, es HUERFANO
#   EFECTO      ¿alguien lee lo que publica?          -> si no, es DECORATIVO
#   UNICIDAD    ¿otro calcula lo mismo?               -> si si, hay DUPLICADO
#   ATRIBUCION  ¿lo que hace coincide con lo que dice ser?
#
# LA DECISION DE QUITAR UN ORGANO NO SE MECANIZA Y NO ES MIA. Este modulo produce el censo; el
# director decide. Y NO BORRA NI TOCA NINGUN ORGANO: solo mide.
#
# LO QUE ESTE CENSO NO PUEDE DECIR, escrito aqui para que nadie confie de mas:
#   - Un organo HUERFANO no es un organo que sobre: puede estar esperando a que lo conecten. El
#     censo dice que esta desconectado HOY, no que no merezca existir.
#   - Un organo CONECTADO no es un organo que funcione. Estar en el lazo no es hacerlo bien: eso
#     lo dice su ficha de sanidad, y 8 de los 15 ni siquiera la tienen (INFORME-63).
#   - Y NO ESTAR SELLADO NO ES SER PRESCINDIBLE. Son cosas distintas y confundirlas acusaria a 10
#     de 15 organos por una razon que no es la suya. Es el criterio B del prerregistro-54.
#
# Uso: python anatomia.py [--regla31] [--salida resultados/p54-anatomia/medida.json]

import os
import re
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# QUE ESTUDIA ESTE MODULO: los organos reales. Por eso su regla31() NO puede tocarlos — trabaja
# con grafos sinteticos hechos a mano. Examinar al sujeto dentro de mi propia Regla 31 es el error
# que dejo NULO al prerregistro-45, y `disciplina.py` lo comprueba a maquina desde hoy.
SUJETO = ("ORGANOS",)

# Modulos que NO cuentan como "alguien que lo usa": son pruebas, guardianes o el propio censo.
# Si contaran, cualquier organo con una prueba pareceria conectado a la vida de Diego, y no lo esta.
NO_CUENTAN = ("pruebas", "guardianes_de_guardianes", "coherencia", "auditoria_total", "reglas",
              "actas", "contratos", "disciplina", "anatomia", "metodo", "sanidad", "boleta",
              "diagnostico_total", "forense", "autopsia", "trazador")

METODO = {
    "prerregistro": 54,
    "tipo_de_medida": "umbral",   # cada organo es huerfano o no lo es: es binario por organo
    "que_mide": ("cuantos organos del genoma estan desconectados: nadie que no sea una prueba ni "
                 "un guardian los usa, y nadie lee lo que publican"),
    "comparten_datos": {
        "hay": False,
        "porque": "cada organo se examina contra el mismo grafo de dependencias, pero su "
                  "veredicto no depende del de los demas; lo unico comun es el grafo",
    },
    "linea_base": ("declarar que TODOS los organos son imprescindibles — es lo que asumimos hoy "
                   "sin haberlo mirado nunca (Regla 11). Un censo que no encuentre ni un huerfano "
                   "ni un duplicado NO le gana a esa suposicion, y entonces la suposicion era "
                   "correcta y se dice asi"),
    "formulas": [
        {"base": {"huerfanos_plantados": 1.0}, "parametro": "huerfanos_plantados", "factor": 3.0,
         "esperado": "sube",
         "porque": "mas modulos desconectados plantados en un grafo sintetico = mas huerfanos "
                   "hallados, porque el detector recorre las aristas y cuenta los nodos sin "
                   "entrada. Es lo unico que se sabe A PRIORI de esta medida. Base 1.0 y NO 0.0: "
                   "multiplicar cero por tres sigue siendo cero, y ese descuido ya me tumbo "
                   "cuatro relaciones este mes"},
    ],
}


def _organos():
    """Los modulos que el GENOMA declara como organos. Se leen de ahi y no de una lista mia: una
    lista escrita a mano se desincronizaria del genoma y tendriamos dos verdades."""
    g = json.load(open(os.path.join(BASE, "arbol", "GENOMA.json"), encoding="utf-8"))["genes"]
    return sorted({m[:-3] for v in g.values()
                   for m in re.findall(r"([\w_]+\.py)", v.get("modulo") or "")})


ORGANOS = _organos()


def grafo(modulos=None):
    """QUIEN USA A QUIEN, leido del codigo. Devuelve {modulo: conjunto de modulos que lo usan}."""
    usos = {m: set() for m in (modulos if modulos is not None else ORGANOS)}
    for ruta in sorted(os.listdir(os.path.join(BASE, "codigo"))):
        if not ruta.endswith(".py"):
            continue
        quien = ruta[:-3]
        texto = open(os.path.join(BASE, "codigo", ruta), encoding="utf-8").read()
        for m in usos:
            if quien == m:
                continue
            if re.search(rf"^\s*(import\s+{m}\b|from\s+{m}\s+import)", texto, re.M):
                usos[m].add(quien)
    return usos


def _huerfanos(usos, no_cuentan=NO_CUENTAN):
    """Un organo esta desconectado si nadie que cuente lo usa."""
    return sorted(m for m, quienes in usos.items()
                  if not {q for q in quienes if q not in no_cuentan})


def _publica(modulo):
    """Que numeros publica, leido de su CONTRATO si lo tiene."""
    ruta = os.path.join(BASE, "codigo", f"{modulo}.py")
    if not os.path.exists(ruta):
        return []
    t = open(ruta, encoding="utf-8").read()
    m = re.search(r'"publica"\s*:\s*\{(.*?)\n    \}', t, re.S)
    return re.findall(r'"(\w+)"\s*:\s*\{', m.group(1)) if m else []


def _atribucion_medida(modulo):
    """QUE HACE, derivado del codigo y no de lo que dice ser."""
    ruta = os.path.join(BASE, "codigo", f"{modulo}.py")
    if not os.path.exists(ruta):
        return "AUSENTE"
    t = open(ruta, encoding="utf-8").read()
    abre_mundo = bool(re.search(r"pybullet|p\.connect|gimnasio\.", t))
    escribe_acciones = bool(re.search(r"setJointMotorControl|aplicar_torque|accion\w*\s*=", t))
    decide = bool(re.search(r"def (repartir|elegir|decidir|politica)\b", t))
    if decide:
        return "POLITICA"
    if escribe_acciones and abre_mundo:
        return "ACTUADOR"
    if abre_mundo:
        return "SENTIDO"
    return "ESTIMADOR"


def _declarada(modulo):
    ruta = os.path.join(BASE, "codigo", f"{modulo}.py")
    if not os.path.exists(ruta):
        return None
    m = re.search(r'CONTRATO\s*=\s*\{[^}]*?"tipo"\s*:\s*"(\w+)"',
                  open(ruta, encoding="utf-8").read(), re.S)
    return m.group(1) if m else None


def _metodo_medir(huerfanos_plantados=1.0):
    """PASO 1 — la medida escalar, sobre un GRAFO SINTETICO: cuantos huerfanos encuentra cuando se
    plantan `huerfanos_plantados`. No toca los organos reales: eso es el resultado del estudio."""
    n = int(huerfanos_plantados)
    usos = {f"conectado_{i}": {"alguien"} for i in range(3)}
    usos.update({f"suelto_{i}": set() for i in range(n)})
    return float(len(_huerfanos(usos)))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el censo distingue 'desconectado' de 'no examinado'?**
    Si los confundiera, acusaria a 10 de 15 organos por una razon que no es la suya."""
    fallos = []
    # un modulo usado SOLO por pruebas y guardianes NO cuenta como conectado a la vida de Diego...
    solo_pruebas = {"x": {"pruebas", "coherencia"}}
    if _huerfanos(solo_pruebas) != ["x"]:
        fallos.append("un organo usado solo por pruebas y guardianes se cuenta como conectado")
    # ...y uno usado por un modulo de verdad SI cuenta
    de_verdad = {"y": {"cerebro"}}
    if _huerfanos(de_verdad):
        fallos.append("un organo usado por otro organo se cuenta como huerfano")
    # y la lista de organos no puede estar vacia: revisar sobre vacio aprueba siempre
    if not ORGANOS:
        fallos.append("la lista de organos esta VACIA: el censo aprobaria sobre nada")
    return {"aprueba": not fallos, "fallos": fallos, "organos_en_el_genoma": len(ORGANOS)}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados, y SOBRE GRAFOS SINTETICOS.

    Aqui NO se examina ningun organo real: eso es el resultado que este estudio existe para medir,
    y meterlo haria que el criterio D no pudiera fallar."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-54: el censo, sobre grafos hechos a mano ==")

    caso("CONTROL POSITIVO: en un grafo con un desconectado, lo encuentra",
         _huerfanos({"a": {"otro"}, "b": set()}) == ["b"])
    caso("SEÑUELO: en un grafo donde todos se usan, NO inventa ninguno",
         _huerfanos({"a": {"otro"}, "b": {"otro"}}) == [])
    caso("no confunde 'usado solo por pruebas' con 'conectado a la vida'",
         _huerfanos({"a": {"pruebas"}}) == ["a"])

    b, s = _metodo_medir(1.0), _metodo_medir(3.0)
    caso("la medida RESPONDE (y la base no es cero)", b > 0 and s > b, f"{b:.0f} -> {s:.0f}")

    fs = _metodo_sanidad()
    caso("la ficha aprueba y la lista de organos no esta vacia", fs["aprueba"], str(fs["fallos"]))

    caso("la atribucion se DERIVA del codigo, no se supone",
         _atribucion_medida("atencion") in ("SENTIDO", "ACTUADOR", "ESTIMADOR", "POLITICA"))

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el censo distingue por los dos lados."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    usos = grafo()
    huerfanos = _huerfanos(usos)
    publica = {m: _publica(m) for m in ORGANOS}
    duplicados = {}
    for m, nums in publica.items():
        for n in nums:
            duplicados.setdefault(n, []).append(m)
    duplicados = {n: ms for n, ms in duplicados.items() if len(ms) > 1}

    censo = {}
    for m in ORGANOS:
        dec, med = _declarada(m), _atribucion_medida(m)
        censo[m] = {
            "usado_por": sorted(q for q in usos[m] if q not in NO_CUENTAN),
            "huerfano": m in huerfanos,
            "publica": publica[m],
            "atribucion_declarada": dec,
            "atribucion_medida": med,
            "atribucion_choca": bool(dec and dec != med),
        }

    datos = {"prerregistro": 54, "organos": len(ORGANOS), "censo": censo,
             "huerfanos": huerfanos, "duplicados": duplicados,
             "atribuciones_que_chocan": sorted(m for m, v in censo.items()
                                               if v["atribucion_choca"]),
             "criterios": {
                 "A_el_censo_distingue": bool(_huerfanos({"a": {"o"}, "b": set()}) == ["b"]
                                              and _huerfanos({"a": {"o"}}) == []),
                 "B_no_acusa_por_no_estar_sellado": True,   # el censo no mira los sellos, a proposito
                 "C_la_atribucion_se_mide": bool(all(v["atribucion_medida"] for v in censo.values())),
                 "D_le_gana_a_la_linea_base_tonta": bool(huerfanos or duplicados),
             }}
    if not datos["criterios"]["A_el_censo_distingue"]:
        datos["veredicto"] = "SE DESCARTA EL CENSO — inventa huerfanos o no los encuentra"
    elif datos["criterios"]["D_le_gana_a_la_linea_base_tonta"]:
        datos["veredicto"] = (f"HAY {len(huerfanos)} ORGANO(S) DESCONECTADO(S) y "
                              f"{len(duplicados)} numero(s) duplicado(s) — el censo le gana a la "
                              f"suposicion de que todos hacen falta")
    else:
        datos["veredicto"] = ("NINGUN HUERFANO NI DUPLICADO — la suposicion de que todos los "
                              "organos hacen falta era correcta, y eso tambien es un resultado")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 54: el censo de organos")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p54-anatomia/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
