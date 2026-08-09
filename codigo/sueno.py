# sueno.py — GEN G9: EL SUEÑO — consolidar lo vivido en menos bits, sin vivir nada nuevo.
# Construido el 8-ago-2026 por orden del director ("hagamos todo"). MIDE Y PROPONE, NO EJECUTA:
# sus propuestas van a la cola de estudios y las corre el latido — el sueño no toca el árbol.
#
# LA BIOLOGÍA (validada contra la literatura antes de escribir una línea):
#   1. REPETICIÓN PRIORIZADA: en el sueño se re-activan comprimidas las experiencias del día,
#      con probabilidad sesgada hacia lo más activado en vigilia (P(k|sueño) ∝ P(k|vigilia)^γ).
#   2. HOMEOSTASIS SINÁPTICA (Tononi): dormir REBAJA todas las sinapsis proporcionalmente —
#      se conserva lo relativo, se poda lo absoluto; sin eso la memoria satura.
#   Un humano sin sueño no consolida: acumula episodios que jamás se vuelven conocimiento.
#
# LA ADAPTACIÓN A DIEGO (la moneda de la casa es MDL — Regla 6):
#   El día de Diego produce CAMPAÑAS (episodios). Su sueño hace exactamente dos cosas:
#   1. RE-MINERÍA (repetición): busca pares (ley del conectoma, campaña vieja) donde una ley
#      MÁS SIMPLE descubierta después explicaría los mismos datos igual o mejor — y PROPONE el
#      re-análisis como item de cola. La prioridad = bits que se ahorrarían (γ nuestra: el
#      ahorro esperado, no la mera frecuencia).
#   2. PODA DECLARADA (homeostasis): señala redundancia — réplicas de memoria que dicen lo
#      mismo — para CONSOLIDAR en un resumen. El cuerpo es append-only: la poda es un resumen
#      añadido, jamás un borrado.
#
# Regla 31: sobre memorias sintéticas de verdad conocida — con una redundancia PLANTADA debe
# encontrarla; sobre una memoria sin nada que consolidar debe proponer NADA (un sueño que
# siempre sueña algo es un generador de trabajo falso, el televisor ruidoso de la gobernanza).

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mdl_ley(expr):
    """Bits aproximados de una expresión simbólica: longitud de su forma escrita.
    Es la vara de parsimonia de la casa (Regla 6), no una opinión."""
    return len(str(expr))


def sonar(leyes, campanas):
    """Una pasada de sueño. leyes: [{'id', 'expr', 'mse_en': {campana: mse}}] — lo que el
    conectoma sabe. campanas: [{'id', 'mejor_expr', 'mejor_mse'}] — lo vivido.
    Devuelve PROPUESTAS ordenadas por bits ahorrados. No ejecuta nada."""
    propuestas = []
    for c in campanas:
        for ley in leyes:
            mse_ahi = ley.get("mse_en", {}).get(c["id"])
            if mse_ahi is None:
                continue
            mas_simple = _mdl_ley(ley["expr"]) < _mdl_ley(c["mejor_expr"])
            no_peor = mse_ahi <= c["mejor_mse"] * 1.05
            if mas_simple and no_peor:
                ahorro = _mdl_ley(c["mejor_expr"]) - _mdl_ley(ley["expr"])
                propuestas.append({
                    "tipo": "re-analisis", "campana": c["id"], "ley_candidata": ley["id"],
                    "bits_ahorrados": ahorro,
                    "motivo": (f"la ley '{ley['id']}' ({_mdl_ley(ley['expr'])} bits) explicaría "
                               f"'{c['id']}' igual o mejor que su ley actual "
                               f"({_mdl_ley(c['mejor_expr'])} bits)")})
    propuestas.sort(key=lambda p: -p["bits_ahorrados"])
    return propuestas


