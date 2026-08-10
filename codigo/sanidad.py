# sanidad.py — LA FICHA DE SANIDAD: lo que hay que comprobar ANTES de escribir la Regla 31.
#
# POR QUE EXISTE, dicho sin adornos. El director lo señalo el 10-ago-2026: "cada cosa nueva te das
# cuenta que cometiste errores... como solventamos que evites tantos errores al armar las pruebas".
# Tenia razon. Conte mis propios fallos de esta sesion: CATORCE, en seis modulos. Pero no son
# catorce errores distintos — son CINCO TIPOS que repito:
#
#   A. LA MEDIDA NO MIDE LO QUE CREO (5 veces). El std agrupado media la geometria del montaje y no
#      el movimiento. 'frenado' correlacionaba -0.586 con la MASA y -0.344 con el roce: leia la
#      propiedad equivocada. El 'avance' mezclaba masa y roce. El margen saturaba en -0.4000. El
#      max(margen,0) media su propio suelo.
#   B. LA TRAMOYA DEL SIMULADOR SE CUELA COMO SI FUERA FISICA (3 veces). El re-soltado parecia caos.
#      El asentamiento delataba la masa. Objetos que "reposaban" a 4.5 cm del suelo.
#   C. DOS CONDICIONES QUE SON LA MISMA POR CONSTRUCCION (2 veces, y la segunda al dia siguiente de
#      diagnosticar la primera). El pasivo heredaba los episodios del dirigido -> 0.0000 EXACTO.
#   D. REGIMEN DEGENERADO: cocientes con denominador casi cero (2 veces). 1e-9 sobre 1e-10 daba
#      -0.80 sin que nada hubiera pasado. 'flota' daba +0.9999 con un coeficiente de 3.500.
#   E. RESTOS DE VERSIONES ANTERIORES (1 vez). Una applyExternalForce duplicada: doble impulso.
#   F. DESLICES DE ESCRITURA (2 veces, añadido a peticion del director el 10-ago). Una 'a' CIRILICA
#      dentro de un nombre de variable, invisible a cualquier busqueda. Y comillas invertidas sin
#      escapar en un mensaje de commit, que bash ejecuto y borro.
#
# EL AGUJERO ESTRUCTURAL, que es el hallazgo de verdad:
#   **Todos mis casos de Regla 31 comprueban que el instrumento hace lo que YO QUISE.
#     NINGUNO comprueba que lo que yo quise fuera correcto.**
#   La Regla 31 valida el diseño contra mis propias suposiciones. Si la suposicion esta mal, la
#   Regla 31 aprueba con entusiasmo. Por eso los fallos aparecen SIEMPRE al correr y nunca al
#   escribir.
#
# LA CURA: esta ficha compara el instrumento contra la VERDAD DEL SIMULADOR — lo que el mundo sabe
# y yo no le he preguntado. Se pasa ANTES de escribir la Regla 31, no despues.
#
# FRONTERA (Regla 27): la verdad del simulador se usa aqui, del LADO HUMANO, para validar el
# instrumento — exactamente como el comparador. JAMAS entra a los datos, prompts o herramientas de
# Diego. Un modulo que le pase `verdad` a una politica esta contaminado, y el caso 6 lo comprueba.

import ast
import os

import numpy as np

PISO_CORRELACION = 0.60   # una lectura debe correlacionar con lo suyo por encima de esto
TECHO_CONFUSION = 0.15    # ...y la propiedad ajena no puede añadir mas de este 15% de
                          # varianza EXTRA a la lectura, una vez ya esta la propia


