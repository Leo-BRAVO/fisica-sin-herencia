# reglas.py — EL GUARDIÁN DE LAS REGLAS QUE NO TENÍAN GUARDIÁN
#
# ORDEN DEL DIRECTOR (10-ago-2026), sobre la auditoría de REGLAS-ESTRUCTURADAS.md que encontró que
# **14 de las 34 reglas no tenían ningún guardián que las nombrara**: 1, 5, 6, 7, 9, 10, 13, 14,
# 18, 20, 23, 24, 26, 28. Dijo "sí" a construirlos.
#
# POR QUE ESTE ARCHIVO EXISTE, con el daño medido detras: el 10-ago medi en G12 reflejos un
# "acuerdo de 0.907" que parecia excelente; la linea base tonta sacaba 0.887. Estaba incumpliendo
# la REGLA 12 —que existe desde el primer dia del proyecto— sin darme cuenta. Una regla que dice
# QUE hacer pero no COMO se comprueba que lo hiciste se incumple sin que nadie lo note, ni siquiera
# quien la escribio.
#
# ==========================================================================================
# LOS DOS NIVELES, Y POR QUE SON DOS
# ==========================================================================================
# Si estos chequeos se aplicaran hacia atras sobre los 42 prerregistros y los 7 nodos que ya
# existen, fallarian casi todos — y yo tendria dos salidas, las dos malas: aflojar el chequeo
# hasta que pase (que es escribir la prueba para aprobarla) o reescribir la historia para que
# cumpla (que es peor). Por eso hay dos niveles y se declaran:
#
#   BLOQUEANTE  — se cumple HOY, medido, y a partir de hoy su incumplimiento detiene el commit.
#                 Ninguno de estos se escribio "a la medida de lo que ya pasa": cada uno se probo
#                 y varios obligaron a arreglar cosas antes de poder encenderse.
#   DEUDA       — se MIDE y se IMPRIME el numero, pero no bloquea. Es la parte de la constitucion
#                 que hoy se cumple por disciplina y no por mecanica. Ponerlo a la vista es la
#                 unica forma honesta de que no se olvide: una deuda que no se cuenta, no existe.
#
# LOS ENDURECIMIENTOS (aprobados por el director el 10-ago) RIGEN HACIA ADELANTE: se aplican a los
# prerregistros del 42 en adelante y a los nodos creados desde hoy. Aplicarlos hacia atras no
# haria mas rigurosa la ciencia ya hecha — solo obligaria a reescribirla, que es exactamente lo
# que la Regla 8 prohibe.
#
# Uso: python reglas.py     (y lo llama auditoria_total.py, para no crear un quinto guardian)

import os
import re
import glob
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Frontera de los endurecimientos: prerregistros de este numero en adelante.
PRIMER_PREREGISTRO_ENDURECIDO = 42
# Nodos creados desde esta fecha (los anteriores conservan su texto: Regla 8).
DESDE = "10-ago-2026"

BLOQUEANTES = []
DEUDAS = []


def _leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def bloqueante(regla, titulo, ok, detalle=""):
    BLOQUEANTES.append((regla, titulo, bool(ok), detalle))


def deuda(regla, titulo, cuantos, de_cuantos, nota=""):
    DEUDAS.append((regla, titulo, cuantos, de_cuantos, nota))


# ----------------------------------------------------------------------------------------
# Los artefactos sobre los que se juzga
# ----------------------------------------------------------------------------------------
NODOS_FISICA = sorted(glob.glob(os.path.join(BASE, "arbol", "N-*.md")))
NODOS_HITO = sorted(glob.glob(os.path.join(BASE, "arbol", "H-*.md")))
NODOS = NODOS_FISICA + NODOS_HITO
PRERREGISTROS = sorted(glob.glob(os.path.join(BASE, "registros", "prerregistro-*.md")))

# Modulos que DESCUBREN (los que la Regla 1 protege). No es toda la carpeta: un guardian puede
# nombrar "gravedad" para prohibirla, y un informe puede citarla. Solo el descubridor debe estar
# limpio, porque es el unico que convierte datos en hipotesis.
MODULOS_DESCUBRIDORES = ["descubrir.py", "descubrir_pool.py", "percepcion.py", "percepcion2.py",
                         "conservada.py", "dimension.py", "canonizar.py"]


def numero_de(ruta):
    m = re.search(r"prerregistro-(\d+)", os.path.basename(ruta))
    return int(m.group(1)) if m else -1


