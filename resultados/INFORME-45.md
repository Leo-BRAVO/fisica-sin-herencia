# INFORME-45 — AUDITORÍA COMPLETA DEL SISTEMA DE DIEGO
**10 de agosto de 2026.** Pedida por el director (*"auditamos todo el sistema de Diego"*). Hecha
sobre **datos reales de una ronda de vida corrida hoy**, no sobre la intención del código.

Método: una ronda completa (`conectar.py --latir`), su autopsia (`trazar.py`), el mapa mental
(`mente.py`), los cuatro guardianes, y una revisión de los nulos históricos.

---

## 1. LO QUE ESTÁ SANO (y conviene decirlo antes que lo otro)

**La coordinación no tiene un solo fallo.** La ronda de hoy: **34 eventos, 15 voces, 50 conexiones
reconstruidas, 27 testigos independientes, 0 fallos de coordinación** — nadie se quedó sin
contestar, ninguna señal cayó en el vacío, ningún ciclo.

**Los testigos son de verdad independientes.** En las tres preguntas de la ronda, voces y testigos
coinciden (4/4, 5/5, 8/8): nadie está repitiendo a otro. Es la métrica que existe para que ocho
órganos repitiendo a un noveno no cuenten como ocho.

**El portero funciona en producción, no en el banco.** Dos intentos bloqueados en vivo:
`G13_poder` intentando publicar una `decision` estando en modo `mide`, y `G4_contingencia`
intentando una `senal`. La constitución se ejecuta, no se recita.

**La estructura no tiene huérfanos.** Cada gen tiene módulo, Regla 31 y banco. Ningún módulo suelto.

**Dos capacidades medidas que no se han celebrado bastante:**
- **G15 metacognición: AUC 0.8292 contra un nulo de 0.5883.** Diego **sabe cuándo se equivoca**,
  muy por encima del azar. Es de lo más sólido que tiene.
- **G13 poder: lazo cerrado 0.0297 contra lazo abierto 0.0191.** Cerrar el lazo lo mejora.

---

## 2. HALLAZGO PRINCIPAL — **el tacto está muerto en la práctica**

En la ronda de hoy, el sentido del tacto reportó:

```
sentido_tacto  respuesta #cuerpo  {"canales": 3, "fraccion_con_contacto": 0.0001}
```

**Uno de cada diez mil pasos.** Diego tiene un sentido del tacto que **prácticamente nunca se
enciende**, porque su brazo **no toca nada**. Balbucea en el aire, en un mundo donde el único objeto
interesante está deliberadamente fuera de su alcance.

**Esto no es un fallo del órgano: es la consecuencia de un diseño nuestro**, y explica de golpe
varias cosas que veníamos tratando como problemas separados:

| Síntoma que veníamos investigando | Lo que el tacto muerto explica |
|---|---|
| El observador pasivo **empata** con el encarnado (H-002) | nuestro "encarnado" en la práctica también está mirando |
| La visión **lee la escena y no el movimiento** | nada en su mundo se mueve por causa suya salvo su propio brazo |
| Ningún nodo del árbol es **causal** | la causalidad exige intervención, y no hay intervención |
| Las firmas conductuales **no se pueden medir** | no tiene sobre qué producir un efecto que valga la pena repetir |

**Un ente con un sentido que nunca se enciende no es un ente con un sentido de más: es un ente al
que no le hemos dado nada que tocar.** Es la conclusión más importante de esta auditoría, y va
directa al prerregistro 37.

## 3. HALLAZGO 2 — **dos genes diseñados y nunca construidos**

| Gen | Estado | Módulo |
|---|---|---|
| `G11_temple` | inactivo | **ninguno** |
| `G12_reflejos` | inactivo | **ninguno** |

Están en el genoma como diseño y **no existen como código**. No es una fuga ni un riesgo —el
gatekeeper los tiene en `inactivo` y no pueden publicar nada— pero el genoma **promete dos órganos
que no hay**. O se construyen con su prerregistro, o se marcan explícitamente como *diseño no
implementado* para que nadie los cuente al describir el sistema.

**Propuesta:** marcarlos como diseño pendiente ahora, y construirlos solo cuando haya una pregunta
que los necesite (Regla 18: cada corrida nace de una pregunta abierta). Construir órganos porque
están en una lista es exactamente cómo se acumula código muerto.

