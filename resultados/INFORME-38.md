# INFORME-38 — ACTA DEL PRERREGISTRO 27: el torneo de los ojos queda **NO CONCLUYENTE POR INSTRUMENTO**
**9 de agosto de 2026. Decisión del director:** *"escribe el acta de prereg 27 y decláralo no
concluyente por instrumento."*

Esta acta cierra el torneo del prerregistro-27 **sin declarar ganador y sin declarar empate.**
Declara que **la vara no midió**, que es una tercera cosa y hay que decirla con su nombre.

---

## 1. LO QUE SE CORRIÓ (hechos, no interpretación)
- Corrida 13 del latido en la nube, disparada sobre el commit `3a7c196`, iniciada 03:28 UTC.
- Procesó **4 de las 5 semillas** encoladas. Las semillas 1, 2 y 3 quedaron commiteadas en `main`
  (`4c86eea`, `ed51275`, `066e562`). La **semilla 4 se calculó completa y aprobó los tres
  guardianes**, pero su push fue **rechazado** por una carrera de git (ver §4) y la corrida
  terminó en rojo. La semilla 5 nunca corrió.

## 2. LA TABLA COMPLETA
| Semilla | A-píxel | B-predictivo | C-corolario | R-ranuras | Origen |
|---|---|---|---|---|---|
| 1 | **0.0000** | **0.0000** | **0.0000** | **0.0000** | `resultados/p27-torneo-ojos-s1` |
| 2 | **0.0000** | **0.0000** | **0.0000** | **0.0000** | `resultados/p27-torneo-ojos-s2` |
| 3 | **0.0000** | **0.0000** | **0.0000** | **0.0000** | `resultados/p27-torneo-ojos-s3` |
| 4 | 0.0000 | 0.0000 | 0.0000 | **0.0558** (5 canales) | **solo en el log de la corrida — nunca llegó a `main`** |
| 5 | — | — | — | — | no corrió |

**Doce corridas oficiales, cuatro arquitecturas distintas, el mismo cero exacto.**

## 3. POR QUÉ ESO NO ES UN EMPATE — el diagnóstico
La aptitud prerregistrada (`filogenia.aptitud`) es:

```
puntaje = media( max(margen, 0) ) + 0.01 · n_canales_mios
```

El `max(·, 0)` es un **suelo**. Y el margen que entra ahí ya viene con otro suelo:
`margen = obedece_en − max(techo_nulo, 0.40)`, donde 0.40 es el piso fijo del prereg-23.

Cuando **ningún latente visual alcanza el piso** — que es **exactamente el régimen documentado de
la vista de Diego** en el INFORME-36 (la visión-que-se-une no replicó: 1/5) — entonces:
1. todos los márgenes son negativos,
2. el `max(·,0)` los aplasta todos a cero,
3. y los cuatro competidores empatan en **0.0000 exacto**.

**La vara no estaba midiendo a los competidores: estaba midiendo su propio suelo.**

Y el suelo resultó más profundo de lo que parecía: al construir el panel de jueces (prereg-31) se
comprobó que **el margen crudo también satura**. Cuando `obedece_en` cae a 0, el margen se clava
en **−0.4000** idéntico para cualquier representación floja, por distintas que sean. Medido: dos
representaciones deliberadamente diferentes dieron el mismo −0.4000 al criterio viejo, y el panel
nuevo las separa en −0.00014 vs −0.00051.

### El agravante de la semilla 4
En la semilla 4, R-ranuras asomó por encima del piso (0.0558, 5 canales) mientras las otras tres
seguían en cero. **Con el criterio de victoria del prereg-27, eso habría coronado a R-ranuras.**
Un ganador nacido de que **una sola semilla de cinco** cruzó un umbral que las demás no cruzaron —
es decir, **azar de semilla presentado como evidencia arquitectónica**. Y R-ranuras es justamente
el competidor que la constitución prohíbe que entre al genoma.

**Este es el escenario que el prerregistro de 5 semillas existía para evitar, y aun así casi
ocurre — porque el problema no estaba en el número de semillas sino en el instrumento.**

