# hito0_v2.py — LA CORRIDA OFICIAL DEL PRERREGISTRO-25 (FIRMADO): tres aparatos de ojos, el
# mismo mundo, el mismo criterio congelado. A (píxel, v1) vs B (predictivo/JEPA) vs C (descarga
# corolaria). Nulo adicional para C: entrenada con comandos desplazados, su ventaja debe morir.
# Uso: python hito0_v2.py [--episodios 12] [--pasos 1500] [--epocas 12]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

from gimnasio import correr
from contingencia import medir
from ojos_gimnasio import entrenar_ojos
import percepcion2 as p2


def evaluar(nombre, latentes, comandos, jueces):
    res = medir(list(zip(comandos, latentes)), jueces, nulos=10)
    mias = sorted(r["variable"] for r in res if r["es_mia"])
    mejor = max(r["obedece_en"] for r in res)
    print(f"\n--- {nombre}: cuerpo hallado {mias or 'ninguno'} | mejor fracción {mejor:.2f} ---",
          flush=True)
    for r in res:
        print(f"    z{r['variable']}: {r['obedece_en']:.2f} (nulo {r['nulo_techo']:.2f})"
              f"{' <- MÍA' if r['es_mia'] else ''}", flush=True)
    return {"candidata": nombre, "cuerpo": mias, "mejor_fraccion": mejor, "detalle": res}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodios", type=int, default=12)
    ap.add_argument("--pasos", type=int, default=1500)
    ap.add_argument("--epocas", type=int, default=12)
    ap.add_argument("--jueces", nargs="+", type=int, default=[10, 11, 12])
    a = ap.parse_args()
    jidx = {j - 1 for j in a.jueces}

    print(f"=== PREREG-25 — {a.episodios} ep x {a.pasos} cuadros, épocas {a.epocas} ===", flush=True)
    eps, verdad, videos = correr(a.episodios, a.pasos, "normal", render=True)
    comandos = [c for c, _ in eps]
    filas = []

    print("\n[A] ojos v1 (reconstrucción de píxel)", flush=True)
    mA = entrenar_ojos(videos, jidx, latente=8, epocas=a.epocas)
    filas.append(evaluar("A-pixel", p2.codificar(mA, videos, jidx), comandos, a.jueces))

    print("\n[B] ojos predictivos (JEPA)", flush=True)
    mB = p2.entrenar(videos, jidx, latente=8, epocas=a.epocas)
    filas.append(evaluar("B-predictivo", p2.codificar(mB, videos, jidx), comandos, a.jueces))

    print("\n[C] descarga corolaria", flush=True)
    mC = p2.entrenar(videos, jidx, latente=8, epocas=a.epocas, comandos=comandos)
    filas.append(evaluar("C-corolario", p2.codificar(mC, videos, jidx), comandos, a.jueces))

    print("\n[C-nulo] C entrenada con comandos DESPLAZADOS (prereg-25)", flush=True)
    rng = np.random.default_rng(3)
    rotos = [np.roll(u, int(rng.integers(len(u) // 4, 3 * len(u) // 4)), axis=0) for u in comandos]
    mCn = p2.entrenar(videos, jidx, latente=8, epocas=a.epocas, comandos=rotos)
    filas.append(evaluar("C-nulo", p2.codificar(mCn, videos, jidx), comandos, a.jueces))

    out = os.path.join(BASE, "resultados", "p25-hito0-v2")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump({"prerregistro": 25, "episodios": a.episodios, "pasos": a.pasos,
                   "epocas": a.epocas, "candidatas": filas,
                   "verdad_de_los_jueces": sorted(verdad)}, f, indent=2, ensure_ascii=False)
    print(f"\nguardado en {out}/resumen.json", flush=True)


if __name__ == "__main__":
    main()
