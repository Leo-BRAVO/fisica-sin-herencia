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
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    if a.semilla is None:
        print("uso: --regla31 | --semilla N")
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