## 4. EL SEGUNDO FALLO, INDEPENDIENTE: por qué murió la corrida
La rama `gimnasio` del workflow hacía `git push origin main` **pelado**, sin el `pull --rebase`
con cuatro reintentos que sí tenía la rama general. Un commit del director a `main` durante la
corrida bastó para que la semilla 4 —ya calculada, guardianes verdes— fuera rechazada y el latido
se detuviera en rojo con el trabajo hecho.
**Arreglado el 9-ago-2026** (commit `f14dd2e`): ambas ramas usan la misma cura, y `GUARDIANES=$?`
uniforme para que el auditor lea la protección.

## 5. EL FALLO — declarado formalmente
> **NO CONCLUYENTE POR INSTRUMENTO.**
> El torneo del prerregistro-27 no declara ganador, no declara empate técnico y no declara
> "ninguno sirve". Declara que **su función de aptitud es ciega en el régimen donde se aplicó**, y
> que por tanto **los doce ceros no contienen información sobre las cuatro arquitecturas**.

**Consecuencias inmediatas:**
- **Ninguna arquitectura reemplaza a los ojos oficiales.** A-píxel sigue siendo la línea del
  Gimnasio, no por haber ganado sino porque nadie fue medido.
- **R-ranuras no gana nada** y su asomo en la semilla 4 **no se registra como ablación válida**:
  una cifra producida por un instrumento ciego no es una medición.
- **La predicción comprometida del prereg-27** (*"espero que C gane o empate con B, y que A quede
  último"*) **queda sin resolver**. No se confirma ni se refuta. Se vuelve a comprometer, sin
  cambios, para la segunda vuelta.
- **Las semillas 1–3 se conservan** en el repositorio con esta acta al lado. No se borran: son la
  evidencia del fallo del instrumento.

## 6. QUÉ SE HIZO CON EL DIAGNÓSTICO (ya construido, ya en `main`)
El **prerregistro-31** (`codigo/panel_jueces.py`, Regla 31 **5/5**) nace enteramente de este
fallo:
- **Sin suelo:** el ordenamiento usa una ganancia de obediencia **continua** (cuánto ayuda conocer
  el comando a predecir el latente) menos su nulo por comandos barajados. No umbraliza nada.
- **Tres lecturas, no una:** contingencia, **flecha del tiempo** (el mismo video al derecho y al
  revés) y **robustez** (ruido de sensor + oclusión).
- **Regla de oro:** gana solo quien gana o empata en **las tres**. Quien gana una y pierde otra
  recibe **asterisco** y no reemplaza los ojos sin segunda vuelta.
- **Su Regla 31 incluye el caso que reproduce este bug:** dos representaciones que el criterio
  viejo aplasta al mismo −0.4000 deben quedar distinguibles. Congelado en el banco: **no puede
  volver sin que grite**.

Además, la auditoría final del INFORME-37 encontró que el propio panel medía la obediencia a **un
paso** mientras el resto del sistema la medía a **ocho** — el error que el prereg-29 ya había
diagnosticado. Corregido antes de esta acta: el puntaje del oráculo en el banco del panel subió de
**0.012 a 0.056**.

## 7. LO QUE SE APRENDIÓ, Y QUE VALE MÁS QUE EL TORNEO
1. **Un prerregistro puede tener criterio de victoria perfecto y aun así no medir nada**, si el
   instrumento que alimenta ese criterio es ciego en el régimen donde se corre. El rigor del
   criterio no sustituye la validación del instrumento.
2. **La Regla 31 se aplicaba a `filogenia.py` (el estadio) pero no a `filogenia.aptitud` (la
   vara).** El estadio aprobó su Regla 31 — empata gemelos, corona oráculos — con puntajes
   sintéticos entregados a mano. Nadie verificó que **la función que produce esos puntajes a
   partir de datos reales** discriminara en el rango real de Diego. **La Regla 31 hay que
   aplicarla a la vara, no solo al juez que la lee.**
3. **Cinco semillas no protegen de un instrumento ciego.** Protegen del azar; no de la ceguera.

## 8. LO QUE SIGUE
- **Segunda vuelta del torneo** con el panel del prereg-31, mismas cuatro arquitecturas, mismo
  mundo, mismas semillas, misma predicción comprometida. Se encola en el latido.
- El prereg-27 **queda cerrado**. La segunda vuelta será un prerregistro nuevo que lo cite.

---
**Firmado como acta:** Leo, director — 9-ago-2026 (*"decláralo no concluyente por instrumento"*).
