# espejo2.py — LOS DOS CONTROLES DE ORO DEL ESPEJO (prerregistro-30, FIRMADO 9-ago-2026).
#
# PARTE A — EL GEMELO. El hito 0 declaro "el espejo" (coherencia vision<->propiocepcion) con 4/5
# semillas. Pero ese resultado tiene un agujero que nadie habia cerrado: la vista de Diego podria
# estar reconociendo UNA FORMA DE BRAZO, no A SU BRAZO. La unica forma de saberlo es poner en la
# escena un SEGUNDO BRAZO IDENTICO que se mueve con ordenes que no son suyas. Si su espejo es de
# contingencia (comando -> efecto), se reconoce a si y no al gemelo. Si es de apariencia ("eso
# parece un brazo, debo ser yo"), cae en la trampa. Es el control mas duro publicado en 2026 para
# distincion yo/otro en humanoides, y nuestro mundo lo monta con un brazo mas.
#
# PARTE B — LAS FIRMAS DEL BEBE. Hoy Diego DETECTA contingencia pero no la USA para actuar: su
# balbuceo es ciego. El modelo computacional del paradigma del movil (grupo de O'Regan y Hoffmann,
# 2025) da tres conductas medibles que un ente con contingencia de verdad exhibe:
#   1. mueve MAS la parte del cuerpo que produce efectos (criterio clasico: 1.5x sobre linea base);
#   2. cuando se le desconecta el efecto, produce una RAFAGA de intentos antes de rendirse
#      (la firma de la extincion);
#   3. distingue desconexion GRADUAL de ABRUPTA.
# Este modulo construye el INSTRUMENTO que las mide. Su Regla 31 exige que las detecte en una
# politica contingente plantada Y QUE NO LAS VEA en el balbuceo ciego actual — porque el resultado
# honesto que esperamos de Diego hoy es justamente el segundo.
#
# Nada de esto le dice a Diego que debe moverse mas donde hay efecto. Mide si lo hace.

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
LIMITE = 2.5


def _suave(pasos, n, rng, suavizado=15, amplitud=2.2):
    u = np.array([rng.normal(0, 1, n) for _ in range(pasos)])
    k = np.ones(suavizado) / suavizado
    return np.column_stack([np.convolve(u[:, j], k, mode="same") for j in range(n)]) * amplitud