def correlaciones(lecturas, verdad, nombres=None):
    """TIPO A — ¿cada lectura mide lo suyo, y NO lo de al lado?
    `lecturas`: dict nombre -> lista de valores medidos, uno por objeto/canal.
    `verdad`:   dict nombre -> lista de valores reales (del simulador, lado humano).
    Las claves deben emparejar: lecturas['masa'] se contrasta con verdad['masa'].

    Habria cazado, sin correr el estudio: el std agrupado (corr con lo suyo ~0), 'frenado'
    (corr -0.34 con lo suyo y -0.59 con lo ajeno) y 'avance' (mezclaba las dos)."""
    claves = list(verdad.keys())
    tabla, fallos = {}, []
    for k in claves:
        if k not in lecturas:
            fallos.append(f"{k}: no hay lectura")
            continue
        propia = abs(_corr(lecturas[k], verdad[k]))
        # PARCIAL, no bruta. Cazado por la meta-prueba de esta misma ficha en su primera corrida —
        # un tipo A dentro del detector de tipos A: si las dos VERDADES estan correlacionadas entre
        # si (en aquel sorteo, masa y roce iban a 0.806), una lectura PERFECTA de una arrastra a la
        # otra y el detector la condenaba por contaminada. Lo que hay que preguntar es si queda
        # confusion DESPUES de descontar lo que la lectura ya explica de lo suyo.
        # CUANTA VARIANZA AÑADE LA PROPIEDAD AJENA, no en que direccion apunta el residuo. Tercera
        # correccion de este mismo detector, y otro tipo A: la correlacion parcial mide DIRECCION,
        # asi que un residuo diminuto pero alineado con lo ajeno daba 0.94 de "contaminacion"
        # aunque explicara el 2% de la lectura. Lo que importa es el tamaño: cuanto mejora el
        # ajuste al añadir la propiedad equivocada. Eso es interpretable y no se dispara.
        ajenas = {o: _r2_extra(lecturas[k], verdad[k], verdad[o]) for o in claves if o != k}
        entre_verdades = {o: round(abs(_corr(verdad[k], verdad[o])), 3) for o in claves if o != k}
        tabla[k] = {"con_lo_suyo": round(propia, 3),
                    "varianza_extra_de_lo_ajeno": {o: round(v, 3) for o, v in ajenas.items()},
                    "las_verdades_entre_si": entre_verdades}
        if propia < PISO_CORRELACION:
            fallos.append(f"{k}: correlaciona {propia:.3f} con lo suyo (piso {PISO_CORRELACION}) "
                          f"— la lectura no mide lo que dice medir")
        for o, v in ajenas.items():
            if v > TECHO_CONFUSION:
                fallos.append(f"{k}: la propiedad ajena '{o}' explica un {v:.1%} EXTRA de la "
                              f"lectura — esta leyendo la propiedad equivocada")
        # AVISO, no fallo: si las verdades vienen confundidas de fabrica, el problema es del MUNDO
        # y no del instrumento, y ninguna lectura podra separarlas. Se dice, no se esconde.
        for o, v in entre_verdades.items():
            if v > 0.70:
                fallos.append(f"AVISO DE MUNDO: '{k}' y '{o}' correlacionan {v:.3f} EN LA VERDAD — "
                              f"ninguna lectura puede separarlas; hay que rediseñar el sorteo")
    return {"tabla": tabla, "fallos": fallos, "aprueba": not fallos}


def _parcial(x, y, z, piso_residuo=0.05):  # (diagnostico; el veredicto usa _r2_extra)
    """Correlacion de x con y descontando lo que z explica de ambas — POR RESIDUOS, no por la
    formula cerrada.

    Cazado por la meta-prueba de esta ficha en su SEGUNDA corrida, y es un tipo D dentro del
    detector de tipos D: la formula (rxy - rxz*ryz)/sqrt((1-rxz^2)(1-ryz^2)) divide por casi cero
    cuando la lectura es casi identica a su propia verdad (rxz -> 1), que es justo el caso bueno.
    Daba 0.910 de "confusion" para una lectura perfecta. Por residuos no hay division peligrosa:
    si tras descontar z no queda casi nada de x, no queda NADA que pueda estar confundido, y la
    respuesta es cero por construccion — la misma guarda de piso de siempre."""
    x, y, z = (np.asarray(v, dtype=float) for v in (x, y, z))
    if x.size < 4 or np.std(z) < 1e-12:
        return _corr(x, y)
    rx = x - np.polyval(np.polyfit(z, x, 1), z)
    ry = y - np.polyval(np.polyfit(z, y, 1), z)
    if np.std(rx) < piso_residuo * max(np.std(x), 1e-12):
        return 0.0
    return _corr(rx, ry)


