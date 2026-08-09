# soporte.py — LA ESCALERA DE SOPORTE: el primer no-yo por definicion POSITIVA (prereg-29).
#
# POR QUE EXISTE (diagnostico, no capricho): el nivel B del hito 0 fracaso limpio 0/5
# (INFORME-36). Buscabamos la gravedad como "lo que NO obedece mis ordenes" — una definicion por
# AUSENCIA, la mas debil que existe: el ruido tampoco obedece. La evidencia infantil (linea
# Baillargeon, revision 2024) dice que los bebes no detectan "la gravedad" como fuerza abstracta:
# aprenden una escalera de expectativas de SOPORTE — que pasa cuando sueltas algo, escalon por
# escalon, y siempre ligada al CONTACTO. Por eso este modulo fusiona el nivel B con el hito de
# causalidad por contacto: en los bebes son el mismo sistema, y nosotros los teniamos separados.
#
# LOS TRES ESCALONES
#   1. "lo que suelto, cae, siempre igual" — la firma NO es 'no me obedece' sino REGULARIDAD
#      POSITIVA: la caida debe ser la parte MAS predecible del mundo desde su propio pasado, y a
#      la vez la que MENOS gana al conocer mis comandos. Positivo y negativo a la vez, no solo
#      negativo. (La pista del reescalado del INFORME-32 vive aqui: la caida es la senal cuya
#      predictibilidad propia es maxima.)
#   2. "no cae si algo lo sostiene" — la ley emergente contacto+caida=soporte. Se mide como
#      CAMBIO de la dinamica vertical condicionado al contacto, con su nulo por contacto barajado.
#   3. EL EXAMEN — sorpresa ante lo imposible. Se aprende un predictor SOLO con escenas posibles
#      y se le muestran pares gemelos posible/imposible (un objeto que flota sin soporte, uno que
#      atraviesa la mesa). Si se sorprende mas ante la imposible, sabe fisica de soporte.
#      NULO NATURAL DE FABRICA: dos escenas POSIBLES comparadas entre si deben dar sorpresa cero.
#
# NADA DE ESTO le dice a Diego que existe la gravedad, ni que hay objetos, ni que el contacto
# sostiene. Le construye el mundo donde eso pasa y le pregunta si lo noto. La escalera de los
# bebes nos dice QUE MEDIR; jamas que responder.
#
# Regla 31: (a) en el mundo normal los tres escalones deben encontrar lo que hay; (b) en el mundo
# SIN GRAVEDAD el escalon 1 debe FRACASAR (no hay caida que hallar); (c) el examen debe dar
# sorpresa ~0 entre dos posibles; (d) con la senal de contacto barajada el escalon 2 debe callar.

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
ALTURA_MESA = 0.55

CASOS = {
    "cae":        "el objeto se suelta en el aire sobre el suelo — cae (POSIBLE)",
    "apoyado":    "el objeto descansa sobre una mesa — no cae (POSIBLE)",
    "flota":      "el objeto se queda quieto en el aire, sin nada debajo (IMPOSIBLE)",
    "atraviesa":  "el objeto cae pero pasa a traves de la mesa solida (IMPOSIBLE)",
}
POSIBLES = ("cae", "apoyado")
IMPOSIBLES = ("flota", "atraviesa")


def _balbuceo(pasos, n, rng, suavizado=40):
    u = np.array([rng.normal(0, 1, n) for _ in range(pasos)])
    k = np.ones(suavizado) / suavizado
    return np.column_stack([np.convolve(u[:, j], k, mode="same") for j in range(n)]) * 2.5


