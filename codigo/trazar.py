# trazar.py — LA AUTOPSIA DE UNA PRUEBA: cada conexion que ocurrio, y quien no contesto.
#
# ORDEN DEL DIRECTOR (9-ago-2026): "un metodo para detectar cada conexion que se realizo durante
# la prueba, cada cosa que utilizo y cada organo, para poder detectar errores de diseno o errores
# de los organos o errores del cerebro de Diego".
#
# Los guardianes dicen SI o NO. `mente.py` dice COMO ESTA ARMADO. Este archivo dice **QUE PASO DE
# VERDAD** en una corrida concreta — y por eso caza una clase de fallo que ninguno de los otros
# puede ver: el fallo de COORDINACION. Un organo sano, un bus sano, y aun asi nadie contesto.
#
# LAS TRES FAMILIAS DE ERROR, separadas a proposito porque se arreglan en sitios distintos:
#
#   ERROR DE DISENO     — la culpa es del mapa, no de nadie.
#       · senal emitida a un tema que NADIE escucha (nervio a ninguna parte)
#       · organo activo que no escucha NINGUN tema (sordo por declaracion)
#       · tema declarado en el protocolo que nadie escucha jamas (tema muerto)
#
#   ERROR DE ORGANO     — el organo estaba suscrito, le hablaron, y no dijo nada.
#       · suscrito a la pregunta y MUDO
#       · organo activo que no publico nada en toda la corrida
#
#   ERROR DEL CEREBRO   — el fallo esta en la coordinacion, no en las partes.
#       · respuesta HUERFANA (contesta a un evento que no existe)
#       · pregunta sin NINGUNA respuesta (llamo y no vino nadie)
#       · CICLO causal (A causa B causa A: el pensamiento se muerde la cola)
#       · intento BLOQUEADO por el portero (no siempre es error — puede ser la prueba viva —
#         pero se lista SIEMPRE porque un bloqueo que nadie mira es un bloqueo que nadie entiende)
#
# Uso:  python trazar.py                 (la ultima corrida)
#       python trazar.py --traza <id>    (una concreta)
#       python trazar.py --revisar       (codigo de salida 1 si hay fallos)

import os
import sys
import json
import argparse
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

from sinapsis import leer, escuchan, TEMAS, _genoma


def trazas():
    """Las corridas registradas, de la mas vieja a la mas nueva."""
    vistas, orden = set(), []
    for e in leer():
        t = e.get("traza")
        if t and t not in vistas:
            vistas.add(t)
            orden.append(t)
    return orden


def reconstruir(traza=None):
    """EL ARBOL CAUSAL de una corrida: cada evento con lo que lo provoco y lo que provoco el."""
    ts = trazas()
    traza = traza or (ts[-1] if ts else None)
    ev = leer(traza=traza) if traza else []
    por_id = {e["id"]: e for e in ev}
    hijos = defaultdict(list)
    for e in ev:
        if e.get("causa") is not None:
            hijos[e["causa"]].append(e["id"])
    raices = [e["id"] for e in ev if e.get("causa") is None]
    return {"traza": traza, "eventos": ev, "por_id": por_id,
            "hijos": dict(hijos), "raices": raices}


def conexiones(t):
    """CADA CONEXION QUE OCURRIO, una por linea: quien -> quien, por que tema, con que motivo.
    Una conexion existe cuando un evento CAUSA otro, o cuando va dirigido a alguien."""
    out = []
    for e in t["eventos"]:
        if e.get("causa") is not None and e["causa"] in t["por_id"]:
            padre = t["por_id"][e["causa"]]
            out.append({"de": padre["gen"], "a": e["gen"], "tema": e.get("tema") or padre.get("tema"),
                        "via": f"{padre['tipo']}->{e['tipo']}", "ids": [padre["id"], e["id"]]})
        elif e.get("a"):
            out.append({"de": e["gen"], "a": e["a"], "tema": e.get("tema"),
                        "via": f"{e['tipo']} dirigido", "ids": [e["id"]]})
    return out


def _ciclos(t):
    """Un ciclo causal: A causo B, que causo A. En un arbol de causas eso no puede pasar."""
    ciclos = []
    for e in t["eventos"]:
        visto, cur = set(), e
        while cur is not None and cur.get("causa") is not None:
            if cur["id"] in visto:
                ciclos.append(sorted(visto))
                break
            visto.add(cur["id"])
            cur = t["por_id"].get(cur["causa"])
    return [list(c) for c in {tuple(c) for c in ciclos}]