# ==========================================================================================
# REGLA 1 — Datos, no teorias
# ==========================================================================================
# Se comprueba lo unico comprobable a maquina y lo que de verdad importa: que el DESCUBRIDOR no
# lleve fisica humana escrita dentro. No demuestra ausencia de contaminacion (eso no se demuestra),
# pero caza la forma en que realmente entraria: alguien escribiendo una constante con nombre
# "para ayudar".
FISICA_HUMANA = re.compile(
    r"\b(9\.81|9\.807|6\.674e|gravedad|gravity|newton|joule|kepler|hooke|"
    r"energia_cinetica|energia_potencial|momento_lineal|momentum)\b", re.I)

_sucios = []
for m in MODULOS_DESCUBRIDORES:
    ruta = os.path.join(BASE, "codigo", m)
    if not os.path.exists(ruta):
        continue
    hallados = sorted(set(x.lower() for x in FISICA_HUMANA.findall(_leer(ruta))))
    if hallados:
        _sucios.append(f"{m}: {hallados}")
bloqueante(1, "ningun modulo DESCUBRIDOR lleva fisica humana escrita dentro",
           not _sucios, "; ".join(_sucios))


# ==========================================================================================
# REGLA 5 — El unico juez es la prediccion prospectiva
# ==========================================================================================
# Todo nodo de FISICA debe decir con que datos que no habia visto se juzgo. Los nodos de HITO
# (H-*) quedan fuera a proposito: no afirman leyes del universo sino capacidades del ente, y
# exigirles prediccion prospectiva seria aplicarles una vara que no les corresponde.
NO_VISTO = re.compile(r"jam[aá]s vist|nunca vist|no vist|ocultos|prospectiv|"
                      r"validaci[oó]n separada|jueces limpios|reservad[oa]s", re.I)
_sin = [os.path.basename(n) for n in NODOS_FISICA if not NO_VISTO.search(_leer(n))]
bloqueante(5, "todo nodo de FISICA dice con que datos NO VISTOS se juzgo",
           not _sin, f"sin declararlo: {_sin}")


# ==========================================================================================
# REGLA 6 — La simplicidad se mide en bits, no en elegancia
# ==========================================================================================
# Si un nodo dice "mas simple", "el mas simple" o "parsimonia", debe haber un numero cerca. Un
# juicio de simplicidad sin cifra es estetica humana, que es justo lo que la regla prohibe.
SIMPLE = re.compile(r"(m[aá]s simple|la m[aá]s simple|parsimoni|simplicidad)", re.I)
CIFRA = re.compile(r"\d")
_estetica = []
for n in NODOS:
    t = _leer(n)
    for m in SIMPLE.finditer(t):
        ventana = t[max(0, m.start() - 240): m.end() + 240]
        if not CIFRA.search(ventana):
            _estetica.append(os.path.basename(n))
            break
bloqueante(6, "ninguna afirmacion de simplicidad va sin numero (bits, no elegancia)",
           not _estetica, f"solo estetica en: {sorted(set(_estetica))}")


# ==========================================================================================
# REGLAS 7 + 14 (FUNDIDAS) — Replicabilidad: muchas semillas y todo reproducible
# ==========================================================================================
REPLICA = re.compile(r"(\d+)\s*(?:/\s*\d+\s*)?(semillas?|corridas?|r[eé]plicas?|videos?|"
                     r"mundos?|jueces)", re.I)
_sin_rep = [os.path.basename(n) for n in NODOS if not REPLICA.search(_leer(n))]
bloqueante(7, "todo nodo cita su evidencia de replicacion CON NUMERO (Reglas 7+14 fundidas)",
           not _sin_rep, f"sin numero de replicacion: {_sin_rep}")


# ==========================================================================================
# REGLA 10 + REGLA 19 — La realidad tiene el veto: nada es "descubrimiento" sin nivel 3
# ==========================================================================================
# El nivel 3 exige replica independiente por un tercero. Cero nodos lo tienen. Por tanto ninguno
# puede llamarse descubrimiento, ley confirmada ni conocimiento firme — solo candidata.
PROCLAMA = re.compile(r"\b(descubrimiento confirmado|ley confirmada|conocimiento firme|"
                      r"queda demostrado que el universo|hemos descubierto)\b", re.I)