## 4. HALLAZGO 3 — **una pregunta del árbol lleva un mes contestada y sigue abierta**

`ARBOL.md` muestra como pregunta abierta:

> **P1** — *"¿Nulos surrogados de las campañas insignia? (mendeley: se corre en la NUBE vía
> Actions; p14 espera ojos)"*

**Los cuatro nulos corrieron y están en disco desde la auditoría AUD-01:**

| Campaña | Nulo | ¿halló ley en el mundo falso? | Lectura |
|---|---|---|---|
| Mendeley (N-001-E2) | surrogado | **NO** | **el nodo sobrevive** |
| Mendeley (N-001-E2) | barajado | **NO** | **el nodo sobrevive** |
| Caída | surrogado | **NO** | el nodo sobrevive |
| p14 latentes (N-002/003) | surrogado | **SÍ** | el nodo fue degradado |

La pregunta está respondida y **con la respuesta más importante del árbol dentro**: **N-001-E2 es el
único nodo que se enfrentó a los dos verdugos y salió vivo.** Llevaba un mes escondida en una
pregunta marcada como pendiente.

**Corregido en esta auditoría:** P1 se cierra en `ARBOL.md` con su respuesta.

## 5. LO QUE LA PROPIA SÍNTESIS DE DIEGO DECLARA QUE NO PUEDE AFIRMAR

La síntesis de la ronda de hoy —el evento donde Diego junta lo que dijeron sus quince órganos—
cerró con estas tres renuncias, escritas por él:

- *"no afirma: que la vista sirva para hallar el cuerpo (el torneo quedó no concluyente por
  instrumento)"*
- *"no afirma: ninguna ley del universo: esto es PyBullet haciendo de mundo"*
- *"no afirma: **que la conducta siga a la detección: Diego detecta contingencia y aún no actúa
  sobre ella**"*

**La tercera es el diagnóstico central del sistema, y lo nombra él mismo.** Detecta que algo obedece
a sus órdenes, y no hace nada con esa información. Es la definición operativa de lo que le falta
para ser un ente que experimenta en lugar de uno que observa.

## 6. ESTADO REAL DEL CONOCIMIENTO (lo que la auditoría obliga a decir)
- **Escalera de la Regla 19:** todos los nodos en **nivel 1**. Cero en nivel 2, cero en nivel 3.
  Ningún experimento físico propio.
- **Comparador:** cero `CONTRADICE`, cero `SIN EQUIVALENTE`. Ver COMPARADOR-02, que corrige el
  informe de julio.
- **Afirmaciones causales: cero.**
- **Lo único limpio y propio:** el puente de unidades (π/180), que es real y **no es una ley de la
  naturaleza**.

## 7. LO QUE SE HACE CON ESTA AUDITORÍA
1. **Cerrar P1 en `ARBOL.md`** con su respuesta. — hecho en este mismo commit.
2. **Marcar G11 y G12 como diseño no implementado** en el genoma, para que nadie los cuente como
   órganos existentes. — hecho.
3. **El tacto muerto va al prerregistro 37** como su justificación principal. No se arregla
   ajustando el sensor: se arregla dándole algo que tocar y una razón para tocarlo.

## 8. LA LECTURA DE FONDO, PARA EL DIRECTOR
Usted dijo que cada fallo son más datos para entender dónde falla el modelo. Esta auditoría es
exactamente eso, y su resultado se resume en una frase:

> **El sistema de Diego está bien construido y mal alimentado.** Los órganos hablan, se escuchan, se
> bloquean cuando deben, cuentan testigos y declaran lo que no saben. Lo que no tienen es **un mundo
> sobre el que actuar**. Le construimos un aparato sensorial completo y lo pusimos a mirar.

Nada de lo que sigue —causalidad, razonamiento, experimentar como experimenta un humano— es posible
mientras el tacto marque 0.0001. **Ese número es el cuello de botella del proyecto entero**, y es
barato de arreglar: no hace falta un órgano nuevo, hace falta ponerle algo al alcance de la mano.

---
**Traza:** ronda de vida del 10-ago-2026 en `arbol/SINAPSIS.jsonl`; `codigo/trazar.py`,
`codigo/mente.py`, los cuatro guardianes en verde; nulos crudos en `resultados/aud01-*`.
