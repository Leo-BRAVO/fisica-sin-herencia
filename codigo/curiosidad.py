# curiosidad.py — LA CURIOSIDAD PROPIA DE LA MENTE (orden del director, 12-jul-2026).
# ELLA propone sus proximas campanas: lee su memoria, encuentra sus huecos (donde su mejor
# esfuerzo quedo lejos de resolver) y escribe propuestas en registros/COLA-ESTUDIOS.json.
# Aprobacion permanente del director: RE-ANALISIS sobre datos ya aprobados se ejecutan solos;
# todo lo que implique DATOS NUEVOS queda como "espera-al-director".
# Uso:  python curiosidad.py --proponer      python curiosidad.py --siguiente
#       python curiosidad.py --completar <id>

import os
import json
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(BASE, "arbol", "MEMORIA-MENTE.jsonl")
COLA = os.path.join(BASE, "registros", "COLA-ESTUDIOS.json")

# recetas de re-analisis que la mente puede pedirse a si misma (datos ya aprobados)
RECETAS = {
    "e2-dp-morpheus": {"datos": "datos/procesados/dp_morpheus", "jueces": "3 6 9",
                       "extra": "--suavizar 3 --retardos 2 --maxsize 25 --niter 800"},
    "p13-latente": {"datos": "datos/procesados/dp_latente_std", "jueces": "3 6 9",
                    "extra": "--maxsize 25 --niter 800"},
    "e2-caida-i2": {"datos": "datos/procesados/caida", "jueces": "3 7 11",
                    "extra": "--suavizar 3 --retardos 0 --maxsize 12 --niter 800"},
}


def cargar_cola():
    return json.load(open(COLA, encoding="utf-8")) if os.path.exists(COLA) else {"items": []}


def guardar_cola(c):
    with open(COLA, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)


def proponer():
    if not os.path.exists(MEM):
        print("sin memoria; nada que proponer"); return
    recuerdos = [json.loads(l) for l in open(MEM, encoding="utf-8") if l.strip()]
    # su criterio: donde quedo hueco (mejora < 50%) y tiene receta para reintentar mas fuerte
    huecos = [r for r in recuerdos if r.get("hueco") and r["campana"] in RECETAS]
    huecos.sort(key=lambda r: (r.get("cuanto_mejore") or 0))  # peor primero: mas curiosidad
    cola = cargar_cola()
    existentes = {i["id"] for i in cola["items"]}
    n = 0
    for h in huecos[:2]:
        iid = f"mente-reintento-{h['campana']}"
        if iid in existentes:
            continue
        rec = RECETAS[h["campana"]]
        cola["items"].append({
            "id": iid, "origen": "PROPUESTA DE LA MENTE (curiosidad.py)",
            "motivo_suyo": f"hueco: solo mejore {h.get('cuanto_mejore')} en {h['campana']}",
            "tipo": "re-analisis", "estado": "pendiente",
            "datos": rec["datos"], "salida": f"resultados/{iid}",
            "args": f"--semillas 5 --paralelo 5 {rec['extra']} --jueces {rec['jueces']}"})
        n += 1
    guardar_cola(cola)
    print(f"propuestas nuevas de la mente: {n} | cola total: {len(cola['items'])}")


def siguiente():
    cola = cargar_cola()
    for i in cola["items"]:
        if i["estado"] == "pendiente" and i["tipo"] == "re-analisis":
            print(json.dumps(i, ensure_ascii=False)); return
    print("{}")


def completar(iid):
    cola = cargar_cola()
    for i in cola["items"]:
        if i["id"] == iid:
            i["estado"] = "hecha"
    guardar_cola(cola)
    print("completada:", iid)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--proponer", action="store_true")
    ap.add_argument("--siguiente", action="store_true")
    ap.add_argument("--completar", default=None)
    a = ap.parse_args()
    if a.proponer:
        proponer()
    if a.siguiente:
        siguiente()
    if a.completar:
        completar(a.completar)
