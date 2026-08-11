# tacto.py — PRERREGISTRO 41: ¿el sentido del tacto está OCIOSO o está AVERIADO?
#
# ORIGEN, Y ES IMPORTANTE QUE SEA ESTE: no lo propuso el director ni lo propuse yo mirando el
# codigo. LO DIJO DIEGO. El 10-ago, en la ronda de vida, `sentido_tacto` publico por el bus una
# medicion sobre si mismo: "tengo un sentido que casi nunca se enciende", con 0.0001 contra un
# umbral de 0.01 — cien veces por debajo. Y declaro las DOS causas que no puede separar mirando:
#   OCIOSO   — el canal funciona y no hay nada a su alcance que tocar
#   AVERIADO — el canal esta roto y no se encenderia ni tocando algo
# Separarlas EXIGE ACTUAR. Eso es lo que hace este modulo.
#
# POR QUE ESCENA PROPIA Y NO `gimnasio.episodio`: la condicion VACIO necesita un mundo SIN SUELO y
# SIN OBJETOS, y `gimnasio.py` no tiene ese modo. Antes que añadirle uno —esta sellado y lo usan
# otros estudios— se construye aqui la misma escena, con LAS MISMAS constantes importadas de
# gimnasio, para que el cuerpo examinado sea el mismo cuerpo.
#
# Uso: python tacto.py [--regla31] [--salida resultados/p41-tacto/medida.json]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

import gimnasio                                                             # noqa: E402

# ------------------------------------------------------------------ EL PRERREGISTRO, EN CODIGO
SEMILLAS = (1, 2, 3, 4, 5)
PASOS = 1200
PISO_BUSCA = 0.05          # BUSCA debe encenderse por encima de esto (5 veces el umbral dormido)
TECHO_APAGADO = 0.01       # QUIETO y VACIO deben quedarse por debajo (el umbral de "dormido")
MINIMOS_BUSCA = 4          # de 5 semillas
PISO_ACUERDO = 0.60        # acuerdo con la verdad del simulador, en los pasos con contacto
MARGEN_SOBRE_TONTO = 0.15  # y debe superar al tonto ("siempre hay contacto") por esto

METODO = {
    "prerregistro": 41,
    "tipo_de_medida": "umbral",
    "que_mide": ("la fraccion de pasos en que ALGUN canal de tacto esta encendido, en tres "
                 "condiciones; y el acuerdo de esos canales con el registro de contactos del "
                 "propio simulador"),
    "comparten_datos": {
        "hay": False,
        "porque": "las tres condiciones corren en mundos SEPARADOS y con la misma semilla, a "
                  "proposito: lo unico que cambia entre ellas es la politica motora (quieto o "
                  "buscando) y si hay algo que tocar. La verdad del simulador se usa para JUZGAR "
                  "el canal, jamas entra en lo que el canal mide (Regla 27).",
    },
    "linea_base": ("decir SIEMPRE 'hay contacto'. Sobre los pasos que el simulador marca como "
                   "contacto, ese tonto acierta el 100%; por eso el acuerdo se exige CON margen "
                   "sobre el, y no en bruto (Regla 11)"),
    "formulas": [
        {"base": {"empuje": 1.0, "hay_suelo": 1.0}, "parametro": "hay_suelo", "factor": 0.0,
         "esperado": "baja",
         "porque": "quitar el suelo y los objetos deja al brazo sin nada que tocar: la fraccion "
                   "encendida tiene que caer. Si NO cayera, el canal no estaria midiendo contacto "
                   "sino movimiento — y el estudio entero seria NULO"},
        {"base": {"empuje": 1.0, "hay_suelo": 1.0}, "parametro": "empuje", "factor": 0.0,
         "esperado": "baja",
         "porque": "sin empuje el brazo no se mueve y no alcanza nada: es la condicion QUIETO, la "
                   "situacion de hoy, y debe dar casi cero"},
    ],
}


