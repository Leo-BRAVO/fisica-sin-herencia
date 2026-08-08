# respaldo.ps1 - copia fria semanal (orden del director, 12-jul-2026):
# el proyecto entero, con su historia git, fuera de OneDrive.
$src = "C:\Users\lrbn2\OneDrive\Desktop\PROJECT TRASFORM 2"
$dest = "C:\FisicaSinHerencia-Respaldo"
robocopy $src $dest /E /XD ".claude" /NFL /NDL /NJH /NJS
Add-Content "$src\registros\respaldo.log" ("{0} | respaldo refrescado" -f (Get-Date -Format "yyyy-MM-dd HH:mm"))