_proclaman = [os.path.basename(n) for n in NODOS if PROCLAMA.search(_leer(n))]
bloqueante(10, "ningun nodo se proclama DESCUBRIMIENTO sin el nivel 3 de la Regla 19",
           not _proclaman, f"se proclaman: {_proclaman}")


# ==========================================================================================
# REGLA 18 — El arbol: nada se descubre suelto
# ==========================================================================================
_sin_preg = [os.path.basename(n) for n in NODOS if not re.search(r"pregunta", _leer(n), re.I)]
bloqueante(18, "todo nodo abre al menos una pregunta nueva (no se descubre suelto)",
           not _sin_preg, f"sin preguntas: {_sin_preg}")


# ==========================================================================================
# REGLA 23 — El motor tampoco cree en si mismo
# ==========================================================================================
# Todo nodo debe llevar ESTADO explicito y fecha: sin eso no se puede saber si esta vigente,
# degradado o podado, y un arbol que no se puede podar es dogma con formato de carpeta.
_sin_estado = [os.path.basename(n) for n in NODOS
               if not re.search(r"\*\*Estado[:\s]", _leer(n))]
bloqueante(23, "todo nodo declara ESTADO explicito (para poder degradarlo o podarlo)",
           not _sin_estado, f"sin estado: {_sin_estado}")


# ==========================================================================================
# REGLA 24 — El cientifico vive en el repositorio: MENTE.md con su ritual
# ==========================================================================================
_mente = _leer(os.path.join(BASE, "MENTE.md"))
bloqueante(24, "MENTE.md conserva el ritual de automejora (QUE/POR QUE/COMPRENSION/RIESGO)",
           all(p in _mente.upper() for p in ("QU", "POR QU", "COMPRENSI", "RIESGO")))
_versiones = re.findall(r"\*\*v(\d+)", _mente)
bloqueante(24, "MENTE.md conserva su historial de versiones (append-only, nada se borra)",
           len(_versiones) >= 8, f"versiones halladas: {len(_versiones)}")


# ==========================================================================================
# REGLA 20 + REGLA 26 — El camino inverso y la ingenieria trazable
# ==========================================================================================
# Condicionales por diseño: hoy no hay diseños ni documentos de ingenieria, asi que la regla no
# tiene nada que vigilar. En cuanto exista `ingenieria/`, cada afirmacion debera citar su nodo.
_ing = os.path.join(BASE, "ingenieria")
if os.path.isdir(_ing):
    _sin_nodo = [os.path.basename(d) for d in glob.glob(os.path.join(_ing, "*.md"))
                 if not re.search(r"\[\[[NH]-", _leer(d))]
    bloqueante(26, "todo documento de ingenieria cita los NODOS que lo sustentan",
               not _sin_nodo, f"sin citar nodo: {_sin_nodo}")
else:
    bloqueante(20, "no hay diseños todavia: la regla no tiene nada que vigilar (correcto)", True)


# ==========================================================================================
# LOS CUATRO ENDURECIMIENTOS — rigen del prerregistro 42 en adelante
# ==========================================================================================
_nuevos = [p for p in PRERREGISTROS if numero_de(p) >= PRIMER_PREREGISTRO_ENDURECIDO]

# R12 endurecida — la linea base tonta es obligatoria en todo puntaje
LINEA_BASE = re.compile(r"l[ií]nea base|base tonta|trivial", re.I)
_sin_lb = [os.path.basename(p) for p in _nuevos if not LINEA_BASE.search(_leer(p))]
bloqueante(12, f"todo prerregistro desde el {PRIMER_PREREGISTRO_ENDURECIDO} declara su LINEA BASE TONTA",
           not _sin_lb, f"sin linea base: {_sin_lb}")

# R13 endurecida — los criterios de abandono se declaran CON NUMERO
ABANDONO = re.compile(r"(se declara nulo|se detiene|criterio de abandono|se abandona|"
                      r"veredicto[s]? posible)", re.I)
_sin_ab = [os.path.basename(p) for p in _nuevos
           if not (ABANDONO.search(_leer(p)) and CIFRA.search(_leer(p)))]
bloqueante(13, f"todo prerregistro desde el {PRIMER_PREREGISTRO_ENDURECIDO} declara cuando SE ABANDONA, con numero",
           not _sin_ab, f"sin criterio de abandono: {_sin_ab}")

