# experimentar.py — LA EXPERIMENTACION DIRIGIDA (prerregistro-37, FIRMADO 10-ago-2026).
#
# POR QUE EXISTE. Hasta hoy cada nodo del arbol es una afirmacion sobre CORRELACIONES en
# grabaciones. Ninguna es causal. Para separar causa de correlacion hacen falta INTERVENCIONES, y
# Diego nunca intervino sobre nada: en el Gimnasio su brazo balbucea en el aire y JAMAS toca el
# objeto. La auditoria del 10-ago (INFORME-45) lo midio: su sentido del tacto se enciende en
# 1 de cada 10.000 pasos. Le construimos un aparato sensorial completo y lo pusimos a mirar.
#
# EL EXPERIMENTO. Dos objetos de aspecto IDENTICO —mismo tamaño, misma forma, misma posicion de
# reposo— que difieren en UNA propiedad oculta que NO se puede ver sin tocar: la masa.
#   Mirandolos quietos, son indistinguibles. Es lo que convierte esto en un experimento y no en
#   una prueba de agudeza visual.
#   Empujandolos, la diferencia salta.
#
# TRES CONDICIONES que se diferencian SOLO en quien decide que hacer:
#   DIRIGIDO — elige a cual empujar segun su propia incertidumbre.
#   AZAROSO  — mismo numero de empujones, misma fuerza, elegidos AL AZAR.
#   PASIVO   — mira los episodios del dirigido, sin actuar.
#
# LA CONDICION AZAROSO ES EL CORAZON. Sin ella, cualquier ventaja del dirigido podria ser
# simplemente "tocar informa mas que mirar", que es trivial. Lo que se mide es si ELEGIR BIEN que
# tocar vale mas que tocar al azar: la diferencia entre agitar el mundo y hacerle una pregunta.
#
# FRONTERA DE CONTAMINACION. A Diego no se le dice que hay dos objetos, ni que difieren, ni en que.
# La politica de eleccion solo puede usar cantidades que el ya calcula sobre sus propios datos —
# ninguna funcion menciona masa, peso ni ninguna propiedad del mundo por su nombre. Que "reducir la
# incertidumbre" lleve a tocar lo dudoso tiene que EMERGER, no programarse.
#
# Regla 31 (siete casos, declarados en el prerregistro ANTES de correr): la duda es real; tocar la
# resuelve; el dirigido gana al pasivo (control positivo); el dirigido gana al azaroso (el caso que
# decide); el señuelo agitador NO puede ganar; en un mundo sin duda la ventaja DESAPARECE; y por
# debajo de N toques no hay veredicto.

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

PASO_FISICO = 1.0 / 240.0
SUBPASOS = 8
N_ART = 3

# El mundo: dos objetos identicos a la vista, en dos sitios al alcance del brazo.
# LA z ES EXACTAMENTE EL MEDIO LADO (0.045): APOYADOS, no soltados desde arriba. Cazado por el
# caso 1 de esta misma Regla 31 en su primera corrida: con z=0.09 los objetos CAIAN 4.5 cm antes de
# quedarse quietos, y el asentamiento delata la masa a simple vista (diferencia visible 0.2176
# contra un techo de 0.05). Un experimento cuya duda se resuelve mirando no es un experimento.
SITIOS = ([0.42, 0.16, 0.045], [0.42, -0.16, 0.045])
PASOS_ASENTAR = 120     # y aun asi se deja asentar antes de mirar: el transitorio no es informacion
PISO_VISIBLE = 1e-4     # por debajo de esto nada se movio; la diferencia relativa es ruido dividido
                        # por ruido. Misma leccion que la guarda de piso de la escalera de soporte.
MASA_LIGERA = 0.15
MASA_PESADA = 1.20
FUERZA = 6.0            # el empujon, IDENTICO en todas las condiciones
PASOS_POR_TOQUE = 90    # cuanto se observa despues de cada empujon
TOQUES_MINIMOS = 12     # guarda de potencia: por debajo, no hay veredicto


def _mundo(semilla, con_duda=True):
    """Sortea que sitio esconde el objeto pesado. `con_duda=False` construye el mundo donde los dos
    son iguales por dentro: ahi la ventaja de intervenir DEBE desaparecer (caso 6 de la Regla 31)."""
    rng = np.random.default_rng(int(semilla) + 700019)
    pesado = int(rng.integers(0, 2)) if con_duda else None
    masas = [MASA_LIGERA, MASA_LIGERA]
    if con_duda:
        masas[pesado] = MASA_PESADA
    return {"pesado": pesado, "masas": masas, "con_duda": bool(con_duda)}