# =============================================================== PARTE A — EL GEMELO
def escena_gemelo(semilla=1, pasos=1200, render=False, gemelo=True):
    """Dos brazos IDENTICOS en la misma escena. El primero obedece los comandos de Diego; el
    segundo obedece ordenes ajenas (otra semilla). Devuelve:
        comandos_propios, comandos_ajenos, sentidos_propios, sentidos_ajenos, video
    `gemelo=False` monta la misma escena SIN el segundo brazo: es el control que dice cuanto del
    resultado se debe al gemelo y cuanto al montaje."""
    import pybullet as p
    cliente = p.connect(p.DIRECT)
    try:
        rng = np.random.default_rng(semilla)
        rng_aj = np.random.default_rng(semilla + 424243)
        p.resetSimulation(physicsClientId=cliente)
        p.setGravity(0, 0, -9.8, physicsClientId=cliente)
        p.setTimeStep(PASO_FISICO, physicsClientId=cliente)
        p.createMultiBody(0, p.createCollisionShape(p.GEOM_PLANE, physicsClientId=cliente),
                          physicsClientId=cliente)

        esl = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.16, 0.04, 0.04],
                                     physicsClientId=cliente)
        base_c = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.08, 0.08, 0.08],
                                        physicsClientId=cliente)
        esl_v = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.16, 0.04, 0.04],
                                    rgbaColor=[0.80, 0.80, 0.80, 1], physicsClientId=cliente)
        base_v = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.08, 0.08, 0.08],
                                     rgbaColor=[0.55, 0.55, 0.55, 1], physicsClientId=cliente)

        def brazo_en(y):
            b = p.createMultiBody(
                baseMass=0, baseCollisionShapeIndex=base_c, baseVisualShapeIndex=base_v,
                basePosition=[0, y, 0.6],
                linkMasses=[0.4] * N_ART, linkCollisionShapeIndices=[esl] * N_ART,
                linkVisualShapeIndices=[esl_v] * N_ART,
                linkPositions=[[0.22, 0, 0]] * N_ART,
                linkOrientations=[[0, 0, 0, 1]] * N_ART,
                linkInertialFramePositions=[[0, 0, 0]] * N_ART,
                linkInertialFrameOrientations=[[0, 0, 0, 1]] * N_ART,
                linkParentIndices=list(range(N_ART)),
                linkJointTypes=[p.JOINT_REVOLUTE] * N_ART,
                linkJointAxis=[[0, 0, 1], [0, 1, 0], [0, 0, 1]],
                physicsClientId=cliente)
            for j in range(N_ART):
                p.setJointMotorControl2(b, j, p.VELOCITY_CONTROL, force=0,
                                        physicsClientId=cliente)
                p.changeDynamics(b, j, jointLowerLimit=-LIMITE, jointUpperLimit=LIMITE,
                                 physicsClientId=cliente)
            return b

        # IDENTICOS en forma, masa y color: lo unico que los distingue es QUIEN LES MANDA.
        propio = brazo_en(-0.45)
        ajeno = brazo_en(0.45) if gemelo else None

        u_pro = _suave(pasos, N_ART, rng)
        u_aje = _suave(pasos, N_ART, rng_aj)
        if render:
            vm = p.computeViewMatrix([1.9, 0.0, 1.25], [0.30, 0.0, 0.55], [0, 0, 1])
            pm = p.computeProjectionMatrixFOV(60, 1.0, 0.1, 8.0)
        s_pro, s_aje, cuadros = [], [], []
        for t in range(pasos):
            for j in range(N_ART):
                p.setJointMotorControl2(propio, j, p.TORQUE_CONTROL,
                                        force=float(u_pro[t, j]), physicsClientId=cliente)
                if ajeno is not None:
                    p.setJointMotorControl2(ajeno, j, p.TORQUE_CONTROL,
                                            force=float(u_aje[t, j]), physicsClientId=cliente)
            for _ in range(SUBPASOS):
                p.stepSimulation(physicsClientId=cliente)
            s_pro.append([p.getJointState(propio, j, physicsClientId=cliente)[0]
                          for j in range(N_ART)]
                         + [p.getJointState(propio, j, physicsClientId=cliente)[1]
                            for j in range(N_ART)])
            if ajeno is not None:
                s_aje.append([p.getJointState(ajeno, j, physicsClientId=cliente)[0]
                              for j in range(N_ART)]
                             + [p.getJointState(ajeno, j, physicsClientId=cliente)[1]
                                for j in range(N_ART)])
            if render:
                w_, h_, rgb, _, _ = p.getCameraImage(64, 64, vm, pm,
                                                     renderer=p.ER_TINY_RENDERER,
                                                     physicsClientId=cliente)
                cuadros.append(np.reshape(rgb, (h_, w_, 4))[:, :, :3].mean(axis=2) / 255.0)
        video = np.stack(cuadros).astype(np.float32) if render else None
        return (u_pro, u_aje, np.array(s_pro, dtype=float),
                np.array(s_aje, dtype=float) if ajeno is not None else None, video)
    finally:
        p.disconnect(physicsClientId=cliente)


# UNA SOLA FUENTE para "cuanto ayuda conocer las ordenes" (auditoria del 9-ago-2026: habia tres
# copias parecidas en tres modulos, y una de ellas medía a un horizonte distinto).
from soporte import HORIZONTE, _ganancia_comando as _ganancia_canal


def _obediencia(Z, u, h=HORIZONTE):
    """Cuanto ayuda conocer ESAS ordenes a predecir esa senal a horizonte h, promediado sobre
    canales. Mismo instrumento del prereg-29: la obediencia se ve cuando el efecto se acumula."""
    Z = np.asarray(Z, dtype=float)
    if Z.ndim == 1:
        Z = Z[:, None]
    return float(np.mean([_ganancia_canal(Z[:, c], u, h=h) for c in range(Z.shape[1])]))


