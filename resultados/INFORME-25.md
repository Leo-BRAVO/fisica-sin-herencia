# INFORME 25 — Los tres verdugos: dos limpios y uno que nunca fue verdugo — 8 de agosto de 2026

## Qué se hizo
Primera corrida autónoma completa del latido en la nube: reconstruyó los datos de tres mundos
desde sus fuentes públicas (huellas verificadas), corrió las tres pruebas nulas pendientes de la
Regla 11 y subió todo a main solo, sin ninguna máquina del director encendida.

## Resultado en una frase
**Dos campañas insignia quedaron BLINDADAS (sus verdugos fracasaron limpio, como debían), y la
tercera reveló algo más valioso que un veredicto: el verdugo que le aplicamos NO FALSIFICABA
NADA — el mundo "falso" era estadísticamente el mismo mundo.**

## Los números
| Campaña | Base real → base falsificada | Semillas que superan el umbral | Veredicto |
|---|---|---|---|
| Mendeley (retardos) | 2.85 → **436.09 (×153)** | 0/2 | ✅ verdugo válido, fracaso limpio |
| Caída | 123.96 → **2986.13 (×24)** | 0/2 | ✅ verdugo válido, fracaso limpio |
| p14 latentes (ojos de Diego) | 0.5944 → **0.5972 (×1.0)** | 2/2 | ⚠️ **VERDUGO INVÁLIDO** |

## Por qué el tercero no fue un verdugo (la evidencia, no la opinión)
El nulo surrogado (IAAFT) conserva el espectro de potencia de cada señal y destruye fases y
acoples. Aplicado a los latentes, **no destruyó nada de lo que la afirmación necesita**:
- base trivial: 0.5944 → 0.5972 (idéntica)
- rival lineal: 0.1470 → 0.1539 (casi idéntico)
- mejor semilla: 0.1663 → **0.1665** (idéntica)
- y las ecuaciones halladas en el mundo FALSO son las mismas del mundo real:
  `(v2+v1)*0.48391813` → `(v1+v2)*0.48429975` · `sin(v3)*1.2079598` → `sin(v3)*1.2083868`
- las dos semillas del nulo incluso replican entre sí a la 7ª cifra (0.48429975 / 0.48429972)

**Diagnóstico:** los latentes son señales suaves cuya predictibilidad a un paso está contenida
por completo en su espectro — y el IAAFT preserva el espectro **por construcción**. El verdugo
entregó el mismo mundo con otro nombre. Un test que no puede fallar no prueba nada: el resultado
"2/2 superan" NO dice que la tubería mienta; dice que **esa prueba nunca fue una prueba.**

## LA LECCIÓN (enmienda a la Regla 31 — la más fina del proyecto hasta hoy)
> **El nulo debe destruir EXACTAMENTE aquello de lo que depende la afirmación — ni más, ni menos.**
> - Afirmación de **conservación**: el barajado destruye también la suavidad (que la conservación
>   no necesita) → acepta mundos vacíos. **IAAFT es el correcto** (AUDITORIA-EXTERNA-01).
> - Afirmación de **predicción**: el IAAFT conserva la autocorrelación, que ES lo que hace posible
>   predecir → no puede falsificar nada. **El barajado es el correcto** (este informe).
> Un nulo demasiado destructivo da falsos positivos; uno demasiado suave da falsos negativos.
> **No existe "el nulo" — existe el nulo de cada afirmación.**

Es, en forma, el mismo error que el director diagnosticó en julio con el péndulo doble ("un KPI
único para todo tipo de sistema"), cometido ahora por el orquestador con los nulos: tras aprender
que el IAAFT salvaba la conservación, lo generalizó a todo. La cura es simétrica: el prerregistro
debe ELEGIR el nulo según la clase de afirmación, y el auditor lo verifica solo (abajo).

## La defensa automática que nace de aquí
`auditoria_total.py` gana un guardián nuevo: **un verdugo que no cambia el mundo no es un verdugo.**
Si la base trivial de una corrida nula queda a menos del 10% de la base de su campaña real, se
marca como NULO INVÁLIDO y no cuenta para la Regla 11 — por muy verde que se vea.

## Qué queda pendiente (encolado, corre solo)
Los tres nulos por **barajado** (el correcto para afirmaciones predictivas). Mendeley y caída ya
sobrevivieron a un verdugo severo; el barajado los cerrará por partida doble. El de p14 es el que
de verdad falta: hasta que corra, **la Regla 11 sigue sin estar al día para los nodos de percepción
propia (N-002-E2 y N-003-E2)**, y así queda declarado.

## Qué NO dice este informe (para que nadie lo lea de más)
No dice que los nodos de percepción sean falsos. Su certificación nunca fue "predice bien" sino
la **replicación estructural** (5 semillas independientes, constantes a la 6ª–7ª cifra). Pero sí
abre una pregunta legítima y registrada: **¿cuánta de esa predictibilidad latente es dinámica y
cuánta es autocorrelación?** El nulo por barajado la responderá.