def escena(caso, semilla=1, pasos=900, sin_gravedad=False, ciclo=60):
    """Devuelve (comandos, canales, nombres, cortes). canales por paso:
       [3 angulos del brazo] + [altura] + [contacto] + [velocidad vertical] + [ruido senuelo]
    El brazo balbucea SIEMPRE: es lo que permite preguntar si la caida obedece o no a sus ordenes.

    EL OBJETO SE RE-SUELTA CADA `ciclo` PASOS. Sin esto, una sola caida dura ~15 pasos de 900 y
    el regimen "sin contacto" queda con tan pocas muestras que el escalon 2 no puede medirse
    (cazado por su propia Regla 31 el 9-ago-2026). Ademas es lo que hace un bebe: soltar la
    cuchara una y otra vez. Cada ciclo es una repeticion del mismo experimento.
    """
    import pybullet as p
    cliente = p.connect(p.DIRECT)
    try:
        rng = np.random.default_rng(semilla)
        p.resetSimulation(physicsClientId=cliente)
        p.setGravity(0, 0, 0.0 if sin_gravedad else -9.8, physicsClientId=cliente)
        p.setTimeStep(PASO_FISICO, physicsClientId=cliente)
        suelo = p.createMultiBody(0, p.createCollisionShape(p.GEOM_PLANE,
                                                            physicsClientId=cliente),
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

        # la mesa existe en los casos donde hace falta algo que sostenga (o que se atraviese)
        mesa = None
        if caso in ("apoyado", "atraviesa"):
            mesa_c = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.30, 0.30, 0.02],
                                            physicsClientId=cliente)
            mesa = p.createMultiBody(0, mesa_c, basePosition=[1.0, 0, ALTURA_MESA],
                                     physicsClientId=cliente)

        alt0 = ALTURA_MESA + 0.09 if caso == "apoyado" else 1.30
        masa = 0.0 if caso == "flota" else 0.25      # masa 0 = cinematico: se queda quieto
        obj_c = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.07, 0.07, 0.07],
                                       physicsClientId=cliente)
        objeto = p.createMultiBody(masa, obj_c, basePosition=[1.0, 0, alt0],
                                   physicsClientId=cliente)
        if caso == "atraviesa" and mesa is not None:
            # LA IMPOSIBILIDAD: se apaga la colision SOLO entre objeto y mesa. Todo lo demas
            # sigue siendo el mismo mundo — un par gemelo del caso 'apoyado'.
            p.setCollisionFilterPair(objeto, mesa, -1, -1, 0, physicsClientId=cliente)

        comandos = _balbuceo(pasos, N_ART, rng)
        rng_ruido = np.random.default_rng(semilla + 500003)
        filas, cortes = [], []
        for t in range(pasos):
            for j in range(N_ART):
                w = p.getJointState(brazo, j, physicsClientId=cliente)[1]
                p.setJointMotorControl2(brazo, j, p.TORQUE_CONTROL,
                                        force=float(comandos[t, j]) - 0.05 * w,
                                        physicsClientId=cliente)
            for _ in range(SUBPASOS):
                p.stepSimulation(physicsClientId=cliente)
            ang = [p.getJointState(brazo, j, physicsClientId=cliente)[0] for j in range(N_ART)]
            (x, y, z), _ = p.getBasePositionAndOrientation(objeto, physicsClientId=cliente)
            vz = p.getBaseVelocity(objeto, physicsClientId=cliente)[0][2]
            toca = 1.0 if p.getContactPoints(bodyA=objeto, physicsClientId=cliente) else 0.0
            # SEÑUELO DECLARADO: un canal de ruido puro que TAMPOCO obedece a sus comandos. Existe
            # para que el escalon 1 no pueda aprobar por la via facil: si el criterio fuera solo
            # "no me obedece", este ruido seria el primer no-yo del proyecto. Debe ser rechazado.
            filas.append(ang + [z, toca, vz, float(rng_ruido.normal())])
            if ciclo and t % ciclo == ciclo - 1 and masa > 0:
                p.resetBasePositionAndOrientation(objeto, [1.0, 0, alt0], [0, 0, 0, 1],
                                                  physicsClientId=cliente)
                p.resetBaseVelocity(objeto, [0, 0, 0], [0, 0, 0], physicsClientId=cliente)
                cortes.append(t + 1)
        nombres = ["art0", "art1", "art2", "altura", "contacto", "vel_z", "ruido"]
        # CORTES: los pasos donde NOSOTROS reponemos el objeto arriba. Es tramoya del simulador,
        # no fisica del mundo: ninguna ley puede predecir un teletransporte que hacemos nosotros.
        # Las ventanas que los cruzan se excluyen de toda medicion (si no, la caida —que dentro
        # de cada suelta es perfectamente predecible— parece caotica y el escalon 1 corona al
        # brazo. Cazado por esta misma Regla 31 el 9-ago-2026).
        return comandos, np.array(filas, dtype=float), nombres, np.array(cortes, dtype=int)
    finally:
        p.disconnect(physicsClientId=cliente)


