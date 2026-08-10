# experimentar2.py — SEGUNDA VUELTA DE LA EXPERIMENTACION DIRIGIDA (prerregistro-39).
#
# POR QUE EXISTE. El prereg-37 quedo NO CONCLUYENTE POR INSTRUMENTO (INFORME-46) por dos fallos
# mios, y este modulo aplica las tres curas que YA ESTABAN ESCRITAS en aquel prerregistro antes de
# correrlo — por eso avanza por quorum y no es una reaccion al resultado.
#
#   FALLO 1: el pasivo heredaba los episodios del dirigido -> diferencia 0.0000 EXACTA en 5/5.
#            Era el mismo numero con otro nombre. CURA: el pasivo ve episodios de OTRO agente,
#            como el pasivo-ajeno del prereg-32, que si funciono.
#   FALLO 2: la medida saturaba al cuarto toque (4 toques -> 0.9725; 24 -> 0.9868). Elegir no
#            puede importar en una tarea que se resuelve tocando cada cosa una vez.
#            CURA: 8 objetos, DOS propiedades ocultas cada uno = 16 incognitas, y un presupuesto
#            de 24 toques que NO alcanza — con lectura RUIDOSA, asi que hace falta repetir donde
#            uno duda. Ahi es donde repartir bien vale algo.
#
# LAS DOS PROPIEDADES, ninguna visible en reposo y cada una con su lectura:
#   MASA — cuanto se desplaza el objeto con un empujon de fuerza fija.
#   ROCE — cuanto tarda en frenar despues (la forma en que se detiene, no cuanto avanza).
# Objetos cerca de la frontera de decision son INTRINSECAMENTE DUDOSOS: se resuelven, pero salen
# caros en toques. Un mundo real tiene casos faciles y casos dificiles; el que reparte bien gasta
# donde duda y no donde ya sabe.
#
# FRONTERA DE CONTAMINACION (Regla 27): a Diego no se le dice que hay dos propiedades, ni cuales,
# ni donde esta la frontera. Su politica solo mira SUS PROPIOS datos: cuantas veces toco cada sitio
# y cuanto le bailan las lecturas. Ninguna funcion de la politica menciona masa, roce ni umbral.

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

PASO_FISICO = 1.0 / 240.0
SUBPASOS = 8
N_OBJ = 8
RADIO = 0.42
ALTO = 0.045
FUERZA = 26.0
EMPUJE_SUBPASOS = 40      # el empujon DURA: una sola llamada de fuerza vale un paso
PASOS_POR_TOQUE = 140
PRESUPUESTO = 24          # 24 toques para 16 incognitas: NO alcanza, y ese es el punto
PRESUPUESTO_MINIMO = 16   # guarda de potencia
RUIDO_SENSOR = 0.10       # lectura ruidosa: por eso hace falta repetir donde uno duda

MASA_MIN, MASA_MAX = 0.20, 1.10
ROCE_MIN, ROCE_MAX = 0.08, 0.85

