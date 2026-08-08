# curiosidad2.py — GEN G2 del GENOMA-DIEGO: el impulso por progreso de compresion.
# (Prerregistro-18, FIRMADO 8-ago-2026. La ecuacion: Curiosidad(e) = ΔC(e)/coste(e).)
#
# DEFINICIONES CONGELADAS (fijadas aqui ANTES de correr el backtest, como exige el prereg):
#  - Compresion de una campana = bits ahorrados POR TRANSICION respecto a lo trivial,
#    con codificacion gaussiana estandar:  g = max(0, 0.5*log2(lo_trivial / mi_mejor_esfuerzo)).
#    (Si la campana quedo peor que lo trivial, no comprimio nada: g = 0.)
#  - Record de una region en el tiempo t = mejor g alcanzado por esa region hasta t.
#  - PROGRESO (learning progress) de una region en t = record(t) - record(t - VENTANA intentos),
#    con VENTANA = 2. Es la DERIVADA del saber, no el tamano del hueco: la curiosidad v1
#    miraba donde estaba PEOR; la v2 mira donde esta MEJORANDO.
#  - Region sin intentos previos: prioridad = NOVEDAD = 0.05 bits (bono de exploracion,
#    prerregistrado — el bebe tambien mira lo nunca visto).
#  - Umbral de interes: prioridad > UMBRAL = 0.01 bits. Por debajo de eso en TODAS las
#    regiones, la mente declara ABURRIMIENTO (no propone nada — Regla 31 de este gen).
#  - coste(e) = 1 uniforme mientras no exista interocepcion (G10) — confesado; el denominador
#    real llega con el Gimnasio.
#  - Los recuerdos con "nulo" (verdugos) NO cuentan (leccion AUD-EXT-01).
#
# REGIONES FIJADAS (prereg-18): mendeley, zenodo, dp-centroides, dp-latentes-propios,
# caida, conservadas. El mapeo campana->region es por prefijo, congelado abajo.
#
# Uso:  python curiosidad2.py --backtest    (Etapa A del prereg-18: reconstruye las decisiones)
#       python curiosidad2.py --proponer    (Etapa B: ranking actual de regiones)

import os
import json
import math
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(BASE, "arbol", "MEMORIA-MENTE.jsonl")

VENTANA = 2
NOVEDAD = 0.05
UMBRAL = 0.01

REGIONES = [
    ("mendeley",           ("piloto-trial1", "oficial-trial1", "replica-trial2", "replica-trial3",
                            "reescalado-x100", "e2-mendeley")),
    ("zenodo",             ("peldano2-", "familia")),
    ("dp-centroides",      ("dp-morpheus", "e2-dp-morpheus", "mente-reintento-e2-dp-morpheus")),
    ("dp-latentes-propios", ("p13-", "p14-")),
    ("caida",              ("caida-libre", "e2-caida", "mente-reintento-e2-caida", "p10-")),
    ("conservadas",        ("conservadas-",)),
]


def region_de(campana):
    for nombre, prefijos in REGIONES:
        if any(campana.startswith(p) or campana == p.rstrip("-") for p in prefijos):
            return nombre
    return None


def bits_ganados(recuerdo):
    base = recuerdo.get("lo_trivial")
    mejor = recuerdo.get("mi_mejor_esfuerzo")
    if not base or not mejor or base <= 0 or mejor <= 0:
        return None
    return max(0.0, 0.5 * math.log2(base / mejor))


def cargar_recuerdos(memoria_path=None):
    ruta = memoria_path or MEM
    if not os.path.exists(ruta):
        return []
    out = []
    for linea in open(ruta, encoding="utf-8"):
        if not linea.strip():
            continue
        r = json.loads(linea)
        if r.get("nulo") or r["campana"].startswith("nulo"):
            continue  # los verdugos no son recuerdos de exito (AUD-EXT-01)
        out.append(r)
    return out