# ALCANCE MEDIDO DEL BRAZO, y es el hallazgo que obligo a rediseñar la escena.
# La punta baja como mucho a z=0.380 y llega a x=0.660. El suelo del gimnasio esta en z=0 y sus
# objetos en z~0.20: EL BRAZO NO PUEDE TOCAR NADA DE LA ESCENA ESTANDAR, con ninguna politica.
# Lo caza LA PUERTA antes de existir un solo dato: mi condicion BUSCA daba 0.0000 igual que
# QUIETO, y el estudio habria concluido "AVERIADO" con un experimento donde tocar era imposible.
# Por eso la condicion BUSCA pone un obstaculo DENTRO del alcance. No es aflojar el criterio —los
# umbrales siguen congelados— es hacer el experimento fisicamente posible.
# GEOMETRIA MEDIDA (10-ago-2026), y es lo que fija donde va el obstaculo:
#   EN REPOSO, sin par, el brazo cuelga a lo largo de +x en y=0, con la punta en (0.593, 0, 0.442).
#   BARRIENDO, con par, la punta recorre x[-0.22,0.657] y[-0.440,0.439] z[0.380,0.820].
# El obstaculo va en y=+0.38: DENTRO del barrido y FUERA de la linea de reposo. Asi QUIETO no lo
# toca (el brazo cuelga en y=0) y BUSCA si (barre hasta y=0.44).
# La primera version lo puso en y=0 y QUIETO dio 0.97 — el brazo caia ENCIMA del obstaculo y se
# quedaba apoyado. La puerta no lo caza (eso es del estudio), pero lo caza el propio criterio de
# QUIETO, que existe justo para eso.
ALCANCE = {"reposo_punta": [0.593, 0.0, 0.442],
           "barrido_x": [-0.220, 0.657], "barrido_y": [-0.440, 0.439],
           "barrido_z": [0.380, 0.820], "medido": "10-ago-2026"}
OBSTACULO = [0.40, 0.38, 0.55]     # dentro del barrido, fuera del reposo. Declarado ANTES de correr


def _escena(p, cliente, hay_suelo=True, obstaculo=True):
    """La MISMA escena del gimnasio —mismas constantes, mismo cuerpo— con dos perillas:
    `hay_suelo` quita suelo y objetos (condicion VACIO) y `obstaculo` pone una caja DENTRO del
    alcance real del brazo, que es la unica forma de que tocar sea posible."""
    p.resetSimulation(physicsClientId=cliente)
    p.setGravity(0, 0, -9.8, physicsClientId=cliente)
    p.setTimeStep(gimnasio.PASO_FISICO, physicsClientId=cliente)
    n = gimnasio.N_ARTICULACIONES
    if hay_suelo:
        p.createMultiBody(0, p.createCollisionShape(p.GEOM_PLANE, physicsClientId=cliente),
                          physicsClientId=cliente)
    esl = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.16, 0.04, 0.04],
                                 physicsClientId=cliente)
    base_c = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.08, 0.08, 0.08],
                                    physicsClientId=cliente)
    # pybullet EXIGE que todos los arreglos de eslabon midan lo mismo, incluido el visual —
    # omitirlo revienta con "All link arrays need to be same size".
    esl_v = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.16, 0.04, 0.04],
                                rgbaColor=[0.80, 0.80, 0.80, 1], physicsClientId=cliente)
    brazo = p.createMultiBody(
        baseMass=0, baseCollisionShapeIndex=base_c, basePosition=[0, 0, 0.6],
        linkMasses=[0.4] * n, linkCollisionShapeIndices=[esl] * n,
        linkVisualShapeIndices=[esl_v] * n,
        linkPositions=[[0.22, 0, 0]] * n, linkOrientations=[[0, 0, 0, 1]] * n,
        linkInertialFramePositions=[[0, 0, 0]] * n,
        linkInertialFrameOrientations=[[0, 0, 0, 1]] * n,
        linkParentIndices=list(range(n)), linkJointTypes=[p.JOINT_REVOLUTE] * n,
        linkJointAxis=[[0, 0, 1], [0, 1, 0], [0, 0, 1]], physicsClientId=cliente)
    for j in range(n):
        p.setJointMotorControl2(brazo, j, p.VELOCITY_CONTROL, force=0, physicsClientId=cliente)
    objetos = []
    if hay_suelo:
        caja = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.07, 0.07, 0.07],
                                      physicsClientId=cliente)
        for i in range(gimnasio.N_OBJETOS):
            objetos.append(p.createMultiBody(
                baseMass=0.25, baseCollisionShapeIndex=caja,
                basePosition=[0.35 + 0.18 * i, 0.0, 0.20], physicsClientId=cliente))
    if obstaculo and hay_suelo:
        # FIJO (masa 0) y dentro del alcance: si fuera libre saldria despedido al primer roce y
        # el contacto duraria un instante. Se declara su posicion en OBSTACULO, arriba.
        blq = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.10, 0.10, 0.10],
                                     physicsClientId=cliente)
        blq_v = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.10, 0.10, 0.10],
                                    rgbaColor=[0.45, 0.45, 0.45, 1], physicsClientId=cliente)
        objetos.append(p.createMultiBody(0, blq, blq_v, basePosition=list(OBSTACULO),
                                         physicsClientId=cliente))
    return brazo, objetos