# ------------------------------------------------------ EL MANIFIESTO DEL METODO (paso 0 y 1)
# Lo exige `codigo/metodo.py`, LA PUERTA. Sin esto el modulo no se puede encolar.
# Aqui se declara QUE CLASE DE PRUEBA es esto y CUAL ES LA FORMULA de cada lectura — antes de que
# nadie corra nada. Las formulas no se creen: se comprueban con relaciones metamorficas (tipo G).
_BASE_MET = {"masa": 0.5, "roce": 0.4, "fuerza": 26.0}
METODO = {
    "tipo_de_medida": "mixta",   # las lecturas son continuas; el puntaje CLASIFICA por umbral
    "comparten_datos": {
        "hay": False,
        "porque": "las tres condiciones actuan por su cuenta. El pasivo ve episodios de OTRO "
                  "agente, nunca los del dirigido — esa copia fue el fallo 1 del prereg-37 y aqui "
                  "esta prohibida por diseño.",
    },
    "formulas": [
        {"base": {**_BASE_MET, "cual": "pico"}, "parametro": "masa", "factor": 2.0, "esperado": 0.5,
         "porque": "v = F*T/m — doblar la masa parte el pico por la mitad"},
        {"base": {**_BASE_MET, "cual": "pico"}, "parametro": "fuerza", "factor": 2.0,
         "esperado": 2.0, "porque": "v = F*T/m — doblar la fuerza dobla el pico"},
        {"base": {**_BASE_MET, "cual": "roce"}, "parametro": "roce", "factor": 2.0, "esperado": 2.0,
         "porque": "a = mu*g — doblar el rozamiento dobla la desaceleracion"},
        {"base": {**_BASE_MET, "cual": "roce"}, "parametro": "masa", "factor": 2.0, "esperado": 1.0,
         "porque": "a = mu*g NO lleva masa dentro — doblarla no debe cambiar la desaceleracion"},
    ],
}


def _sitio(i):
    ang = 2.0 * np.pi * i / N_OBJ
    return [RADIO * np.cos(ang), RADIO * np.sin(ang), ALTO]


def mundo(semilla, con_duda=True):
    """Sortea las 16 incognitas. Con `con_duda=False` todos los objetos son iguales por dentro:
    ahi la ventaja de repartir bien DEBE desaparecer (caso 7 de la Regla 31)."""
    rng = np.random.default_rng(int(semilla) + 550007)
    med_m = 0.5 * (MASA_MIN + MASA_MAX)
    med_r = 0.5 * (ROCE_MIN + ROCE_MAX)
    if not con_duda:
        m = [med_m] * N_OBJ
        r = [med_r] * N_OBJ
    else:
        # VERDAD BALANCEADA POR CONSTRUCCION: 4 por encima del umbral y 4 por debajo, en cada
        # propiedad. Cazado por el caso 2 de esta Regla 31 en su primera corrida: sin balancear,
        # la verdad podia ser 6-2 mientras el clasificador —que no conoce el umbral y parte por la
        # mediana observada— fuerza 4-4. El desajuste hundia el puntaje POR DEBAJO del azar (4/16
        # contra 8), y eso no medía a la politica: medía un error de diseño mio.
        # La dificultad viene de la DISTANCIA a la frontera, no del desbalance: dos cerca (caros
        # en toques) y dos lejos (baratos) a cada lado.
        def _lado(lo, hi, med):
            cerca = 0.10 * (hi - lo)
            bajo = [rng.uniform(med - cerca, med - 0.02 * (hi - lo)) for _ in range(2)] + \
                   [rng.uniform(lo, med - 3 * cerca) for _ in range(2)]
            alto = [rng.uniform(med + 0.02 * (hi - lo), med + cerca) for _ in range(2)] + \
                   [rng.uniform(med + 3 * cerca, hi) for _ in range(2)]
            v = bajo + alto
            rng.shuffle(v)
            return [float(x) for x in v]
        m = _lado(MASA_MIN, MASA_MAX, med_m)
        r = _lado(ROCE_MIN, ROCE_MAX, med_r)
    return {"masas": [round(x, 4) for x in m], "roces": [round(x, 4) for x in r],
            "umbral_masa": med_m, "umbral_roce": med_r, "con_duda": bool(con_duda),
            "verdad": {"pesado": [bool(x > med_m) for x in m],
                       "rugoso": [bool(x > med_r) for x in r]}}


