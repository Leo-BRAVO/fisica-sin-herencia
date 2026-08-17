# Prerregistro 54 — EL CENSO DE ÓRGANOS: ¿sobra alguno, y son correctas las atribuciones? — 11 de agosto de 2026
**Encargo del director. Peldaño (Regla 9): Fase 1 — propiedad de nuestro código, no del universo.**
**Estado: FIRMADO antes de escribir `anatomia.py`.**

---

## 0. EL ENCARGO
> *"primero valida si realmente todos los órganos deberían funcionar, si las atribuciones a la
> mente de Diego son las correctas"* · *"los órganos decidir si son prescindibles"*

## 1. LA PREGUNTA, hecha medible
No se puede medir si un órgano *"debería existir"* — eso es un juicio. **Sí se pueden medir cuatro
cosas que, juntas, dicen si un órgano está haciendo algo:**

| | pregunta | qué significa que falle |
|---|---|---|
| **conexión** | ¿algún otro módulo lo usa? | **HUÉRFANO**: publica números que nadie lee |
| **efecto** | ¿su número cambia alguna decisión? | **DECORATIVO**: si cambia y nada cambia, no está en el lazo |
| **unicidad** | ¿hay otro que calcule lo mismo? | **DUPLICADO**: dos verdades sobre lo mismo |
| **atribución** | ¿lo que hace coincide con lo que dice ser? | **MAL ATRIBUIDO**: la etiqueta miente |

**La decisión de quitar un órgano NO se mecaniza y no es mía.** Este estudio produce el censo; el
director decide.

## 2. POR QUÉ ESTO NO ES UNA REORGANIZACIÓN
Ya está respondido y medido: **12 de los 15 son mente y 3 tocan el cuerpo**, y renombrarlos no
habría evitado la cadena G14→G8, porque **el problema era una interfaz sin contrato**. Este estudio
**no propone renombrar nada**: pregunta si alguno **sobra**, que es distinto.

## 3. LA LÍNEA BASE TONTA (Reglas 11 y 12)
**Declarar que todos los órganos son imprescindibles.** Es lo que asumimos hoy sin haberlo mirado
nunca. Un censo que no encuentre ni un huérfano ni un duplicado **no le gana a esa suposición**, y
entonces habrá que decir que la suposición era correcta.

## 4. EL DISEÑO, congelado
- **Conexión:** se mide sobre el código —quién importa a quién y quién llama a quién— y sobre el
  conectoma declarado. Un órgano está conectado si **al menos un módulo que no sea él mismo ni una
  prueba** lo usa.
- **Efecto:** un órgano tiene efecto si **algún módulo lee un número que él publica**. Se mide por
  el nombre de lo que publica, no por suposición.
- **Unicidad:** dos órganos son duplicados si **publican un número con el mismo nombre**.
- **Atribución:** se compara lo que el módulo **hace** —¿abre el simulador? ¿escribe acciones?
  ¿devuelve números? ¿elige entre opciones?— con el tipo que **declara** en su `CONTRATO`, si lo
  tiene.

## 5. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **el censo distingue** | Sobre un grafo sintético con un huérfano puesto a propósito, lo encuentra; sobre uno sin huérfanos, no inventa ninguno |
| **B** | **no acusa por no estar sellado** | Un órgano sin sello **no** cuenta como prescindible: son cosas distintas y confundirlas sería injusto y falso |
| **C** | **la atribución se mide, no se supone** | Todo órgano recibe un tipo **derivado de lo que hace**, y se reporta si choca con el declarado |
| **D** | **le gana a la línea base tonta** | Encuentra **al menos un** huérfano o duplicado. Si no encuentra ninguno, se escribe que **la suposición de que todos hacen falta era correcta**, y eso también es un resultado |

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo:** sobre un grafo hecho a mano con un huérfano, lo marca.
- **Señuelo:** sobre un grafo donde todos se usan, **no marca a nadie**. Un censo que siempre
  encuentra algo que quitar es tan inútil como uno que nunca encuentra nada.
- **La medida responde:** más huérfanos plantados ⇒ más huérfanos hallados. **Base distinta de
  cero.** Octava vez que lo escribo este mes.
- **`SUJETO` declarado**, y la Regla 31 **no toca los órganos reales**: trabaja con grafos
  sintéticos. Examinar a los órganos dentro de mi propia Regla 31 es el error del prerregistro 45.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si falla el **señuelo** —marca huérfanos donde no los hay—, **se descarta el censo**: una lista
  de órganos prescindibles con falsos positivos es peor que no tener lista, porque invita a
  amputar lo que funciona.
- Si falla **B**, se descarta: acusaría a 10 de 15 órganos por una razón que no es la suya.

## 8. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **No se afirma que un órgano huérfano deba borrarse.** Puede estar esperando a que lo conecten.
  El censo dice **qué está desconectado hoy**, no qué merece existir.
- **No se borra ni se toca ningún órgano.** Este estudio **solo mide**.
- **No se afirma que un órgano conectado sirva.** Estar en el lazo no es hacerlo bien — eso lo
  dice su ficha de sanidad, y 8 de ellos ni siquiera la tienen (INFORME-63).

## 9. FIRMA
Avanza por **quórum adversarial**: el señuelo manda descartar el censo si inventa huérfanos, el
criterio **B** impide confundir *"sin examinar"* con *"prescindible"*, y el **D** contempla
explícitamente el resultado que me deja sin hallazgo. Revocable con una palabra del director.
