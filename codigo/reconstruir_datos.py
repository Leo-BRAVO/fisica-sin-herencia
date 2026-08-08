# reconstruir_datos.py — EL PROYECTO YA NO DEPENDE DE NINGUNA MAQUINA (INFORME-22, 8-ago-2026).
# Reconstruye los datos procesados desde sus FUENTES PUBLICAS originales y VERIFICA por huella
# digital que la reconstruccion es identica a la historica: la base trivial recalculada debe
# coincidir con el numero registrado en el resumen de la campana insignia de ese mundo.
# Es la Regla 14 (replicabilidad) hecha ejecutable: cualquiera, en cualquier maquina, reproduce.
#
# Uso: python reconstruir_datos.py mendeley_epoca2 [destino]
#      python reconstruir_datos.py caida [destino]      (requiere opencv-python-headless)
# destino por defecto: datos/procesados/<mundo>  (la ruta que esperan la cola y las recetas)

import os
import sys
import csv
import glob
import json
import zipfile
import subprocess
import urllib.request

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))
from descubrir import preparar, error_linea_base

MENDELEY_ZIP = ("https://data.mendeley.com/public-files/datasets/7yd2ntbh3w/files/"
                "91cc2fa5-2640-404b-8696-05f0aede2f88/file_downloaded")
MORPHEUS = ("https://huggingface.co/datasets/physics-from-video/morpheus-real-world/"
            "resolve/main/real-world-cropped/{exp}/video_{v}_fps30/cropped_video.mp4")
VIDEOS_CAIDA = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
VIDEOS_DP = list(range(10))
JUECES_DP = [3, 6, 9]                      # posiciones 1-indexadas, congeladas desde prereg-13

# huellas: (resumen historico, kwargs de preparar, jueces 0-indexados, tolerancia relativa)
HUELLAS = {
    "mendeley_epoca2": ("resultados/e2-mendeley-i2/resumen.json",
                        {"suavizar": 3, "retardos": 2}, {2}, 1e-9),
    "caida": ("resultados/e2-caida-i2/resumen.json",
              {"suavizar": 3}, {2, 6, 10}, 1e-9),
    # cadena de VIDEO: la tolerancia es 1e-3, no identidad — el decodificador difiere entre
    # versiones de OpenCV (documentado y medido en arbol/pesos/LEEME.md: 2.3e-5 observado).
    "p14_lat4": ("resultados/p14-final/resumen.json", {}, {2, 5, 8}, 1e-3),
}


def bajar(url, destino):
    print(f"descargando {url[:80]}...")
    urllib.request.urlretrieve(url, destino)
    return destino


def reconstruir_mendeley(destino):
    os.makedirs(destino, exist_ok=True)
    tmp = os.path.join(destino, "_tracking.zip")
    bajar(MENDELEY_ZIP, tmp)
    with zipfile.ZipFile(tmp) as z:
        z.extractall(os.path.join(destino, "_tracking"))
    for t in (1, 2, 3):
        carpeta = os.path.join(destino, "_tracking", "Video_Tracking_Data", f"Trial{t}")
        rb0 = np.load(os.path.join(carpeta, "DPmean_data_RB0.npy"))
        rb1 = np.load(os.path.join(carpeta, "DPmean_data_RB1.npy"))
        assert np.allclose(rb0[0], rb1[0]), "bases de tiempo distintas"
        # submuestreo generico 500->50 Hz: 1 de cada 10 (prerregistro-01)
        with open(os.path.join(destino, f"trial{t}_50hz.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t", "s1", "s2"])
            for i in range(0, len(rb0[0]), 10):
                w.writerow([rb0[0][i], rb0[1][i], rb1[1][i]])
        print(f"trial{t}_50hz.csv listo")
    import shutil
    shutil.rmtree(os.path.join(destino, "_tracking")); os.remove(tmp)


def reconstruir_caida(destino):
    os.makedirs(destino, exist_ok=True)
    vids = os.path.join(destino, "_videos")
    os.makedirs(vids, exist_ok=True)
    for v in VIDEOS_CAIDA:
        mp4 = os.path.join(vids, f"video_{v}.mp4")
        bajar(MORPHEUS.format(exp="falling_ball", v=v), mp4)
        r = subprocess.run([sys.executable, os.path.join(BASE, "codigo", "extraer_posiciones.py"),
                            mp4, os.path.join(destino, f"video_{v}_fps30.csv")],
                           capture_output=True, text=True)
        print(r.stdout.strip().splitlines()[-2] if r.returncode == 0 else r.stderr[-300:])
        if r.returncode != 0:
            raise SystemExit(f"extraccion fallo en video_{v}")
    import shutil
    shutil.rmtree(vids)