def prueba_gemelo(latentes_o_sentidos, u_propios, u_ajenos, semilla=30, nulos=6):
    """¿Se reconoce a SI o solo reconoce 'un brazo'? Se mide cuanto obedece la representacion a
    SUS ordenes y cuanto a las del gemelo, y se exige que la diferencia supere el nulo barajado.
    Un espejo de APARIENCIA da la misma cifra para ambos: no puede distinguirlos."""
    g_pro = _obediencia(latentes_o_sentidos, u_propios)
    g_aje = _obediencia(latentes_o_sentidos, u_ajenos)
    rng = np.random.default_rng(semilla)
    nulo = [abs(_obediencia(latentes_o_sentidos, u_propios[rng.permutation(len(u_propios))])
                - _obediencia(latentes_o_sentidos, u_ajenos[rng.permutation(len(u_ajenos))]))
            for _ in range(nulos)]
    techo = float(np.max(nulo))
    return {"obedece_a_mis_ordenes": round(g_pro, 4),
            "obedece_al_gemelo": round(g_aje, 4),
            "diferencia": round(g_pro - g_aje, 4), "nulo_techo": round(techo, 4),
            "se_reconoce": bool(g_pro - g_aje > techo and g_pro > g_aje)}


# =============================================================== PARTE B — FIRMAS DEL BEBE
FASES = ("linea_base", "contingencia", "extincion")