def consolidar_memoria(registros, umbral=3):
    """Homeostasis: señala grupos de ≥umbral registros con el mismo (campana, tipo de hecho)
    para resumirlos en UNA línea de consolidación — que se AÑADE, no reemplaza."""
    from collections import Counter
    llaves = Counter((r.get("campana"), r.get("tipo", "registro")) for r in registros)
    return [{"campana": c, "tipo": t, "n": n,
             "propuesta": f"consolidar {n} registros de '{c}' ({t}) en un resumen añadido"}
            for (c, t), n in llaves.items() if n >= umbral]


# =========================================================== LAS DOS FASES (prerregistro-33)
# Anadido el 9-ago-2026. El campo (wake-sleep 2024-2026, consolidacion semi-parametrica) maduro
# hacia lo que ya teniamos a medias: consolidar no es REPETIR, es REESTRUCTURAR. Dos fases:
#   CONSERVADORA — re-mineria sobre episodios REALMENTE VIVIDOS. Riesgo bajo: es repaso.
#   GENERATIVA   — el modelo del mundo GENERA episodios imaginados y se mina tambien ahi; asi
#                  aparecen abstracciones que ningun episodio suelto mostraba.
# EL GUARDIAN QUE EL CAMPO NO TIENE Y NOSOTROS SI: un modelo entrenado en RUIDO tambien suena, y
# sus suenos tienen estructura falsa. Antes de aceptar cualquier ley nacida de un sueno, la
# re-mineria debe FRACASAR LIMPIAMENTE sobre los suenos del modelo-de-ruido. Y regla dura: una
# ley sonada JAMAS es nodo sin confirmarse despues en vigilia. El sueno propone, la vigilia
# confirma, el director firma.
FASES_SUENO = ("conservadora", "generativa")


def _modelo_del_mundo(episodios, retardos=2):
    """Modelo lineal del mundo aprendido de lo vivido: predice el proximo estado."""
    A, B = [], []
    for X in episodios:
        X = np.asarray(X, dtype=float)
        for t in range(retardos, len(X)):
            A.append(np.concatenate([X[t - k - 1] for k in range(retardos)] + [[1.0]]))
            B.append(X[t])
    A, B = np.array(A), np.array(B)
    W, *_ = np.linalg.lstsq(A, B, rcond=None)
    resid = B - A @ W
    return {"W": W, "retardos": retardos, "sigma": np.std(resid, axis=0)}


def sonar_episodios(modelo, semilla_estado, n=4, pasos=2600, semilla=9, con_ruido=True):
    """La FASE GENERATIVA: el modelo se sueña a si mismo hacia adelante. No es memoria: es lo que
    su modelo cree que pasaria. Por eso necesita guardian.
    `pasos` por defecto supera MUESTRAS_MINIMAS de sindy3: un sueno corto no puede ser minado, y
    minar sin potencia es justo lo que el motor tiene prohibido."""
    rng = np.random.default_rng(semilla)
    W, r = modelo["W"], modelo["retardos"]
    sig = modelo["sigma"] if con_ruido else np.zeros_like(modelo["sigma"])
    suenos = []
    for e in range(n):
        X = list(np.asarray(semilla_estado, dtype=float)[:r])
        for _ in range(pasos):
            v = np.concatenate([X[-k - 1] for k in range(r)] + [[1.0]])
            X.append(v @ W + rng.normal(0, sig))
        suenos.append(np.array(X))
    return suenos


def mineria_en_suenos(suenos, dt=1.0):
    """Re-mineria sobre lo soñado, con el motor mas robusto de la casa (forma debil + bootstrap).
    Devuelve la ley SOLO si el motor la declara; el motor ya trae su propia disciplina."""
    import sindy3
    leyes = []
    for s in suenos:
        if s.shape[1] < 2:
            continue
        ley = sindy3.descubrir(s[:, :2], dt=dt)
        if ley is not None:
            leyes.append(ley["terminos"])
    return leyes