def _escena(w):
    import pybullet as p
    cliente = p.connect(p.DIRECT)
    p.resetSimulation(physicsClientId=cliente)
    p.setGravity(0, 0, -9.8, physicsClientId=cliente)
    p.setTimeStep(PASO_FISICO, physicsClientId=cliente)
    p.createMultiBody(0, p.createCollisionShape(p.GEOM_PLANE, physicsClientId=cliente),
                      physicsClientId=cliente)
    forma = p.createCollisionShape(p.GEOM_BOX, halfExtents=[ALTO] * 3, physicsClientId=cliente)
    objetos = []
    for i in range(N_OBJ):
        o = p.createMultiBody(w["masas"][i], forma, basePosition=_sitio(i),
                              physicsClientId=cliente)
        p.changeDynamics(o, -1, lateralFriction=w["roces"][i], physicsClientId=cliente)
        objetos.append(o)
    return cliente, objetos


def _leer(cliente, objetos, cual, rng):
    """UN empujon y sus DOS lecturas ruidosas: el PICO de velocidad (masa) y el tiempo hasta
    parar (roce).
    El ruido es del sensor, no del mundo: la misma escena leida dos veces da cifras distintas, que
    es la razon por la que hace falta repetir donde uno duda."""
    import pybullet as p
    o = objetos[cual]
    # (Aqui vivia una segunda llamada de fuerza, resto de la version anterior. PyBullet ACUMULA las
    # fuerzas hasta el siguiente stepSimulation, asi que el primer paso de cada toque recibia el
    # DOBLE de impulso. No sesgaba una propiedad frente a la otra —era identico para los ocho
    # objetos— pero era un defecto real y se quito ANTES de la primera corrida oficial.)
    fx = FUERZA * np.cos(2 * np.pi * cual / N_OBJ)
    fy = FUERZA * np.sin(2 * np.pi * cual / N_OBJ)
    v = []
    for k in range(PASOS_POR_TOQUE * SUBPASOS):
        # EL EMPUJON DURA. Cazado por el caso 2 en su segunda corrida: una sola llamada de fuerza
        # vale UN paso de simulacion, y con ese impulso los objetos pesados y rugosos no llegaban
        # a moverse (pico exactamente 0.0000 en 4 de 8). Una lectura que no distingue "pesado" de
        # "no se movio" no es una lectura.
        if k < EMPUJE_SUBPASOS:
            p.applyExternalForce(o, -1, [fx, fy, 0], _sitio(cual), p.WORLD_FRAME,
                                 physicsClientId=cliente)
        p.stepSimulation(physicsClientId=cliente)
        vx, vy, _ = p.getBaseVelocity(o, physicsClientId=cliente)[0]
        v.append(float(np.hypot(vx, vy)))
    # PICO al terminar el empujon: v ~ F*T/m. Lee la MASA.
    pico = max(v[:EMPUJE_SUBPASOS + 1]) if v else 0.0
    # LA DESACELERACION, no el tiempo hasta parar. Con friccion seca a = mu*g: la pendiente de la
    # velocidad NO contiene la masa por ninguna via. Cazado por la ficha de sanidad (sanidad.py) el
    # 10-ago-2026 sobre este mismo modulo DESPUES de que su Regla 31 lo aprobara 8/8: la lectura
    # anterior (pico / tiempo_hasta_parar) seguia correlacionando 0.945 con la MASA una vez
    # descontado lo que la masa ya explicaba. Las correlaciones brutas parecian sanas (+0.881 con
    # el roce); la PARCIAL enseño que no lo estaban.
    tras = v[EMPUJE_SUBPASOS:]
    umbral = 0.02 * max(pico, 1e-12)
    fin = next((j for j, sv in enumerate(tras) if sv < umbral), len(tras))
    if fin >= 4:
        t = np.arange(fin, dtype=float)
        frenado = float(-np.polyfit(t, np.asarray(tras[:fin], dtype=float), 1)[0])
    else:
        frenado = 0.0
    n1 = float(rng.normal(1.0, RUIDO_SENSOR))
    n2 = float(rng.normal(1.0, RUIDO_SENSOR))
    return pico * n1, frenado * n2