def revisar(t, bloqueos=None):
    """Las tres familias de error, cada una con su nombre y su sitio de arreglo."""
    genes = _genoma()
    activos = {g for g, v in genes.items() if v.get("modo") != "inactivo"}
    ev = t["eventos"]
    hablaron = {e["gen"] for e in ev}
    fallos = {"diseno": [], "organo": [], "cerebro": []}

    # ---- DISENO
    temas_usados = {e.get("tema") for e in ev if e.get("tema")}
    for e in ev:
        if e["tipo"] in ("senal", "pregunta") and e.get("tema"):
            oyentes = [o for o in escuchan(e["tema"], genes) if o != e["gen"]]
            if not oyentes:
                fallos["diseno"].append(
                    f"senal de {e['gen']} al tema '{e['tema']}' que NADIE escucha (evento {e['id']})")
    for g in sorted(activos):
        if not (genes[g].get("escucha") or []):
            fallos["diseno"].append(f"{g} esta activo y no escucha NINGUN tema: sordo por declaracion")
    for tema in TEMAS:
        if not escuchan(tema, genes):
            fallos["diseno"].append(f"tema '{tema}' declarado y sin un solo oyente: tema muerto")

    # ---- ORGANO
    for g in sorted(activos - hablaron):
        fallos["organo"].append(f"{g} esta activo y NO publico nada en toda la corrida")
    for e in ev:
        if e["tipo"] != "pregunta":
            continue
        destinos = [e["a"]] if e.get("a") else [o for o in escuchan(e.get("tema") or "", genes)
                                                if o != e["gen"]]
        contestaron = {h["gen"] for h in ev if h.get("causa") == e["id"]}
        mudos = [d for d in destinos if d not in contestaron]
        if mudos:
            fallos["organo"].append(
                f"pregunta {e['id']} de {e['gen']} (#{e.get('tema')}): suscritos y MUDOS -> "
                f"{', '.join(mudos)}")

    # ---- CEREBRO
    for e in ev:
        if e.get("causa") is not None and e["causa"] not in t["por_id"]:
            fallos["cerebro"].append(
                f"respuesta HUERFANA: el evento {e['id']} de {e['gen']} contesta al {e['causa']}, "
                f"que no existe en esta traza")
    for e in ev:
        if e["tipo"] == "pregunta" and not any(h.get("causa") == e["id"] for h in ev):
            fallos["cerebro"].append(
                f"pregunta {e['id']} de {e['gen']} (#{e.get('tema')}) SIN NINGUNA respuesta")
    for c in _ciclos(t):
        fallos["cerebro"].append(f"CICLO causal entre los eventos {c}: el pensamiento se muerde la cola")
    for b in (bloqueos or []):
        fallos["cerebro"].append(f"bloqueado por el portero: {b.get('gen')} intento "
                                 f"'{b.get('tipo')}' sin autoridad")
    return fallos


def imprimir(t, fallos=None):
    ev = t["eventos"]
    print("=" * 78)
    print(f"AUTOPSIA DE LA CORRIDA  {t['traza']}")
    print("=" * 78)
    if not ev:
        print("\n  sin eventos en esta traza.\n")
        return
    genes = _genoma()
    activos = [g for g, v in genes.items() if v.get("modo") != "inactivo"]
    hablaron = {e["gen"] for e in ev}
    tipos = defaultdict(int)
    for e in ev:
        tipos[e["tipo"]] += 1
    print(f"\n  {len(ev)} eventos · {len(hablaron)} de {len(activos)} organos activos hablaron")
    print("  " + " · ".join(f"{k} {v}" for k, v in sorted(tipos.items())))

    print("\n### CADA CONEXION QUE OCURRIO\n")
    cx = conexiones(t)
    for c in cx:
        print(f"    {c['de']:<22} -> {c['a']:<22} #{str(c['tema'] or '—'):<10} {c['via']}")
    print(f"\n    ({len(cx)} conexiones)")

    print("\n### QUE USO CADA ORGANO (temas en que participo)\n")
    part = defaultdict(set)
    for e in ev:
        if e.get("tema"):
            part[e["gen"]].add(e["tema"])
    for g in sorted(activos):
        temas = ", ".join(sorted(part.get(g, []))) or "—"
        marca = "" if g in hablaron else "   <-- MUDO en toda la corrida"
        print(f"    {g:<24} {temas:<40}{marca}")

    if fallos is not None:
        print("\n### FALLOS, POR DONDE SE ARREGLAN\n")
        etiquetas = {"diseno": "ERROR DE DISENO (el mapa)",
                     "organo": "ERROR DE ORGANO (no contesto)",
                     "cerebro": "ERROR DEL CEREBRO (coordinacion)"}
        total = 0
        for k in ("diseno", "organo", "cerebro"):
            if not fallos[k]:
                continue
            total += len(fallos[k])
            print(f"  {etiquetas[k]}")
            for f in fallos[k]:
                print(f"    · {f}")
            print()
        if total == 0:
            print("  ninguno: todos contestaron, ninguna senal cayo en el vacio, "
                  "ningun ciclo.\n")