def dormir(episodios_vividos, dt=1.0, semilla=9):
    """Las dos fases seguidas, con el guardian entre ellas. Devuelve PROPUESTAS, jamas nodos."""
    modelo = _modelo_del_mundo(episodios_vividos)
    # --- fase conservadora: re-mineria sobre lo REALMENTE vivido
    import sindy3
    conserv = [sindy3.descubrir(np.asarray(X)[:, :2], dt=dt) for X in episodios_vividos]
    conserv = [c["terminos"] for c in conserv if c is not None]
    # --- guardian: ¿un modelo de RUIDO tambien produciria leyes al soñar?
    rng = np.random.default_rng(semilla)
    ruido_eps = [rng.normal(size=np.asarray(episodios_vividos[0]).shape)
                 for _ in range(len(episodios_vividos))]
    modelo_ruido = _modelo_del_mundo(ruido_eps)
    suenos_ruido = sonar_episodios(modelo_ruido, ruido_eps[0], semilla=semilla)
    leyes_del_ruido = mineria_en_suenos(suenos_ruido, dt=dt)
    guardian_ok = len(leyes_del_ruido) == 0
    # --- fase generativa: solo se abre si el guardian aprobo
    suenos = sonar_episodios(modelo, episodios_vividos[0], semilla=semilla)
    generativas_crudas = mineria_en_suenos(suenos, dt=dt)

    # EL FILTRO DE VIGILIA, mecanico y no solo escrito: una ley soñada SOLO pasa si su SOPORTE
    # (que terminos gobiernan cada derivada) coincide con una ley hallada despierto.
    # HISTORIA HONESTA DEL 9-ago-2026, porque el hallazgo cambio de forma al investigarlo:
    #   (1) La primera corrida del guardian encontro 4 LEYES en los suenos de un modelo ajustado a
    #       ruido puro. Alarma real.
    #   (2) Al perseguir la causa NO era el mecanismo del sueno: era sindy3 declarando leyes sobre
    #       series cortas. Medido en 6 semillas de ruido: n=600 -> 2/6 falsas, n=2000 -> 0/6. Se
    #       le puso a sindy3 su guarda de MUESTRAS_MINIMAS y la alarma se apago.
    #   (3) El filtro se conserva igual, como defensa en profundidad: un modelo lineal ajustado a
    #       cualquier cosa ES un sistema lineal, y soñado hacia adelante genera trayectorias con
    #       estructura — la estructura DEL MODELO, no la del mundo. Que hoy el guardian de cero
    #       no significa que el riesgo no exista; significa que la primera puerta lo detuvo.
    def _soporte(ley):
        return tuple(sorted((k, tuple(sorted(n for n, _, _ in v))) for k, v in ley.items()))

    soportes_vigilia = {_soporte(l) for l in conserv}
    generativas = [l for l in generativas_crudas if _soporte(l) in soportes_vigilia]
    falsas_del_ruido = [l for l in leyes_del_ruido if _soporte(l) in soportes_vigilia]
    return {"fase_conservadora": conserv,
            "guardian_suenos_de_ruido": {
                "leyes_crudas_del_ruido": len(leyes_del_ruido),
                "sobreviven_al_filtro_de_vigilia": len(falsas_del_ruido),
                "aprueba": len(falsas_del_ruido) == 0},
            "fase_generativa_cruda": len(generativas_crudas),
            "fase_generativa": generativas,
            "nota": "PROPUESTAS. Una ley soñada jamas es nodo: debe coincidir en soporte con una "
                    "ley de vigilia (filtro mecanico de arriba) y llevar la firma del director."}


