# bucle14.ps1 — Primer bucle interior (prerregistro-14). Jueces reales (3 6 9): INTOCABLES.
$base = "C:\Users\lrbn2\OneDrive\Desktop\PROJECT TRASFORM 2"
$env:PYTHONUTF8 = "1"
$videos = "$base\datos\crudos\morpheus\real-world-cropped\double_pendulum"

foreach ($dim in @(4, 8, 12)) {
  Write-Output "=== BUCLE iteracion: latente $dim ==="
  python "$base\codigo\percepcion.py" $videos "$base\datos\procesados\p14_lat$dim" --latente $dim --epocas 15 --jueces 3 6 9
  python -c "
import pandas as pd, glob, os
src = r'$base\datos\procesados\p14_lat$dim'; dst = src + '_std'; os.makedirs(dst, exist_ok=True)
csvs = sorted(glob.glob(os.path.join(src, '*.csv')))
cols = [c for c in pd.read_csv(csvs[0]).columns if c.startswith('s')]
tren = pd.concat([pd.read_csv(c)[cols] for i, c in enumerate(csvs) if i not in {2,5,8}])
mu, sd = tren.mean(), tren.std().replace(0, 1)
for c in csvs:
    df = pd.read_csv(c); df[cols] = (df[cols]-mu)/sd
    df.to_csv(os.path.join(dst, os.path.basename(c)), index=False)
print('std ok', dst)"
  python "$base\codigo\descubrir_pool.py" "$base\datos\procesados\p14_lat${dim}_std" "$base\resultados\p14-inner-d$dim" --semillas 2 --paralelo 2 --maxsize 20 --niter 300 --jueces 5 8
}

# Seleccion INTERNA (jueces internos 5,8): mejor proporcion mse/base
$ganador = python -c "
import json
mejor, ratio = None, 9e9
for d in (4, 8, 12):
    r = json.load(open(rf'$base\resultados\p14-inner-d{d}\resumen.json'))
    rat = min(s['mse_total'] for s in r['semillas'].values()) / r['mse_base']
    print(f'latente {d}: proporcion {rat:.4f}')
    if rat < ratio: mejor, ratio = d, rat
print(mejor)"
$dimG = ($ganador | Select-Object -Last 1)
Write-Output "=== GANADOR del bucle: latente $dimG — veredicto final ante jueces congelados ==="
python "$base\codigo\descubrir_pool.py" "$base\datos\procesados\p14_lat${dimG}_std" "$base\resultados\p14-final" --semillas 5 --paralelo 5 --maxsize 20 --niter 400 --jueces 3 6 9
Write-Output "BUCLE COMPLETO"
