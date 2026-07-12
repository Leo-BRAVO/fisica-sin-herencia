# bucle14.ps1 - Primer bucle interior (prerregistro-14). Jueces reales (3 6 9): INTOCABLES.
$base = "C:\Users\lrbn2\OneDrive\Desktop\PROJECT TRASFORM 2"
$env:PYTHONUTF8 = "1"
$videos = "$base\datos\crudos\morpheus\real-world-cropped\double_pendulum"

foreach ($dim in @(4, 8, 12)) {
  Write-Output "=== BUCLE iteracion: latente $dim ==="
  python "$base\codigo\percepcion.py" $videos "$base\datos\procesados\p14_lat$dim" --latente $dim --epocas 15 --jueces 3 6 9
  python "$base\codigo\estandarizar.py" "$base\datos\procesados\p14_lat$dim" "$base\datos\procesados\p14_lat${dim}_std" --jueces 3 6 9
  python "$base\codigo\descubrir_pool.py" "$base\datos\procesados\p14_lat${dim}_std" "$base\resultados\p14-inner-d$dim" --semillas 2 --paralelo 2 --maxsize 20 --niter 300 --jueces 5 8
}

Write-Output "=== SELECCION interna ==="
$sel = python "$base\codigo\selector14.py" $base
$sel | Write-Output
$dimG = ($sel | Select-Object -Last 1)
Write-Output "=== GANADOR: latente $dimG - veredicto final ante jueces congelados ==="
python "$base\codigo\descubrir_pool.py" "$base\datos\procesados\p14_lat${dimG}_std" "$base\resultados\p14-final" --semillas 5 --paralelo 5 --maxsize 20 --niter 400 --jueces 3 6 9
Write-Output "BUCLE COMPLETO"