# ------------------------------------------------------------------ escalon 1
# HORIZONTE: por que no se mide a un solo paso.
# LECCION CAZADA POR ESTA REGLA 31 (9-ago-2026): a un paso, la articulacion del brazo salia MAS
# "no-yo" que la caida. Motivo real: con comandos suaves, tres retardos del angulo extrapolan la
# trayectoria casi perfecta, y lo que el torque agrega en UN paso es del orden de a*dt^2 —
# invisible. La obediencia no se ve en el instante siguiente: se ve cuando el efecto se acumula.
# Se mide entonces a horizonte h: "¿saber lo que ordene me ayuda a saber donde estara esto dentro
# de un rato?". Es tambien la pregunta honesta: nadie siente que manda su brazo por un paso de
# simulacion.
HORIZONTE = 8


def _validos(n_total, retardos, h, cortes):
    """Indices de ventana que NO cruzan un corte (un reposicionamiento hecho por nosotros)."""
    n = n_total - retardos - h + 1
    if n <= 0:
        return np.array([], dtype=int)
    ok = np.ones(n, dtype=bool)
    for c in (cortes if cortes is not None else []):
        ini = max(0, c - retardos - h + 1)
        ok[ini:min(n, c + 1)] = False
    return np.nonzero(ok)[0]


def _matriz_pasado(x, retardos, h, cortes=None):
    n = len(x) - retardos - h + 1
    if n < 20:
        return None, None
    idx = _validos(len(x), retardos, h, cortes)
    if len(idx) < 20:
        return None, None
    A = np.column_stack([x[retardos - k - 1:retardos - k - 1 + n] for k in range(retardos)]
                        + [np.ones(n)])[idx]
    b = x[retardos + h - 1: retardos + h - 1 + n][idx]
    return A, b


def _r2_autopredictivo(x, retardos=3, h=HORIZONTE, cortes=None):
    """Cuanto se predice una senal a horizonte h desde SU PROPIO pasado (nada mas)."""
    x = np.asarray(x, dtype=float)
    if np.var(x) < 1e-12:
        return 0.0
    A, b = _matriz_pasado(x, retardos, h, cortes)
    if A is None or np.var(b) < 1e-12:
        return 0.0
    r = b - A @ np.linalg.lstsq(A, b, rcond=None)[0]
    return float(max(0.0, 1.0 - np.var(r) / np.var(b)))


def _ganancia_comando(x, u, retardos=3, h=HORIZONTE, cortes=None):
    """Cuanto MEJORA esa prediccion al anadir lo que ORDENE durante el horizonte. Es la
    contingencia en continuo, medida donde el torque alcanza a producir efecto."""
    x = np.asarray(x, dtype=float)
    u = np.asarray(u, dtype=float)
    if np.var(x) < 1e-12:
        return 0.0
    A, b = _matriz_pasado(x, retardos, h, cortes)
    if A is None or np.var(b) < 1e-12:
        return 0.0
    idx = _validos(len(x), retardos, h, cortes)
    # media de cada comando a lo largo de la ventana [t, t+h): el empujon acumulado
    U = np.array([u[retardos - 1 + i: retardos - 1 + i + h].mean(axis=0) for i in idx])
    Au = np.column_stack([A, U])
    e0 = np.var(b - A @ np.linalg.lstsq(A, b, rcond=None)[0])
    e1 = np.var(b - Au @ np.linalg.lstsq(Au, b, rcond=None)[0])
    return float(max(0.0, 1.0 - e1 / max(e0, 1e-12)))


