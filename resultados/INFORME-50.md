# INFORME-50 — EL MOTOR SIMBÓLICO NO ES INVARIANTE A LA ESCALA (y lo encontró un órgano que nadie había examinado)
**10 de agosto de 2026. Hallazgo de ingeniería, no de física. No genera nodo.**
**Datos crudos:** `resultados/p43-escala-sindy3/medida.json`. Módulo implicado: `codigo/sindy3.py`.

---

## 1. QUÉ SE ENCONTRÓ, en una frase
**La misma ley, sobre los mismos datos multiplicados por una constante, se encuentra o no según la
constante.**

| escala de los datos | ¿encuentra la ley? |
|---|---|
| ×0.1 | **NO** |
| ×1 | sí |
| ×10 | sí |
| ×100 | **NO** |

Los datos son un oscilador amortiguado limpio (4000 muestras, `dt=0.02`, ruido 0.002). **Lo único
que cambia entre las cuatro filas es un factor multiplicativo** — es decir, las unidades.

## 2. CÓMO APARECIÓ, que importa tanto como el hallazgo
No se buscaba. Salió al pasar **G9 (el sueño)** por LA PUERTA — uno de los seis órganos que llevaban
meses publicando sin haber sido examinados nunca. Su ficha de sanidad incluye un **señuelo de
escala** (multiplicar el mundo por 10 no puede cambiar lo que se descubre), y ese señuelo se puso
rojo: con el mundo ×10 sobrevivían **0 leyes en vez de 3**.

Persiguiendo la causa: **no era el sueño.** Los sueños escalan bien (±1.53 → ±15.3, todo finito, el
modelo del mundo se ajusta igual). El que falla es **`sindy3`, el motor simbólico de la casa**.

**La lección de método:** el defecto llevaba ahí desde que existe el motor y ningún guardián lo
tocaba, porque nadie había preguntado *"¿y si los mismos datos vinieran en otras unidades?"*. Lo
encontró **una prueba de un órgano que ni siquiera es el motor**. Ése es el argumento entero a favor
de pasar por la puerta también lo que ya lleva meses funcionando.

## 3. POR QUÉ ESTO IMPORTA MÁS DE LO QUE PARECE
La **Regla 2** exige el dato más crudo posible: píxeles, voltajes, conteos. **Los datos crudos vienen
en las unidades que vengan** — píxeles de una cámara, milímetros, cuentas de un sensor. Si el motor
solo ve leyes dentro de una banda estrecha de magnitud, entonces:

- **una ley pudo haberse perdido por venir en las unidades equivocadas**, y lo habríamos leído como
  "no hay ley aquí";
- y peor: **un resultado negativo del proyecto no es interpretable** hasta saber si el motor estaba
  dentro de su banda. Eso toca a todos los "no concluyente" que llevamos.

**Lo que NO se puede concluir todavía:** cuáles de nuestros resultados pasados están afectados. Eso
exige medirlo campaña por campaña, y **no se hace hoy con el hallazgo caliente delante**.

## 4. LO QUE **NO** SE HACE
- **No se toca `sindy3`.** Normalizar antes de ajustar y re-escalar los coeficientes después es el
  arreglo estándar y probablemente el correcto — **y cambiar el motor de descubrimiento del
  proyecto sin prerregistro es exactamente lo que las reglas prohíben.** Va en el prerregistro 45.
- **No se sella G9.** Su ficha reprueba, y reprueba por una causa real que no es suya. Queda
  declarado que **G9 no ha pasado la puerta**, con el motivo escrito, en vez de forzarlo.
- **No se degrada ningún nodo todavía.** Primero hay que medir el alcance; degradar por precaución
  sin medir sería tan poco riguroso como no hacer nada.

## 5. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuál es la banda de escala en la que el motor ve, y qué campañas nuestras cayeron fuera?**
> Se contesta midiendo: barrido de escala sobre un sistema conocido para hallar los bordes, y
> después el mismo barrido sobre los datos de cada campaña insignia.

## 6. LO QUE ESTE HALLAZGO SÍ AFIRMA
- **Es reproducible y determinista:** semillas fijas, 4000 muestras, cuatro escalas, mismo
  resultado en cada corrida.
- **Es del motor, no del sueño:** verificado aislando `sindy3.descubrir` sin ninguna capa encima.
- **No dice nada del universo.** Es una propiedad de nuestro código.

## 7. LA DECISIÓN QUE LE TOCA AL DIRECTOR
Ninguna urgente, pero sí una que conviene que sepa: **es la primera vez que un defecto del motor
central sale a la luz**, y salió porque empezamos a examinar órganos que llevaban meses corriendo
sin examen. Quedan **12 órganos más sin pasar la puerta**. Si uno solo de ellos esconde algo
parecido, prefiero encontrarlo yo a que lo encuentre un revisor externo.
