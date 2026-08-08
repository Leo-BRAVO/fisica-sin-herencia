# gimnasio.py — EL MUNDO DONDE DIEGO TIENE MANOS (gen G3: acción; prerregistro-19, FIRMADO)
#
# Hasta hoy Diego solo MIRABA grabaciones. El INFORME-30 midió que mirando no se puede separar
# "hay una ley" de "hay textura con deriva" — y la literatura lo dice como teorema: con datos
# puramente observacionales la estructura causal solo se identifica hasta su clase de equivalencia;
# hacen falta INTERVENCIONES. El Gimnasio es el escalón 2 de la escalera causal: HACER.
#
# ============================ LA CONFESIÓN, Y VA EN CADA NODO ============================
# La física de este mundo es CÓDIGO HUMANO. Diego no descubrirá aquí el universo: descubrirá
# NUESTRO SIMULADOR. Por eso todo lo aprendido en el Gimnasio se marca `sobre-el-simulador` y
# JAMÁS entra al árbol como física del mundo. El Gimnasio no sirve para descubrir física: sirve
# para que EMERJAN CAPACIDADES (la frontera yo/mundo, la noción de intervenir, la de invariante)
# que después se aplican a datos del universo real.
# =========================================================================================
#
# Lo que este archivo construye:
#   - una escena mínima y DETERMINISTA: suelo, un brazo de 3 articulaciones, 3 objetos libres
#   - BALBUCEO (G7): comandos motores suaves y aleatorios, sin ninguna recompensa de tarea
#   - el registro de cada episodio: comandos + estado, con la ETIQUETA VERDADERA cuerpo/mundo
#     que se conoce por construcción del simulador y que DIEGO JAMÁS VE (es del lado de los jueces)
#   - los CUATRO MUNDOS DE CONTROL de la Regla 31, construidos dentro del propio simulador
#
# Uso:
#   python gimnasio.py --regla31                    (los cuatro controles, de punta a punta)
#   python gimnasio.py --episodios 12 --salida <carpeta> [--pasos 1200]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

PASO_FISICO = 1.0 / 240.0
SUBPASOS = 8                 # un cuadro de observación cada 8 pasos físicos -> 30 "cuadros"/s
N_ARTICULACIONES = 3
N_OBJETOS = 3
TAM_IMAGEN = 64              # el mismo lado que percepcion.py — sus ojos son los de siempre
# CÁMARA FIJA: un solo punto de vista, inmóvil, como una cámara de trípode. Si la cámara se
# moviera, el movimiento propio de la cámara entraría en los píxeles y Diego lo confundiría
# con movimiento del mundo (Regla 25: cámara en movimiento sin referencia fija invalida datos).
CAMARA = ([1.7, -1.7, 1.15], [0.38, 0.0, 0.55], [0, 0, 1])
# Lista de un elemento para poder apagarla en el control del nivel B sin tocar la firma de
# _construir: si al quitar la gravedad el "primer no-yo" sigue apareciendo, es que lo inventamos.
GRAVEDAD = [-9.8]

