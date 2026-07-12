# percepcion.py — PELDAÑO 2b: Percepción Pura (prerregistro-13)
# Autoencoder entrenado DESDE CERO, solo con cuadros de nuestros videos (regla de pureza:
# jamás modelos pre-entrenados), con pérdida CONJUNTA (lección de la auditoría):
#   reconstrucción + dinámica simple en el latente (un predictor lineal z_t,z_{t-1} -> z_{t+1}
#   entrenado a la par: las variables se aprenden PORQUE hacen predecible la ley).
# Salida: trayectorias latentes por video (CSV s1..sN neutros) para el motor simbólico.
# Uso: python percepcion.py <carpeta_videos_mp4> <carpeta_salida> [--latente 8] [--epocas 15] [--jueces 3 6 9]

import os
import sys
import json
import glob
import argparse

import numpy as np
import cv2
import torch
import torch.nn as nn

torch.manual_seed(1)
np.random.seed(1)

TAM = 64  # lado de la imagen de trabajo


def cargar_video(mp4):
    cap = cv2.VideoCapture(mp4)
    cuadros = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        g = cv2.resize(g, (TAM, TAM), interpolation=cv2.INTER_AREA)
        cuadros.append(g.astype(np.float32) / 255.0)
    cap.release()
    return np.stack(cuadros)  # (T, 64, 64)


class Ojos(nn.Module):
    def __init__(self, latente):
        super().__init__()
        self.enc = nn.Sequential(
            nn.Conv2d(1, 16, 4, 2, 1), nn.ReLU(),   # 32
            nn.Conv2d(16, 32, 4, 2, 1), nn.ReLU(),  # 16
            nn.Conv2d(32, 64, 4, 2, 1), nn.ReLU(),  # 8
            nn.Flatten(), nn.Linear(64 * 8 * 8, latente))
        self.dec_fc = nn.Linear(latente, 64 * 8 * 8)
        self.dec = nn.Sequential(
            nn.ConvTranspose2d(64, 32, 4, 2, 1), nn.ReLU(),
            nn.ConvTranspose2d(32, 16, 4, 2, 1), nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 4, 2, 1), nn.Sigmoid())
        self.dinamica = nn.Linear(2 * latente, latente)  # z(t), z(t-1) -> z(t+1)

    def codificar(self, x):
        return self.enc(x.unsqueeze(1))

    def decodificar(self, z):
        h = self.dec_fc(z).view(-1, 64, 8, 8)
        return self.dec(h).squeeze(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("salida")
    ap.add_argument("--latente", type=int, default=8)
    ap.add_argument("--epocas", type=int, default=15)
    ap.add_argument("--jueces", nargs="+", type=int, default=[3, 6, 9])
    args = ap.parse_args()
    os.makedirs(args.salida, exist_ok=True)

    mp4s = sorted(glob.glob(os.path.join(args.carpeta, "*", "cropped_video.mp4")))
    nombres = [os.path.basename(os.path.dirname(m)) for m in mp4s]
    jidx = {j - 1 for j in args.jueces}
    videos = [cargar_video(m) for m in mp4s]
    print(f"{len(videos)} videos | jueces: {[nombres[i] for i in sorted(jidx)]}", flush=True)

    # tripletas (t-1, t, t+1) SOLO de videos de entrenamiento
    tripletas = []
    for i, v in enumerate(videos):
        if i in jidx:
            continue
        for t in range(1, len(v) - 1):
            tripletas.append((i, t))
    vt = [torch.tensor(v) for v in videos]

    modelo = Ojos(args.latente)
    opt = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    registro = []
    for ep in range(args.epocas):
        perm = np.random.permutation(len(tripletas))
        tot_r, tot_d, n = 0.0, 0.0, 0
        for lote0 in range(0, len(perm), 128):
            idx = perm[lote0:lote0 + 128]
            xa = torch.stack([vt[tripletas[i][0]][tripletas[i][1] - 1] for i in idx])
            xb = torch.stack([vt[tripletas[i][0]][tripletas[i][1]] for i in idx])
            xc = torch.stack([vt[tripletas[i][0]][tripletas[i][1] + 1] for i in idx])
            za, zb, zc = modelo.codificar(xa), modelo.codificar(xb), modelo.codificar(xc)
            rec = ((modelo.decodificar(zb) - xb) ** 2).mean()
            zpred = modelo.dinamica(torch.cat([zb, za], dim=1))
            din = ((zpred - zc) ** 2).mean()
            perdida = rec + din
            opt.zero_grad(); perdida.backward(); opt.step()
            tot_r += float(rec) * len(idx); tot_d += float(din) * len(idx); n += len(idx)
        registro.append({"epoca": ep + 1, "reconstruccion": tot_r / n, "dinamica": tot_d / n})
        print(f"época {ep+1}/{args.epocas} | reconstrucción {tot_r/n:.5f} | dinámica {tot_d/n:.5f}", flush=True)

    # evaluación en jueces (reconstrucción de videos jamás vistos)
    with torch.no_grad():
        rec_jueces = {}
        for i in sorted(jidx):
            z = modelo.codificar(vt[i])
            rec = float(((modelo.decodificar(z) - vt[i]) ** 2).mean())
            rec_jueces[nombres[i]] = rec
        # trayectorias latentes de TODOS los videos (para el motor simbólico)
        for i, v in enumerate(vt):
            z = modelo.codificar(v).numpy()
            import csv as _csv
            with open(os.path.join(args.salida, f"{nombres[i]}.csv"), "w", newline="") as f:
                w = _csv.writer(f)
                w.writerow(["t"] + [f"s{k+1}" for k in range(args.latente)])
                for t in range(len(z)):
                    w.writerow([t] + [round(float(x), 6) for x in z[t]])

    torch.save(modelo.state_dict(), os.path.join(args.salida, "ojos.pt"))
    with open(os.path.join(args.salida, "entrenamiento.json"), "w") as f:
        json.dump({"registro": registro, "reconstruccion_jueces": rec_jueces,
                   "latente": args.latente, "videos": nombres}, f, indent=2)
    print("Reconstrucción en jueces:", {k: round(v, 5) for k, v in rec_jueces.items()}, flush=True)
    print("Ojos y trayectorias latentes guardados en", args.salida, flush=True)


if __name__ == "__main__":
    main()