def corrida(semilla, condicion="busca", pasos=PASOS, empuje=1.0, hay_suelo=True):
    """Una corrida. Devuelve la fraccion encendida del tacto y la verdad de contactos del
    simulador, paso a paso.

    CONDICIONES (las tres del prerregistro):
      quieto — sin empuje: la situacion de hoy. El tacto debe quedarse apagado.
      busca  — el brazo se mueve a proposito hasta chocar con algo.
      vacio  — se mueve IGUAL que en 'busca' pero no hay suelo ni objetos. ES EL SEÑUELO: si el
               canal se enciende aqui, mide MOVIMIENTO y no contacto, y el estudio es NULO.
    """
    import pybullet as p
    cliente = p.connect(p.DIRECT)
    try:
        con_suelo = hay_suelo and condicion != "vacio"
        brazo, _ = _escena(p, cliente, hay_suelo=con_suelo)
        n = gimnasio.N_ARTICULACIONES
        rng = np.random.default_rng(int(semilla))
        e = 0.0 if condicion == "quieto" else float(empuje)
        tacto, verdad = [], []
        for t in range(int(pasos)):
            for j in range(n):
                # BUSCA: un balbuceo amplio y lento que barre el espacio hasta topar con algo.
                # No se le dice DONDE esta el suelo — solo que se mueva. Si supiera donde tocar,
                # el estudio no probaria nada sobre el sentido.
                par = e * (2.5 * np.sin(0.004 * t + j) + 0.8 * rng.normal())
                p.setJointMotorControl2(brazo, j, p.TORQUE_CONTROL, force=float(par),
                                        physicsClientId=cliente)
            p.stepSimulation(physicsClientId=cliente)
            # EL CANAL DE TACTO tal como lo lee Diego (gimnasio: contacto binario por eslabon)
            canales = [1.0 if p.getContactPoints(bodyA=brazo, linkIndexA=j,
                                                 physicsClientId=cliente) else 0.0
                       for j in range(n)]
            tacto.append(max(canales))
            # LA VERDAD DEL SIMULADOR: ¿hubo contacto de verdad en este paso? Es del lado de los
            # jueces — sirve para saber si el canal acierta, jamas entra en lo que el canal mide.
            verdad.append(1.0 if p.getContactPoints(bodyA=brazo,
                                                    physicsClientId=cliente) else 0.0)
        return {"fraccion_encendida": float(np.mean(tacto)),
                "tacto": tacto, "verdad_del_simulador": verdad}
    finally:
        p.disconnect(physicsClientId=cliente)


def _metodo_medir(empuje=1.0, hay_suelo=1.0):
    """PASO 1 — la medida escalar: la fraccion de pasos con el tacto encendido."""
    return float(corrida(1, condicion="busca", pasos=400, empuje=empuje,
                         hay_suelo=bool(hay_suelo))["fraccion_encendida"])