def reconstruir_p14_lat4(destino):
    """Regenera los latentes de N-003-E2 con LOS OJOS CANONICOS del repositorio
    (arbol/pesos/ojos_p14_lat4.pt) sobre los videos publicos del pendulo doble, y los
    estandariza con las estadisticas del entrenamiento (jueces congelados 3,6,9).
    Regla 3 intacta: los ojos son NUESTROS, entrenados desde cero — no un modelo ajeno."""
    import csv as _csv
    import torch
    import pandas as pd
    sys.path.insert(0, os.path.join(BASE, "codigo"))
    from percepcion import Ojos, cargar_video

    pesos = os.path.join(BASE, "arbol", "pesos", "ojos_p14_lat4.pt")
    if not os.path.exists(pesos):
        raise SystemExit(f"faltan los ojos canonicos: {pesos} (ver arbol/pesos/LEEME.md)")
    crudo = os.path.join(destino, "_lat")
    os.makedirs(crudo, exist_ok=True)
    os.makedirs(destino, exist_ok=True)

    modelo = Ojos(4)
    modelo.load_state_dict(torch.load(pesos, map_location="cpu"))
    modelo.eval()
    vids = os.path.join(destino, "_videos")
    os.makedirs(vids, exist_ok=True)
    nombres = []
    for v in VIDEOS_DP:
        mp4 = os.path.join(vids, f"video_{v}.mp4")
        bajar(MORPHEUS.format(exp="double_pendulum", v=v), mp4)
        n = f"video_{v}_fps30"
        nombres.append(n)
        with torch.no_grad():
            z = modelo.codificar(torch.tensor(cargar_video(mp4))).numpy()
        with open(os.path.join(crudo, f"{n}.csv"), "w", newline="") as f:
            w = _csv.writer(f)
            w.writerow(["t"] + [f"s{k+1}" for k in range(4)])
            for t_i in range(len(z)):
                w.writerow([t_i] + [round(float(x), 6) for x in z[t_i]])
        print(f"{n}: {len(z)} cuadros codificados")

    # estandarizar con estadisticas SOLO del entrenamiento (identico a estandarizar.py)
    csvs = sorted(glob.glob(os.path.join(crudo, "*.csv")))
    jidx = {j - 1 for j in JUECES_DP}
    cols = [c for c in pd.read_csv(csvs[0]).columns if c.startswith("s")]
    tren = pd.concat([pd.read_csv(c)[cols] for i, c in enumerate(csvs) if i not in jidx])
    mu, sd = tren.mean(), tren.std().replace(0, 1)
    for c in csvs:
        df = pd.read_csv(c)
        df[cols] = (df[cols] - mu) / sd
        df.to_csv(os.path.join(destino, os.path.basename(c)), index=False)
    import shutil
    shutil.rmtree(vids); shutil.rmtree(crudo)
    print(f"latentes estandarizados: {len(csvs)} replicas -> {destino}")


def verificar(mundo, destino):
    resumen_path, kwargs, jidx, tol = HUELLAS[mundo]
    reg = json.load(open(os.path.join(BASE, resumen_path)))
    csvs = sorted(glob.glob(os.path.join(destino, "*.csv")))
    Xtr, Ytr, Xte, Yte = [], [], [], []
    for i, c in enumerate(csvs):
        X, Y = preparar(c, **kwargs)
        (Xte if i in jidx else Xtr).append(X)
        (Yte if i in jidx else Ytr).append(Y)
    base = error_linea_base(np.vstack(Xte), np.vstack(Yte), np.vstack(Ytr))
    desv = abs(base - reg["mse_base"]) / reg["mse_base"]
    print(f"HUELLA {mundo}: base reconstruida {base!r} vs registrada {reg['mse_base']!r} "
          f"| desviacion {desv:.2e}")
    if desv > tol:
        raise SystemExit("HUELLA NO COINCIDE — los datos reconstruidos NO son los historicos; "
                         "no usar para veredictos (revisar versiones de librerias/fuentes).")
    print("HUELLA VERIFICADA: los datos reconstruidos son los historicos. Listos para veredictos.")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in HUELLAS:
        raise SystemExit(f"uso: python reconstruir_datos.py {{{'|'.join(HUELLAS)}}} [destino]")
    mundo = sys.argv[1]
    carpeta = "p14_lat4_std" if mundo == "p14_lat4" else mundo
    destino = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "datos", "procesados", carpeta)
    if mundo == "mendeley_epoca2":
        reconstruir_mendeley(destino)
    elif mundo == "caida":
        reconstruir_caida(destino)
    else:
        reconstruir_p14_lat4(destino)
    verificar(mundo, destino)


if __name__ == "__main__":
    main()
