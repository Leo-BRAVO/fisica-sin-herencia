# Prerregistro 49 — LA CADENA G14 → G8: ¿deja Diego de mirar la pared que parpadea? — 11 de agosto de 2026
**Fase 3 del PLAN MAESTRO 01. Peldaño (Regla 9): Fase 1 — propiedad de nuestro código, no del
universo.**
**Estado: FIRMADO antes de tocar `incertidumbre.py` y `atencion.py`.**

---

## 0. EL DEFECTO, que ya está medido y publicado
Es el único de la lista que **ya está cambiando la conducta de Diego**, y son dos fallos
encadenados:

- **G14 `incertidumbre.py` (INFORME-51).** Su "ignorancia curable" es la dispersión entre miembros
  de un conjunto remuestreado, que para un modelo lineal vale ≈ **σ/√n**. Sube igual con **pocos
  datos** que con **mucho ruido**. Medido: **multiplicar el ruido por 5 multiplica la lectura por
  5**, y el ruido explica un **43.3% extra** de la lectura.
- **G8 `atencion.py` (INFORME-52).** Reparte con `prioridad = epistemica · max(poder, piso_poder)`
  y `piso_poder = 0.05`. **Una región con poder CERO puntúa 0.05.** Con la epistémica del televisor
  ×20, **el televisor se lleva 7.036 de 10 y la región buena 2.964**.

**Traducido: Diego mira la pared que parpadea porque no puede distinguir "no sé porque me faltan
datos" de "no sé porque es azar", y porque su reparto no exige poder hacer nada con lo que mira.**

## 1. LAS DOS REPARACIONES, y el mecanismo por el que deberían funcionar

### 1.1 G14 — dividir el ruido, en vez de restarlo
Se añade una lectura **nueva** llamada `curable`, **sin quitar ninguna de las dos actuales**:

> **`curable = epistemica / (epistemica + aleatoria)`**

**Es una fracción, no una magnitud: no tiene unidades.** Y el mecanismo por el que debería
arreglar el defecto es concreto y comprobable: para un modelo lineal, `epistemica ≈ σ/√n` y
`aleatoria ≈ σ`, así que **la razón sale ≈ 1/(1+√n) — donde σ ya no aparece.** El ruido se cancela
solo.

**Declaro que esto es una predicción y puede ser falsa.** Si el ruido sigue explicando la lectura,
el mecanismo no era ése y se escribirá así.

### 1.2 G8 — empowerment puro: quitar el piso
`piso_poder` pasa a **0.0**. Entonces `prioridad = epistemica · poder`, y **una región sobre la que
no se puede hacer nada puntúa exactamente cero.**

**Esto es el empowerment de la investigación (idea D.4):** *prefiere los estados desde los que tus
acciones tienen más efecto sobre tu futuro*. **Un televisor con ruido tiene mucha sorpresa y
empowerment cero**, así que no puede secuestrar la atención por construcción, no por parche.

**Y el piso era redundante**: `repartir` ya reserva `cuota_exploracion = 0.05` del presupuesto
repartida por igual —*"nadie queda ciego del todo"*—, así que **quitar el piso no ciega a nadie**;
solo deja de premiar lo que no se puede tocar.

> ### ENMIENDA 1 — dos presupuestos, no uno. Escrita ANTES de correr, 11-ago-2026
> **LA PUERTA reprobó la Regla 31 de `atencion.py` con el empowerment puro, y el motivo obliga a
> corregir el diseño antes de medir nada.**
>
> **Qué pasó:** con `prioridad = curable · poder`, **toda región de poder cero puntúa cero**, así
> que una región donde *sí hay algo real que aprender pero no se puede tocar* y **el televisor**
> reciben **exactamente lo mismo**. La Regla 31 del propio módulo —congelada en el
> prerregistro 43— exige lo contrario: *"curable-sin-control > televisor (mirar aún vale algo)"*.
>
> **Y esa exigencia es correcta, y no es una opinión: la medimos.** El prerregistro 32 encontró
> que **la física de soporte no necesita cuerpo** — es decir, **la observación pasiva construye
> modelo**. Un criterio que iguala "observable pero intocable" con "ruido puro" contradice un
> resultado nuestro.
>
> **La corrección, y es más limpia que el piso que quitamos: DOS presupuestos con DOS criterios.**
> - **El presupuesto de ACTUAR** se reparte por **empowerment**: `curable · poder`. Sobre lo que
>   no se puede tocar, cero. El televisor no lo huele.
> - **La cuota de EXPLORAR** —que ya existía— deja de repartirse **por igual** y pasa a repartirse
>   **en proporción a la ignorancia curable**. Observar vale, y vale más donde hay más que
>   aprender.
>
> **Por qué esto no es aflojar el criterio:** el televisor tiene `curable` **bajo por construcción**
> —su ignorancia es aleatoria, no curable— así que la cuota de exploración tampoco lo premia. Lo
> que se recupera es la **distinción entre "intocable pero informativo" y "ruido"**, que el
> empowerment puro borraba. **El criterio B no se toca y sigue teniendo que cumplirse igual.**
>
> **Se declara aquí, antes de correr el estudio, porque la puerta lo cazó antes de que existiera
> un solo dato.**