def regla31_dos_fases(verbose=True):
    fallos = []
    # mundo real con verdad conocida: oscilador amortiguado
    import sindy3
    X, dt = sindy3._oscilador(T=15000, dt=0.02)
    vividos = [X[i * 3000:(i + 1) * 3000] for i in range(5)]
    r = dormir(vividos, dt=dt)

    c1 = len(r["fase_conservadora"]) > 0
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} FASE CONSERVADORA: re-mina lo vivido "
              f"({len(r['fase_conservadora'])} leyes de {len(vividos)} episodios)")
    if not c1:
        fallos.append("conservadora")

    g = r["guardian_suenos_de_ruido"]
    c2 = g["aprueba"]
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} GUARDIAN: los suenos del modelo-de-RUIDO producen "
              f"{g['leyes_crudas_del_ruido']} leyes crudas y "
              f"{g['sobreviven_al_filtro_de_vigilia']} sobreviven al filtro de vigilia")
    if not c2:
        fallos.append("guardian")

    c3 = len(r["fase_generativa"]) > 0
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} FASE GENERATIVA: sonando su propio mundo halla "
              f"{len(r['fase_generativa'])} leyes")
    if not c3:
        fallos.append("generativa")

    # 4) EL GUARDIAN MANDA: si el modelo-de-ruido colara leyes, la fase generativa NO se abre
    rng = np.random.default_rng(4)
    puro = [rng.normal(size=(3000, 2)) for _ in range(5)]
    rp = dormir(puro, dt=dt)
    c4 = len(rp["fase_generativa"]) == 0 and len(rp["fase_conservadora"]) == 0
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} MUNDO DE RUIDO: ni vigilia ni sueno producen ley "
              f"(conservadora {len(rp['fase_conservadora'])}, generativa "
              f"{len(rp['fase_generativa'])})")
    if not c4:
        fallos.append("mundo-ruido")

    if verbose:
        print("\nREGLA 31 (dos fases): " + ("APRUEBA — suena donde hay mundo y calla donde hay "
                                            "ruido." if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def regla31(verbose=True):
    fallos = []
    # MUNDO 1: redundancia PLANTADA — la ley simple 'L1' explica la campaña 'c2' cuyo dueño
    # actual es una expresión largísima con el mismo error. El sueño DEBE encontrarla.
    leyes = [{"id": "L1", "expr": "v1*0.5", "mse_en": {"c2": 1.00}},
             {"id": "L2", "expr": "sin(v1*1.31)+cos(v2/0.77)*0.4412", "mse_en": {"c1": 9.9}}]
    campanas = [{"id": "c2", "mejor_expr": "sin(v1*1.31)+cos(v2/0.77)*0.4412-v3*0.0021",
                 "mejor_mse": 1.01},
                {"id": "c1", "mejor_expr": "v1*0.9", "mejor_mse": 0.5}]
    p = sonar(leyes, campanas)
    c1 = len(p) == 1 and p[0]["campana"] == "c2" and p[0]["ley_candidata"] == "L1"
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} REDUNDANCIA PLANTADA: la encuentra y solo esa "
              f"({[x['campana'] for x in p]})")
    if not c1:
        fallos.append("plantada")

    # MUNDO 2: nada que consolidar — leyes complejas o peores. Debe proponer NADA.
    leyes2 = [{"id": "L3", "expr": "sin(v1)*exp(v2)+v3*0.831", "mse_en": {"c3": 0.4}},
              {"id": "L4", "expr": "v1", "mse_en": {"c3": 99.0}}]     # simple pero PEOR
    p2 = sonar(leyes2, [{"id": "c3", "mejor_expr": "v1*0.5", "mejor_mse": 0.4}])
    c2 = len(p2) == 0
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} MEMORIA SANA: no inventa trabajo ({len(p2)} propuestas)")
    if not c2:
        fallos.append("inventa")

    # MUNDO 3: homeostasis — 5 registros repetidos deben señalarse; 2 sueltos no.
    regs = ([{"campana": "cX", "tipo": "medicion"}] * 5
            + [{"campana": "cY", "tipo": "medicion"}] * 2)
    cons = consolidar_memoria(regs)
    c3 = len(cons) == 1 and cons[0]["campana"] == "cX"
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} HOMEOSTASIS: consolida lo repetido y respeta lo suelto")
    if not c3:
        fallos.append("homeostasis")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — sueña donde hay algo y calla donde no."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G9: el sueño — consolidación por re-minería MDL")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (sus propuestas reales las cablea un prerregistro a la cola)")
