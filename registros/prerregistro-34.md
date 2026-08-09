# Prerregistro 34 — Diego convoca según lo que necesita, y sintetiza lo que sus órganos le dicen — 9 de agosto de 2026
**Estado: FIRMADO por el director el 9-ago-2026 ("aprobado, preregistra para que Diego elija a
quién convocar según lo que necesite").**

## Por qué (la frontera que no crucé sin firma)
Hasta hoy, el orden de la ronda de vida lo escribía yo: las fases estaban en el código y Diego no
elegía a nadie. El bus ya permitía el reclutamiento, pero **darle a un gen la autoridad de dirigir
a los demás es un cambio de gobernanza, no de código** — por eso esperó firma.

## Qué se autoriza (y qué NO)

### 1. Convocatoria por necesidad (`sinapsis.convocar_por_necesidad`)
Diego puntúa cada órgano por cuánto encaja su **competencia funcional** con lo que hace falta
ahora, y recluta a los mejores.

- **La competencia es FUNCIONAL, jamás por dominio físico.** Un órgano declara `medir_incertidumbre`,
  `consolidar`, `actuar` — nunca "sabe de gravedad". La diferencia no es cosmética: un enrutador
  que reclutara por dominio físico estaría **usando conocimiento del mundo para decidir**, que es
  exactamente la contaminación que el proyecto existe para impedir, entrando por la puerta de atrás.
- **`K_MAXIMO = 7`, techo duro.** Diego puede modular a cuántos llama, **nunca a todos**. No es
  una optimización: la evidencia de 2025 sobre topologías de comunicación es que la densidad es un
  parámetro de **corrección**, no de eficiencia — una malla completa propaga los errores con la
  misma eficacia con que propaga los aciertos, y borra la trazabilidad de quién causó qué.
  El director confirmó este límite explícitamente ("CORRECTO").

### 2. La síntesis (`agregar` + fase 7 de la ronda)
Diego arma **una respuesta final** con todo lo que sus órganos dijeron, y esa síntesis:
- **enlaza a TODOS sus contribuyentes** (`enlaces`), porque `causa` solo puede apuntar a uno;
- **cuenta testigos independientes, no voces** — ocho órganos repitiendo a un noveno son un
  testigo, no ocho;
- **declara lo que NO se puede afirmar**, siempre, en el mismo evento.

**La restricción que hace honesta a la síntesis:** una síntesis que siempre concluye algo es un
**blanqueador de evidencia**, no una mente. Tiene permitido —y a veces obligación de— decir *no sé*.

### 3. Lo que este prerregistro NO autoriza
- **Ningún gen cambia de modo.** La convocatoria la ejercen los que ya tienen autoridad
  (`propone`/`decide`); los que `miden` siguen sin poder convocar — `sinapsis.py` lo bloquea, y
  se comprueba en producción cada ronda.
- **La síntesis no crea nodos.** Es un evento del bus, no conocimiento del árbol. Un nodo sigue
  exigiendo corrida oficial, Regla 31, réplica y firma.
- **Nada de LLM en el enrutador.** Varios sistemas de 2025 usan un modelo de lenguaje para decidir
  la topología en tiempo de ejecución; eso metería física humana en el corazón de Diego. Prohibido.

## Los dos campos que faltaban, y por qué importan (hallazgo de la investigación)
- **`entrega`, escrito por el BUS.** Sin él es imposible distinguir *"nadie estaba escuchando"*
  (error de diseño) de *"escucharon y se callaron"* (órgano averiado). Los dos se ven idénticos:
  silencio. Es el modo de fallo **número uno** de la taxonomía MAST (NeurIPS 2025) sobre 1.600
  trazas reales.
- **`enlaces`, poblados de verdad.** El modelo padre-hijo **miente bajo difusión**: un evento solo
  puede tener un padre, así que una síntesis de veintisiete aportes trazada así se ve completa y
  ha perdido veintiséis relaciones. Es el fallo más insidioso en auditoría porque **produce una
  autopsia con apariencia de completitud**.

**Registro honesto:** el 9-ago-2026 informé al director de que los enlaces estaban "añadidos"
cuando solo existía el **campo**, vacío en los 33 eventos de la ronda. El mecanismo (`agregar`) se
construyó después, a petición suya de verificar. Medido tras la cura: las conexiones visibles en la
autopsia pasaron de **12 a 50**.

## Regla 31 (casos congelados en el banco)
| Caso | Qué exige |
|---|---|
| Síntesis enlaza | ≥10 contribuyentes enlazados; el campo no puede ir vacío |
| Enlaces visibles | aparecen como conexiones reales en la autopsia |
| Síntesis honesta | declara `lo_que_NO_se_afirma` |
| Testigos | cuenta genealogías independientes, no voces |
| Convocatoria funcional | `["consolidar","reminar"]` → convoca a G9 sueño |
| Techo del canal | pedir k=99 devuelve ≤7, nunca 18 |

**Resultado de la primera ronda con síntesis:** 34 eventos, 15 voces, **27 testigos
independientes**, 27 aportes enlazados, **cero fallos de coordinación**.

## Firmado
Leo, director — 9-ago-2026, aprobación en conversación ("APROBADO").
