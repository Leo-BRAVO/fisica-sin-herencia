# ranuras.py — OJOS DE RANURAS: la frontera gris, construida para ser JUZGADA, no creída.
#
# QUÉ ES: una arquitectura donde la escena se reparte en K "ranuras" — K mapas de atención
# espacial (softmax sobre los píxeles) que cada uno resume su región en un puñado de números
# (dónde está su masa, cuánta hay, cómo se mueve). La literatura la llama slot attention.
#
# POR QUÉ ES GRIS, dicho sin maquillaje: "la escena se descompone en cosas separadas y
# persistentes" es un HECHO SOBRE EL MUNDO (biblioteca), no una disposición. El GENOMA declara
# que la permanencia de objeto NO se le da a Diego: debe emerger. Por eso estas ranuras:
#   - NO entran al genoma por diseño,
#   - entran al TORNEO DE LA FILOGENIA (Regla 33) como ABLACIÓN MEDIDA: Diego-con-ranuras contra
#     Diego-sin-ranuras, mismo currículo, mismos jueces. Cuánto vale ese prior es un RESULTADO
#     CIENTÍFICO — quizá el más citable del proyecto: nadie mide el precio de sus priors.
#
# Uso: python ranuras.py --regla31

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))


def construir(k_ranuras=4, canales=32):
    import torch
    import torch.nn as nn

    class OjosRanuras(nn.Module):
        def __init__(self):
            super().__init__()
            self.tronco = nn.Sequential(
                nn.Conv2d(1, 16, 4, 2, 1), nn.ReLU(),    # 32
                nn.Conv2d(16, canales, 4, 2, 1), nn.ReLU())  # 16x16
            self.atencion = nn.Conv2d(canales, k_ranuras, 1)  # un mapa por ranura
            self.k = k_ranuras
            # malla fija de coordenadas (matemática, no contenido)
            ys, xs = torch.meshgrid(torch.linspace(0, 1, 16), torch.linspace(0, 1, 16),
                                    indexing="ij")
            self.register_buffer("xs", xs.reshape(-1))
            self.register_buffer("ys", ys.reshape(-1))
            # latente por ranura: (x, y, masa) -> 3*k
            self.dinamica = nn.Linear(2 * 3 * k_ranuras, 3 * k_ranuras)
            self.dec = nn.Linear(3 * k_ranuras, 64 * 64)   # ancla débil, como en v2

        def codificar(self, x):
            import torch
            h = self.tronco(x.unsqueeze(1))                       # (B, C, 16, 16)
            a = self.atencion(h).reshape(len(x), self.k, -1)      # (B, K, 256)
            a = torch.softmax(a, dim=-1)                          # cada ranura reparte su mirada
            masa = (a * h.abs().mean(1, keepdim=True).reshape(len(x), 1, -1)).sum(-1)
            cx = (a * self.xs).sum(-1)
            cy = (a * self.ys).sum(-1)
            return torch.cat([cx, cy, masa], dim=1)               # (B, 3K)

        def decodificar(self, z):
            return self.dec(z).reshape(len(z), 64, 64)

    return OjosRanuras()


