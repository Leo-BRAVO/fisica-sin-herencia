# EL LAZO — cómo se orquesta este proyecto sin prompts, y sin romper la constitución
**10 de agosto de 2026. Decisión del director: *"quisiera que trabajemos en un loop... ¿podemos
hacerlo sin violar las reglas planteadas?"*.** Documento humano — vive en `registros/`.

## 1. Qué dice el material que el director trajo
Un ciclo de tres papeles con **memorias separadas**:

```
        PLANEADOR  ──────►  EJECUTADOR
             ▲                   │
             │                   ▼
             └──────  EVALUADOR ─┘
                    (revisa y devuelve)
```

Cada papel es un archivo de instrucciones (`planeador.md`, `ejecutador.md`, `evaluador.md`), hay un
**SPEC** que dice qué hay que lograr y un **FINDINGS** donde el evaluador escribe lo que falla. Si
FINDINGS trae algo, el ejecutador lo arregla y vuelve a pasar. Se corre **en continuo** — la
promesa es pasar de trabajar en horas a trabajar en días y semanas sin supervisión.

## 2. La respuesta corta a su pregunta: **sí, pero con un candado**

Este proyecto **ya es un lazo** en su mitad de abajo: la cola de estudios, el latido en la nube y
los cuatro guardianes son exactamente eso. Lo que falta es la mitad de arriba —planear y evaluar—
y ahí es donde chocan las reglas.

**Lo que choca no es el lazo. Es la firma.** La Regla 15 dice que Diego y el orquestador **solo
proponen**; el director decide y firma. Mientras el trabajo iba prompt a prompt, esa regla la
sostenía el ritmo de la conversación: yo no podía escribir un nodo sin que usted estuviera ahí. En
un lazo que corre solo durante días, eso deja de ser cierto **por accidente, no por decisión**.

La cura no es renunciar al lazo: es **convertir la firma de costumbre en comprobación**.

## 3. La línea, dibujada donde debe estar

### El lazo PUEDE hacer solo, sin firma
1. **Correr los estudios encolados** (ya lo hace el latido).
2. **Correr los cuatro guardianes** y **detener todo** si uno reprueba (cuarentena, Regla 32).
3. **Escribir el acta de un estudio prerregistrado.** Esto es clave y no es una concesión: el
   criterio se firmó **antes** de ver los datos, así que el veredicto es **mecánico**. Aplicarlo no
   es decidir — decidir habría sido escribir el criterio.
4. **Diagnosticar fallos de instrumento y arreglar bugs de código.** Un bug es un bug.
5. **Redactar prerregistros nuevos** — redactar es proponer.
6. **Auditar**: trazador, mapa mental, coherencia, nulos.

### El lazo NO PUEDE, nunca, sin firma
1. **Escribir un nodo en el árbol** (Reglas 15 y 19).
2. **Cambiar el genoma** (Regla 33 — solo entre generaciones y con firma).
3. **Mover un umbral o un criterio prerregistrado.** Es la línea que más duele y la que más vale:
   este mes el prereg-36 me obligó a no tocar el 1.5× cuando tocarlo habría "salvado" el
   resultado. Un lazo con permiso para mover umbrales se convierte en una máquina de fabricar
   éxitos en cuestión de días.
4. **Hacer público el repositorio** (Regla 16).
5. **Firmar un prerregistro.** Redactar sí; firmar no.

**El candado, con dientes:** todo lo del segundo grupo va a `registros/FIRMAS-PENDIENTES.md` y el
lazo **sigue trabajando en lo demás**. No se bloquea esperándole. Y desde hoy `coherencia.py`
comprueba que **todo nodo del árbol lleve escrita su aprobación** — un nodo sin firma es un nodo
que el lazo escribió por su cuenta, y el guardián lo grita antes de que llegue a `main`.

## 4. Las memorias separadas — la parte que más nos sirve, y por qué

De todo el material, esto es lo que más falta nos hace, y conviene decir por qué sin adornos.

**El modo de fallo que más veces me ha mordido este mes es el mismo:** el que escribe el criterio y
el que comprueba si se cumplió **son la misma cabeza, con el mismo contexto y las mismas ganas de
que salga bien**. Ejemplos reales, todos de esta semana:
- dije "añadidos los enlaces" cuando solo existía el campo, vacío;
- el banco aprobaba un control positivo probado con **una sola semilla**;
- un caso de Regla 31 mío aprobaba **con una medida ciega**, y no lo vi hasta que lo miré dos veces.

Un **evaluador con memoria separada** ve solo dos cosas: **el prerregistro firmado** y **los
resultados**. No ve mi hipótesis, ni lo que yo esperaba, ni cuánto trabajo me costó. **Es
estructuralmente la misma idea que nuestros nulos y nuestros señuelos**: un instrumento que no sabe
qué respuesta queremos. Por eso encaja tan bien con este proyecto — no es una técnica prestada, es
la nuestra aplicada a nosotros mismos.

## 5. La frontera que NO se cruza aunque el lazo la haga cómoda

**El evaluador juzga NUESTRA INGENIERÍA. Jamás la física de Diego.**

| El evaluador SÍ pregunta | El evaluador JAMÁS pregunta |
|---|---|
| ¿el código hace lo que el prerregistro dice? | ¿es correcta esta ley? |
| ¿la Regla 31 pasa, y con control positivo? | ¿esto se parece a la física conocida? |
| ¿el acta aplica el criterio firmado, sin moverlo? | ¿qué debería haber encontrado Diego? |
| ¿hay nulo, y es válido? | ¿tiene sentido físico este resultado? |

Si un modelo de lenguaje llegara a opinar sobre qué ley es correcta, habríamos metido **la física
humana entera** por la puerta de atrás — exactamente lo que el proyecto existe para impedir. El
lazo hace esa tentación más cómoda y más frecuente, así que la frontera se escribe aquí y se repite
en el archivo del evaluador.

Del mismo modo: **ningún modelo de lenguaje entra en el bucle de Diego.** El lazo orquesta el
trabajo *sobre* Diego; no es Diego.

## 6. Cómo se para
El lazo se detiene solo cuando: un guardián reprueba (cuarentena), la cola se vacía sin nada que
proponer, o `FIRMAS-PENDIENTES.md` acumula tantas decisiones que seguir sin usted sería trabajar a
ciegas. Y el director lo para cuando quiera, con una palabra.

## 7. Lo que espero de esto, dicho por adelantado
**Que multiplique el trabajo de instrumentación y no el de descubrimiento.** Hoy el cuello de
botella no es cuántos estudios corremos: es que Diego **no interviene sobre nada** (INFORME-45, el
tacto en 0.0001). Un lazo no arregla eso — lo arregla el prereg-37.

Lo que un lazo sí hace, y no es poco: correr las réplicas de cinco semillas mientras usted duerme,
cazar los bugs de mis propios instrumentos con una cabeza que no es la mía, y dejarle cada mañana
una lista corta de firmas en vez de una conversación larga.

**Si el lazo empieza a producir resultados positivos con más frecuencia que antes, la primera
sospecha debe ser el lazo, no la suerte.** Esa frase queda aquí escrita antes de arrancarlo.