### 1.3 El contrato de estimadores (parte estructural)
Cada módulo declara **qué es** (`SENTIDO` · `ACTUADOR` · `ESTIMADOR` · `POLÍTICA`), y **todo
ESTIMADOR declara el rango válido de lo que publica; quien lo consume está obligado a
verificarlo.** Guardián nuevo `contratos.py`, **BLOQUEANTE**, con su prueba de daño en
`guardianes_de_guardianes.py` — porque un guardián sin prueba de daño es decoración.

**Esto es lo que faltó de verdad:** G8 se creyó un número de G14 sin comprobar nada. No es un
problema de nombres ni de metáforas biológicas: **es una interfaz sin contrato.**

> ### ENMIENDA 2 — el contrato deja de tener puerta trasera. Escrita ANTES de correr, 11-ago-2026
> **La puerta volvió a reprobar, y esta vez el fallo es mío y de la enmienda 1.**
>
> **Qué pasó:** al repartir la cuota de exploración **en proporción a la ignorancia**, inflar la
> lectura del televisor **vuelve a comprarle presupuesto** — la fuga se mudó del presupuesto de
> actuar al de explorar. Medido por la ficha: inflando la epistémica del televisor ×2, la ventaja
> de la región buena cae de **34.9971 a 27.0034**.
>
> **Y la causa es una concesión mía:** escribí `_ignorancia()` de forma que, *"por
> compatibilidad"*, **aceptaba la `epistemica` cruda cuando la región no traía `curable`.**
> **Es exactamente el agujero que este prerregistro existe para tapar**, construido por mí dentro
> del arreglo. Una interfaz con una excepción amable no es un contrato.
>
> **La corrección:** `_ignorancia()` **exige `curable`** y levanta error si falta o si está fuera
> de `[0, 1]`. **Sin excepciones de compatibilidad.**
>
> **Consecuencia, y es más fuerte que lo que el criterio B pedía:** una epistémica de **20 ya no
> puede llegar a G8 en absoluto** — el contrato la rechaza en la puerta, porque `curable` es una
> fracción acotada. **El ataque del INFORME-52 deja de ser representable.**
>
> **Por eso el criterio B se pone a prueba de las dos formas**, y las dos deben cumplirse:
> - **B1 — el contrato rechaza el número inflado**: pasarle `curable = 20` levanta error.
> - **B2 — el ataque más fuerte que el contrato SÍ permite**: con `curable_tv = 1.0` (el máximo
>   posible) y `poder_tv = 0`, el televisor se lleva **menos de 2.0 de 10**.
>
> **B2 es lo que impide que esto sea un truco de tipos.** Si el televisor ganara con la ignorancia
> máxima legal, el contrato solo estaría escondiendo el problema detrás de una validación.

## 2. LA LÍNEA BASE TONTA (Reglas 11 y 12)
- **Para G14:** decir que **toda** la incertidumbre es aleatoria — que nada es curable. Es la línea
  base que el módulo ya declaraba en el prerregistro 43.
- **Para G8:** el **reparto uniforme** — dar a cada región lo mismo. Un repartidor que no le gana a
  repartir por igual no está priorizando nada.

