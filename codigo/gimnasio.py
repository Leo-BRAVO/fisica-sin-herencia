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

# MODOS: los controles de la Regla 31 viven DENTRO del mundo, no en datos sintéticos aparte.
MODOS = {
    "normal":        "el cuerpo obedece a los tres comandos",
    "sin_agencia":   "los comandos se emiten pero NO se aplican (control 1 del prereg-19)",
    "un_grado":      "solo la articulación 0 obedece (control 2 del prereg-19)",
    "tv_ruidoso":    "la articulación 1 responde al comando con RUIDO PURO (control 3, INF-30)",
}


def _construir(p, cliente):
    """Escena mínima, sin ninguna forma que insinúe física humana: un suelo, un brazo de tres
    eslabones anclado, y objetos libres que caen. Todo con masas y tamaños arbitrarios."""
    p.resetSimulation(physicsClientId=cliente)
    p.setGravity(0, 0, -9.8, physicsClientId=cliente)
    p.setTimeStep(PASO_FISICO, physicsClientId=cliente)

    suelo_c = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=cliente)
    p.createMultiBody(0, suelo_c, physicsClientId=cliente)

    # brazo: base fija + 3 eslabones con articulaciones de revoluta
    esl = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.16, 0.04, 0.04],
                                 physicsClientId=cliente)
    base_c = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.08, 0.08, 0.08],
                                    physicsClientId=cliente)
    brazo = p.createMultiBody(
        baseMass=0, baseCollisionShapeIndex=base_c, basePosition=[0, 0, 0.6],
        linkMasses=[0.4] * N_ARTICULACIONES,
        linkCollisionShapeIndices=[esl] * N_ARTICULACIONES,
        linkVisualShapeIndices=[-1] * N_ARTICULACIONES,
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

    objetos = []
    caja = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.07, 0.07, 0.07],
                                  physicsClientId=cliente)
    for i in range(N_OBJETOS):
        objetos.append(p.createMultiBody(
            baseMass=0.25, baseCollisionShapeIndex=caja,
            basePosition=[0.45 + 0.22 * i, 0.12 * (i - 1), 1.15 + 0.2 * i],
            physicsClientId=cliente))
    return brazo, objetos


def _balbuceo(pasos, n, rng, suavizado=15):
    """G7 — el juego: comandos SUAVES y aleatorios, sin objetivo. Suaves a propósito: un balbuceo
    de ruido blanco no mueve un cuerpo con inercia, y además el caso suave es el DIFÍCIL para el
    detector de contingencia (un comando suave codifica 'cuándo')."""
    k = np.ones(suavizado) / suavizado
    return np.column_stack([
        np.convolve(rng.normal(size=pasos + suavizado - 1), k, mode="valid")[:pasos] * 2.2
        for _ in range(n)])


def episodio(semilla, pasos=1200, modo="normal"):
    """Corre un episodio y devuelve (comandos, señales, etiqueta_verdadera).

    señales: [3 ángulos del cuerpo] + [3 alturas de objetos] + [1 distancia entre dos objetos]
    etiqueta_verdadera: qué columnas son CUERPO por construcción del simulador.
      *** ESTA ETIQUETA ES DE LOS JUECES. Diego jamás la recibe. ***
    """
    import pybullet as p
    cliente = p.connect(p.DIRECT)
    try:
        rng = np.random.default_rng(semilla)
        brazo, objetos = _construir(p, cliente)
        comandos = _balbuceo(pasos, N_ARTICULACIONES, rng)
        rng_tv = np.random.default_rng(semilla + 99991)

        filas = []
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
                p.setJointMotorControl2(brazo, j, p.TORQUE_CONTROL, force=par,
                                        physicsClientId=cliente)
            for _ in range(SUBPASOS):
                p.stepSimulation(physicsClientId=cliente)

            ang = [p.getJointState(brazo, j, physicsClientId=cliente)[0]
                   for j in range(N_ARTICULACIONES)]
            pos = [p.getBasePositionAndOrientation(o, physicsClientId=cliente)[0]
                   for o in objetos]
            alturas = [q[2] for q in pos]
            d01 = float(np.linalg.norm(np.array(pos[0]) - np.array(pos[1])))
            filas.append(ang + alturas + [d01])

        senales = np.array(filas, dtype=float)
        # verdad de los jueces: las 3 primeras columnas son el cuerpo... salvo donde el control
        # lo cambia a propósito.
        if modo == "sin_agencia":
            cuerpo = set()
        elif modo == "un_grado":
            cuerpo = {0}
        elif modo == "tv_ruidoso":
            cuerpo = {0, 2}          # la 1 responde con ruido: NO es agencia, es televisor
        else:
            cuerpo = {0, 1, 2}
        return comandos, senales, cuerpo
    finally:
        p.disconnect(physicsClientId=cliente)


def correr(n_episodios=12, pasos=1200, modo="normal", semilla0=1000):
    eps, verdad = [], None
    for i in range(n_episodios):
        c, s, v = episodio(semilla0 + i, pasos=pasos, modo=modo)
        eps.append((c, s))
        verdad = v
    return eps, verdad


def regla31(pasos=900, n_episodios=12, verbose=True):
    """LOS CUATRO CONTROLES DEL PRERREGISTRO-19, corridos DENTRO del simulador de punta a punta.
    Si el Gimnasio no los pasa, no puede producir ningún hito."""
    from contingencia import medir
    jueces = [10, 11, 12]
    fallos = []
    if verbose:
        print("=== REGLA 31 del GIMNASIO — los controles corridos dentro del propio mundo ===")
        print(f"    {n_episodios} episodios x {pasos} cuadros | jueces congelados {jueces}\n")
    for modo, desc in MODOS.items():
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