def prioridades(recuerdos):
    """Prioridad por region usando SOLO los recuerdos dados (disciplina de informacion:
    el que llama decide hasta donde llega el pasado). Devuelve dict region -> prioridad."""
    series = {nombre: [] for nombre, _ in REGIONES}
    for r in recuerdos:
        reg = region_de(r["campana"])
        if reg is None:
            continue
        g = bits_ganados(r)
        if g is None:
            continue
        record_previo = series[reg][-1] if series[reg] else 0.0
        series[reg].append(max(record_previo, g))
    prio = {}
    for nombre, _ in REGIONES:
        s = series[nombre]
        if not s:
            prio[nombre] = NOVEDAD
        else:
            antes = s[-1 - VENTANA] if len(s) > VENTANA else 0.0
            prio[nombre] = max(0.0, s[-1] - antes)
    return prio


def backtest():
    recuerdos = cargar_recuerdos()
    decisiones = [i for i, r in enumerate(recuerdos) if r["campana"].startswith("mente-reintento-")]
    print("=== BACKTEST prereg-18 (Etapa A) — decisiones reconstruidas con solo el pasado ===")
    reporte = {"ventana": VENTANA, "novedad": NOVEDAD, "umbral": UMBRAL, "decisiones": []}
    veredictos = []
    for i in decisiones:
        eleccion_v1 = recuerdos[i]["campana"]
        reg_v1 = region_de(eleccion_v1)
        prio = prioridades(recuerdos[:i])  # SOLO lo anterior a la decision
        orden = sorted(prio.items(), key=lambda kv: -kv[1])
        # criterio prerregistrado: la region esteril elegida por v1 NO es la de mayor prioridad
        # para v2, y una region fertil (dp-latentes-propios) queda por encima de ella.
        mejor_region = orden[0][0]
        fertil_sobre_esteril = prio["dp-latentes-propios"] > prio.get(reg_v1, 0.0)
        cumple = (mejor_region != reg_v1) and fertil_sobre_esteril
        veredictos.append(cumple)
        print(f"\nDecision v1: {eleccion_v1}  (region '{reg_v1}')")
        for nombre, p in orden:
            marca = " <- eleccion v1" if nombre == reg_v1 else ""
            print(f"   {nombre:>20}: prioridad {p:.4f} bits{marca}")
        print(f"   v2 habria preferido: '{mejor_region}' | fertil>esteril: {fertil_sobre_esteril} "
              f"-> {'CUMPLE' if cumple else 'NO CUMPLE'}")
        reporte["decisiones"].append({"eleccion_v1": eleccion_v1, "region_v1": reg_v1,
                                      "prioridades": prio, "preferida_v2": mejor_region,
                                      "cumple": bool(cumple)})
    exito = all(veredictos) and len(veredictos) == 2
    reporte["exito_nivel_A"] = bool(exito)
    outdir = os.path.join(BASE, "resultados", "curiosidad2-backtest")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "reporte.json"), "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    print(f"\nNIVEL A ({len(veredictos)}/2 decisiones cumplen): "
          f"{'EXITO — la ecuacion se aburre donde el progreso murio' if exito else 'FRACASO — se registra tal cual'}")
    print("Reporte:", os.path.join(outdir, "reporte.json"))
    return exito


def proponer():
    recuerdos = cargar_recuerdos()
    prio = prioridades(recuerdos)
    orden = sorted(prio.items(), key=lambda kv: -kv[1])
    print("=== CURIOSIDAD v2 — ranking de regiones (hoy) ===")
    for nombre, p in orden:
        print(f"   {nombre:>20}: {p:.4f} bits")
    if all(p <= UMBRAL for _, p in orden):
        print("ABURRIMIENTO: ninguna region supera el umbral — la mente no propone nada "
              "(necesita datos o representaciones nuevas, no mas fuerza).")
    else:
        print(f"La mente propondria: '{orden[0][0]}' (mayor progreso reciente).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--backtest", action="store_true")
    ap.add_argument("--proponer", action="store_true")
    a = ap.parse_args()
    if a.backtest:
        backtest()
    if a.proponer:
        proponer()