def _reponer(cliente, objetos):
    import pybullet as p
    for i, o in enumerate(objetos):
        p.resetBasePositionAndOrientation(o, _sitio(i), [0, 0, 0, 1], physicsClientId=cliente)
        p.resetBaseVelocity(o, [0, 0, 0], [0, 0, 0], physicsClientId=cliente)


# ------------------------------------------------------------------- las politicas
def _duda(obs, i):
    """Cuanto NO se de este sitio. Solo mira SUS PROPIOS datos: cuantas veces lo toco y cuanto le
    bailan las lecturas. No menciona masa, roce ni umbral — esa es la Regla 27 en la politica."""
    v = obs[i]
    if len(v) == 0:
        return 1e9
    if len(v) == 1:
        return 10.0
    a = np.array([x[0] for x in v])
    b = np.array([x[1] for x in v])
    disp = float(np.std(a) / (abs(np.mean(a)) + 1e-9) + np.std(b) / (abs(np.mean(b)) + 1e-9))
    return disp / len(v)


def politica(nombre, obs, rng):
    if nombre == "dirigido":
        return int(np.argmax([_duda(obs, i) for i in range(N_OBJ)]))
    if nombre == "azaroso":
        return int(rng.integers(0, N_OBJ))
    if nombre == "agitador":
        return 0        # SEÑUELO: toca mucho y siempre lo mismo. Actividad sin pregunta.
    if nombre == "uniforme":
        return int(sum(len(obs[i]) for i in range(N_OBJ)) % N_OBJ)
    raise ValueError(nombre)


def _saber(obs, w):
    """Cuantas de las 16 incognitas quedan resueltas. NO satura: va de 0 a 16.
    Se clasifica por la MEDIANA de las lecturas de cada sitio contra la mediana global observada —
    nunca contra el umbral verdadero, que Diego no conoce ni puede conocer."""
    med_a, med_b = [], []
    for i in range(N_OBJ):
        if obs[i]:
            med_a.append(np.median([x[0] for x in obs[i]]))
            med_b.append(np.median([x[1] for x in obs[i]]))
    if len(med_a) < 2:
        return 0
    corte_a, corte_b = float(np.median(med_a)), float(np.median(med_b))
    aciertos = 0
    for i in range(N_OBJ):
        if not obs[i]:
            continue                     # sitio nunca tocado: no sabe, no cuenta
        a = float(np.median([x[0] for x in obs[i]]))
        b = float(np.median([x[1] for x in obs[i]]))
        # mas masa = PICO de velocidad menor ; mas roce = frena ANTES (mas fraccion quieta)
        if (a < corte_a) == w["verdad"]["pesado"][i]:
            aciertos += 1
        if (b > corte_b) == w["verdad"]["rugoso"][i]:
            aciertos += 1
    return int(aciertos)


def correr(condicion, semilla=1, presupuesto=PRESUPUESTO, w=None, con_duda=True):
    """Un episodio. El PASIVO ve los episodios de OTRO agente en el mismo mundo — nunca los del
    dirigido: esa copia fue el fallo 1 del prereg-37 y aqui esta prohibida por diseño."""
    import pybullet as p
    w = w or mundo(semilla, con_duda=con_duda)
    if condicion == "pasivo":
        ajeno = correr("azaroso", semilla=semilla + 991, presupuesto=presupuesto, w=w)
        return {"condicion": "pasivo", "puntaje": _saber(ajeno["obs"], w), "obs": ajeno["obs"],
                "reparto": ajeno["reparto"], "presupuesto": presupuesto,
                "nota": "ve los episodios de OTRO agente en el mismo mundo (nunca los del dirigido)"}
    rng = np.random.default_rng(int(semilla) + 12345)
    cliente, objetos = _escena(w)
    try:
        obs = {i: [] for i in range(N_OBJ)}
        for _ in range(presupuesto):
            cual = politica(condicion, obs, rng)
            obs[cual].append(_leer(cliente, objetos, cual, rng))
            _reponer(cliente, objetos)
        return {"condicion": condicion, "puntaje": _saber(obs, w), "obs": obs,
                "reparto": [len(obs[i]) for i in range(N_OBJ)], "presupuesto": presupuesto}
    finally:
        p.disconnect(physicsClientId=cliente)