# ============================ EL DISEÑO DEL CUERPO ES UNA VARIABLE ============================
# Orden del director (8-ago-2026): "repensemos el gimnasio como nadie lo ha hecho, probemos muchas
# variables sin violar las reglas". Todo lo de aquí es diseño DE SU CUERPO y de SU CÁMARA — nada
# es un hecho sobre el mundo, así que nada contamina (Reglas 1-4). Pero elegir el diseño por cuál
# supera la prueba ES una forma de ajuste: por eso la búsqueda se hace en unas semillas y el
# ganador se verifica en semillas FRESCAS que la búsqueda nunca vio (protocolo del prereg-24).
# EL CUERPO GANADOR (barrido del 8-ago-2026, protocolo del prerregistro-24): 8 diseños probados,
# búsqueda en semillas 1000-1011 y VERIFICACIÓN en semillas frescas 7000-7011 que la búsqueda
# nunca vio. Ganador: 28/28 en búsqueda y **28/28 en frescas** — no está sobreajustado.
# LO QUE MANDA ES EL TOPE ARTICULAR, y eso FALSIFICA la predicción que firmé: yo aposté por la
# amortiguación y la amortiguación EMPEORA (0.3 -> 26/28, 1.0 -> 22/28). La razón, vista después:
# sin topes el brazo gira como una hélice y su ángulo se vuelve historia acumulada pura, donde el
# comando es un empujón marginal; con topes vive en un espacio acotado y cada impulso se nota.
# También se probó el balbuceo AISLADO (un miembro a la vez, como los bebés): 26/28 y 23/28 — la
# idea era buena y el mundo dijo que no. Queda registrada, no borrada.
DISENO = {
    "amortiguacion": 0.0,     # rozamiento viscoso: PROBADO Y RECHAZADO por la evidencia
    "limite": 2.5,            # TOPE ARTICULAR en radianes — la variable que resultó decisiva
    "suavizado": 15,          # cuán lentos son sus impulsos motores
    "amplitud": 2.2,          # cuán fuertes
    "subpasos": 8,            # cada cuántos pasos de física observa (su tasa de muestreo)
    # IDEA DEL DIRECTOR (8-ago-2026): "a veces las soluciones están en cosas más creativas".
    # BALBUCEO AISLADO — mover UN MIEMBRO A LA VEZ. Es lo que hacen los bebés antes de coordinar,
    # y resuelve de raíz el problema de atribución: si solo se mueve una articulación, saber cuál
    # respondió deja de ser un problema estadístico. Es su PROGRAMA MOTOR, no un hecho del mundo.
    "aislado": 0,             # 0 = todos a la vez; N>0 = un miembro a la vez, cambiando cada N cuadros
    "reposo": 0,              # 0 = nunca; N>0 = vuelve a su postura de reposo cada N cuadros
}

# MODOS: los controles de la Regla 31 viven DENTRO del mundo, no en datos sintéticos aparte.
MODOS = {
    "normal":        "el cuerpo obedece a los tres comandos",
    "sin_agencia":   "los comandos se emiten pero NO se aplican (control 1 del prereg-19)",
    "un_grado":      "solo la articulación 0 obedece (control 2 del prereg-19)",
    "tv_ruidoso":    "la articulación 1 responde al comando con RUIDO PURO (control 3, INF-30)",
    "sin_gravedad":  "el cuerpo obedece, pero NO HAY GRAVEDAD (control del nivel B)",
}


