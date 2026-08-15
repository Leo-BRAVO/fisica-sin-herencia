# Prerregistro 48 — ¿SE RECUPERA EL ÓRGANO DEL SUEÑO CON EL MOTOR NUEVO? — 11 de agosto de 2026
**Fase 2 del PLAN MAESTRO 01. Peldaño (Regla 9): Fase 1 — propiedad de nuestro código, no del
universo.**
**Estado: FIRMADO antes de tocar `sueno.py`.**

---

## 0. POR QUÉ ESTE ESTUDIO ES EL ÚNICO DE LA FASE 2
El `INVENTARIO-MOTOR-01` contó las corridas que usan de verdad `sindy3` y **son dos**: `escala.py`
—que es un estudio *del* motor— y **`sueno.py`, el único órgano que lo consume**. Las 67 corridas
de la cola pasan por PySR y estos defectos no las tocan.

**Y `sueno.py` está REPROBADO por culpa de este motor.** El INFORME-50 midió que **con el mundo
×10 sobrevivían 0 leyes en vez de 3**, y la causa quedó escrita en el momento: *"la causa NO es
suya — es que `sindy3` no es invariante a la escala"*.

## 1. LA PROPIEDAD MÁS IMPORTANTE DE ESTE ESTUDIO: **el criterio no se toca**
El señuelo de escala **no lo escribo hoy**. Está en la ficha de sanidad de `sueno.py`, declarado
en el **prerregistro 43**, y dice literalmente:

> *"el señuelo de escala: multiplicar el mundo por 10 no puede cambiar cuántas leyes pasan"* —
> falla si `sin_escalar != escalado_x10`.

**Cambio el instrumento y vuelvo a correr una prueba que ya estaba congelada.** No hay ningún
umbral nuevo que yo pueda ajustar para que salga bien. Es la mejor situación posible para un
estudio de reparación, y es casualidad favorable, no mérito.

## 2. LA PREGUNTA
> Sustituyendo `sindy3` por `sindy4` como motor de minería del sueño, ¿pasa `sueno.py` la ficha de
> sanidad que reprobó — **o aparece otro defecto que el primero tapaba**?

## 3. LO QUE YA SÉ, declarado antes de correr
- `sindy4` **cierra los agujeros de escala en el oscilador**: un tramo de 5.5 décadas frente a los
  tres tramos de 1.5 décadas de `sindy3` (INFORME-58). El mundo de juguete de `sueno.py` **es un
  oscilador amortiguado**, que es justo la familia donde el arreglo funcionó.
- `sindy4` **calla mucho más**: 0 de 25 sobre señal constante, y silencio total en la caída con
  roce.

**Declaro mi expectativa, para que se me pueda descontar:** espero que **el señuelo de escala
pase**. Y espero, con menos confianza, que **el riesgo real sea el veredicto 4** — que `sindy4`
sea tan estricto que no encuentre ninguna ley y no haya nada que comparar.

## 4. LA LÍNEA BASE TONTA (Reglas 11 y 12)
La que ya tiene el módulo, declarada en el prerregistro 43: **soñar sobre un modelo ajustado a
RUIDO PURO. Cuántas leyes sobreviven al filtro allí es el suelo, y debe ser cero.** Se mide con
los dos motores.

## 5. EL DISEÑO, congelado
- **No se reescribe `sueno.py`.** Se le añade un parámetro `motor` que **por defecto sigue siendo
  `sindy3`**, de forma que el comportamiento actual del órgano **no cambia en absoluto**. El
  estudio corre las dos versiones.
- **Se corre la ficha de sanidad entera** —la parte de correlaciones y el señuelo de escala— con
  los dos motores, sobre el mismo mundo y las mismas semillas.
- **Mismo `dt` de juguete (0.02)**, que es el que el módulo ya usa. *(Integrar a 0.02 y medir con
  `dt=1.0` fue un error real de este mismo módulo; queda escrito para no repetirlo.)*

## 6. LOS CRITERIOS CONGELADOS
1. **RECUPERADO** — con `sindy4`, la ficha de sanidad **aprueba entera**: el señuelo de escala da
   el mismo número con el mundo ×1 y ×10, **y** la parte de correlaciones sigue aprobando.