def _visible_en_reposo(w, pasos=60, plantar=False):
    """CASO 1, por los DOS lados: en reposo nada distingue a los objetos (~0), y con una diferencia
    PLANTADA la misma medida TIENE que verla. Sin el segundo lado, una medida ciega aprobaria —
    que es el agujero que el prereg-36 nos enseño y que volvi a abrir en el prereg-37."""
    import pybullet as p
    cliente, objetos = _escena(w)
    try:
        if plantar:
            p.resetBaseVelocity(objetos[0], [0.6, 0, 0], [0, 0, 0], physicsClientId=cliente)
        else:
            for _ in range(120 * SUBPASOS):
                p.stepSimulation(physicsClientId=cliente)
        filas = []
        for _ in range(pasos):
            for _ in range(SUBPASOS):
                p.stepSimulation(physicsClientId=cliente)
            fila = []
            for o in objetos:
                (x, y, z), _ = p.getBasePositionAndOrientation(o, physicsClientId=cliente)
                fila += [x, y, z]
            filas.append(fila)
        x = np.array(filas, dtype=float)
        movs = [float(np.max(np.std(x[:, 3 * i:3 * i + 3], axis=0))) for i in range(N_OBJ)]
        if max(movs) < 1e-4:      # guarda de piso: nada se movio, la diferencia es cero
            return 0.0
        return float((max(movs) - min(movs)) / (max(movs) + min(movs) + 1e-9))
    finally:
        p.disconnect(physicsClientId=cliente)


