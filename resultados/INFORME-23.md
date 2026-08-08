# INFORME 23 — La mudanza del corazón: el latido vive en la nube y se cuida solo — 8 de agosto de 2026

## Qué se hizo (orden del director: "que se actualice solo después de las pruebas en nube; valida los huecos y arreglémoslos")
Auditoría de la infraestructura bajo la realidad nueva (todo corre en nube, sin máquina personal).
**Siete huecos encontrados, siete cerrados:**

| # | Hueco | Arreglo |
|---|---|---|
| 1 | La nube commiteaba SIN guardianes (violaba la Regla 32 en cada commit automático) | ambos workflows corren `pruebas.py` + `coherencia.py` ANTES de commitear; si fallan, no hay commit |
| 2 | El latido murió con la laptop (la tarea horaria era de Windows) | **`latido-nube.yml`**: GitHub Actions diario ejecuta la cola solo — el corazón ya no tiene dueño de hardware |
| 3 | La nube no marcaba la cola ni actualizaba la boleta | `latido_nube.py --completar-si-terminado` (marca `hecha` SOLO si existe el resumen) + boleta en el cierre |
| 4 | Sin checkpoints en la nube: una corrida muerta al minuto 55 perdía todo | el commit corre con `if: always()` — los parciales POR SEMILLA se commitean aunque el runner muera, y la corrida siguiente REANUDA (la lección de los 3 apagones, versión nube) |
| 5 | Carrera de commits si dos corridas empujaban a la vez | `concurrency: group: nube` (una a la vez) + push con `pull --rebase` y 4 reintentos exponenciales |
| 6 | El item p14 de la cola era inejecutable en nube sin declararlo (necesita `ojos.pt` del OneDrive) | marcado `espera-al-director` con sus dos opciones escritas (subir ojos.pt, o re-derivar con prerregistro de equivalencia) |
| 7 | El verdugo de la caída nunca se encoló (solo el de Mendeley) | `aud01-nulo-caida` encolado con reconstrucción automática |

## Cómo funciona el ciclo completo, ya sin manos
1. Cada día a las 06:00 UTC (o con un clic en Actions), el latido revisa la cola.
2. Si hay un re-análisis pendiente: reconstruye los datos desde la fuente pública, **verifica la
   huella digital** (si no coincide, se detiene — jamás corre veredictos sobre datos dudosos),
   corre la campaña, actualiza memoria/conectoma/boleta, marca la cola.
3. **Los dos guardianes aprueban o no hay commit** — la Regla 32 rige también para la máquina.
4. Commitea a main con manejo de carreras. Si el runner murió a medias: los checkpoints quedaron
   commiteados igual y el latido de mañana reanuda solo.
- Gobernanza intacta: el latido SOLO toma `tipo: re-analisis` (aprobación permanente); datos
  nuevos, nodos y reglas esperan al director, como siempre.
- Cola vacía = el latido sale en ~1 minuto (no gasta los minutos gratuitos de Actions).

## Qué le queda al director (nada técnico)
- Nada obligatorio: el latido correrá los dos verdugos pendientes (Mendeley y caída) solo, uno
  por día. Si quiere adelantarlos: Actions → latido-nube → Run workflow (dos veces, con un día
  o unas horas entre ambas — la concurrencia protege igual).
- El item p14 espera su decisión (dos opciones escritas en la cola).
- Leer los INFORMES que el latido irá dejando — el veredicto esperado de AMBOS verdugos es
  **fracasar limpio** (son pruebas nulas: si "descubren", la tubería miente).