def _escena(mundo):
    """Levanta el mundo y devuelve (cliente, brazo, objetos). El brazo ALCANZA los dos sitios:
    es la unica diferencia de diseño con el Gimnasio de la escalera de soporte, y es toda la
    diferencia entre mirar y experimentar."""
    import pybullet as p
    cliente = p.connect(p.DIRECT)
    p.resetSimulation(physicsClientId=cliente)
    p.setGravity(0, 0, -9.8, physicsClientId=cliente)
    p.setTimeStep(PASO_FISICO, physicsClientId=cliente)
    p.createMultiBody(0, p.createCollisionShape(p.GEOM_PLANE, physicsClientId=cliente),
                      physicsClientId=cliente)
    esl = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.11, 0.03, 0.03],
                                 physicsClientId=cliente)
    base_c = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.05],
                                    physicsClientId=cliente)
    brazo = p.createMultiBody(
        baseMass=0, baseCollisionShapeIndex=base_c, basePosition=[0, 0, 0.20],
        linkMasses=[0.3] * N_ART, linkCollisionShapeIndices=[esl] * N_ART,
        linkVisualShapeIndices=[-1] * N_ART,
        linkPositions=[[0.15, 0, 0]] * N_ART,
        linkOrientations=[[0, 0, 0, 1]] * N_ART,
        linkInertialFramePositions=[[0, 0, 0]] * N_ART,
        linkInertialFrameOrientations=[[0, 0, 0, 1]] * N_ART,
        linkParentIndices=list(range(N_ART)),
        linkJointTypes=[p.JOINT_REVOLUTE] * N_ART,
        linkJointAxis=[[0, 0, 1], [0, 1, 0], [0, 0, 1]],
        physicsClientId=cliente)
    for j in range(N_ART):
        p.setJointMotorControl2(brazo, j, p.VELOCITY_CONTROL, force=0, physicsClientId=cliente)
    # LOS DOS OBJETOS: identicos de forma y tamaño. Solo la masa —invisible— los separa.
    forma = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.045, 0.045, 0.045],
                                   physicsClientId=cliente)
    objetos = [p.createMultiBody(mundo["masas"][i], forma, basePosition=SITIOS[i],
                                 physicsClientId=cliente) for i in range(2)]
    return cliente, brazo, objetos


def _observar(cliente, objetos):
    import pybullet as p
    fila = []
    for o in objetos:
        (x, y, z), _ = p.getBasePositionAndOrientation(o, physicsClientId=cliente)
        vx, vy, vz = p.getBaseVelocity(o, physicsClientId=cliente)[0]
        fila += [x, y, z, vx, vy, vz]
    return fila


def _empujar(cliente, objetos, cual, pasos=PASOS_POR_TOQUE):
    """UN empujon de fuerza fija sobre el objeto `cual`, y despues se mira que pasa.
    Devuelve el desplazamiento observado — la unica lectura, identica en las tres condiciones."""
    import pybullet as p
    antes = _observar(cliente, objetos)
    p.applyExternalForce(objetos[cual], -1, [FUERZA, 0, 0], SITIOS[cual], p.WORLD_FRAME,
                         physicsClientId=cliente)
    for _ in range(pasos * SUBPASOS):
        p.stepSimulation(physicsClientId=cliente)
    despues = _observar(cliente, objetos)
    i = 6 * cual
    return float(np.hypot(despues[i] - antes[i], despues[i + 1] - antes[i + 1]))


def _reponer(cliente, objetos):
    import pybullet as p
    for i, o in enumerate(objetos):
        p.resetBasePositionAndOrientation(o, SITIOS[i], [0, 0, 0, 1], physicsClientId=cliente)
        p.resetBaseVelocity(o, [0, 0, 0], [0, 0, 0], physicsClientId=cliente)


# ------------------------------------------------------- las politicas de eleccion
def _incertidumbre(observado):
    """Cuanto NO sabe de cada sitio. Solo mira SUS PROPIOS datos: cuantas veces toco cada uno y
    cuanto varian las respuestas que obtuvo. No menciona masa, ni peso, ni nada del mundo — esa es
    la frontera de la Regla 27 aplicada a la politica."""
    u = []
    for k in (0, 1):
        v = observado[k]
        if len(v) < 2:
            u.append(1.0)                      # nunca tocado: incertidumbre maxima
        else:
            # dispersion relativa: sitios que responden de forma inconsistente siguen siendo dudosos
            m = float(np.mean(v))
            u.append(float(np.std(v) / (abs(m) + 1e-9)) / max(1.0, len(v)))
    return u