def regla31(verbose=True, presupuesto=PRESUPUESTO):
    if presupuesto < PRESUPUESTO_MINIMO:
        raise SystemExit(f"MEDICION INVALIDA: {presupuesto} toques (minimo {PRESUPUESTO_MINIMO}).")
    fallos = []
    w = mundo(1)

    # 1) LA DUDA ES REAL, POR LOS DOS LADOS
    quieto = _visible_en_reposo(w)
    plantado = _visible_en_reposo(w, plantar=True)
    c1 = quieto < 0.05 and plantado > 0.50
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} LA DUDA ES REAL: en reposo {quieto:.4f} (<0.05) y con "
              f"diferencia plantada {plantado:.4f} (>0.50) — la medida no es ciega")
    if not c1:
        fallos.append("duda-real")

    dir1 = correr("dirigido", semilla=1, presupuesto=presupuesto, w=w)
    aza1 = correr("azaroso", semilla=1, presupuesto=presupuesto, w=w)
    pas1 = correr("pasivo", semilla=1, presupuesto=presupuesto, w=w)
    agi1 = correr("agitador", semilla=1, presupuesto=presupuesto, w=w)

    # 2) TOCAR RESUELVE ALGO: con presupuesto, el dirigido debe superar claramente el azar (8/16)
    c2 = dir1["puntaje"] > 8
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} TOCAR RESUELVE: el dirigido acierta "
              f"{dir1['puntaje']}/16 (el azar ciego daria 8)")
    if not c2:
        fallos.append("tocar-resuelve")

    # 3) EL PRESUPUESTO NO ALCANZA. Si alguna politica resuelve las 16, el mundo volvio a ser
    #    demasiado facil y el estudio no mide estrategia: mide que sobra tiempo.
    c3 = max(dir1["puntaje"], aza1["puntaje"], pas1["puntaje"]) < 16
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} EL PRESUPUESTO NO ALCANZA: nadie resuelve las 16 "
              f"(dirigido {dir1['puntaje']}, azaroso {aza1['puntaje']}, pasivo {pas1['puntaje']})")
    if not c3:
        fallos.append("presupuesto-alcanza")

    # 4) NO HAY TAUTOLOGIA. Es un FALLO y no una nota, y esa distincion es la leccion literal del
    #    INFORME-46: ayer imprimi una advertencia sobre esta misma condicion y deje correr cinco
    #    semillas igual. Una advertencia sobre una condicion debe REPROBAR.
    c4 = dir1["reparto"] != pas1["reparto"]
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} NO HAY TAUTOLOGIA: dirigido y pasivo NO comparten "
              f"episodios (repartos {dir1['reparto']} vs {pas1['reparto']})")
    if not c4:
        fallos.append("tautologia")

    # 5) EL SEÑUELO DEL AGITADOR: tocar mucho y sin criterio no puede ganar.
    c5 = agi1["puntaje"] <= dir1["puntaje"]
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} SEÑUELO AGITADOR: reparto {agi1['reparto']} y puntaje "
              f"{agi1['puntaje']} <= dirigido {dir1['puntaje']}")
    if not c5:
        fallos.append("senuelo-agitador")

    # 6) MUNDO SIN DUDA: si todos los objetos son iguales por dentro, no hay nada que averiguar y
    #    el puntaje debe caer al nivel del azar. Premiar la intervencion donde no hay pregunta es
    #    medir el propio entusiasmo.
    sin = correr("dirigido", semilla=1, presupuesto=presupuesto, con_duda=False)
    c6 = sin["puntaje"] <= 12
    if verbose:
        print(f"  {'ok  ' if c6 else 'FALLO'} MUNDO SIN DUDA: sin nada que averiguar el dirigido "
              f"saca {sin['puntaje']}/16 (no puede lucirse donde no hay pregunta)")
    if not c6:
        fallos.append("mundo-sin-duda")

    # 7) LA MEDIDA NO SATURA — el fallo 2 del prereg-37, congelado para que no vuelva.
    #    SE COMPARA CONTRA UN CUARTO DE PRESUPUESTO, no contra la mitad. Motivo medido antes de
    #    correr el estudio: la politica dirigida alcanza el techo alcanzable (14/16) ya con 8
    #    toques, asi que comparar 16 contra 24 no dice nada sobre la medida — dice que el dirigido
    #    es eficiente. Lo que este caso debe comprobar es que la medida NO esta capada por
    #    construccion, y eso se ve donde todavia hay margen. Medido: 6 toques -> 9/16, 24 -> 14/16.
    #    NO se bajo el presupuesto del estudio para agrandar la ventaja: a 10 toques el dirigido le
    #    saca +5 al azaroso y a los 24 prerregistrados solo +2. Se mantiene 24, el que menos
    #    favorece a la hipotesis.
    poco = correr("dirigido", semilla=1, presupuesto=max(6, presupuesto // 4), w=w)["puntaje"]
    c7 = poco < dir1["puntaje"]
    if verbose:
        print(f"  {'ok  ' if c7 else 'FALLO'} LA MEDIDA NO SATURA: con {max(6, presupuesto // 4)} "
              f"toques {poco}/16 y con {presupuesto} toques {dir1['puntaje']}/16 — mas presupuesto "
              f"sigue comprando saber")
    if not c7:
        fallos.append("medida-satura")

    # 8) GUARDA DE POTENCIA declarada y viva.
    c8 = PRESUPUESTO_MINIMO >= 16
    if verbose:
        print(f"  {'ok  ' if c8 else 'FALLO'} GUARDA DE POTENCIA: minimo {PRESUPUESTO_MINIMO} "
              f"toques, por debajo el modulo se niega a dar veredicto")
    if not c8:
        fallos.append("guarda-potencia")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el mundo tiene duda real, el presupuesto no alcanza, y "
                                "la vara no premia la agitacion."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="Experimentacion dirigida, 2a vuelta (prereg-39)")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--semilla", type=int, default=None)
    ap.add_argument("--presupuesto", type=int, default=PRESUPUESTO)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31(presupuesto=a.presupuesto))
    if a.semilla is None:
        print("uso: --regla31 | --semilla N [--presupuesto K]")
        return
    if a.presupuesto < PRESUPUESTO_MINIMO:
        raise SystemExit(f"MEDICION INVALIDA: {a.presupuesto} toques "
                         f"(minimo {PRESUPUESTO_MINIMO}).")
    w = mundo(a.semilla)
    filas = {c: correr(c, semilla=a.semilla, presupuesto=a.presupuesto, w=w)
             for c in ("dirigido", "azaroso", "pasivo")}
    d, z, p_ = (filas["dirigido"]["puntaje"], filas["azaroso"]["puntaje"],
                filas["pasivo"]["puntaje"])
    salida = {
        "prerregistro": 39, "semilla": a.semilla, "presupuesto": a.presupuesto,
        "incognitas": 2 * N_OBJ,
        "mundo": {k: v for k, v in w.items() if k != "verdad"},
        "condiciones": {k: {kk: vv for kk, vv in v.items() if kk != "obs"}
                        for k, v in filas.items()},
        "dirigido_menos_azaroso": d - z,
        "dirigido_menos_pasivo": d - p_,
        "nota": "el veredicto del hito exige las 5 semillas juntas; esto es una sola",
    }
    out = os.path.join(BASE, "resultados", f"p39-experimentar2-s{a.semilla}")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False, default=str)
    print(f"guardado en {out}/resumen.json (parcial — el veredicto exige las 5 semillas juntas)")