2. **SIGUE REPROBADO POR LA ESCALA** — el señuelo de escala vuelve a fallar. Entonces **la causa
   no era `sindy3`** y el REPROBADO de `sueno.py` tiene otro dueño. **Sería mi error de
   diagnóstico** y se escribiría así.
3. **CAMBIA DE DEFECTO** — el señuelo de escala pasa pero la ficha reprueba por otra cosa. El
   arreglo destapó algo que el primer defecto tapaba.
4. **NO CONCLUYENTE POR INSTRUMENTO** — con `sindy4` la lectura base es **0 leyes**, así que no hay
   nada que comparar. **Un cero no se compara con otro cero**: es la trampa de la base nula que ya
   me tumbó tres relaciones metamórficas en un día, y aquí se declara **antes** como veredicto
   posible en vez de descubrirse después.

## 7. REGLA 31 — sobre MI PROCEDIMIENTO, **los dos lados**, y no sobre el órgano
- **Control positivo (debe aprobar):** con `sindy3`, el estudio debe **reproducir el REPROBADO ya
  publicado** — señuelo de escala en rojo. Si no lo reprodujera, mi montaje no estaría midiendo lo
  mismo que el INFORME-50 y **se detiene**.
- **Señuelo / control negativo (debe fallar):** la línea base tonta —soñar sobre un modelo
  ajustado a ruido puro— debe dar **0 leyes con los dos motores**. Si diera más de 0, la medida
  aprueba sobre nada.
- **La medida debe RESPONDER a la estructura del mundo**, que es lo único que se sabe a priori:
  con `estructura=0` la cuenta debe caer respecto de `estructura=1`. **Base distinta de cero**, o
  no se compara nada.
- **No se mete aquí ninguna prueba sobre lo que hace `sindy4`.** Eso es el resultado. Es el error
  que dejó NULO al prerregistro 45.

## 8. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si el **control positivo** no reproduce el REPROBADO con `sindy3` → **se detiene**: el montaje no
  mide lo que dice medir.
- Si la **línea base tonta** da **≥1** ley con cualquiera de los dos motores → **se detiene**.
- Si sale **NO CONCLUYENTE POR INSTRUMENTO** → **no hay segunda versión de este estudio**. Se
  escribe que `sindy4` es demasiado estricto para este órgano, y **eso es un resultado sobre el
  motor**, no una excusa para aflojarlo.

## 9. LA OBLIGACIÓN DE PUBLICACIÓN, decidida antes de mirar
Heredada de la Fase 2 del plan y vigente aunque la revisión sea de una sola cosa:

| lo que puede pasar | qué se hace |
|---|---|
| El órgano **se recupera** | Se publica, y `sueno.py` sale de la lista de REPROBADOS con acta. |
| El órgano **sigue reprobado** | Se publica igual de fuerte. **Mi diagnóstico habría sido erróneo.** |
| El órgano **empeora** (veredicto 4) | **Se publica el primero.** Un arreglo que rompe un órgano es la noticia más importante de las tres. |

**Ningún acta antigua se edita ni se borra.** El INFORME-50 se queda como está; si hace falta, se
le añade una corrección con acta propia.

## 10. LO QUE ESTE ESTUDIO **NO** PUEDE AFIRMAR
- **Nada del universo.**
- **No dice que `sindy4` sea buen motor** — solo si este órgano concreto se recupera.
- **No cambia el motor por defecto de `sueno.py`.** Esa decisión se toma **después**, con el acta
  delante, y es un cambio del órgano, no de este estudio.
- **No toca `escala.py` ni el INFORME-55.**

## 11. FIRMA
Avanza por **quórum adversarial**: el criterio decisivo estaba congelado desde el prerregistro 43
y no se toca, la expectativa va declarada, hay dos veredictos que me dejan mal (**SIGUE REPROBADO
POR LA ESCALA** sería un error de diagnóstico mío, y **NO CONCLUYENTE POR INSTRUMENTO** sería un
arreglo que empeora un órgano) y un criterio de abandono que impide una segunda versión.
Revocable con una palabra del director.
