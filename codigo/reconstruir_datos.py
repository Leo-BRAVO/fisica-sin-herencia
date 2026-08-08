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
            "resolve/main/real-world-cropped/falling_ball/video_{v}_fps30/cropped_video.mp4")
VIDEOS_CAIDA = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# huellas: (resumen historico, kwargs de preparar, jueces 0-indexados, tolerancia relativa)
HUELLAS = {
    "mendeley_epoca2": ("resultados/e2-mendeley-i2/resumen.json",
                        {"suavizar": 3, "retardos": 2}, {2}, 1e-9),
    "caida": ("resultados/e2-caida-i2/resumen.json",
              {"suavizar": 3}, {2, 6, 10}, 1e-9),
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
        bajar(MORPHEUS.format(v=v), mp4)
        r = subprocess.run([sys.executable, os.path.join(BASE, "codigo", "extraer_posiciones.py"),
                            mp4, os.path.join(destino, f"video_{v}_fps30.csv")],
                           capture_output=True, text=True)
        print(r.stdout.strip().splitlines()[-2] if r.returncode == 0 else r.stderr[-300:])
        if r.returncode != 0:
            raise SystemExit(f"extraccion fallo en video_{v}")
    import shutil
    shutil.rmtree(vids)


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
    destino = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "datos", "procesados", mundo)
    if mundo == "mendeley_epoca2":
        reconstruir_mendeley(destino)
    else:
        reconstruir_caida(destino)
    verificar(mundo, destino)


if __name__ == "__main__":
    main()