def _metodo_sanidad():
    """PASO 3 — LA FICHA, sobre MI PROCEDIMIENTO de medida y nada mas (la leccion de hoy: lo que
    haga el sujeto es resultado, no requisito de entrada):
      (a) la corrida es DETERMINISTA con la misma semilla — sin eso comparar condiciones no vale;
      (b) el canal leido y la verdad del simulador tienen la MISMA longitud y son comparables;
      (c) semillas distintas dan mundos distintos — si no, las 5 semillas serian una sola.
    """
    a = corrida(1, condicion="busca", pasos=300)
    b = corrida(1, condicion="busca", pasos=300)
    c = corrida(2, condicion="busca", pasos=300)
    fallos = []
    if a["fraccion_encendida"] != b["fraccion_encendida"]:
        fallos.append(f"NO ES DETERMINISTA: {a['fraccion_encendida']} vs {b['fraccion_encendida']}")
    if len(a["tacto"]) != len(a["verdad_del_simulador"]):
        fallos.append("el canal y la verdad del simulador no tienen la misma longitud")
    if a["fraccion_encendida"] == c["fraccion_encendida"]:
        fallos.append("dos semillas distintas dan el MISMO numero: no son mundos distintos")
    return {"aprueba": not fallos, "fallos": fallos,
            "semilla_1": a["fraccion_encendida"], "semilla_2": c["fraccion_encendida"]}