def _r2_extra(lectura, propia, ajena):
    """Cuanta varianza de la lectura explica la propiedad AJENA por encima de lo que ya explica la
    propia. 0.0 = la ajena no añade nada; 0.30 = añade un 30% y la lectura esta contaminada."""
    y = np.asarray(lectura, dtype=float)
    a = np.asarray(propia, dtype=float)
    b = np.asarray(ajena, dtype=float)
    if y.size < 4 or np.std(y) < 1e-12:
        return 0.0
    return max(0.0, _r2(y, np.column_stack([a, b])) - _r2(y, a.reshape(-1, 1)))


def _r2(y, X):
    X = np.column_stack([np.ones(len(y)), X])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ coef
    tot = float(np.sum((y - np.mean(y)) ** 2))
    return 0.0 if tot < 1e-18 else float(1.0 - np.sum(res ** 2) / tot)


def _corr(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if a.size < 3 or np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def condiciones_distintas(datos_por_condicion, separadas_por=None):
    """TIPO C — ¿hay dos condiciones que son la MISMA por construccion?
    `datos_por_condicion`: dict nombre -> lo observado (array, lista o dict serializable).

    Este es el tipo que repeti DOS VECES, la segunda al dia siguiente de diagnosticar la primera:
    el pasivo heredaba los episodios del dirigido y la diferencia salia 0.0000 EXACTA en 5/5.
    Un cero exacto repetido no es un empate: es una identidad, y hay que cazarla comparando los
    DATOS, no los numeros finales — para cuando el numero sale ya se perdio la corrida.

    `separadas_por`: dict {("a","b"): (razon, prueba_bool)} para los pares que comparten datos A
    PROPOSITO. Distingue dos situaciones que se ven IDENTICAS y no lo son:
      - prereg-32: encarnado y pasivo-propio ven los MISMOS episodios por diseño, y lo que los
        separa es la COPIA EFERENTE. Diseño valido, y se comprobo que la copia entra al modelo.
      - prereg-37: el pasivo heredaba los episodios Y el puntaje no usaba los comandos. Nada los
        separaba. Diferencia 0.0000 exacta en 5/5, y el estudio no midio nada.
    Compartir datos es legitimo SI otra cosa los separa Y esa otra cosa esta COMPROBADA. Sin
    prueba, es tautologia. (Añadido al aplicar la ficha hacia atras, 10-ago-2026.)
    """
    nombres = list(datos_por_condicion)
    separadas_por = separadas_por or {}
    fallos = []
    for i, a in enumerate(nombres):
        for b in nombres[i + 1:]:
            if _huella(datos_por_condicion[a]) != _huella(datos_por_condicion[b]):
                continue
            decl = separadas_por.get((a, b)) or separadas_por.get((b, a))
            if decl is None:
                fallos.append(f"'{a}' y '{b}' observaron EXACTAMENTE lo mismo y NADA se declara "
                              f"que los separe: no son dos condiciones, son el mismo numero con "
                              f"dos nombres")
            else:
                razon, probado = decl
                if not probado:
                    fallos.append(f"'{a}' y '{b}' comparten datos y se declara que los separa "
                                  f"'{razon}' — pero esa separacion NO esta comprobada")
    return {"fallos": fallos, "aprueba": not fallos}


def _huella(x):
    if isinstance(x, dict):
        return tuple(sorted((str(k), _huella(v)) for k, v in x.items()))
    if isinstance(x, (list, tuple, np.ndarray)):
        a = np.asarray(x, dtype=object).ravel()
        return tuple(_huella(v) if isinstance(v, (list, tuple, np.ndarray, dict))
                     else round(float(v), 12) if isinstance(v, (int, float, np.floating))
                     else str(v) for v in a)
    return round(float(x), 12) if isinstance(x, (int, float, np.floating)) else str(x)


def tramoya_declarada(n_pasos, cortes, maximo=0.25):
    """TIPO B — ¿cuanta de la señal es maquinaria NUESTRA en vez de fisica?
    `cortes`: los pasos donde el codigo reposiciona, teletransporta o deja asentar. Ninguna ley
    puede predecir algo que hacemos nosotros, asi que esas ventanas se excluyen SIEMPRE.

    Habria cazado: el re-soltado que hacia parecer caotica la caida (y coronaba al brazo), y el
    asentamiento que delataba la masa a simple vista."""
    # list(cortes or []) revienta con un array de numpy: "el valor de verdad de un array es
    # ambiguo". Cazado al aplicar la ficha hacia atras sobre soporte.py, que declara sus cortes
    # como array. La ficha tenia el mismo tipo de descuido que persigue.
    cortes = [] if cortes is None else list(cortes)
    frac = len(cortes) / max(1, n_pasos)
    fallos = []
    if not cortes:
        fallos.append("no se declaro NINGUN corte: o el mundo no tiene tramoya (raro) o no se "
                      "declaro (peligroso). Declarar cero cortes debe ser una decision, no un olvido")
    if frac > maximo:
        fallos.append(f"la tramoya ocupa {frac:.1%} de la señal (techo {maximo:.0%})")
    return {"fraccion": round(frac, 4), "fallos": fallos, "aprueba": not fallos}


def clasificacion(decision, verdad_binaria, nombres=None):
    """TIPO A, VERSION PARA INSTRUMENTOS QUE CLASIFICAN POR UMBRAL (no por correlacion).

    POR QUE EXISTE, y es una leccion del director: "cada experimento es distinto". Al aplicar
    `correlaciones()` a soporte.py —que NO devuelve una lectura continua sino un si/no por canal
    contra un umbral— salieron tres "fallos" que eran FALSAS ALARMAS MIAS: la obediencia vale
    0.0735 en una articulacion y 0.7032 en otra, asi que correlaciona flojo con "esto es mi
    cuerpo" aunque las CLASIFIQUE bien a las dos. Aplicar el estadistico equivocado a un
    instrumento correcto es, otra vez, un error de tipo A — esta vez en el detector.

    Para un clasificador la pregunta correcta no es "¿el numero sube junto con la verdad?" sino
    "¿acierta, y acierta por los dos lados?". Un clasificador que dice que si a todo acierta el
    100% de los positivos y no sabe nada."""
    d = [bool(x) for x in decision]
    v = [bool(x) for x in verdad_binaria]
    nombres = list(nombres or range(len(v)))
    vp = sum(1 for a, b in zip(d, v) if a and b)
    vn = sum(1 for a, b in zip(d, v) if not a and not b)
    fp = [n for n, a, b in zip(nombres, d, v) if a and not b]
    fn = [n for n, a, b in zip(nombres, d, v) if not a and b]
    fallos = []
    if fp:
        fallos.append(f"FALSOS POSITIVOS: {fp} — declarados y no lo son")
    if fn:
        fallos.append(f"FALSOS NEGATIVOS: {fn} — lo son y no los declaro")
    if sum(v) == 0 or sum(v) == len(v):
        fallos.append("la verdad es todo si o todo no: el caso no discrimina nada")
    return {"aciertos_positivos": vp, "aciertos_negativos": vn,
            "falsos_positivos": fp, "falsos_negativos": fn,
            "fallos": fallos, "aprueba": not fallos}


def cociente_seguro(numerador, denominador, piso):
    """TIPO D — un cociente cuyo denominador ronda el ruido no es una medida: es ruido dividido
    por ruido, y se dispara solo. Devuelve 0.0 por construccion bajo el piso.

    Habria cazado: 1e-9 sobre 1e-10 dando -0.80 con dos escenas quietas, y el +0.9999 de 'flota'
    con un coeficiente interno de 3.500 que delataba la degeneracion."""
    if abs(denominador) < piso or abs(numerador) < piso:
        return 0.0
    return float(numerador) / float(denominador)


def restos_de_versiones(ruta):
    """TIPO E — llamadas repetidas seguidas con los mismos argumentos, y variables locales
    asignadas y nunca usadas. Restos de una version anterior que siguen ejecutandose.

    Habria cazado: la applyExternalForce duplicada que daba DOBLE impulso en el primer paso de
    cada toque, y el 'avance' que quedo muerto al pasar la lectura de masa al pico."""
    arbol = ast.parse(open(ruta, encoding="utf-8").read())
    fallos = []
    for fn in [n for n in ast.walk(arbol) if isinstance(n, ast.FunctionDef)]:
        asignadas, usadas = {}, set()
        # SOLO asignaciones simples `x = algo`. Se ignoran los desempaquetados de tupla
        # (`a, b, _ = f()`), los bucles y los `with ... as`, porque en Python es idioma normal
        # recibir algo que no se usa. Cazado al aplicar esta ficha hacia atras sobre los 59
        # modulos: daba 27 hallazgos y casi todos eran ruido — entre ellos el `verdad` que
        # torneo_ojos recibe y NO usa, que no es un resto sino el cortafuegos funcionando.
        # Un guardian que grita de mas es peor que ninguno: se deja de leer.
        for n in ast.walk(fn):
            if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                    and isinstance(n.targets[0], ast.Name):
                asignadas.setdefault(n.targets[0].id, n.lineno)
        for n in ast.walk(fn):
            if isinstance(n, ast.Name) and not isinstance(n.ctx, ast.Store):
                usadas.add(n.id)
        for v, ln in asignadas.items():
            if v not in usadas and not v.startswith("_"):
                fallos.append(f"{os.path.basename(ruta)}:{ln} '{v}' se calcula y no se usa "
                              f"(resto de una version anterior)")
    return {"fallos": fallos, "aprueba": not fallos}


def politica_limpia(ruta, prohibidas=("verdad", "masas", "roces", "umbral", "pesado", "rugoso")):
    """FRONTERA (Regla 27) — ninguna funcion de politica puede nombrar la verdad del mundo.
    Que Diego elija bien tiene que EMERGER de sus propios datos, no de que le pasemos la respuesta.
    Se mira solo el codigo, no los comentarios: nombrar una leccion esta permitido, usarla no."""
    fuente = open(ruta, encoding="utf-8").read()
    arbol = ast.parse(fuente)
    fallos = []
    for fn in [n for n in ast.walk(arbol) if isinstance(n, ast.FunctionDef)]:
        if not (fn.name.startswith("politica") or fn.name.startswith("_duda")
                or fn.name.startswith("_incertidumbre")):
            continue
        for n in ast.walk(fn):
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value in prohibidas:
                fallos.append(f"{fn.name} nombra '{n.value}': la politica no puede ver la verdad")
            if isinstance(n, ast.Attribute) and n.attr in prohibidas:
                fallos.append(f"{fn.name} usa '.{n.attr}': la politica no puede ver la verdad")
    return {"fallos": fallos, "aprueba": not fallos}


# ============================================================ Regla 31 de la propia ficha
def regla31(verbose=True):
    """LA META-PRUEBA: la ficha debe CAZAR los catorce errores que de verdad cometi. Se reproducen
    en miniatura y se exige que los detecte. Una ficha que no caza los errores conocidos es un
    tramite; el precedente es guardianes_de_guardianes.py, que exige lo mismo a los guardianes."""
    fallos = []
    rng = np.random.default_rng(31)

    # A1 — la lectura que mide la geometria del montaje y no el movimiento (prereg-37)
    # verdades DESCORRELACIONADAS a proposito: si vinieran confundidas de fabrica, el aviso de
    # mundo saltaria con razon y no estariamos probando el detector sino el sorteo.
    verdad = {"masa": [0.2, 0.4, 0.6, 0.8, 1.0, 0.3, 0.7, 1.1],
              "roce": [0.8, 0.1, 0.9, 0.2, 0.7, 0.3, 0.1, 0.6]}
    ciega = {"masa": [0.42] * 8, "roce": list(rng.uniform(0, 1, 8))}
    a1 = not correlaciones(ciega, verdad)["aprueba"]
    _di(verbose, a1, "TIPO A — caza una lectura que no correlaciona con lo que dice medir")
    if not a1:
        fallos.append("A1")

    # A2 — la lectura que mide la propiedad EQUIVOCADA (el 'frenado' del prereg-39)
    cruzada = {"masa": verdad["masa"], "roce": [-x for x in verdad["masa"]]}
    a2 = not correlaciones(cruzada, verdad)["aprueba"]
    _di(verbose, a2, "TIPO A — caza una lectura que correlaciona con la propiedad ajena")
    if not a2:
        fallos.append("A2")

    # A3 — y APRUEBA cuando las lecturas son correctas (si no, seria un guardian que grita siempre)
    buena = {k: [x + 0.01 * rng.normal() for x in v] for k, v in verdad.items()}
    a3 = correlaciones(buena, verdad)["aprueba"]
    _di(verbose, a3, "TIPO A — y APRUEBA lecturas correctas (no es un guardian que grita siempre)")
    if not a3:
        fallos.append("A3")

    # C1 — dos condiciones identicas por construccion (prereg-32 y prereg-37, el mismo error)
    epis = {0: [1.0, 2.0], 1: [3.0]}
    c1 = not condiciones_distintas({"dirigido": epis, "pasivo": dict(epis)})["aprueba"]
    _di(verbose, c1, "TIPO C — caza dos condiciones que observaron EXACTAMENTE lo mismo")
    if not c1:
        fallos.append("C1")
    c1b = condiciones_distintas({"dirigido": epis, "pasivo": {0: [1.0], 1: [3.0, 9.0]}})["aprueba"]
    _di(verbose, c1b, "TIPO C — y aprueba condiciones que de verdad difieren")
    if not c1b:
        fallos.append("C1b")

    # B1 — tramoya no declarada (el re-soltado del prereg-29)
    b1 = not tramoya_declarada(900, [])["aprueba"]
    _di(verbose, b1, "TIPO B — caza un mundo que no declara su tramoya")
    if not b1:
        fallos.append("B1")
    b2 = tramoya_declarada(900, list(range(59, 900, 60)))["aprueba"]
    _di(verbose, b2, "TIPO B — y aprueba una tramoya declarada y acotada")
    if not b2:
        fallos.append("B2")

    # D1 — el cociente que se dispara con denominadores de ruido (prereg-29)
    d1 = cociente_seguro(1e-9, 1e-10, piso=1e-6) == 0.0
    _di(verbose, d1, "TIPO D — un cociente bajo el piso de ruido vale CERO por construccion")
    if not d1:
        fallos.append("D1")
    d2 = abs(cociente_seguro(2.0, 4.0, piso=1e-6) - 0.5) < 1e-12
    _di(verbose, d2, "TIPO D — y sigue midiendo donde hay señal de verdad")
    if not d2:
        fallos.append("D2")

    # F1 — deslices de escritura: la letra que parece latina y no lo es (pedido del director)
    import tempfile as _tmp
    _p = os.path.join(_tmp.mkdtemp(), "senuelo.py")
    open(_p, "w", encoding="utf-8").write("def f():\n    az\u04301 = 3\n    return az\u04301\n")
    f1 = not homoglifos(_p)["aprueba"]
    _di(verbose, f1, "TIPO F — caza una letra cirilica dentro de un nombre de variable")
    if not f1:
        fallos.append("F1")
    f2 = not texto_para_shell("la variable `x` fallo")["aprueba"]
    _di(verbose, f2, "TIPO F — avisa de una comilla invertida que bash se comeria")
    if not f2:
        fallos.append("F2")
    f3 = texto_para_shell("la variable x fallo")["aprueba"]
    _di(verbose, f3, "TIPO F — y no grita en un texto limpio")
    if not f3:
        fallos.append("F3")

    # E1 — restos de versiones anteriores, sobre codigo real del repositorio
    aqui = os.path.dirname(os.path.abspath(__file__))
    e1 = restos_de_versiones(os.path.join(aqui, "sanidad.py"))["aprueba"]
    _di(verbose, e1, "TIPO E — esta misma ficha no tiene codigo muerto")
    if not e1:
        fallos.append("E1")

    if verbose:
        print("\nSANIDAD: " + ("APRUEBA — caza los cinco tipos de error que de verdad cometi, y no "
                               "grita donde no hay nada." if not fallos
                               else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def _di(verbose, ok, texto):
    if verbose:
        print(f"  {'ok  ' if ok else 'FALLO'} {texto}")




# ============================================================ TIPO F: mis deslices de escritura
# Pedido por el director el 10-ago-2026: "incluye algo que te avise si escribes mal algo sin
# comillas". Nace de DOS errores mios del mismo dia y del mismo tipo — escribir sin releer:
#   - una variable llamada `azа1` con una 'a' CIRILICA. Python la acepta como identificador valido,
#     ninguna busqueda por texto la encontraba, y la condicion azarosa quedo calculada y sin usar:
#     la Regla 31 del prereg-37 nunca probo la condicion que decidia el estudio.
#   - un mensaje de commit con comillas invertidas sin escapar: bash se comio dos nombres de
#     variable y el registro quedo incompleto.
# Los dos son invisibles al ojo y triviales para una maquina. Por eso van aqui.

_CONFUSABLES = {
    "а": "a (cirilica)", "е": "e (cirilica)", "о": "o (cirilica)",
    "р": "p (cirilica)", "с": "c (cirilica)", "х": "x (cirilica)",
    "у": "y (cirilica)", "ο": "o (griega)", "Α": "A (griega)",
    "Β": "B (griega)", "Ε": "E (griega)", "–": "guion largo",
    "‘": "comilla tipografica", "’": "comilla tipografica",
    "“": "comilla tipografica", "”": "comilla tipografica",
    " ": "espacio duro",
}


def homoglifos(ruta):
    """TIPO F — letras que PARECEN latinas y no lo son, dentro de nombres del codigo.
    Se miran los identificadores (via AST), no los comentarios: en un comentario en español una
    tilde es correcta; en un nombre de variable una 'a' cirilica es una bomba de relojeria."""
    fuente = open(ruta, encoding="utf-8").read()
    try:
        arbol = ast.parse(fuente)
    except SyntaxError as e:
        return {"fallos": [f"{os.path.basename(ruta)}: no parsea ({e})"], "aprueba": False}
    fallos = []
    nombres = set()
    for n in ast.walk(arbol):
        if isinstance(n, ast.Name):
            nombres.add(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            nombres.add(n.name)
        elif isinstance(n, ast.arg):
            nombres.add(n.arg)
        elif isinstance(n, ast.Attribute):
            nombres.add(n.attr)
    for nom in sorted(nombres):
        # SOLO los confusables declarados. Cazado por el propio detector en su primera pasada:
        # marcaba 'señales' en seis modulos porque la ñ no es ASCII. La ñ no engaña a nadie — el
        # peligro es la letra que se ve IGUAL que otra, no la que se ve distinta.
        malos = [(c, _CONFUSABLES[c]) for c in nom if c in _CONFUSABLES]
        if malos:
            fallos.append(f"{os.path.basename(ruta)}: el nombre '{nom}' lleva "
                          f"{', '.join(d for _, d in malos)} — parece latino y no lo es")
    return {"fallos": fallos, "aprueba": not fallos}


def texto_para_shell(s):
    """TIPO F — ¿este texto se puede pasar sin peligro dentro de comillas dobles en la terminal?
    Devuelve los caracteres que bash INTERPRETARIA en vez de escribir. La cura correcta no es
    escaparlos uno a uno: es escribir el texto a un archivo y pasar el archivo (git commit -F).
    Esta funcion existe para AVISAR antes, no para arreglarlo despues."""
    peligros = []
    if "`" in s:
        peligros.append("comilla invertida ` — bash ejecuta lo que hay dentro y BORRA el texto")
    if "$(" in s:
        peligros.append("$( — bash ejecuta lo que hay dentro")
    for i, c in enumerate(s):
        if c == "$" and i + 1 < len(s) and (s[i + 1].isalpha() or s[i + 1] == "{"):
            peligros.append(f"${s[i+1]}... — bash lo sustituye por una variable")
            break
    for c, d in _CONFUSABLES.items():
        if c in s:
            peligros.append(f"{d} — caracter que parece otro")
    return {"peligros": sorted(set(peligros)), "aprueba": not peligros}


if __name__ == "__main__":
    import sys
    sys.exit(regla31())
