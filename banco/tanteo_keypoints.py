# TANTEO DEL BANCO — NO ES EVIDENCIA. Carril rapido (banco.py).
# Pregunta: ¿la perdida por pixel produce latentes que NO son coordenadas, y un cuello de botella
# de softmax espacial si lo hace? Se compara sobre una escena con la verdad conocida POR NOSOTROS.
# LA VERDAD SOLO SE USA PARA EVALUAR, NUNCA PARA ENTRENAR: entrenar contra ella seria darle la
# respuesta, y ademas no mediria nada.
import os, sys, json
import numpy as np, torch, torch.nn as nn
sys.path.insert(0, "/home/user/fisica-sin-herencia/codigo")
import banco

T, N = 600, 32
SEMILLAS = (211, 223)          # nuevas: quedan QUEMADAS por tantear con ellas


def escena(semilla=211):
    """Fondo estatico con textura + un objeto PEQUEÑO que se mueve. La verdad la ponemos nosotros."""
    rng = np.random.default_rng(semilla)
    fondo = rng.normal(0.5, 0.15, (N, N)).astype(np.float32)      # >90% de los pixeles
    t = np.arange(T) * 0.05
    cx = (N / 2 + 8 * np.cos(0.9 * t)).astype(int).clip(2, N - 3)
    cy = (N / 2 + 8 * np.sin(0.9 * t)).astype(int).clip(2, N - 3)
    vids = np.tile(fondo, (T, 1, 1))
    yy, xx = np.mgrid[0:N, 0:N]
    for i in range(T):
        vids[i][(yy - cy[i]) ** 2 + (xx - cx[i]) ** 2 <= 4] = 1.0   # el objeto: ~13 px de 1024
    return vids[:, None, :, :], np.stack([cx, cy], 1).astype(np.float32)


class Pixel(nn.Module):
    """El de hoy: convolucional -> latente plano -> reconstruir TODA la imagen."""
    def __init__(s, d=8):
        super().__init__()
        s.e = nn.Sequential(nn.Conv2d(1, 16, 3, 2, 1), nn.ReLU(), nn.Conv2d(16, 32, 3, 2, 1),
                            nn.ReLU(), nn.Flatten(), nn.Linear(32 * 8 * 8, d))
        s.d = nn.Sequential(nn.Linear(d, 32 * 8 * 8), nn.ReLU(), nn.Unflatten(1, (32, 8, 8)),
                            nn.ConvTranspose2d(32, 16, 4, 2, 1), nn.ReLU(),
                            nn.ConvTranspose2d(16, 1, 4, 2, 1))
    def z(s, x): return s.e(x)
    def forward(s, x): return s.d(s.e(x))


class Keypoint(nn.Module):
    """SOFTMAX ESPACIAL: el cuello de botella son PUNTOS (x,y), no numeros sueltos."""
    def __init__(s, k=2):
        super().__init__()
        s.k = k
        s.f = nn.Sequential(nn.Conv2d(1, 16, 3, 2, 1), nn.ReLU(), nn.Conv2d(16, k, 3, 2, 1))
        s.d = nn.Sequential(nn.Linear(2 * k, 32 * 8 * 8), nn.ReLU(), nn.Unflatten(1, (32, 8, 8)),
                            nn.ConvTranspose2d(32, 16, 4, 2, 1), nn.ReLU(),
                            nn.ConvTranspose2d(16, 1, 4, 2, 1))
    def z(s, x):
        m = s.f(x)                                   # (B,k,h,w)
        B, k, h, w = m.shape
        p = torch.softmax(m.reshape(B, k, -1), -1).reshape(B, k, h, w)
        gx = torch.linspace(-1, 1, w, device=x.device)
        gy = torch.linspace(-1, 1, h, device=x.device)
        return torch.cat([(p.sum(2) * gx).sum(-1), (p.sum(3) * gy).sum(-1)], 1)
    def forward(s, x): return s.d(s.z(x))


def entrenar(modelo, X, epocas=25, semilla=211):
    torch.manual_seed(semilla)
    opt = torch.optim.Adam(modelo.parameters(), lr=2e-3)
    for _ in range(epocas):
        for i in range(0, len(X), 64):
            xb = X[i:i + 64]
            p = ((modelo(xb) - xb) ** 2).mean()       # LA MISMA perdida por pixel en los dos
            opt.zero_grad(); p.backward(); opt.step()
    return modelo


def r2_posicion(Z, verdad):
    """¿Cuanto de la posicion VERDADERA se recupera linealmente del latente? Es la pregunta
    entera: un latente que es coordenada da r2 alto; uno que es mezcla de textura, no."""
    A = np.column_stack([Z, np.ones(len(Z))])
    c = int(len(Z) * 0.7)
    w, *_ = np.linalg.lstsq(A[:c], verdad[:c], rcond=None)
    pred, y = A[c:] @ w, verdad[c:]
    ss = ((y - y.mean(0)) ** 2).sum()
    return float(1 - ((y - pred) ** 2).sum() / ss) if ss > 0 else 0.0


out = {}
for sem in SEMILLAS:
    vids, verdad = escena(sem)
    X = torch.tensor(vids)
    for nombre, M in (("pixel_mse", Pixel()), ("keypoint_softmax", Keypoint())):
        m = entrenar(M, X, semilla=sem)
        with torch.no_grad():
            Z = m.z(X).numpy()
        out.setdefault(nombre, []).append(round(r2_posicion(Z, verdad), 4))
out["que_mide"] = "r2 fuera de muestra de la POSICION VERDADERA recuperada del latente"
out["verdad_solo_para_evaluar"] = "nunca se uso para entrenar: los dos usan la misma perdida por pixel"
print(json.dumps(out, indent=1, ensure_ascii=False))
banco.escribir("keypoints/tanteo.json", out, semillas=SEMILLAS,
               que_se_tanteaba="perdida por pixel contra cuello de botella de softmax espacial")