def paradigma_movil(semilla=1, pasos_fase=400, politica="ciega", desconexion="abrupta",
                    art_efecto=0, ganancia=0.6):
    """EL MOVIL DE ROVEE-COLLIER, en el Gimnasio. Tres fases seguidas:
       linea_base   — mover no produce ningun efecto
       contingencia — mover LA ARTICULACION `art_efecto` mueve el movil
       extincion    — el efecto se corta (abrupta) o se desvanece (gradual)
    politica: 'ciega' = el balbuceo actual de Diego (no usa la contingencia para nada)
              'contingente' = POLITICA PLANTADA (control positivo del instrumento, jamas un
              competidor real): sube la amplitud de la articulacion cuyo movimiento predijo el
              efecto. Es "un bebe que aprende", construido a proposito para probar el aparato.
              'agitada' = SEÑUELO (prereg-36): reparte el MISMO presupuesto finito de esfuerzo,
              pero AL AZAR, sin mirar el movil. Se mueve mas y de forma desigual sin que la
              contingencia tenga nada que ver. Si la vara la corona, esta midiendo actividad y no
              contingencia — es el analogo exacto del señuelo de ruido de la escalera de soporte.
    Devuelve actividad por articulacion y por fase, y la serie del movil."""
    import pybullet as p
    cliente = p.connect(p.DIRECT)
    try:
        rng = np.random.default_rng(semilla)
        p.resetSimulation(physicsClientId=cliente)
        p.setGravity(0, 0, -9.8, physicsClientId=cliente)
        p.setTimeStep(PASO_FISICO, physicsClientId=cliente)
        p.createMultiBody(0, p.createCollisionShape(p.GEOM_PLANE, physicsClientId=cliente),
                          physicsClientId=cliente)
        esl = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.16, 0.04, 0.04],
                                     physicsClientId=cliente)
        base_c = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.08, 0.08, 0.08],
                                        physicsClientId=cliente)
        brazo = p.createMultiBody(
            baseMass=0, baseCollisionShapeIndex=base_c, basePosition=[0, 0, 0.6],
            linkMasses=[0.4] * N_ART, linkCollisionShapeIndices=[esl] * N_ART,
            linkVisualShapeIndices=[-1] * N_ART,
            linkPositions=[[0.22, 0, 0]] * N_ART,
            linkOrientations=[[0, 0, 0, 1]] * N_ART,
            linkInertialFramePositions=[[0, 0, 0]] * N_ART,
            linkInertialFrameOrientations=[[0, 0, 0, 1]] * N_ART,
            linkParentIndices=list(range(N_ART)),
            linkJointTypes=[p.JOINT_REVOLUTE] * N_ART,
            linkJointAxis=[[0, 0, 1], [0, 1, 0], [0, 0, 1]],
            physicsClientId=cliente)
        for j in range(N_ART):
            p.setJointMotorControl2(brazo, j, p.VELOCITY_CONTROL, force=0,
                                    physicsClientId=cliente)
            p.changeDynamics(brazo, j, jointLowerLimit=-LIMITE, jointUpperLimit=LIMITE,
                             physicsClientId=cliente)

        total = pasos_fase * 3
        u = _suave(total, N_ART, rng)
        amplitud = np.ones(N_ART)
        hist_vel = [[] for _ in range(N_ART)]
        hist_movil = []
        actividad = {f: np.zeros(N_ART) for f in FASES}
        cuenta = {f: 0 for f in FASES}
        movil_serie = []
        for t in range(total):
            fase = FASES[min(2, t // pasos_fase)]
            for j in range(N_ART):
                p.setJointMotorControl2(brazo, j, p.TORQUE_CONTROL,
                                        force=float(u[t, j] * amplitud[j]),
                                        physicsClientId=cliente)
            for _ in range(SUBPASOS):
                p.stepSimulation(physicsClientId=cliente)
            vel = np.array([p.getJointState(brazo, j, physicsClientId=cliente)[1]
                            for j in range(N_ART)])
            # el movil: responde SOLO durante la contingencia, y segun el modo de desconexion
            if fase == "contingencia":
                acople = 1.0
            elif fase == "extincion":
                paso_ext = t - 2 * pasos_fase
                acople = 0.0 if desconexion == "abrupta" else max(
                    0.0, 1.0 - paso_ext / float(pasos_fase))
            else:
                acople = 0.0
            movil = acople * float(vel[art_efecto])
            movil_serie.append(movil)
            actividad[fase] += np.abs(vel)
            cuenta[fase] += 1
            for j in range(N_ART):
                hist_vel[j].append(float(vel[j]))
            hist_movil.append(movil)

            if politica == "agitada" and t > 60 and t % 20 == 0:
                # SEÑUELO (prereg-36): el MISMO presupuesto finito, repartido al azar. Se mueve mas
                # y de forma desigual, pero nada de eso viene del movil. Una vara que corone a esta
                # esta midiendo actividad, no contingencia.
                r = rng.random(N_ART)
                objetivo = np.clip(N_ART * r / r.sum(), 0.2, 4.0)
                amplitud = amplitud + ganancia * (objetivo - amplitud)

            if politica == "contingente" and t > 60 and t % 20 == 0:
                # POLITICA PLANTADA (control positivo del instrumento, jamas un competidor real):
                # reparte un PRESUPUESTO FINITO de esfuerzo entre las articulaciones, en proporcion
                # a cuanto correlaciona el movimiento reciente de cada una con el movil.
                # POR QUE EL PRESUPUESTO ES FINITO, y no cada una por su cuenta: el brazo es una
                # cadena, asi que mover la articulacion 0 sacude tambien a la 1 y a la 2. Con
                # refuerzo independiente TODAS suben (medido: 2.64x la buena, 2.26x las otras) y
                # la firma pierde su especificidad — que es justamente lo que la literatura
                # infantil mide. Un bebe tampoco tiene energia infinita: subir un brazo es bajar
                # el otro. Cazado por esta misma Regla 31 el 9-ago-2026.
                v = np.array(hist_movil[-60:])
                if np.std(v) > 1e-9:
                    cs = []
                    for j in range(N_ART):
                        w = np.array(hist_vel[j][-60:])
                        cs.append(0.0 if np.std(w) < 1e-9
                                  else abs(float(np.corrcoef(w, v)[0, 1])))
                    cs = np.array(cs)
                    if cs.sum() > 1e-9:
                        objetivo = np.clip(N_ART * cs / cs.sum(), 0.2, 4.0)
                        amplitud = amplitud + ganancia * (objetivo - amplitud)
                else:
                    # sin efecto que perseguir, la amplitud vuelve hacia su linea base
                    amplitud = 1.0 + (amplitud - 1.0) * 0.9
        for f in FASES:
            if cuenta[f]:
                actividad[f] /= cuenta[f]
        return {"actividad": {f: actividad[f].tolist() for f in FASES},
                "movil": movil_serie, "art_efecto": art_efecto,
                "politica": politica, "desconexion": desconexion}
    finally:
        p.disconnect(physicsClientId=cliente)


def firmas(res):
    """Las tres firmas conductuales, con el criterio clasico de la literatura infantil."""
    a = {f: np.array(res["actividad"][f]) for f in FASES}
    j = res["art_efecto"]
    base = a["linea_base"][j]
    razon = float(a["contingencia"][j] / base) if base > 1e-9 else 0.0
    # la rafaga: la extincion debe superar a la contingencia (protesta antes de rendirse)
    rafaga = float(a["extincion"][j] / a["contingencia"][j]) if a["contingencia"][j] > 1e-9 else 0.0
    # especificidad: ¿sube SOLO la articulacion que produce el efecto, o sube todo el cuerpo?
    otras = [k for k in range(len(base if hasattr(base, "__len__") else a["linea_base"]))
             if k != j]
    r_otras = float(np.mean([a["contingencia"][k] / a["linea_base"][k]
                             for k in otras if a["linea_base"][k] > 1e-9])) if otras else 0.0
    return {"razon_contingencia_sobre_base": round(razon, 4),
            "criterio_clasico_1.5x": bool(razon >= 1.5),
            "rafaga_de_extincion": round(rafaga, 4),
            "hay_rafaga": bool(rafaga > 1.0),
            "razon_otras_articulaciones": round(r_otras, 4),
            "especifica": bool(razon > r_otras * 1.2)}


# ======================================================= EL CALIBRADOR (prereg-36)
# POR QUE EXISTE. El INFORME-40 cerro las firmas conductuales como NO CONCLUYENTE POR INSTRUMENTO:
# la politica contingente PLANTADA —construida a proposito para tener la firma— solo disparo el
# criterio clasico en 2 de 5 semillas, y en la semilla 3 se movio MENOS que su propia linea base.
# "Diego no exhibe las firmas" puede ser cierto, pero un instrumento que falla sobre un caso
# conocido no puede certificar una ausencia.
#
# EL ERROR DE DISEÑO QUE LO PERMITIO, dicho con su nombre: el caso B1 del banco probaba el control
# positivo con UNA semilla (la 2, que resulto ser de las que funcionan). Un control positivo de una
# sola muestra no es un control positivo: es una anecdota que aprueba.
#
# ESTE MODULO NO MIDE A DIEGO. Mide la VARA. Solo cuando la vara pase su propio examen tiene
# sentido volver a preguntarle nada a Diego.
DURACIONES = (400, 800, 1600, 3200)
SEMILLAS_CALIBRACION = (1, 2, 3, 4, 5)


def _veredicto_calibracion(filas):
    """Funcion PURA sobre las filas del barrido: decide si la vara sirve y con que duracion.
    Se separa a proposito del calculo caro para poder congelarla en el banco sin simular nada —
    es la logica que fallo en el prereg-30, y la logica es lo que hay que blindar."""
    usables = [f for f in filas
               if f["tasa_control_positivo"] >= 1.0
               and f["tasa_ciega"] <= 0.0
               and f["tasa_agitada_especifica"] <= 0.0]
    if not usables:
        return {"vara_usable": False, "pasos_fase_recomendado": None,
                "lectura": "NINGUNA duracion probada hace fiable la vara. Las firmas conductuales "
                           "siguen sin poder medirse, y eso se escribe como resultado — no se "
                           "vuelve a preguntar a Diego con un instrumento que no pasa su examen."}
    mejor = min(usables, key=lambda f: f["pasos_fase"])
    return {"vara_usable": True, "pasos_fase_recomendado": mejor["pasos_fase"],
            "lectura": f"con {mejor['pasos_fase']} pasos por fase el control positivo dispara 5/5, "
                       f"el balbuceo ciego 0/5 y el señuelo agitado no resulta especifico. "
                       f"Recien ahi se puede volver a preguntar por Diego."}


def calibrar(duraciones=DURACIONES, semillas=SEMILLAS_CALIBRACION, verbose=False):
    """Barre la duracion de fase y mide, para cada una, si el instrumento sirve.
    Tres politicas por celda: contingente (debe disparar SIEMPRE), ciega (NUNCA) y agitada
    (se mueve mas sin contingencia: nunca puede resultar especifica)."""
    filas = []
    for d in duraciones:
        cont, cieg, agit = [], [], []
        for s in semillas:
            cont.append(firmas(paradigma_movil(semilla=2000 + s, pasos_fase=d,
                                               politica="contingente")))
            cieg.append(firmas(paradigma_movil(semilla=2000 + s, pasos_fase=d, politica="ciega")))
            agit.append(firmas(paradigma_movil(semilla=2000 + s, pasos_fase=d,
                                               politica="agitada")))
        rz = [f["razon_contingencia_sobre_base"] for f in cieg]
        fila = {
            "pasos_fase": d,
            "tasa_control_positivo": round(np.mean([f["criterio_clasico_1.5x"] for f in cont]), 3),
            "tasa_ciega": round(np.mean([f["criterio_clasico_1.5x"] for f in cieg]), 3),
            "tasa_agitada": round(np.mean([f["criterio_clasico_1.5x"] for f in agit]), 3),
            "tasa_agitada_especifica": round(
                np.mean([f["criterio_clasico_1.5x"] and f["especifica"] for f in agit]), 3),
            # LA CIFRA QUE DIAGNOSTICA: si la dispersion de la linea base es del orden del efecto
            # que buscamos (0.5 sobre 1.0), la vara no puede ver ese efecto por mucho que insistamos.
            "dispersion_ciega": round(float(np.std(rz)), 4),
            "razon_media_contingente": round(
                float(np.mean([f["razon_contingencia_sobre_base"] for f in cont])), 4),
            "razon_media_ciega": round(float(np.mean(rz)), 4),
            "razones_contingente": [f["razon_contingencia_sobre_base"] for f in cont],
        }
        fila["separacion_en_sigmas"] = round(
            float((fila["razon_media_contingente"] - fila["razon_media_ciega"])
                  / fila["dispersion_ciega"]), 3) if fila["dispersion_ciega"] > 1e-9 else None
        filas.append(fila)
        if verbose:
            print(f"  fase={d:5d}  positivo {fila['tasa_control_positivo']:.1f}  "
                  f"ciega {fila['tasa_ciega']:.1f}  agitada-especifica "
                  f"{fila['tasa_agitada_especifica']:.1f}  dispersion {fila['dispersion_ciega']}")
    return {"filas": filas, "veredicto": _veredicto_calibracion(filas)}


# =============================================================== Regla 31
def regla31(verbose=True, pasos=1200, pasos_fase=400):
    fallos = []

    # --- A1: la propiocepcion PROPIA se reconoce a si misma, no al gemelo
    u_pro, u_aje, s_pro, s_aje, _ = escena_gemelo(semilla=1, pasos=pasos)
    r_yo = prueba_gemelo(s_pro, u_pro, u_aje)
    c1 = r_yo["se_reconoce"]
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} MI CUERPO: obedece a mis ordenes "
              f"{r_yo['obedece_a_mis_ordenes']} vs al gemelo {r_yo['obedece_al_gemelo']} "
              f"(nulo {r_yo['nulo_techo']})")
    if not c1:
        fallos.append("mi-cuerpo")

    # --- A2: EL CUERPO DEL GEMELO no puede ser declarado mio (la trampa, al reves)
    r_otro = prueba_gemelo(s_aje, u_pro, u_aje)
    c2 = not r_otro["se_reconoce"]
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} EL GEMELO NO SOY YO: su cuerpo obedece a mis "
              f"ordenes {r_otro['obedece_a_mis_ordenes']} vs a las suyas "
              f"{r_otro['obedece_al_gemelo']} — no se declara mio")
    if not c2:
        fallos.append("gemelo-ajeno")

    # --- A3: una representacion de APARIENCIA (la media de ambos cuerpos, como veria una vista
    #     que no distingue quien es quien) NO puede reconocerse: es el modo de fallo que buscamos
    mezcla = (s_pro + s_aje) / 2.0
    r_mez = prueba_gemelo(mezcla, u_pro, u_aje)
    c3 = r_mez["diferencia"] < r_yo["diferencia"]
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} APARIENCIA MEZCLADA: se distingue menos "
              f"({r_mez['diferencia']}) que el cuerpo propio ({r_yo['diferencia']})")
    if not c3:
        fallos.append("apariencia")

    # --- B1: la politica CONTINGENTE plantada exhibe las tres firmas
    rc = paradigma_movil(semilla=2, pasos_fase=pasos_fase, politica="contingente")
    fc = firmas(rc)
    c4 = fc["criterio_clasico_1.5x"] and fc["especifica"]
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} POLITICA CONTINGENTE (control positivo): "
              f"{fc['razon_contingencia_sobre_base']}x sobre linea base "
              f"(otras {fc['razon_otras_articulaciones']}x), especifica={fc['especifica']}")
    if not c4:
        fallos.append("firmas-positivo")

    # --- B2: el BALBUCEO CIEGO (lo que Diego hace HOY) no puede exhibirlas. Si el instrumento
    #     las ve donde no las hay, mide su propio ruido.
    rb = paradigma_movil(semilla=2, pasos_fase=pasos_fase, politica="ciega")
    fb = firmas(rb)
    c5 = not fb["criterio_clasico_1.5x"]
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} BALBUCEO CIEGO (control negativo): "
              f"{fb['razon_contingencia_sobre_base']}x — NO alcanza el 1.5x, como debe ser")
    if not c5:
        fallos.append("firmas-negativo")

    # --- B3: la desconexion GRADUAL y la ABRUPTA no pueden dar la misma conducta
    rg = paradigma_movil(semilla=2, pasos_fase=pasos_fase, politica="contingente",
                         desconexion="gradual")
    fg = firmas(rg)
    c6 = abs(fg["rafaga_de_extincion"] - fc["rafaga_de_extincion"]) > 1e-6
    if verbose:
        print(f"  {'ok  ' if c6 else 'FALLO'} GRADUAL vs ABRUPTA: rafagas distintas "
              f"({fg['rafaga_de_extincion']} vs {fc['rafaga_de_extincion']})")
    if not c6:
        fallos.append("gradual-abrupta")

    # ------------------------------------------------ prereg-36: la vara pasa su propio examen
    # C1) LA LOGICA QUE FALLO, BLINDADA. Es el caso mas importante de este modulo y no simula nada:
    #     con el control positivo disparando 2 de 5 —exactamente lo que ocurrio en la corrida
    #     oficial del prereg-30— el veredicto TIENE que ser "vara NO usable". Si esta funcion
    #     dijera que si, volveriamos a firmar una ausencia con un instrumento roto.
    _falso = [{"pasos_fase": 500, "tasa_control_positivo": 0.4, "tasa_ciega": 0.0,
               "tasa_agitada_especifica": 0.0}]
    _bueno = [{"pasos_fase": 500, "tasa_control_positivo": 0.4, "tasa_ciega": 0.0,
               "tasa_agitada_especifica": 0.0},
              {"pasos_fase": 900, "tasa_control_positivo": 1.0, "tasa_ciega": 0.0,
               "tasa_agitada_especifica": 0.0}]
    v_falso, v_bueno = _veredicto_calibracion(_falso), _veredicto_calibracion(_bueno)
    c7 = (not v_falso["vara_usable"]) and v_bueno["vara_usable"] \
        and v_bueno["pasos_fase_recomendado"] == 900
    if verbose:
        print(f"  {'ok  ' if c7 else 'FALLO'} VEREDICTO DE CALIBRACION: con el positivo en 2/5 la "
              f"vara se declara NO usable ({v_falso['vara_usable']}); con 5/5 recomienda 900 "
              f"({v_bueno['pasos_fase_recomendado']})")
    if not c7:
        fallos.append("veredicto-calibracion")

    # C2) UN CONTROL POSITIVO DE UNA SOLA SEMILLA NO ES UN CONTROL POSITIVO. El caso B1 de arriba
    #     usaba la semilla 2 —que resulto ser de las que funcionan— y por eso el banco aprobo un
    #     instrumento que en la nube fallo 3 de 5 veces. Aqui se exige la tasa sobre VARIAS
    #     semillas, y se registra cual es de verdad. No se exige que sea 1.0: se exige MEDIRLA,
    #     porque el prereg-36 existe precisamente para averiguar a que duracion lo es.
    tasa = np.mean([firmas(paradigma_movil(semilla=2000 + s, pasos_fase=300,
                                           politica="contingente"))["criterio_clasico_1.5x"]
                    for s in (1, 2, 3)])
    c8 = 0.0 <= tasa <= 1.0
    if verbose:
        print(f"  {'ok  ' if c8 else 'FALLO'} CONTROL POSITIVO MULTI-SEMILLA: a 300 pasos/fase el "
              f"positivo dispara {tasa:.2f} de las veces (una sola semilla habria dicho "
              f"'funciona' o 'no funciona', y las dos serian mentira)")
    if not c8:
        fallos.append("positivo-multisemilla")

    # C3) EL SEÑUELO AGITADO: moverse mas, y de forma desigual, SIN contingencia. No puede resultar
    #     especifico — si lo fuera, la vara estaria midiendo actividad y no contingencia. Es el
    #     analogo exacto del señuelo de ruido que salvo a la escalera de soporte.
    ag = firmas(paradigma_movil(semilla=2002, pasos_fase=300, politica="agitada"))
    c9 = not (ag["criterio_clasico_1.5x"] and ag["especifica"])
    if verbose:
        print(f"  {'ok  ' if c9 else 'FALLO'} SEÑUELO AGITADO: se mueve sin contingencia "
              f"({ag['razon_contingencia_sobre_base']}x, especifica={ag['especifica']}) y NO es "
              f"coronado")
    if not c9:
        fallos.append("senuelo-agitado")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — distingue al gemelo y mide las firmas donde las hay."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="El gemelo y las firmas del bebe (prereg-30)")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--semilla", type=int, default=None)
    ap.add_argument("--pasos", type=int, default=1500)
    ap.add_argument("--pasos-fase", type=int, default=500)
    ap.add_argument("--calibrar", action="store_true",
                    help="prereg-36: mide LA VARA, no a Diego. Barre la duracion de fase hasta que "
                         "el control positivo plantado dispare 5/5 y el ciego 0/5.")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    if a.calibrar:
        res = calibrar(verbose=True)
        salida = {"prerregistro": 36, "semillas": list(SEMILLAS_CALIBRACION), **res}
        out = os.path.join(BASE, "resultados", "p36-calibracion-firmas")
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
            json.dump(salida, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n{res['veredicto']['lectura']}\nguardado en {out}/resumen.json")
        return
    if a.semilla is None:
        print("uso: --regla31 | --semilla N | --calibrar")
        return
    s = a.semilla
    u_pro, u_aje, s_pro, s_aje, _ = escena_gemelo(semilla=1000 + s, pasos=a.pasos)
    salida = {"prerregistro": 30, "semilla": s, "pasos": a.pasos,
              "gemelo_propio": prueba_gemelo(s_pro, u_pro, u_aje),
              "gemelo_ajeno": prueba_gemelo(s_aje, u_pro, u_aje),
              "firmas_diego_hoy": firmas(paradigma_movil(semilla=2000 + s,
                                                         pasos_fase=a.pasos_fase,
                                                         politica="ciega")),
              "firmas_control_positivo": firmas(paradigma_movil(semilla=2000 + s,
                                                                pasos_fase=a.pasos_fase,
                                                                politica="contingente"))}
    out = os.path.join(BASE, "resultados", f"p30-espejo-gemelo-s{s}")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False, default=str)
    print(f"guardado en {out}/resumen.json (parcial — el veredicto exige las 5 semillas juntas)")


if __name__ == "__main__":
    main()
