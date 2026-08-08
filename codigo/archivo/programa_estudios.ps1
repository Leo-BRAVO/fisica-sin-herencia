# programa_estudios.ps1 - LA CONTINUIDAD (acelerador nº1, orden del director 12-jul-2026).
# Cada hora: si la mente no esta ocupada, toma la siguiente campana de su cola
# (incluidas las que ELLA se propuso), la corre, actualiza su memoria y su conectoma.
# NO toma decisiones cientificas nuevas: solo ejecuta la cola (re-analisis con
# aprobacion permanente; datos nuevos esperan al director). Jueces: intocables.
$base = "C:\Users\lrbn2\OneDrive\Desktop\PROJECT TRASFORM 2"
$log = "$base\registros\estudios.log"
$env:PYTHONUTF8 = "1"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm"

# ocupada? (cualquier campana o entrenamiento en curso)
$ocupada = Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
  Where-Object { $_.CommandLine -match "descubrir_pool|percepcion|bucle" }
if ($ocupada) { Add-Content $log "$ts | ocupada - sigo esperando"; exit 0 }

# memoria y curiosidad al dia
python "$base\codigo\memoria.py" --retro | Out-Null
python "$base\codigo\curiosidad.py" --proponer | Out-Null

# siguiente deseo de la mente
$sig = python "$base\codigo\curiosidad.py" --siguiente | Select-Object -Last 1
$item = $sig | ConvertFrom-Json
if (-not $item.id) { Add-Content $log "$ts | cola vacia - la mente descansa"; exit 0 }

Add-Content $log "$ts | EJECUTANDO deseo de la mente: $($item.id) | motivo: $($item.motivo_suyo)"
$args = "`"$base\codigo\descubrir_pool.py`" `"$base\$($item.datos)`" `"$base\$($item.salida)`" $($item.args)"
Start-Process -Wait -WindowStyle Hidden -FilePath "python" -ArgumentList $args
python "$base\codigo\curiosidad.py" --completar $item.id | Out-Null
python "$base\codigo\memoria.py" --retro | Out-Null
python "$base\codigo\conectoma.py" | Out-Null
Add-Content $log "$ts | COMPLETADA: $($item.id) - memoria y conectoma actualizados"
