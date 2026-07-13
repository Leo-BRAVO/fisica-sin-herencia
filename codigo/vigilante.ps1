# vigilante.ps1 — LA ALARMA (orden del director, 13-jul-2026).
# Corre SOLO cada 30 min por tarea programada. Detecta el cuelgue de Julia
# (proceso vivo pero la carpeta de salida no se escribe hace mas de 30 min)
# y lo reinicia solo desde checkpoint. No depende de que nadie este despierto.
$base = "C:\Users\lrbn2\OneDrive\Desktop\PROJECT TRASFORM 2"
$activa = "$base\registros\campana-activa.json"
$log = "$base\registros\vigilante.log"
$env:PYTHONUTF8 = "1"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm"

if (-not (Test-Path $activa)) { Add-Content $log "$ts | sin campana activa - ok"; exit 0 }

$c = Get-Content $activa -Raw | ConvertFrom-Json
$campPid = [int]$c.pid
$outdir = [string]$c.outdir
$proc = Get-Process -Id $campPid -ErrorAction SilentlyContinue
if (-not $proc) { Add-Content $log "$ts | proceso $campPid ya no existe (termino o murio) - ok"; exit 0 }

# Ultima escritura en la carpeta de salida, con PISO en el momento de lanzamiento
# (la campana-activa.json se escribe al arrancar): asi un arranque fresco sobre una
# carpeta con archivos viejos no se confunde con un cuelgue durante el compilado de Julia.
$ultimo = Get-ChildItem $outdir -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$ult = (Get-Item $activa).LastWriteTime
if ($ultimo -and $ultimo.LastWriteTime -gt $ult) { $ult = $ultimo.LastWriteTime }
$mins = [int]((Get-Date) - $ult).TotalMinutes

if ($mins -le 30) { Add-Content $log "$ts | viva y escribiendo (hace $mins min) - ok"; exit 0 }

# COLGADO: matar y relanzar desde checkpoint el MISMO comando
Add-Content $log "$ts | COLGADO ($mins min sin escribir) - matando PID $campPid y relanzando"
Stop-Process -Id $campPid -Force -ErrorAction SilentlyContinue
Get-Process julia -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
$argv = @($c.argv | ForEach-Object { if ($_ -match '\s') { "`"$_`"" } else { "$_" } })
Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList $argv
Add-Content $log "$ts | relanzado desde checkpoint (semillas completas se reutilizan)"
