# selector14.py — seleccion INTERNA del bucle (prereg-14): mejor proporcion mse/base
# sobre los jueces internos. Imprime SOLO la dimension ganadora en la ultima linea.
import json
import sys

base = sys.argv[1]
mejor, ratio = None, 9e9
for d in (4, 8, 12):
    r = json.load(open(rf"{base}\resultados\p14-inner-d{d}\resumen.json"))
    rat = min(s["mse_total"] for s in r["semillas"].values()) / r["mse_base"]
    print(f"latente {d}: proporcion {rat:.4f}")
    if rat < ratio:
        mejor, ratio = d, rat
print(mejor)