def politica(nombre, observado, rng):
    """Devuelve a cual sitio tocar. UNICA diferencia entre las tres condiciones."""
    if nombre == "dirigido":
        u = _incertidumbre(observado)
        return int(np.argmax(u))               # ir donde mas ignoro
    if nombre == "azaroso":
        return int(rng.integers(0, 2))
    if nombre == "agitador":
        # SEÑUELO: toca SIEMPRE el mismo sitio, mucho y sin criterio. Actividad sin pregunta.
        return 0
    raise ValueError(nombre)


def _saber(observado, mundo):
    """Cuanto sabe: ¿puede decir cual de los dos es el distinto, y con cuanto margen?
    Puntaje = separacion relativa entre las respuestas medias de los dos sitios. Un sitio nunca
    tocado no aporta separacion: no saber es no saber."""
    if any(len(observado[k]) == 0 for k in (0, 1)):
        return 0.0
    a, b = float(np.mean(observado[0])), float(np.mean(observado[1]))
    sep = abs(a - b) / (abs(a) + abs(b) + 1e-9)
    if not mundo["con_duda"]:
        return float(sep)                      # sin duda que resolver, la separacion es ruido
    # ACIERTO: el objeto pesado debe moverse MENOS. Se exige que el orden sea el correcto; si el
    # ente "separa" pero al reves, no sabe nada — sabe al reves.
    menor = 0 if a < b else 1
    return float(sep) if menor == mundo["pesado"] else -float(sep)


def correr(condicion, semilla=1, toques=TOQUES_MINIMOS, con_duda=True, mundo=None):
    """Un episodio completo de una condicion. El PASIVO no actua: ve los mismos episodios que el
    dirigido produjo, sin poder cambiar ninguno."""
    import pybullet as p
    mundo = mundo or _mundo(semilla, con_duda=con_duda)
    rng = np.random.default_rng(int(semilla) + 31337)
    if condicion == "pasivo":
        # Ve lo que el dirigido hizo. Sin acceso a la eleccion: solo al resultado.
        vistos = correr("dirigido", semilla=semilla, toques=toques, con_duda=con_duda,
                        mundo=mundo)["observado"]
        return {"condicion": "pasivo", "mundo": mundo, "observado": vistos,
                "puntaje": _saber(vistos, mundo), "toques": toques,
                "nota": "no eligio nada: heredo los episodios del dirigido"}
    cliente, brazo, objetos = _escena(mundo)
    try:
        observado = {0: [], 1: []}
        elecciones = []
        for _ in range(toques):
            cual = politica(condicion, observado, rng)
            elecciones.append(cual)
            d = _empujar(cliente, objetos, cual)
            observado[cual].append(d)
            _reponer(cliente, objetos)
        return {"condicion": condicion, "mundo": mundo, "observado": observado,
                "puntaje": _saber(observado, mundo), "toques": toques,
                "reparto": [elecciones.count(0), elecciones.count(1)]}
    finally:
        p.disconnect(physicsClientId=cliente)


