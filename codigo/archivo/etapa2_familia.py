# etapa2_familia.py — Etapa 2 del prerregistro-07: buscar la ley de la familia.
# Tabla (longitud → constante descubierta) y regresión simbólica sobre la tabla,
# con 3 longitudes jueces fuera de muestra (posiciones 3, 8, 12 de la lista ordenada, 1-indexado).
#
# Definición NEUTRA y uniforme de "la constante" de cada sistema (documentada aquí antes de correr):
# las ecuaciones descubiertas tienen formas algebraicas diversas; para compararlas se usa la
# linealización local del mapa descubierto en el origen: a = ∂f/∂v1 evaluada en (0,0), por
# diferencias centrales. Para la forma pura (v1+v2)*c esto devuelve exactamente c (el factor
# de pérdida). Es una operación matemática genérica, no física (Regla 1).

import os
import json

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(BASE, "resultados", "familia")


def evaluar(eq, v1, v2):
    ns = {"v1": np.array([v1]), "v2": np.array([v2]),
          "sin": np.sin, "cos": np.cos, "exp": np.exp, "sqrt": np.sqrt,
          "square": lambda x: x * x}
    return float(eval(eq, {"__builtins__": {}}, ns)[0])


def constante_de(eq, h=1e-4):
    return (evaluar(eq, h, 0.0) - evaluar(eq, -h, 0.0)) / (2 * h)


def main():
    familia = json.load(open(os.path.join(RES, "familia_resumen.json")))

    # Corrección de etiquetas documentada: los archivos réplica 63.3_v1 / 63.3_v2 fueron
    # etiquetados 1.0 / 2.0 por el error de regex cazado el 10-jul-2026 (commit 8d5657a).
    for nombre, v in familia.items():
        if "63.3" in nombre and v["longitud_cm"] in (1.0, 2.0):
            v["longitud_cm"] = 63.3

    filas = []
    for nombre, v in familia.items():
        mejor = min(v["semillas"].values(), key=lambda s: s["mse_total"])
        try:
            a = constante_de(mejor["ecuacion"])
        except Exception as e:
            print(f"[{nombre}] ecuación no evaluable ({e}) — se excluye, documentado")
            continue
        filas.append({"sistema": nombre, "L": v["longitud_cm"], "constante": a,
                      "ecuacion": mejor["ecuacion"], "mse": mejor["mse_total"]})

    filas.sort(key=lambda f: (f["L"], f["sistema"]))
    print("Tabla de la familia (ordenada por longitud):")
    for i, f in enumerate(filas, 1):
        print(f"  {i:2d}. L={f['L']:5.1f} cm  constante={f['constante']:.5f}  ({f['sistema']})")

    jueces_idx = [2, 7, 11]  # posiciones 3, 8, 12 (1-indexado) — fijadas en prereg-07
    jueces = [filas[i] for i in jueces_idx]
    entren = [f for i, f in enumerate(filas) if i not in jueces_idx]
    print(f"\nJueces fuera de muestra: " + ", ".join(f"L={j['L']}cm" for j in jueces))

    X = np.array([[f["L"]] for f in entren])
    y = np.array([f["constante"] for f in entren])

    from pysr import PySRRegressor
    modelo = PySRRegressor(niterations=200, binary_operators=["+", "-", "*", "/"],
                           unary_operators=["sin", "cos", "exp", "sqrt", "square"],
                           maxsize=15, random_state=1, deterministic=True,
                           parallelism="serial", progress=False, temp_equation_file=True)
    modelo.fit(X, y, variable_names=["L"])
    ley = str(modelo.get_best()["equation"])
    print(f"\nLey candidata de la familia: constante = {ley}")

    errores = []
    for j in jueces:
        pred = float(modelo.predict(np.array([[j["L"]]]))[0])
        err = abs(pred - j["constante"]) / abs(j["constante"])
        errores.append(err)
        print(f"  Juez L={j['L']}cm: real={j['constante']:.5f} predicho={pred:.5f} error={err*100:.2f}%")

    exito = all(e < 0.10 for e in errores)
    print(f"\nVEREDICTO prerregistrado (<10% en los 3 jueces): {'EXITO' if exito else 'FRACASO'}")

    with open(os.path.join(RES, "etapa2.json"), "w") as f:
        json.dump({"tabla": filas, "jueces": [j["sistema"] for j in jueces], "ley": ley,
                   "errores_jueces": errores, "exito": exito}, f, indent=2)


if __name__ == "__main__":
    main()
