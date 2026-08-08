# ojos_ganados.py — PRERREGISTRO-21: los ojos que se GANAN su dimension.
#
# La idea que nadie usa: los laboratorios eligen la dimension de una representacion por error de
# RECONSTRUCCION o de PREDICCION — y la textura satisface AMBOS (INFORME-27: los ojos de Diego
# predecian al 72% con ganancia honesta de -0.1%). Aqui la dimension no se elige: SE GANA.
#
#     GANANCIA_HONESTA(d) = reduccion(datos reales) - reduccion(datos surrogados)
#
# medida SOBRE LOS JUECES CONGELADOS. Gana la d cuyo poder la textura NO puede explicar.
#
# Protocolo (identico a N-002-E2 salvo la dimension, para que la comparacion sea limpia):
# ojos desde cero por candidata, misma semilla, mismas epocas, misma perdida conjunta
# (reconstruccion + dinamica), estandarizacion con estadisticas SOLO de entrenamiento,
# jueces 3/6/9 congelados e invisibles a todo el proceso.
#
# Uso: python ojos_ganados.py <carpeta_videos> [--dims 2 3 4 6 8] [--epocas 15] [--jueces 3 6 9]

import os
import sys
import csv
import json
import glob
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))
from ganancia_honesta import medir


def entrenar_ojos(videos_t, nombres, jidx, latente, epocas, semilla=1):
    """Entrena unos ojos desde cero (protocolo de percepcion.py, prereg-13) y devuelve el
    modelo. Los jueces NO participan del entrenamiento — la muralla de siempre."""
    import torch
    from percepcion import Ojos
    torch.manual_seed(semilla)
    np.random.seed(semilla)

    tripletas = [(i, t) for i, v in enumerate(videos_t) if i not in jidx
                 for t in range(1, len(v) - 1)]
    modelo = Ojos(latente)
    opt = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    for ep in range(epocas):
        perm = np.random.permutation(len(tripletas))
        tot, n = 0.0, 0
        for lote0 in range(0, len(perm), 128):
            idx = perm[lote0:lote0 + 128]
            xa = torch.stack([videos_t[tripletas[i][0]][tripletas[i][1] - 1] for i in idx])
            xb = torch.stack([videos_t[tripletas[i][0]][tripletas[i][1]] for i in idx])
            xc = torch.stack([videos_t[tripletas[i][0]][tripletas[i][1] + 1] for i in idx])
            za, zb, zc = modelo.codificar(xa), modelo.codificar(xb), modelo.codificar(xc)
            rec = ((modelo.decodificar(zb) - xb) ** 2).mean()
            din = ((modelo.dinamica(torch.cat([zb, za], dim=1)) - zc) ** 2).mean()
            p = rec + din
            opt.zero_grad(); p.backward(); opt.step()
            tot += float(p) * len(idx); n += len(idx)
        print(f"   d={latente} epoca {ep+1}/{epocas} perdida {tot/n:.5f}", flush=True)
    return modelo