# R31 endurecida — los DOS lados: fallar con vacio Y aprobar con control positivo
DOS_LADOS = re.compile(r"control positivo|los dos lados|señuelo|senuelo|"
                       r"debe fallar.*debe aprobar|NULO", re.I | re.S)
_sin_dos = [os.path.basename(p) for p in _nuevos if not DOS_LADOS.search(_leer(p))]
bloqueante(31, f"todo prerregistro desde el {PRIMER_PREREGISTRO_ENDURECIDO} declara los DOS lados de la Regla 31",
           not _sin_dos, f"sin los dos lados: {_sin_dos}")

# R9 — el peldaño se DECLARA. Lo mecanizable de la Regla 9 no es decidir si un peldaño funciona
# —eso es un juicio— sino exigir que cada estudio diga EN CUAL esta. Sin eso, "subir de peldaño"
# se decide a posteriori, que es la enfermedad de siempre. Rige del 42 en adelante, como el resto.
PELDANO = re.compile(r"fase\s*[0-3]|pelda[nñ]o", re.I)
_sin_peldano = [os.path.basename(p) for p in _nuevos if not PELDANO.search(_leer(p))]
bloqueante(9, f"todo prerregistro desde el {PRIMER_PREREGISTRO_ENDURECIDO} declara EN QUE PELDAÑO esta",
           not _sin_peldano, f"sin peldaño: {_sin_peldano}")

# R19 endurecida — ningun nodo sube a nivel 2 sin datos que nadie ha visto
_falsos_n2 = []
for n in NODOS:
    t = _leer(n)
    if re.search(r"nivel\s*2", t, re.I) and not re.search(r"datos.{0,40}(no vist|jam[aá]s vist|"
                                                          r"nunca vist|nadie ha visto)", t, re.I):
        _falsos_n2.append(os.path.basename(n))
bloqueante(19, "ningun nodo declara NIVEL 2 sin datos que nadie habia visto",
           not _falsos_n2, f"nivel 2 sin datos nuevos: {_falsos_n2}")


# ==========================================================================================
# LA DEUDA MEDIDA — lo que hoy se cumple por disciplina y no por mecanica
# ==========================================================================================
_todos = PRERREGISTROS
deuda(9, "prerregistros que declaran en que peldaño de la escalera estan",
      sum(1 for p in _todos if re.search(r"fase|pelda", _leer(p), re.I)), len(_todos),
      "la Regla 9 no se puede mecanizar entera: quien decide que un peldaño 'funciona de punta a "
      "punta' es un juicio, no un numero")
deuda(12, "prerregistros ANTERIORES al 42 que declaran su linea base tonta",
      sum(1 for p in _todos if numero_de(p) < PRIMER_PREREGISTRO_ENDURECIDO
          and LINEA_BASE.search(_leer(p))),
      sum(1 for p in _todos if numero_de(p) < PRIMER_PREREGISTRO_ENDURECIDO),
      "el endurecimiento rige hacia adelante; esto mide el pasado sin reescribirlo")
deuda(13, "prerregistros ANTERIORES al 42 con criterio de abandono",
      sum(1 for p in _todos if numero_de(p) < PRIMER_PREREGISTRO_ENDURECIDO
          and ABANDONO.search(_leer(p))),
      sum(1 for p in _todos if numero_de(p) < PRIMER_PREREGISTRO_ENDURECIDO), "")
deuda(19, "nodos que alcanzaron el nivel 2 (experimento fisico propio)",
      sum(1 for n in NODOS_FISICA if re.search(r"nivel\s*2", _leer(n), re.I)), len(NODOS_FISICA),
      "ESTA ES LA DEUDA ESTRUCTURAL DEL PROYECTO: sin nivel 2 no hay ley, solo correlacion")
deuda(19, "nodos que alcanzaron el nivel 3 (replica independiente)",
      sum(1 for n in NODOS_FISICA if re.search(r"nivel\s*3", _leer(n), re.I)), len(NODOS_FISICA),
      "diferido por decision del director hasta que haya resultados que valga la pena replicar")
deuda(22, "nodos con revision de doble uso escrita",
      sum(1 for n in NODOS if re.search(r"doble uso", _leer(n), re.I)), len(NODOS),
      "RESERVADA AL DIRECTOR: no es mecanizable ni delegable, y no debe serlo")