def _mirando_sin_tocar(mundo, semilla=1, pasos=60, mover_uno=False):
    """CASO 1 de la Regla 31: mirando la escena EN REPOSO, ¿se distingue el objeto pesado?
    Debe dar ~0. Si diera algo, no habria duda que resolver y todo el experimento seria falso.

    `mover_uno=True` es el CONTROL POSITIVO DE ESTA MISMA MEDIDA: se le da velocidad inicial a uno
    solo, asi que la diferencia visible existe de verdad y la medida TIENE que verla. Sin este lado,
    el caso 1 se aprobaria con una medida ciega — que es exactamente el agujero que el prereg-36
    nos enseño a tapar: alli protegimos el falso positivo y dejamos abierto el falso negativo."""
    import pybullet as p
    cliente, brazo, objetos = _escena(mundo)
    try:
        if mover_uno:
            p.resetBaseVelocity(objetos[0], [0.6, 0, 0], [0, 0, 0], physicsClientId=cliente)
        if not mover_uno:
            for _ in range(PASOS_ASENTAR * SUBPASOS):  # se deja asentar: el transitorio no cuenta
                p.stepSimulation(physicsClientId=cliente)
        filas = []
        for _ in range(pasos):
            for _ in range(SUBPASOS):
                p.stepSimulation(physicsClientId=cliente)
            filas.append(_observar(cliente, objetos))
        x = np.array(filas, dtype=float)
        # CUANTO SE MOVIO CADA UNO: desviacion EN EL TIEMPO, eje por eje. Cazado por este mismo
        # caso: agrupar los tres ejes en un solo std mide que un objeto esta en y=+0.16 y el otro
        # en y=-0.16 —la geometria del montaje— y no si alguno se movio. Daba 0.21 con los dos
        # objetos perfectamente quietos.
        a = float(np.max(np.std(x[:, 0:3], axis=0)))
        b = float(np.max(np.std(x[:, 6:9], axis=0)))
        # GUARDA DE PISO: si NINGUNO se movio por encima del piso, no hay nada visible y la
        # diferencia es cero POR CONSTRUCCION — no un cociente de dos ruidos, que se dispara solo.
        if max(a, b) < PISO_VISIBLE:
            return 0.0
        return abs(a - b) / (a + b + 1e-9)
    finally:
        p.disconnect(physicsClientId=cliente)