PISO_LEGALIDAD = 0.30      # por debajo de esto un canal no tiene ley: es ruido
TECHO_OBEDIENCIA = 0.05    # por encima de esto el canal es (al menos en parte) suyo


def escalon1(comandos, canales, nombres, cortes=None, semilla=29, nulos=6):
    """"Lo que suelto, cae, SIEMPRE IGUAL". El primer no-yo necesita DOS condiciones, no una:
      (A) LEGALIDAD — el canal debe ser predecible desde su propio pasado por encima de un piso.
          Es la parte POSITIVA, y es la que faltaba en el nivel B fracasado: sin ella, el ruido
          puro (que tampoco obedece) seria el primer no-yo del proyecto.
      (B) NO-MIO — conocer mis comandos no debe ayudar a predecirlo, por encima de su nulo.
    Entre los canales que cumplen ambas, gana el MENOS obediente; a igual obediencia, el mas
    legal. La maximizacion pura de autopredictibilidad estaba mal y su propia Regla 31 lo cazo:
    coronaba al brazo, que por ser suave es trivialmente autopredecible."""
    rng = np.random.default_rng(semilla)
    filas = []
    for i, n in enumerate(nombres):
        x = canales[:, i]
        auto = _r2_autopredictivo(x, cortes=cortes)
        g = _ganancia_comando(x, comandos, cortes=cortes)
        g_nulo = float(np.mean([_ganancia_comando(x, comandos[rng.permutation(len(comandos))],
                                                  cortes=cortes)
                                for _ in range(nulos)]))
        g_neta = max(0.0, g - g_nulo)
        filas.append({"canal": n, "autopredictible": round(auto, 4),
                      "gana_con_mi_comando": round(g, 4), "nulo": round(g_nulo, 4),
                      "obediencia_neta": round(g_neta, 4),
                      "legal": bool(auto >= PISO_LEGALIDAD),
                      "no_mio": bool(g_neta <= TECHO_OBEDIENCIA)})
    aptos = [f for f in filas if f["legal"] and f["no_mio"]]
    if not aptos:
        return {"detalle": filas, "candidato": None, "hallado": False,
                "motivo": "ningun canal es a la vez legal y no-mio"}
    mejor = min(aptos, key=lambda f: (f["obediencia_neta"], -f["autopredictible"]))
    return {"detalle": filas, "candidato": mejor["canal"],
            "autopredictible": mejor["autopredictible"],
            "obediencia_neta": mejor["obediencia_neta"],
            "candidatos_aptos": [f["canal"] for f in aptos], "hallado": True}


# ------------------------------------------------------------------ escalon 2
def escalon2(canales, nombres, semilla=29, nulos=8):
    """"No cae si algo lo sostiene": la dinamica vertical debe CAMBIAR segun el contacto.
    Se mide como diferencia de |velocidad vertical| entre pasos con y sin contacto, contra el
    nulo de barajar la senal de contacto (que destruye exactamente la ligadura afirmada)."""
    ic, iv = nombres.index("contacto"), nombres.index("vel_z")
    c, v = canales[:, ic], np.abs(canales[:, iv])
    if c.sum() < 20 or (len(c) - c.sum()) < 20:
        return {"hallado": False, "motivo": "sin ambos regimenes (contacto y no contacto)"}
    real = float(np.mean(v[c == 0]) - np.mean(v[c == 1]))
    rng = np.random.default_rng(semilla)
    nulo = [float(np.mean(v[cs == 0]) - np.mean(v[cs == 1]))
            for cs in (c[rng.permutation(len(c))] for _ in range(nulos))]
    techo = float(np.max(nulo))
    return {"efecto": round(real, 4), "nulo_techo": round(techo, 4),
            "hallado": bool(real > techo and real > 0.05),
            "lectura": "con contacto la caida se detiene" if real > techo else "sin ligadura"}