# ------------------------------------------------------ LO QUE LA PUERTA EJECUTA (metodo.py)
def _metodo_medir(masa=0.5, roce=0.4, fuerza=26.0, cual="pico"):
    """Un toque sobre un objeto de masa y roce dados. Es lo que la puerta usa para comprobar que
    las formulas declaradas en METODO se cumplen de verdad. Tres repeticiones porque el sensor
    tiene un 10% de ruido: una sola lectura no distingue una formula rota de una mota de polvo."""
    import pybullet as p
    w = {"masas": [masa] * N_OBJ, "roces": [roce] * N_OBJ}
    global FUERZA
    viejo, FUERZA = FUERZA, fuerza
    cliente, objetos = _escena(w)
    try:
        rng = np.random.default_rng(0)
        picos, roces = [], []
        for _ in range(3):
            a, b = _leer(cliente, objetos, 0, rng)
            _reponer(cliente, objetos)
            picos.append(a)
            roces.append(b)
        return float(np.median(picos if cual == "pico" else roces))
    finally:
        p.disconnect(physicsClientId=cliente)
        FUERZA = viejo


def _metodo_sanidad():
    """PASO 3 — la ficha, contra la VERDAD del simulador. Comprueba lo que la Regla 31 no puede:
    que cada lectura mida lo suyo y no la de al lado, y que las tres condiciones no sean copias."""
    import sanidad as S
    import pybullet as p
    w = mundo(1)
    cliente, objetos = _escena(w)
    try:
        rng = np.random.default_rng(0)
        picos, roces = [], []
        for i in range(N_OBJ):
            a, b = _leer(cliente, objetos, i, rng)
            _reponer(cliente, objetos)
            picos.append(a)
            roces.append(b)
    finally:
        p.disconnect(physicsClientId=cliente)
    fallos = []
    fallos += S.correlaciones({"masa": picos, "roce": roces},
                              {"masa": w["masas"], "roce": w["roces"]})["fallos"]
    d = correr("dirigido", semilla=1, w=w)
    z = correr("azaroso", semilla=1, w=w)
    q = correr("pasivo", semilla=1, w=w)
    fallos += S.condiciones_distintas({"dirigido": d["obs"], "azaroso": z["obs"],
                                       "pasivo": q["obs"]})["fallos"]
    return {"aprueba": not fallos, "fallos": fallos}


if __name__ == "__main__":
    main()