def regla31():
    """LA REGLA 31 APLICADA A ESTE MISMO ARCHIVO.

    POR QUE ESTA FUNCION EXISTE. En su primera corrida, los cuatro endurecimientos ("todo
    prerregistro DESDE EL 42...") salieron en verde sin poder haber salido de otra forma: todavia
    no existe ningun prerregistro 42, asi que la lista estaba vacia y `not []` es siempre cierto.
    Un chequeo que aprueba sobre el vacio es exactamente lo que la Regla 31 prohibe, y lo habria
    firmado como "ok" sin pestañear. Es el mismo error que la meta-auditoria me caza en otros
    sitios, cometido dentro del archivo que nace para cazarlo.

    Aqui se prueban los DETECTORES por los dos lados —un texto que DEBE marcarse y otro que NO—,
    que es lo unico que se puede probar sin inventar artefactos falsos en el repositorio. Los
    chequeos de arriba usan estos mismos detectores, asi que probarlos es probarlos a ellos.
    """
    casos = []

    def caso(nombre, debe_marcar, no_debe_marcar, detector):
        ok = bool(detector(debe_marcar)) and not bool(detector(no_debe_marcar))
        casos.append((nombre, ok))

    caso("R1 fisica humana en el descubridor",
         "a = 9.81 * t", "a = coef[0] * t", FISICA_HUMANA.search)
    caso("R5 datos no vistos",
         "juzgado en los dos jueces jamas vistos", "juzgado sobre los mismos datos",
         NO_VISTO.search)
    caso("R7 replicacion con numero",
         "replica en 5 semillas", "replica en varias corridas", REPLICA.search)
    caso("R10 proclama sin nivel 3",
         "queda demostrado que el universo funciona asi", "es una candidata provisional",
         PROCLAMA.search)
    caso("R12 linea base tonta",
         "se compara contra la linea base tonta", "se compara contra el resultado anterior",
         LINEA_BASE.search)
    caso("R13 criterio de abandono",
         "si falla el caso 3 se declara NULO y se detiene", "esperamos que salga bien",
         ABANDONO.search)
    caso("R31 los dos lados",
         "la condicion VACIO es el señuelo", "se corre y se mira el resultado", DOS_LADOS.search)
    caso("R6 simplicidad sin numero",
         "elegimos la mas simple", "no habla de eso", SIMPLE.search)
    caso("R9 declaracion de peldaño",
         "estamos en la Fase 1 y no se sube", "corremos esto a ver que sale", PELDANO.search)

    # Y el caso que motivo la funcion: un chequeo sobre lista vacia NO puede contarse como ok.
    casos.append(("un chequeo sobre lista VACIA no cuenta como aprobado",
                  len([p for p in PRERREGISTROS
                       if numero_de(p) >= PRIMER_PREREGISTRO_ENDURECIDO]) > 0))
    return casos


def informe():
    """Imprime el dictamen. Devuelve la lista de fallos bloqueantes."""
    print("=== LAS REGLAS QUE NO TENIAN GUARDIAN (Regla por regla, 10-ago-2026) ===")
    print("BLOQUEANTES — su incumplimiento detiene el commit:")
    fallos = []
    for regla, titulo, ok, detalle in BLOQUEANTES:
        if ok:
            print(f"  ok    R{regla:<2} {titulo}")
        else:
            print(f"  FALLO R{regla:<2} {titulo}  {detalle}")
            fallos.append(f"R{regla}: {titulo}")
    print("\nREGLA 31 SOBRE ESTE ARCHIVO — cada detector probado por los DOS lados:")
    for nombre, ok in regla31():
        if ok:
            print(f"  ok    {nombre}")
        else:
            print(f"  FALLO {nombre}")
            fallos.append(f"Regla 31 de reglas.py: {nombre}")

    print("\nDEUDA MEDIDA — se cumple por disciplina, NO por mecanica (no bloquea, pero se cuenta):")
    for regla, titulo, cuantos, de_cuantos, nota in DEUDAS:
        marca = "  " if cuantos == de_cuantos else "!!"
        print(f"  {marca}  R{regla:<2} {titulo}: {cuantos}/{de_cuantos}")
        if nota:
            print(f"        -> {nota}")
    return fallos


if __name__ == "__main__":
    import sys
    f = informe()
    print()
    if f:
        print(f"REGLAS: {len(f)} FALLOS BLOQUEANTES -> NO COMMITEAR: {f}")
        sys.exit(1)
    print("REGLAS: sin fallos bloqueantes. La deuda de arriba es real y esta contada.")