def entrenar(videos, jidx, k_ranuras=4, epocas=6, semilla=1, lote=64):
    """El mismo régimen que los ojos v2 (predicción en latente + ancla débil): lo único que
    cambia es la ARQUITECTURA. Así la comparación de la filogenia es limpia: mismo alimento,
    distinto órgano."""
    import torch
    torch.manual_seed(semilla)
    rng = np.random.default_rng(semilla)
    modelo = construir(k_ranuras)
    tren = [i for i in range(len(videos)) if i not in jidx]
    vids = {i: torch.tensor(videos[i]) for i in tren}
    trip = [(i, t) for i in tren for t in range(1, len(videos[i]) - 1)]
    opt = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    for ep in range(epocas):
        perm = rng.permutation(len(trip))
        tot = n = 0
        for a in range(0, len(perm), lote):
            idx = perm[a:a + lote]
            xa = torch.stack([vids[trip[i][0]][trip[i][1] - 1] for i in idx])
            xb = torch.stack([vids[trip[i][0]][trip[i][1]] for i in idx])
            xc = torch.stack([vids[trip[i][0]][trip[i][1] + 1] for i in idx])
            za, zb = modelo.codificar(xa), modelo.codificar(xb)
            zc = modelo.codificar(xc).detach()
            pred = ((modelo.dinamica(torch.cat([zb, za], dim=1)) - zc) ** 2).mean()
            rec = ((modelo.decodificar(zb) - xb) ** 2).mean()
            var = torch.relu(0.05 - zb.std(dim=0)).mean()
            p = pred + 0.1 * rec + 0.5 * var
            opt.zero_grad(); p.backward(); opt.step()
            tot += float(p.detach()) * len(idx); n += len(idx)
        print(f"   época {ep + 1}/{epocas} pérdida {tot / n:.5f}", flush=True)
    return modelo


def codificar(modelo, videos, jidx):
    import torch
    with torch.no_grad():
        zs = [modelo.codificar(torch.tensor(v)).numpy() for v in videos]
    tren = np.vstack([z for i, z in enumerate(zs) if i not in jidx])
    mu, sd = tren.mean(0), tren.std(0)
    sd[sd == 0] = 1.0
    return [(z - mu) / sd for z in zs]


def regla31(verbose=True, epocas=5):
    """Mundo de DOS puntos independientes sobre textura ruidosa (verdad conocida). El reclamo de
    las ranuras es exactamente 'una ranura por cosa': deben leer AMBAS posiciones mejor que los
    ojos monolíticos v2 con el mismo régimen. Si no lo logran ni aquí, no tienen nada que hacer
    en el torneo."""
    from percepcion2 import entrenar as entrenar_v2, codificar as cod_v2, _r2
    rng = np.random.default_rng(7)
    T, n_ep = 160, 8
    vids, verdad = [], []
    for _ in range(n_ep):
        p = np.array([[16.0, 16.0], [46.0, 46.0]])
        v = np.zeros((T, 64, 64), dtype=np.float32)
        tr = np.zeros((T, 4))
        for t in range(T):
            p += rng.normal(0, 1.1, (2, 2))
            p = np.clip(p, 6, 57)
            cuadro = rng.uniform(0.3, 0.7, (64, 64)).astype(np.float32)
            for (x, y) in p:
                cuadro[int(y) - 3:int(y) + 3, int(x) - 3:int(x) + 3] = 1.0
            v[t] = cuadro
            tr[t] = p.reshape(-1)
        vids.append(v); verdad.append(tr)
    jidx = {6, 7}
    tren = [i for i in range(n_ep) if i not in jidx]; test = sorted(jidx)

    mV2 = entrenar_v2(vids, jidx, latente=12, epocas=epocas)
    rV2 = _r2(cod_v2(mV2, vids, jidx), verdad, tren, test)
    mR = entrenar(vids, jidx, k_ranuras=4, epocas=epocas)
    rR = _r2(codificar(mR, vids, jidx), verdad, tren, test)
    ok_ = rR > rV2 + 0.05
    if verbose:
        print(f"  {'ok  ' if ok_ else 'FALLO'} DOS PUNTOS: ranuras R² {rR:+.3f} vs monolítico "
              f"{rV2:+.3f} — una ranura por cosa, o nada")
        print("\nREGLA 31: " + ("APRUEBA — las ranuras ganan su derecho a ENTRAR AL TORNEO "
                                "(no al genoma)." if ok_ else
                                "REPRUEBA — sin ventaja ni en su mundo ideal, no van al torneo."))
    return 0 if ok_ else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Ojos de ranuras: candidata GRIS para la filogenia")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--epocas", type=int, default=5)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31(epocas=a.epocas))
    print("uso: --regla31 (su veredicto real lo da el torneo de la Regla 33)")