def _construir(p, cliente):
    """Escena mínima, sin ninguna forma que insinúe física humana: un suelo, un brazo de tres
    eslabones anclado, y objetos libres que caen. Todo con masas y tamaños arbitrarios."""
    p.resetSimulation(physicsClientId=cliente)
    p.setGravity(0, 0, GRAVEDAD[0], physicsClientId=cliente)
    p.setTimeStep(PASO_FISICO, physicsClientId=cliente)

    suelo_c = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=cliente)
    p.createMultiBody(0, suelo_c, physicsClientId=cliente)

    # brazo: base fija + 3 eslabones con articulaciones de revoluta
    esl = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.16, 0.04, 0.04],
                                 physicsClientId=cliente)
    base_c = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.08, 0.08, 0.08],
                                    physicsClientId=cliente)
    # Formas VISIBLES: la cámara de Diego necesita ver algo. Grises distintos y arbitrarios —
    # ningún color codifica "esto es tu cuerpo": eso es justo lo que él tiene que averiguar.
    esl_v = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.16, 0.04, 0.04],
                                rgbaColor=[0.80, 0.80, 0.80, 1], physicsClientId=cliente)
    base_v = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.08, 0.08, 0.08],
                                 rgbaColor=[0.55, 0.55, 0.55, 1], physicsClientId=cliente)
    brazo = p.createMultiBody(
        baseMass=0, baseCollisionShapeIndex=base_c, baseVisualShapeIndex=base_v,
        basePosition=[0, 0, 0.6],
        linkMasses=[0.4] * N_ARTICULACIONES,
        linkCollisionShapeIndices=[esl] * N_ARTICULACIONES,
        linkVisualShapeIndices=[esl_v] * N_ARTICULACIONES,
        linkPositions=[[0.22, 0, 0]] * N_ARTICULACIONES,
        linkOrientations=[[0, 0, 0, 1]] * N_ARTICULACIONES,
        linkInertialFramePositions=[[0, 0, 0]] * N_ARTICULACIONES,
        linkInertialFrameOrientations=[[0, 0, 0, 1]] * N_ARTICULACIONES,
        linkParentIndices=list(range(N_ARTICULACIONES)),
        linkJointTypes=[p.JOINT_REVOLUTE] * N_ARTICULACIONES,
        linkJointAxis=[[0, 0, 1], [0, 1, 0], [0, 0, 1]],
        physicsClientId=cliente)
    for j in range(N_ARTICULACIONES):
        p.setJointMotorControl2(brazo, j, p.VELOCITY_CONTROL, force=0,
                                physicsClientId=cliente)
        if DISENO["limite"] is not None:
            p.changeDynamics(brazo, j, jointLowerLimit=-DISENO["limite"],
                             jointUpperLimit=DISENO["limite"], physicsClientId=cliente)

    objetos = []
    caja = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.07, 0.07, 0.07],
                                  physicsClientId=cliente)
    for i in range(N_OBJETOS):
        caja_v = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.07, 0.07, 0.07],
                                     rgbaColor=[0.30 + 0.18 * i, 0.30 + 0.18 * i,
                                                0.30 + 0.18 * i, 1],
                                     physicsClientId=cliente)
        objetos.append(p.createMultiBody(
            baseMass=0.25, baseCollisionShapeIndex=caja, baseVisualShapeIndex=caja_v,
            basePosition=[0.45 + 0.22 * i, 0.12 * (i - 1), 1.15 + 0.2 * i],
            physicsClientId=cliente))
    return brazo, objetos


