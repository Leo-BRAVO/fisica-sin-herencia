# conectoma.py — Regla 29: el tejido que conecta el árbol (idea del director, 12-jul-2026).
# Genera arbol/CONECTOMA.json: registro LEGIBLE POR MÁQUINA de todo el conocimiento validado —
# cada nodo con su mejor ley, su representación, sus constantes canónicas y su procedencia —
# para que TODA campaña futura lo consulte automáticamente: leyes compatibles entran como
# rivales del árbol y candidatas a herencia sin que nadie tenga que acordarse.
# Solo conocimiento PROPIO (el cortafuegos intacto).

import os
import re
import json
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# nodo -> (carpeta de resultados con sus semillas, nº de señales de su representación)
# AUDITORIA TOTAL 8-ago-2026: este diccionario se habia quedado en el 12-jul y le faltaban
# DOS nodos vivos (N-003-E2 y N-004-E2) — la Regla 29 dice "la mente ve TODAS sus hojas" y
# no las veia. Toda alta de nodo DEBE agregarse aqui; coherencia.py ahora lo verifica.
FUENTES = {
    "N-001-E2 (Mendeley, retardos)": ("resultados/e2-mendeley-i2", 2),
    "N-002-E2 (dp Morpheus, latentes propios)": ("resultados/p13-latente", 8),
    "N-003-E2 (ojos autoelegidos, latente 4 — primera automejora)": ("resultados/p14-final", 4),
    "epoca1/N-001 (Mendeley angulos — archivado, confianza retirada)": ("resultados/oficial-trial1", 2),
    "epoca1/caida (observacion, firma vertical)": ("resultados/caida-libre-p09", 2),
    "epoca1/dp centroides (sin nodo, mejor ley disponible)": ("resultados/e2-dp-morpheus", 4),
}

# Nodos que NO nacen de semillas simbolicas (otra clase de ley): se tejen aparte para que
# la mente los vea igual. N-004-E2 es una cantidad CONSERVADA (herramienta F3).
FUENTES_CONSERVADAS = {
    "N-004-E2 (caida — cantidad conservada, verdugo surrogado)": "resultados/conservadas-caida_aud01",
}


def mejor_semilla(carpeta):
    fs = [f for f in glob.glob(os.path.join(BASE, carpeta, "semilla_*.json"))
          if re.fullmatch(r"semilla_\d+\.json", os.path.basename(f))]
    if not fs:
        return None
    return min(fs, key=lambda p: json.load(open(p)).get("mse_total", float("inf")))


def main():
    import datetime as _dt  # solo para fechar el tejido (no entra a ninguna decision)
    conectoma = {"generado": _dt.date.today().isoformat(), "nodos": {}}
    for nombre, (carpeta, n_sig) in FUENTES.items():
        f = mejor_semilla(carpeta)
        if not f:
            continue
        r = json.load(open(f))
        leyes = {k: v["ecuacion"] for k, v in r.items() if k != "mse_total"}
        constantes = sorted({round(abs(float(c)), 5)
                             for eq in leyes.values()
                             for c in re.findall(r"-?\d+\.\d+", eq)})
        conectoma["nodos"][nombre] = {
            "semilla": os.path.relpath(f, BASE), "n_senales": n_sig,
            "mse_total": r["mse_total"], "leyes": leyes, "constantes": constantes}
    # tejer las conservadas (Regla 29: TODAS sus hojas, sea cual sea su forma)
    for nombre, carpeta in FUENTES_CONSERVADAS.items():
        ruta = os.path.join(BASE, carpeta, "resumen.json")
        if not os.path.exists(ruta):
            continue
        r = json.load(open(ruta, encoding="utf-8"))
        validadas = [v for v in r.get("validacion_jueces", [])
                     if sum(1 for x in v["ratios_jueces"].values() if x < 0.2) >= 2]
        if not validadas:
            continue
        mejor = min(validadas, key=lambda v: v["score"])
        conectoma["nodos"][nombre] = {
            "tipo": "cantidad_conservada", "fuente": os.path.join(carpeta, "resumen.json"),
            "nulo": r.get("nulo"), "score": mejor["score"], "expresion": mejor["expresion"],
            "ratios_jueces": mejor["ratios_jueces"]}

    salida = os.path.join(BASE, "arbol", "CONECTOMA.json")
    with open(salida, "w") as f:
        json.dump(conectoma, f, indent=2)
    print(f"Conectoma: {len(conectoma['nodos'])} nodos tejidos -> {salida}")
    for n, v in conectoma["nodos"].items():
        if v.get("tipo") == "cantidad_conservada":
            print(f"  {n} | conservada (nulo {v['nulo']}) | score {v['score']:.4g}")
        else:
            print(f"  {n} | {v['n_senales']} señales | constantes: {v['constantes'][:6]}")


if __name__ == "__main__":
    main()