def latentes_a_csv(modelo, videos_t, nombres, destino, jidx, latente):
    """Codifica y estandariza con estadisticas SOLO del entrenamiento (como estandarizar.py)."""
    import torch
    import pandas as pd
    crudo = destino + "_crudo"
    os.makedirs(crudo, exist_ok=True); os.makedirs(destino, exist_ok=True)
    with torch.no_grad():
        for n, v in zip(nombres, videos_t):
            z = modelo.codificar(v).numpy()
            with open(os.path.join(crudo, f"{n}.csv"), "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["t"] + [f"s{k+1}" for k in range(latente)])
                for t in range(len(z)):
                    w.writerow([t] + [round(float(x), 6) for x in z[t]])
    csvs = sorted(glob.glob(os.path.join(crudo, "*.csv")))
    cols = [c for c in pd.read_csv(csvs[0]).columns if c.startswith("s")]
    tren = pd.concat([pd.read_csv(c)[cols] for i, c in enumerate(csvs) if i not in jidx])
    mu, sd = tren.mean(), tren.std().replace(0, 1)
    for c in csvs:
        df = pd.read_csv(c); df[cols] = (df[cols] - mu) / sd
        df.to_csv(os.path.join(destino, os.path.basename(c)), index=False)
    import shutil
    shutil.rmtree(crudo)
    return destino


def main():
    ap = argparse.ArgumentParser(description="Prereg-21: la dimension se gana, no se elige")
    ap.add_argument("videos", help="carpeta con <video>/cropped_video.mp4")
    ap.add_argument("--dims", nargs="+", type=int, default=[2, 3, 4, 6, 8])
    ap.add_argument("--epocas", type=int, default=15)
    ap.add_argument("--jueces", nargs="+", type=int, default=[3, 6, 9])
    ap.add_argument("--trabajo", default=None, help="carpeta temporal para los latentes")
    args = ap.parse_args()

    import torch
    from percepcion import cargar_video
    mp4s = sorted(glob.glob(os.path.join(args.videos, "*", "cropped_video.mp4")))
    if not mp4s:
        raise SystemExit(f"sin videos en {args.videos}")
    nombres = [os.path.basename(os.path.dirname(m)) for m in mp4s]
    videos_t = [torch.tensor(cargar_video(m)) for m in mp4s]
    jidx = {j - 1 for j in args.jueces}
    trabajo = args.trabajo or os.path.join(BASE, "resultados", "_ojos_ganados_tmp")
    print(f"{len(videos_t)} videos | jueces congelados: {[nombres[i] for i in sorted(jidx)]}", flush=True)

    filas = []
    for d in args.dims:
        print(f"\n=== candidata d={d} ===", flush=True)
        modelo = entrenar_ojos(videos_t, nombres, jidx, d, args.epocas)
        carpeta = latentes_a_csv(modelo, videos_t, nombres, os.path.join(trabajo, f"d{d}"), jidx, d)
        g = medir(carpeta, args.jueces)
        g["dimension"] = d
        filas.append(g)
        print(f"   d={d}: reduccion real {g['reduccion_real']:.4f} | falsa {g['reduccion_falsa']:.4f} "
              f"| GANANCIA HONESTA {g['ganancia_honesta']:+.4f}", flush=True)

    filas.sort(key=lambda r: -r["ganancia_honesta"])
    outdir = os.path.join(BASE, "resultados", "p21-ojos-ganados")
    os.makedirs(outdir, exist_ok=True)
    ganadora = filas[0]
    mejor = ganadora["ganancia_honesta"]
    todas = [r["ganancia_honesta"] for r in filas]
    # VEREDICTO ESTRICTAMENTE SEGUN EL PRERREGISTRO-21 — nada de reglas post-hoc.
    # CORRECCION 8-ago-2026: la primera version de este codigo declaraba "prediccion 2" en cuanto
    # nadie superaba 0.10, pero la prediccion 2 exige que TODAS esten por debajo de 0.05. Entre
    # 0.05 y 0.10 el prerregistro NO PREDIJO NADA: es una banda descubierta, y lo honesto es
    # decirlo, no inventar una regla que declare victoria o derrota a conveniencia.
    if mejor > 0.10:
        veredicto = (f"PREDICCION 1: existe dinamica capturable — gana d={ganadora['dimension']} "
                     f"con ganancia honesta {mejor:+.4f}")
    elif all(g < 0.05 for g in todas):
        veredicto = ("PREDICCION 2: ninguna dimension llega a 0.05 — la certificacion predictiva "
                     "de N-002-E2 y N-003-E2 se degrada formalmente a estructural")
    else:
        veredicto = (f"INCONCLUSO: el mejor resultado ({mejor:+.4f}) cae en la BANDA DESCUBIERTA "
                     f"del prerregistro-21 (0.05 a 0.10) — ni la prediccion 1 ni la 2 aplican. "
                     f"El prerregistro tenia un hueco y se registra como tal; no se declara "
                     f"veredicto sobre los nodos")
    with open(os.path.join(outdir, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump({"prerregistro": 21, "jueces": args.jueces, "epocas": args.epocas,
                   "candidatas": filas, "ganadora": ganadora, "veredicto": veredicto}, f, indent=2,
                  ensure_ascii=False)

    print("\n" + "=" * 72)
    print(f"{'d':>3} {'red. real':>11} {'red. falsa':>11} {'GANANCIA HONESTA':>18}")
    for r in sorted(filas, key=lambda r: r["dimension"]):
        print(f"{r['dimension']:>3} {r['reduccion_real']:>11.4f} {r['reduccion_falsa']:>11.4f} "
              f"{r['ganancia_honesta']:>+18.4f}")
    print("=" * 72)
    print("VEREDICTO:", veredicto)
    print("guardado en", os.path.join(outdir, "resumen.json"))


if __name__ == "__main__":
    main()