def regla31(verbose=True, toques=TOQUES_MINIMOS):
    if toques < TOQUES_MINIMOS:
        raise SystemExit(f"MEDICION INVALIDA: {toques} toques (minimo {TOQUES_MINIMOS}). Con menos "
                         f"intervenciones la diferencia entre elegir y no elegir no puede verse.")
    fallos = []
    mundo = _mundo(1)

    # 1) LA DUDA ES REAL, POR LOS DOS LADOS: mirando quietos no se distinguen (debe dar ~0), Y la
    #    medida no es ciega — con una diferencia visible plantada TIENE que verla.
    visto = _mirando_sin_tocar(mundo)
    visible = _mirando_sin_tocar(mundo, mover_uno=True)
    c1 = visto < 0.05 and visible > 0.50
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} LA DUDA ES REAL: en reposo la diferencia visible es "
              f"{visto:.4f} (< 0.05), y con una diferencia PLANTADA la misma medida la ve: "
              f"{visible:.4f} (> 0.50) — no es una medida ciega aprobando")
    if not c1:
        fallos.append("duda-real")

    # 2) TOCAR LA RESUELVE: un solo empujon a cada uno ya separa.
    import pybullet as p
    cliente, brazo, objetos = _escena(mundo)
    try:
        d0 = _empujar(cliente, objetos, 0); _reponer(cliente, objetos)
        d1 = _empujar(cliente, objetos, 1)
    finally:
        p.disconnect(physicsClientId=cliente)
    sep = abs(d0 - d1) / (d0 + d1 + 1e-9)
    menor_ok = (0 if d0 < d1 else 1) == mundo["pesado"]
    c2 = sep > 0.20 and menor_ok
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} TOCAR LA RESUELVE: un empujon separa {sep:.3f} "
              f"(d0={d0:.4f}, d1={d1:.4f}) y el pesado se mueve menos: {menor_ok}")
    if not c2:
        fallos.append("tocar-resuelve")

    dir1 = correr("dirigido", semilla=1, toques=toques)
    pas1 = correr("pasivo", semilla=1, toques=toques)
    # AQUI VIVIA `azа1 = correr("azaroso", ...)`, calculado y nunca usado — y el nombre llevaba
    # una 'a' cirilica por un desliz de teclado, asi que ninguna busqueda por texto lo encontraba.
    # Consecuencia real: la Regla 31 de este modulo NUNCA probo la condicion azarosa, que es
    # justamente la que decide si ELEGIR vale mas que ACTUAR. Cazado por la ficha de sanidad el
    # 10-ago-2026. El estudio ya estaba cerrado como NO CONCLUYENTE (INFORME-46) y lo sustituye
    # experimentar2.py, que si la prueba; queda escrito para que conste que el banco tenia un
    # caso menos de los que aparentaba.

    # 3) CONTROL POSITIVO: el que interviene supera al que solo mira. Si ni aqui ganara, la
    #    comparacion seria ciega y ningun resultado posterior significaria nada.
    c3 = dir1["puntaje"] > pas1["puntaje"] or abs(dir1["puntaje"] - pas1["puntaje"]) < 1e-9
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} CONTROL POSITIVO: dirigido {dir1['puntaje']:.4f} vs "
              f"pasivo {pas1['puntaje']:.4f} (el pasivo HEREDA sus episodios: empatar es el suelo, "
              f"no un exito)")
    if not c3:
        fallos.append("control-positivo")

    # 4) EL SEÑUELO DEL AGITADOR: tocar mucho y sin criterio no puede ganar. Es el hermano del
    #    señuelo de ruido de la escalera y del agitado del prereg-36 — los dos cazaron fallos
    #    reales en su primera corrida.
    agi = correr("agitador", semilla=1, toques=toques)
    c4 = agi["puntaje"] <= dir1["puntaje"]
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} SEÑUELO AGITADOR: toca siempre el mismo sitio "
              f"(reparto {agi['reparto']}) y puntua {agi['puntaje']:.4f} <= dirigido "
              f"{dir1['puntaje']:.4f}")
    if not c4:
        fallos.append("senuelo-agitador")

    # 5) MUNDO SIN DUDA: si los dos objetos son iguales tambien por dentro, la ventaja de
    #    intervenir DEBE desaparecer. Un instrumento que premia la intervencion donde no hay nada
    #    que averiguar esta midiendo su propio entusiasmo.
    sin = correr("dirigido", semilla=1, toques=toques, con_duda=False)
    c5 = abs(sin["puntaje"]) < 0.20
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} MUNDO SIN DUDA: sin nada que averiguar el dirigido "
              f"puntua {sin['puntaje']:.4f} (debe quedarse cerca de 0)")
    if not c5:
        fallos.append("mundo-sin-duda")

    # 6) EL DIRIGIDO REPARTE SUS TOQUES; el azaroso tambien, pero por otra razon. Lo que NO puede
    #    pasar es que el dirigido se comporte como el agitador: si concentra todo en un sitio, su
    #    "eleccion" no esta usando la incertidumbre para nada.
    c6 = min(dir1["reparto"]) >= 2
    if verbose:
        print(f"  {'ok  ' if c6 else 'FALLO'} EL DIRIGIDO EXPLORA: reparto {dir1['reparto']} — "
              f"no se comporta como el agitador")
    if not c6:
        fallos.append("dirigido-explora")

    # 7) GUARDA DE POTENCIA declarada y viva.
    c7 = TOQUES_MINIMOS >= 12
    if verbose:
        print(f"  {'ok  ' if c7 else 'FALLO'} GUARDA DE POTENCIA: minimo {TOQUES_MINIMOS} toques, "
              f"por debajo el modulo se niega a dar veredicto")
    if not c7:
        fallos.append("guarda-potencia")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la duda es real, tocar la resuelve, y la vara no premia "
                                "la agitacion." if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="La experimentacion dirigida (prereg-37)")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--semilla", type=int, default=None)
    ap.add_argument("--toques", type=int, default=TOQUES_MINIMOS)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31(toques=a.toques))
    if a.semilla is None:
        print("uso: --regla31 | --semilla N [--toques K]")
        return
    if a.toques < TOQUES_MINIMOS:
        raise SystemExit(f"MEDICION INVALIDA: {a.toques} toques (minimo {TOQUES_MINIMOS}).")
    mundo = _mundo(a.semilla)
    filas = {c: correr(c, semilla=a.semilla, toques=a.toques, mundo=mundo)
             for c in ("dirigido", "azaroso", "pasivo")}
    d, z, p_ = (filas["dirigido"]["puntaje"], filas["azaroso"]["puntaje"],
                filas["pasivo"]["puntaje"])
    salida = {
        "prerregistro": 37, "semilla": a.semilla, "toques": a.toques, "mundo": mundo,
        "condiciones": {k: {kk: vv for kk, vv in v.items() if kk != "observado"}
                        for k, v in filas.items()},
        "dirigido_menos_azaroso": round(d - z, 4),
        "dirigido_menos_pasivo": round(d - p_, 4),
        "veredicto": ("EL CUERPO APORTA CUANDO ELIGE" if d - z > 0.10 else
                      "ACTUAR SI, ELEGIR NO" if d - p_ > 0.10 else
                      "EMPATE TOTAL — ni siquiera intervenir aporta aqui"),
        "nota": "el veredicto del hito exige las 5 semillas juntas; esto es una sola",
    }
    out = os.path.join(BASE, "resultados", f"p37-experimentar-s{a.semilla}")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False, default=str)
    print(f"guardado en {out}/resumen.json (parcial — el veredicto exige las 5 semillas juntas)")


if __name__ == "__main__":
    main()