def regla31(verbose=True):
    """Los dos lados declarados en el prerregistro-41, sobre el procedimiento."""
    fallos = []

    def caso(nombre, ok, extra=""):
        print(f"  {'ok  ' if ok else 'FALLO'} {nombre} {extra}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-41 ==")

    # LADO NEGATIVO — sin empuje el brazo no alcanza nada.
    q = corrida(1, condicion="quieto", pasos=400)["fraccion_encendida"]
    caso("QUIETO: sin empuje el tacto no se enciende", q < TECHO_APAGADO, f"{q:.4f}")

    # LADO POSITIVO — moviendose en un mundo con suelo, algo tiene que tocar.
    b = corrida(1, condicion="busca", pasos=400)["fraccion_encendida"]
    caso("BUSCA: moviendose en un mundo con suelo, el tacto se enciende", b > PISO_BUSCA,
         f"{b:.4f}")

    # LA MEDIDA DISTINGUE — si diera lo mismo quieto que buscando, no mediria nada.
    caso("la medida distingue quieto de buscando", (b - q) > PISO_BUSCA, f"{b - q:+.4f}")

    # LA VERDAD DEL SIMULADOR ES USABLE: tiene los dos valores, no es constante.
    v = corrida(1, condicion="busca", pasos=400)["verdad_del_simulador"]
    caso("la verdad del simulador no es constante (hay pasos con y sin contacto)",
         0.0 < float(np.mean(v)) < 1.0, f"{float(np.mean(v)):.4f}")

    if verbose:
        print("REGLA 31: " + ("APRUEBA" if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def veredicto(filas):
    """Los criterios congelados del prerregistro-41, aplicados tal cual."""
    busca = [f["busca"] for f in filas]
    quieto = [f["quieto"] for f in filas]
    vacio = [f["vacio"] for f in filas]
    acuerdos = [f["acuerdo"] for f in filas if f["acuerdo"] is not None]
    tontos = [f["tonto"] for f in filas if f["tonto"] is not None]

    c1 = sum(1 for x in busca if x >= PISO_BUSCA) >= MINIMOS_BUSCA
    c2 = all(x < TECHO_APAGADO for x in quieto)
    c3 = all(x < TECHO_APAGADO for x in vacio)
    ganancia = (float(np.mean(acuerdos)) - float(np.mean(tontos))) if acuerdos else None
    c4 = (acuerdos and float(np.mean(acuerdos)) >= PISO_ACUERDO
          and ganancia is not None and ganancia >= MARGEN_SOBRE_TONTO)

    if not c3:
        v = ("NULO — el canal se enciende en el mundo VACIO: mide MOVIMIENTO y no contacto. No se "
             "usa el tacto para nada hasta rediseñarlo, gane lo que gane en el resto")
    elif c1 and c2 and c4:
        v = ("EL CANAL FUNCIONA Y ESTABA OCIOSO — el tacto queda disponible como evidencia de "
             "contacto INDEPENDIENTE DE LA VISTA")
    elif c2 and c3 and not c1:
        v = ("EL CANAL ESTA AVERIADO — hallazgo de ingenieria, no de fisica: se arregla el sensor "
             "y se repite. NADA se afirma sobre el mundo")
    else:
        v = "NO CONCLUYENTE — los criterios no encajan en ninguno de los tres veredictos escritos"
    return {"busca_enciende_en": sum(1 for x in busca if x >= PISO_BUSCA), "de": len(busca),
            "quieto_max": max(quieto), "vacio_max": max(vacio),
            "acuerdo_medio": float(np.mean(acuerdos)) if acuerdos else None,
            "linea_base_tonta_media": float(np.mean(tontos)) if tontos else None,
            "ganancia_sobre_el_tonto": ganancia,
            "criterio_1_busca_enciende": bool(c1), "criterio_2_quieto_apagado": bool(c2),
            "criterio_3_vacio_apagado_SEÑUELO": bool(c3), "criterio_4_acuerdo": bool(c4),
            "veredicto": v}


def main():
    ap = argparse.ArgumentParser(description="Prerregistro 41 — el sentido dormido")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("=== PRERREGISTRO 41 — el tacto: ¿ocioso o averiado? ===")
    filas = []
    for s in SEMILLAS:
        q = corrida(s, condicion="quieto")
        b = corrida(s, condicion="busca")
        v = corrida(s, condicion="vacio")
        # acuerdo: de los pasos que el SIMULADOR marca como contacto, ¿en cuantos se enciende el
        # canal? Y el tonto: decir siempre "hay contacto", que ahi acierta el 100% por definicion.
        conts = [i for i, x in enumerate(b["verdad_del_simulador"]) if x > 0.5]
        acuerdo = float(np.mean([b["tacto"][i] for i in conts])) if conts else None
        tonto = 1.0 if conts else None
        filas.append({"semilla": s, "quieto": q["fraccion_encendida"],
                      "busca": b["fraccion_encendida"], "vacio": v["fraccion_encendida"],
                      "pasos_con_contacto_real": len(conts),
                      "acuerdo": acuerdo, "tonto": tonto})
        print(f"  s{s}  quieto={q['fraccion_encendida']:.4f}  busca={b['fraccion_encendida']:.4f}  "
              f"vacio={v['fraccion_encendida']:.4f}  contactos_reales={len(conts)}  "
              f"acuerdo={'—' if acuerdo is None else f'{acuerdo:.4f}'}")
    r = veredicto(filas)
    print(f"\nVEREDICTO: {r['veredicto']}")
    if a.salida:
        os.makedirs(os.path.dirname(a.salida) or ".", exist_ok=True)
        # LA GEOMETRIA Y LOS UMBRALES VIAJAN CON LOS DATOS. El auditor de actas me cazo
        # publicando el alcance del brazo (0.593, 0.380, 0.38...) y los pisos del criterio en el
        # INFORME-57 sin que estuvieran en ningun archivo: numeros que solo existian en mi cabeza.
        json.dump({"prerregistro": 41, "semillas": list(SEMILLAS), "filas": filas,
                   "alcance_medido_del_brazo": ALCANCE, "obstaculo": OBSTACULO,
                   "suelo_del_gimnasio_z": 0.0, "objetos_del_gimnasio_z": 0.20,
                   "umbrales": {"piso_busca": PISO_BUSCA, "techo_apagado": TECHO_APAGADO,
                                "minimos_busca": MINIMOS_BUSCA, "piso_acuerdo": PISO_ACUERDO,
                                "margen_sobre_tonto": MARGEN_SOBRE_TONTO},
                   **r},
                  open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"escrito: {a.salida}")


if __name__ == "__main__":
    main()