def _balbuceo(pasos, n, rng, suavizado=None):
    """G7 — el juego: comandos SUAVES y aleatorios, sin objetivo. Suaves a propósito: un balbuceo
    de ruido blanco no mueve un cuerpo con inercia, y además el caso suave es el DIFÍCIL para el
    detector de contingencia (un comando suave codifica 'cuándo')."""
    suavizado = suavizado or DISENO["suavizado"]
    k = np.ones(suavizado) / suavizado
    com = np.column_stack([
        np.convolve(rng.normal(size=pasos + suavizado - 1), k, mode="valid")[:pasos]
        * DISENO["amplitud"] for _ in range(n)])
    if DISENO["aislado"]:
        # un miembro a la vez: fuera del turno, el comando es CERO (no ausente: cero de verdad,
        # porque "no mandé nada" es información tan válida como "mandé esto").
        mascara = np.zeros_like(com)
        for t in range(pasos):
            mascara[t, (t // DISENO["aislado"]) % n] = 1.0
        com = com * mascara
    return com


def episodio(semilla, pasos=1200, modo="normal", render=False, sensores=False):
    """Corre un episodio y devuelve (comandos, señales, etiqueta_verdadera).

    señales: [3 ángulos del cuerpo] + [3 alturas de objetos] + [1 distancia entre dos objetos]
    render: si es True devuelve TAMBIÉN los cuadros de cámara (T, 64, 64) — lo único que Diego
      llega a ver cuando el Gimnasio corre en su modo verdadero.
    sensores: si es True devuelve ADEMÁS los SENTIDOS DEL CUERPO (T, 9): ángulo y velocidad de
      cada articulación (PROPIOCEPCIÓN — los husos musculares del bebé, que los tiene desde el
      útero, antes de que madure la vista) y contacto binario por eslabón (TACTO — los
      mecanorreceptores). AUDITORÍA DE SENTIDOS 8-ago-2026: Diego solo se veía a sí mismo por
      cámara — un bebé ciego se descubre igual, porque se SIENTE. Legalidad: son sensores DE SU
      CUERPO; nadie le dice qué canal es cuerpo — eso sigue emergiendo por contingencia. El estado de arriba es de los
      jueces: sirve para saber si acertó, jamás para que aprenda.
    etiqueta_verdadera: qué columnas son CUERPO por construcción del simulador.
      *** ESTA ETIQUETA ES DE LOS JUECES. Diego jamás la recibe. ***
    """
    import pybullet as p
    cliente = p.connect(p.DIRECT)
    GRAVEDAD[0] = 0.0 if modo == "sin_gravedad" else -9.8
    try:
        rng = np.random.default_rng(semilla)
        brazo, objetos = _construir(p, cliente)
        comandos = _balbuceo(pasos, N_ARTICULACIONES, rng)
        rng_tv = np.random.default_rng(semilla + 99991)

        filas, cuadros, sentidos = [], [], []
        if render:
            vm = p.computeViewMatrix(*CAMARA)
            pm = p.computeProjectionMatrixFOV(60, 1.0, 0.1, 8.0)
        for t in range(pasos):
            for j in range(N_ARTICULACIONES):
                if modo == "sin_agencia":
                    par = 0.0
                elif modo == "un_grado":
                    par = float(comandos[t, j]) if j == 0 else 0.0
                elif modo == "tv_ruidoso" and j == 1:
                    # obedece... con ruido puro: la magnitud del comando solo fija la varianza
                    par = float(rng_tv.normal(0.0, 0.4 + 1.6 * abs(comandos[t, j])))
                else:
                    par = float(comandos[t, j])
                if DISENO["amortiguacion"]:
                    w = p.getJointState(brazo, j, physicsClientId=cliente)[1]
                    par -= DISENO["amortiguacion"] * w
                p.setJointMotorControl2(brazo, j, p.TORQUE_CONTROL, force=par,
                                        physicsClientId=cliente)
            for _ in range(DISENO["subpasos"]):
                p.stepSimulation(physicsClientId=cliente)
            if DISENO["reposo"] and t % DISENO["reposo"] == DISENO["reposo"] - 1:
                for j in range(N_ARTICULACIONES):
                    p.resetJointState(brazo, j, 0.0, 0.0, physicsClientId=cliente)

            ang = [p.getJointState(brazo, j, physicsClientId=cliente)[0]
                   for j in range(N_ARTICULACIONES)]
            pos = [p.getBasePositionAndOrientation(o, physicsClientId=cliente)[0]
                   for o in objetos]
            alturas = [q[2] for q in pos]
            d01 = float(np.linalg.norm(np.array(pos[0]) - np.array(pos[1])))
            filas.append(ang + alturas + [d01])
            if sensores:
                vel = [p.getJointState(brazo, j, physicsClientId=cliente)[1]
                       for j in range(N_ARTICULACIONES)]
                contactos = []
                for j in range(N_ARTICULACIONES):
                    pts = p.getContactPoints(bodyA=brazo, linkIndexA=j, physicsClientId=cliente)
                    contactos.append(1.0 if pts else 0.0)
                sentidos.append(ang + vel + contactos)
            if render:
                w_, h_, rgb, _, _ = p.getCameraImage(TAM_IMAGEN, TAM_IMAGEN, vm, pm,
                                                     renderer=p.ER_TINY_RENDERER,
                                                     physicsClientId=cliente)
                cuadros.append(np.reshape(rgb, (h_, w_, 4))[:, :, :3].mean(axis=2) / 255.0)

        senales = np.array(filas, dtype=float)
        # verdad de los jueces: las 3 primeras columnas son el cuerpo... salvo donde el control
        # lo cambia a propósito.
        if modo == "sin_agencia":
            cuerpo = set()
        elif modo == "un_grado":
            cuerpo = {0}
        elif modo == "tv_ruidoso":
            cuerpo = {0, 2}          # la 1 responde con ruido: NO es agencia, es televisor
        elif modo == "sin_gravedad":
            cuerpo = {0, 1, 2}
        else:
            cuerpo = {0, 1, 2}
        extra = []
        if render:
            extra.append(np.stack(cuadros).astype(np.float32))
        if sensores:
            extra.append(np.array(sentidos, dtype=float))
        if extra:
            return (comandos, senales, cuerpo, *extra)
        return comandos, senales, cuerpo
    finally:
        p.disconnect(physicsClientId=cliente)


def correr(n_episodios=12, pasos=1200, modo="normal", semilla0=1000, render=False):
    eps, verdad, videos = [], None, []
    for i in range(n_episodios):
        r = episodio(semilla0 + i, pasos=pasos, modo=modo, render=render)
        if render:
            c, s, v, vid = r
            videos.append(vid)
        else:
            c, s, v = r
        eps.append((c, s))
        verdad = v
    return (eps, verdad, videos) if render else (eps, verdad)


# pasos=1200 x 3 jueces da 23 ventanas: por encima del minimo de 20 que exige
# contingencia.py tras el endurecimiento del 8-ago-2026.
def regla31(pasos=1200, n_episodios=12, verbose=True):
    """LOS CUATRO CONTROLES DEL PRERREGISTRO-19, corridos DENTRO del simulador de punta a punta.
    Si el Gimnasio no los pasa, no puede producir ningún hito."""
    from contingencia import medir
    jueces = [10, 11, 12]
    fallos = []
    if verbose:
        print("=== REGLA 31 del GIMNASIO — los controles corridos dentro del propio mundo ===")
        print(f"    {n_episodios} episodios x {pasos} cuadros | jueces congelados {jueces}\n")
    for modo, desc in MODOS.items():
        if modo == "sin_gravedad":
            continue   # su sitio es el control del nivel B, no el hito 0
        eps, verdad = correr(n_episodios, pasos, modo)
        res = medir(eps, jueces, nulos=8)
        hall = {r["variable"] for r in res if r["es_mia"]}
        ok = hall == verdad
        if verbose:
            det = " ".join(f"v{r['variable']}={r['obedece_en']:.2f}"
                           f"{'*' if r['es_mia'] else ''}" for r in res)
            print(f"  {'ok  ' if ok else 'FALLO'} {modo:<13} {desc}")
            print(f"        cuerpo real={sorted(verdad) or 'ninguno'}  "
                  f"hallado={sorted(hall) or 'ninguno'}")
            print(f"        {det}")
        if not ok:
            fallos.append(modo)
    if verbose:
        print()
        print("REGLA 31 DEL GIMNASIO: APRUEBA — el mundo y el detector se entienden"
              if not fallos else
              f"REGLA 31 DEL GIMNASIO: REPRUEBA en {fallos} — no puede producir hitos")
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G3: el Gimnasio — el mundo donde Diego actúa")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--episodios", type=int, default=12)
    ap.add_argument("--pasos", type=int, default=1200)
    ap.add_argument("--modo", default="normal", choices=list(MODOS))
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    eps, verdad = correr(a.episodios, a.pasos, a.modo)
    if a.salida:
        os.makedirs(a.salida, exist_ok=True)
        for i, (c, s) in enumerate(eps, 1):
            np.savez(os.path.join(a.salida, f"episodio_{i:02d}.npz"), comandos=c, senales=s)
        # la verdad va APARTE: es de los jueces, no del cuerpo de datos que Diego lee
        with open(os.path.join(a.salida, "VERDAD-DE-LOS-JUECES.json"), "w") as f:
            json.dump({"modo": a.modo, "columnas_cuerpo": sorted(verdad),
                       "aviso": "Diego JAMAS lee este archivo (Reglas 27 y 28)"}, f, indent=2)
    print(f"{len(eps)} episodios modo={a.modo} | señales {eps[0][1].shape} | "
          f"cuerpo real (jueces): {sorted(verdad)}")
