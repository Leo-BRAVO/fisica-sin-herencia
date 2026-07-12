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
FUENTES = {
    "N-001-E2 (Mendeley, retardos)": ("resultados/e2-mendeley-i2", 2),
    "N-002-E2 (dp Morpheus, latentes propios)": ("resultados/p13-latente", 8),
    "epoca1/N-001 (Mendeley angulos — archivado, confianza retirada)": ("resultados/oficial-trial1", 2),
    "epoca1/caida (observacion, firma vertical)": ("resultados/caida-libre-p09", 2),
    "epoca1/dp centroides (sin nodo, mejor ley disponible)": ("resultados/e2-dp-morpheus", 4),
}


def mejor_semilla(carpeta):
    fs = [f for f in glob.glob(os.path.join(BASE, carpeta, "semilla_*.json"))
          if re.fullmatch(r"semilla_\d+\.json", os.path.basename(f))]
    if not fs:
        return None
    return min(fs, key=lambda p: json.load(open(p)).get("mse_total", float("inf")))


def main():
    conectoma = {"generado": "2026-07-12", "nodos": {}}
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
    salida = os.path.join(BASE, "arbol", "CONECTOMA.json")
    with open(salida, "w") as f:
        json.dump(conectoma, f, indent=2)
    print(f"Conectoma: {len(conectoma['nodos'])} nodos tejidos -> {salida}")
    for n, v in conectoma["nodos"].items():
        print(f"  {n} | {v['n_senales']} señales | constantes: {v['constantes'][:6]}")


if __name__ == "__main__":
    main()