# ------------------------------------------------------------------ escalon 3: el examen VOE
def _predictor(datos, retardos=3):
    """Modelo lineal del mundo aprendido SOLO con escenas posibles: predice el proximo vector
    de canales desde los `retardos` anteriores. Devuelve (W, retardos)."""
    A, B = [], []
    for canales in datos:
        X = canales
        for t in range(retardos, len(X)):
            A.append(np.concatenate([X[t - k - 1] for k in range(retardos)] + [[1.0]]))
            B.append(X[t])
    A, B = np.array(A), np.array(B)
    W, *_ = np.linalg.lstsq(A, B, rcond=None)
    return W, retardos


def _escala_error(modelo, entrenamiento):
    """El PISO DE RUIDO del propio modelo: cuanto se equivoca sobre lo que ya vio. Por debajo de
    esto ninguna diferencia es sorpresa — es aritmetica de punto flotante."""
    return float(np.mean([_sorpresa(modelo, c) for c in entrenamiento]))


def _sorpresa(modelo, canales):
    W, retardos = modelo
    A, B = [], []
    X = canales
    for t in range(retardos, len(X)):
        A.append(np.concatenate([X[t - k - 1] for k in range(retardos)] + [[1.0]]))
        B.append(X[t])
    A, B = np.array(A), np.array(B)
    return float(np.mean((B - A @ W) ** 2))


def examen_voe(entrenamiento, par_a, par_b):
    """Sorpresa relativa entre dos escenas gemelas. >0 significa que 'par_b' sorprende mas.
    El nulo natural: si las dos son POSIBLES, debe dar ~0."""
    modelo = _predictor(entrenamiento)
    sa, sb = _sorpresa(modelo, par_a), _sorpresa(modelo, par_b)
    piso = _escala_error(modelo, entrenamiento)
    # GUARDA DE PISO (leccion cazada por esta Regla 31 el 9-ago-2026): dos escenas casi estaticas
    # dan errores de 1e-9 y 1e-10, y su cociente relativo se dispara a -0.80 sin que nada haya
    # sorprendido a nadie. Si AMBOS errores viven por debajo del propio piso de ruido del modelo,
    # la sorpresa es cero por construccion, no por medicion.
    if max(sa, sb) < 0.01 * max(piso, 1e-12):
        return {"sorpresa_relativa": 0.0, "a": round(sa, 9), "b": round(sb, 9),
                "piso_ruido": round(piso, 9), "bajo_piso": True}
    if sa + sb <= 0:
        return {"sorpresa_relativa": 0.0, "a": sa, "b": sb, "piso_ruido": round(piso, 9)}
    return {"sorpresa_relativa": round((sb - sa) / (sa + sb), 4), "a": round(sa, 6),
            "b": round(sb, 6), "piso_ruido": round(piso, 9), "bajo_piso": False}


# ------------------------------------------------------------------ Regla 31
PASOS_MINIMOS = 900   # 15 sueltas: por debajo, el nulo natural no separa (medido 9-ago-2026)