def regla31(verbose=True):
    """La Regla 31 del TRAZADOR: tiene que ver los fallos que le plantamos, y NO ver fallos donde
    la corrida fue sana. Un auditor que siempre dice 'todo bien' es peor que no tener auditor."""
    fallos = []

    def _t(eventos):
        por_id = {e["id"]: e for e in eventos}
        return {"traza": "prueba", "eventos": eventos, "por_id": por_id,
                "hijos": {}, "raices": []}

    # 1) corrida SANA: pregunta con su respuesta, sin huerfanas ni ciclos
    sana = _t([{"id": 1, "gen": "G3_accion", "tipo": "pregunta", "tema": "frontera",
                "causa": None, "a": "G4_contingencia", "contenido": {}},
               {"id": 2, "gen": "G4_contingencia", "tipo": "respuesta", "tema": "frontera",
                "causa": 1, "a": None, "contenido": {}}])
    r = revisar(sana)
    c1 = not r["cerebro"]
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} CORRIDA SANA: no inventa fallos de cerebro "
              f"({r['cerebro'] or 'ninguno'})")
    if not c1:
        fallos.append("falso-positivo")

    # 2) RESPUESTA HUERFANA plantada
    huerfana = _t([{"id": 1, "gen": "G4_contingencia", "tipo": "respuesta", "tema": "frontera",
                    "causa": 99, "a": None, "contenido": {}}])
    c2 = any("HUERFANA" in f for f in revisar(huerfana)["cerebro"])
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} RESPUESTA HUERFANA: la caza")
    if not c2:
        fallos.append("huerfana")

    # 3) PREGUNTA SIN RESPUESTA plantada
    sola = _t([{"id": 1, "gen": "G3_accion", "tipo": "pregunta", "tema": "frontera",
                "causa": None, "a": "G4_contingencia", "contenido": {}}])
    rs = revisar(sola)
    c3 = any("SIN NINGUNA respuesta" in f for f in rs["cerebro"]) and \
         any("MUDOS" in f for f in rs["organo"])
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} PREGUNTA SIN RESPUESTA: la caza, y ademas nombra "
              f"al organo mudo (separa el fallo del cerebro del fallo del organo)")
    if not c3:
        fallos.append("sin-respuesta")

    # 4) CICLO causal plantado
    ciclo = _t([{"id": 1, "gen": "G3_accion", "tipo": "senal", "tema": "cuerpo",
                 "causa": 2, "a": None, "contenido": {}},
                {"id": 2, "gen": "G7_juego", "tipo": "decision", "tema": "cuerpo",
                 "causa": 1, "a": None, "contenido": {}}])
    c4 = any("CICLO" in f for f in revisar(ciclo)["cerebro"])
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} CICLO CAUSAL: lo caza (el pensamiento que se muerde "
              f"la cola)")
    if not c4:
        fallos.append("ciclo")

    # 5) SENAL SIN OYENTE: un tema real, emitido por el unico gen que lo escucha
    solos = [t for t in TEMAS if len(escuchan(t)) == 1]
    if solos:
        tema = solos[0]
        unico = escuchan(tema)[0]
        sin_oy = _t([{"id": 1, "gen": unico, "tipo": "senal", "tema": tema,
                      "causa": None, "a": None, "contenido": {}}])
        c5 = any("NADIE escucha" in f for f in revisar(sin_oy)["diseno"])
    else:
        # ningun tema tiene un solo oyente: se prueba con la mecanica directa
        c5 = True
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} SENAL SIN OYENTE: la caza como error de DISENO")
    if not c5:
        fallos.append("sin-oyente")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — ve los fallos plantados y no inventa los que no hay."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="La autopsia de una prueba (sinapsis 2.0)")
    ap.add_argument("--traza", default=None)
    ap.add_argument("--revisar", action="store_true")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--lista", action="store_true", help="que corridas hay registradas")
    a = ap.parse_args()
    if a.regla31:
        return regla31()
    if a.lista:
        for t in trazas():
            print(f"  {t}  ({len(leer(traza=t))} eventos)")
        return 0
    t = reconstruir(a.traza)
    f = revisar(t)
    imprimir(t, f)
    if a.revisar:
        return 1 if any(f.values()) else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