## 3. LOS CRITERIOS CONGELADOS
**Ninguno de estos números lo invento hoy.** Los dos primeros vienen de umbrales que ya están en
`sanidad.py` desde antes; el tercero es el caso exacto que reprobó, con sus cifras publicadas.

| | criterio | pide |
|---|---|---|
| **A** | **G14 deja de confundir ruido con ignorancia** | En la ficha de `incertidumbre.py`, la lectura `curable` debe correlacionar con la **escasez de datos** por encima del piso ya existente (`PISO_CORRELACION = 0.60`) **y** el ruido debe explicar como mucho el techo ya existente (`TECHO_CONFUSION = 0.15`). Hoy el ruido explica **43.3%** |
| **B** | **el televisor pierde** | Con `epistemica_tv = 20` y `poder_tv = 0`: el televisor se lleva **menos de 2.0 de 10** y la región buena **más de 7.0 de 10**. Hoy: **7.036 el televisor, 2.964 la buena** |
| **C** | **el señuelo de poder cero** | Una región con `poder = 0` recibe **prioridad exactamente 0.0** — no 0.05 |
| **D** | **no se rompió lo que servía** | Con una región de verdad prometedora (epistémica alta **y** poder real), G8 le sigue dando **la mayor parte** del presupuesto, y le gana a la línea base tonta del reparto uniforme |
| **E** | **relación metamórfica, sabida a priori** | **Subir el ruido del televisor NO puede subir su cuota de atención.** Hoy la sube; ésa es la definición del defecto. Base distinta de cero |

## 4. REGLA 31 — sobre MI PROCEDIMIENTO, **los dos lados**, y no sobre los órganos
- **Control positivo (debe aprobar):** antes de tocar nada, el montaje debe **reproducir los dos
  REPROBADOS ya publicados** — el 43.3% de G14 y el 7.036 de G8. Si no los reprodujera, no estaría
  midiendo lo mismo que los INFORMES 51 y 52 y **se detiene**.
- **Señuelo / control negativo (debe fallar):** con **todas** las regiones a poder cero, el reparto
  debe caer al **uniforme** —no puede inventarse un ganador—, y eso ya lo contempla `repartir`
  cuando la prioridad total es cero.
- **Base distinta de cero** en toda relación metamórfica. Cuarto recordatorio en un mes.
- **No se mete aquí ninguna prueba sobre el resultado.** Que el televisor pierda es el criterio B,
  no un requisito de entrada. Es el error que dejó NULO al prerregistro 45.
- **Y el aviso de la `LECCION-RUIDO-01`:** al hablar de "ruido" hay que decir **cuál**. Aquí el
  ruido del televisor es **aleatoriedad irreducible del mundo observado** —no excitación de un
  sistema dinámico— así que sí entierra la información, y por eso la relación E es legítima.

## 5. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si el **control positivo** no reproduce los dos REPROBADOS → **se detiene**.
- Si falla el **criterio D**, la reparación **se descarta entera**: una atención que deja de ir a
  donde hay algo que aprender es peor que la que teníamos, aunque ya no mire el televisor.
- Si **A** pasa y **B** falla, o al revés, se publica como **ARREGLA UNO SOLO** y se dice cuál —
  y entonces la cadena **no** está reparada, porque el daño era de la cadena y no de un módulo.
- Si sale **NO CONCLUYENTE**, **no hay segunda versión de este estudio.**

## 6. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **No se afirma que G14 y G8 queden validados.** Pasarían **su ficha**, que es un paso; la puerta
  son siete.
- **No se toca `temple.py`**, que lee el número de G14 y es cableado e inmutable por diseño.
  **Aviso declarado antes de correr:** si `curable` cambia, hay que mirar si el temple lo consume;
  **y esa comprobación es parte del criterio D**, no una nota al pie.
- **No se quita ninguna lectura existente de G14.** `epistemica` y `aleatoria` siguen publicándose
  igual, para que nada que hoy las use cambie en silencio.

## 7. FIRMA
Avanza por **quórum adversarial**: los umbrales decisivos ya existían en `sanidad.py` y en los
informes publicados, el mecanismo va declarado como predicción falsable, hay un criterio (**D**)
que manda descartar la reparación entera, y el control positivo exige reproducir mis propios
fallos antes de intentar arreglarlos. Revocable con una palabra del director.