def regla31(verbose=True, pasos=900):
    # GUARDA DE POTENCIA, igual que el minimo de 20 ventanas del detector de contingencia: con
    # 600 pasos (10 sueltas) el nulo natural REPRUEBA por falta de muestras, no porque el mundo
    # sorprenda. Un instrumento que entrega veredicto sin potencia es un instrumento que miente.
    if pasos < PASOS_MINIMOS:
        raise SystemExit(f"MEDICION INVALIDA: {pasos} pasos (minimo {PASOS_MINIMOS}). Con menos "
                         f"sueltas el nulo natural no separa y el examen fabrica sorpresa donde "
                         f"no la hay — medido el 9-ago-2026.")
    fallos = []
    c_cae, x_cae, nom, k_cae = escena("cae", semilla=1, pasos=pasos)
    c_apo, x_apo, _, k_apo = escena("apoyado", semilla=2, pasos=pasos)
    c_flo, x_flo, _, _ = escena("flota", semilla=3, pasos=pasos)
    c_atr, x_atr, _, _ = escena("atraviesa", semilla=4, pasos=pasos)
    c_cae2, x_cae2, _, _ = escena("cae", semilla=5, pasos=pasos)
    c_apo2, x_apo2, _, _ = escena("apoyado", semilla=6, pasos=pasos)

    # 1) ESCALON 1 en el mundo normal: la caida es la regularidad positiva que no obedece
    e1 = escalon1(c_cae, x_cae, nom, cortes=k_cae)
    c1 = e1["hallado"] and e1["candidato"] in ("altura", "contacto", "vel_z")
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} ESCALON 1: candidato no-yo = {e1['candidato']} "
              f"(autopredictible {e1.get('autopredictible')}, "
              f"obediencia neta {e1.get('obediencia_neta')}) — aptos {e1.get('candidatos_aptos')}")
    if not c1:
        fallos.append("escalon1")

    # 1b) EL SEÑUELO: el ruido puro tampoco obedece, y JAMAS puede ser declarado no-yo.
    #     Es la prueba de que el criterio dejo de ser una definicion por ausencia.
    ruido_fila = [d for d in e1["detalle"] if d["canal"] == "ruido"][0]
    c1b = (not ruido_fila["legal"]) and "ruido" not in (e1.get("candidatos_aptos") or [])
    if verbose:
        print(f"  {'ok  ' if c1b else 'FALLO'} SEÑUELO DE RUIDO: rechazado por ilegal "
              f"(autopredictible {ruido_fila['autopredictible']} < piso {PISO_LEGALIDAD}) "
              f"aunque su obediencia sea {ruido_fila['obediencia_neta']}")
    if not c1b:
        fallos.append("senuelo-ruido")

    # 2) SIN GRAVEDAD el escalon 1 no puede hallar caida alguna: no hay nada que hallar
    c_sg, x_sg, _, k_sg = escena("cae", semilla=7, pasos=pasos, sin_gravedad=True)
    e1sg = escalon1(c_sg, x_sg, nom, cortes=k_sg)
    alt = [d for d in e1sg["detalle"] if d["canal"] == "altura"][0]
    c2 = not (alt["legal"] and np.var(x_sg[:, nom.index("altura")]) > 1e-8)
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} SIN GRAVEDAD: la altura no se mueve, no hay caida "
              f"que declarar (varianza {np.var(x_sg[:, nom.index('altura')]):.2e})")
    if not c2:
        fallos.append("sin-gravedad")

    # 3) ESCALON 2: con contacto la caida se detiene, por encima del nulo de contacto barajado
    junto = np.vstack([x_cae, x_apo])
    e2 = escalon2(junto, nom)
    c3 = e2.get("hallado", False)
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} ESCALON 2: {e2.get('lectura', e2.get('motivo'))} "
              f"(efecto {e2.get('efecto')} vs nulo {e2.get('nulo_techo')})")
    if not c3:
        fallos.append("escalon2")

    # 4) EXAMEN: lo imposible sorprende mas que su gemelo posible
    entren = [x_cae, x_apo]
    v_flota = examen_voe(entren, x_cae2, x_flo)        # gemelos EN EL AIRE: cae vs flota
    v_atrav = examen_voe(entren, x_apo2, x_atr)        # gemelos SOBRE LA MESA: apoyado vs atraviesa
    c4 = v_flota["sorpresa_relativa"] > 0.05 and v_atrav["sorpresa_relativa"] > 0.05
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} EXAMEN VOE: flotar sorprende {v_flota['sorpresa_relativa']:+.3f}, "
              f"atravesar {v_atrav['sorpresa_relativa']:+.3f} (ambos deben ser > 0.05)")
    if not c4:
        fallos.append("examen")

    # 5) EL NULO NATURAL: dos escenas POSIBLES **DEL MISMO TIPO** no pueden sorprender.
    #    LECCION CAZADA POR ESTA MISMA REGLA 31 (9-ago-2026): comparar 'cae' con 'apoyado' daba
    #    sorpresa enorme y parecia un fallo del instrumento — pero son escenas DISTINTAS, no
    #    gemelas. El par debe ser gemelo: mismo montaje, unica diferencia la (im)posibilidad.
    _, x_cae3, _, _ = escena("cae", semilla=8, pasos=pasos)
    _, x_apo3, _, _ = escena("apoyado", semilla=9, pasos=pasos)
    v_nulo = examen_voe(entren, x_cae2, x_cae3)
    v_nulo2 = examen_voe(entren, x_apo2, x_apo3)
    c5 = (abs(v_nulo["sorpresa_relativa"]) < 0.05
          and abs(v_nulo2["sorpresa_relativa"]) < 0.05)
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} NULO NATURAL: dos posibles gemelas sorprenden "
              f"{v_nulo['sorpresa_relativa']:+.4f} y {v_nulo2['sorpresa_relativa']:+.4f} "
              f"(ambas deben ser < 0.05 en magnitud)")
    if not c5:
        fallos.append("nulo-natural")

    # 6) CONTACTO BARAJADO: el escalon 2 debe callar (su ligadura era exactamente esa senal)
    baraj = junto.copy()
    rng = np.random.default_rng(29)
    baraj[:, nom.index("contacto")] = baraj[rng.permutation(len(baraj)), nom.index("contacto")]
    e2b = escalon2(baraj, nom)
    c6 = not e2b.get("hallado", False)
    if verbose:
        print(f"  {'ok  ' if c6 else 'FALLO'} CONTACTO BARAJADO: el escalon 2 calla "
              f"(efecto {e2b.get('efecto')} vs nulo {e2b.get('nulo_techo')})")
    if not c6:
        fallos.append("contacto-barajado")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la escalera halla lo que hay y calla donde no."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="La escalera de soporte (prereg-29)")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--pasos", type=int, default=900)
    ap.add_argument("--semilla", type=int, default=None,
                    help="corrida oficial de UNA semilla (para encolar en el latido)")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31(pasos=a.pasos))
    if a.pasos < PASOS_MINIMOS:
        raise SystemExit(f"MEDICION INVALIDA: {a.pasos} pasos (minimo {PASOS_MINIMOS}).")
    if a.semilla is None:
        print("uso: --regla31 | --semilla N")
        return
    s = a.semilla
    base = 100 * s
    c1, x1, nom, k1 = escena("cae", semilla=base + 1, pasos=a.pasos)
    c2, x2, _, _ = escena("apoyado", semilla=base + 2, pasos=a.pasos)
    _, x3, _, _ = escena("flota", semilla=base + 3, pasos=a.pasos)
    _, x4, _, _ = escena("atraviesa", semilla=base + 4, pasos=a.pasos)
    _, x5, _, _ = escena("cae", semilla=base + 5, pasos=a.pasos)
    _, x6, _, _ = escena("apoyado", semilla=base + 6, pasos=a.pasos)
    _, x7, _, _ = escena("cae", semilla=base + 7, pasos=a.pasos)
    _, x8, _, _ = escena("apoyado", semilla=base + 8, pasos=a.pasos)
    salida = {"prerregistro": 29, "semilla": s, "pasos": a.pasos,
              "escalon1": escalon1(c1, x1, nom, cortes=k1),
              "escalon2": escalon2(np.vstack([x1, x2]), nom),
              "examen_flota": examen_voe([x1, x2], x5, x3),
              "examen_atraviesa": examen_voe([x1, x2], x6, x4),
              "nulo_natural_aire": examen_voe([x1, x2], x5, x7),
              "nulo_natural_mesa": examen_voe([x1, x2], x6, x8)}
    out = os.path.join(BASE, "resultados", f"p29-soporte-s{s}")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False, default=str)
    print(f"guardado en {out}/resumen.json (parcial — el veredicto exige las 5 semillas juntas)")


if __name__ == "__main__":
    main()
