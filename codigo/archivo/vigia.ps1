# vigia.ps1 — VIGÍA de resiliencia (idea del director, 11-jul-2026)
# Mantiene VIVA la campana aprobada E2-Mendeley: si la maquina se reinicio o el
# proceso murio, lo relanza desde el checkpoint. NO toma decisiones cientificas
# (Regla 15): no crea prerregistros, no aprueba nodos, no avanza de campana.
# Cuando la campana completa, se detiene y deja nota para el director.

$base = "C:\Users\lrbn2\OneDrive\Desktop\PROJECT TRASFORM 2"
$log = "$base\registros\vigia.log"
$out = "$base\resultados\e2-mendeley"
$resumen = "$out\resumen.json"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Campana completa? (>=5 semillas registradas en resumen.json)
if (Test-Path $resumen) {
  try {
    $j = Get-Content $resumen -Raw | ConvertFrom-Json
    if (($j.semillas.PSObject.Properties | Measure-Object).Count -ge 5) {
      Add-Content $log "$ts | E2-Mendeley COMPLETA - vigia en reposo, esperando al director."
      exit 0
    }
  } catch {}
}

# Hay un proceso de la campana corriendo?
$corriendo = Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
  Where-Object { $_.CommandLine -like "*descubrir_pool*e2-mendeley*" }
if ($corriendo) {
  Add-Content $log "$ts | corriendo (PID $($corriendo.ProcessId)) - ok"
  exit 0
}

# No corre y no esta completa -> relanzar desde checkpoint (misma orden del prereg-12)
Add-Content $log "$ts | NO corria - RELANZANDO desde checkpoint"
$env:PYTHONUTF8 = "1"
Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList @(
  "`"$base\codigo\descubrir_pool.py`"",
  "`"$base\datos\procesados\mendeley_epoca2`"",
  "`"$out`"",
  "--semillas","5","--paralelo","5","--maxsize","25","--niter","400",
  "--jueces","3","--suavizar","3","--retardos","2",
  "--rival-arbol","`"$base\resultados\oficial-trial1\semilla_9.json`""
)
