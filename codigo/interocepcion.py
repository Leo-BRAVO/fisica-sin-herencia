# interocepcion.py — GEN G10 del GENOMA-DIEGO: que la mente SIENTA su propio gasto.
# (Aprobado por el director el 8-ago-2026. Prerregistro-20 para su uso en decisiones.)
#
# Por que existe: la ecuacion del impulso (G2) tiene hoy el denominador FALSO — coste = 1
# uniforme, un numero que pusimos nosotros. Un ente que no siente lo que le cuesta algo no
# puede elegir de verdad: perseguiria una ganancia diminuta a costo infinito (el canal de
# Goodhart nº4 de la critica de 2026). G10 lo vuelve real.
#
# Que mide (todo sobre SU cuerpo, cero informacion del mundo — Regla 1 intacta):
#   - tiempo de reloj de cada campana
#   - trabajo del motor: semillas x iteraciones x complejidad maxima (proxy de computo)
#   - tamano del territorio: transiciones y replicas procesadas
#   - y de ahi un COSTE en unidades propias, comparable entre campanas
#
# ESTADO (blindaje que ordeno el director): esto MIDE y REGISTRA. NO alimenta ninguna decision
# hasta que el prerregistro-20 este firmado y sus pruebas de la Regla 31 aprobadas. Un organo
# nuevo se enciende despues de saber que no miente, no antes.
#
# Uso:  python interocepcion.py --sentir <carpeta_resultados>   (registra el gasto de una campana)
#       python interocepcion.py --ver                            (lo que la mente ha sentido)

import os
import re
import json
import glob
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUERPO = os.path.join(BASE, "arbol", "INTEROCEPCION.jsonl")   # append-only, como su memoria

# Referencia de normalizacion, congelada aqui ANTES de cualquier uso (no se ajusta despues):
# una campana "unidad" = 5 semillas x 400 iteraciones x maxsize 20 sobre 1000 transiciones.
UNIDAD = {"semillas": 5, "niter": 400, "maxsize": 20, "transiciones": 1000}


def leer_args(resumen):
    """Extrae el esfuerzo declarado de una campana desde su resumen (o valores por defecto)."""
    n_sem = len(resumen.get("semillas", {})) or 1
    n_rep = len(resumen.get("replicas", [])) or 1
    return n_sem, n_rep


def trabajo_del_motor(n_semillas, niter, maxsize):
    """Proxy de computo: el motor evalua ~ semillas x iteraciones x complejidad. Sin unidades
    fisicas — es esfuerzo propio, medido en multiplos de la campana unidad."""
    return (n_semillas / UNIDAD["semillas"]) * (niter / UNIDAD["niter"]) * (maxsize / UNIDAD["maxsize"])


def sentir(carpeta, niter=400, maxsize=20, segundos=None):
    """Registra lo que le costo una campana. El tiempo se toma del disco (mtime del primer y
    ultimo archivo escrito) si no se pasa explicitamente: la mente siente cuanto duro, no
    cuanto dijimos que duraria."""
    ruta = os.path.join(BASE, carpeta) if not os.path.isabs(carpeta) else carpeta
    resumen_p = os.path.join(ruta, "resumen.json")
    if not os.path.exists(resumen_p):
        raise SystemExit(f"sin resumen en {carpeta} — no hay campana que sentir")
    resumen = json.load(open(resumen_p, encoding="utf-8"))
    n_sem, n_rep = leer_args(resumen)

    archivos = sorted(glob.glob(os.path.join(ruta, "*.json")), key=os.path.getmtime)
    if segundos is None and len(archivos) >= 2:
        segundos = os.path.getmtime(archivos[-1]) - os.path.getmtime(archivos[0])
    segundos = float(segundos or 0.0)
    # HONESTIDAD DEL ORGANO (8-ago-2026): si el tiempo salio de las fechas del disco y estas
    # vienen de un clon de git, TODAS son iguales y el resultado es 0.0 — una sensacion falsa.
    # Se marca en el propio registro en vez de aparentar que se sintio algo.
    tiempo_fiable = segundos > 0.0

    trabajo = trabajo_del_motor(n_sem, niter, maxsize)
    territorio = n_rep / 1.0
    # Coste sentido: el esfuerzo del motor pesa por el territorio recorrido. Definicion
    # congelada; cualquier cambio exige enmienda registrada (misma disciplina que las varas).
    coste = trabajo * max(territorio, 1.0) ** 0.5

    sensacion = {
        "campana": os.path.basename(os.path.normpath(ruta)),
        "segundos": round(segundos, 1),
        "semillas": n_sem, "replicas": n_rep,
        "trabajo_motor": round(trabajo, 4),
        "coste_sentido": round(coste, 4),
        "tiempo_fiable": tiempo_fiable,
        "es_nulo": bool(resumen.get("nulo")),
    }
    with open(CUERPO, "a", encoding="utf-8") as f:
        f.write(json.dumps(sensacion, ensure_ascii=False) + "\n")
    print(json.dumps(sensacion, ensure_ascii=False, indent=2))
    return sensacion


def coste_de(campana):
    """Lo que le costo una campana, si lo recuerda. None si nunca la sintio.
    (Esta es la funcion que G2 usara COMO DENOMINADOR cuando el prereg-20 lo autorice.)"""
    if not os.path.exists(CUERPO):
        return None
    ultimo = None
    for linea in open(CUERPO, encoding="utf-8"):
        if not linea.strip():
            continue
        s = json.loads(linea)
        if s.get("campana") != campana:
            continue
        # El cuerpo es append-only: una CORRECCION posterior anula la sensacion anterior en vez
        # de borrarla (8-ago-2026: un registro fabricado en pruebas quedo anulado asi).
        if s.get("tipo") == "CORRECCION" and s.get("anula_anterior"):
            ultimo = None
            continue
        ultimo = s
    if ultimo is None or not ultimo.get("tiempo_fiable", False):
        return None          # sin tiempo fiable no hay coste que ofrecer: mejor nada que mentir
    return ultimo["coste_sentido"]


def ver(n=12):
    if not os.path.exists(CUERPO):
        print("la mente aun no ha sentido nada")
        return
    lineas = [l for l in open(CUERPO, encoding="utf-8") if l.strip()][-n:]
    print(f"{'campana':38} {'segundos':>9} {'trabajo':>8} {'coste':>8}")
    for l in lineas:
        s = json.loads(l)
        print(f"{s['campana']:38} {s['segundos']:>9.1f} {s['trabajo_motor']:>8.3f} {s['coste_sentido']:>8.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="G10 — la mente siente su propio gasto")
    ap.add_argument("--sentir", default=None, help="carpeta de resultados de una campana")
    ap.add_argument("--segundos", type=float, default=None,
                    help="tiempo REAL de reloj de la campana; sin el, se deduce del disco "
                         "(poco fiable: git iguala las fechas al clonar)")
    ap.add_argument("--niter", type=int, default=400)
    ap.add_argument("--maxsize", type=int, default=20)
    ap.add_argument("--ver", action="store_true")
    a = ap.parse_args()
    if a.sentir:
        sentir(a.sentir, a.niter, a.maxsize, a.segundos)
    if a.ver:
        ver()
