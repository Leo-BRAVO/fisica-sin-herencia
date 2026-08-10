# INFORME-54 — EL MOTOR ALUCINA LEYES SOBRE SEÑAL CASI CONSTANTE, con confianza 1.0
**10 de agosto de 2026. El señuelo del prerregistro-45 aprobó donde no debía.**
**Datos crudos:** `resultados/p45-senuelo/medida.json`. Módulo implicado: `codigo/sindy3.py`.
**VEREDICTO, con las mismas palabras que el archivo de datos:** *EL SEÑUELO DEL PRERREGISTRO 45
APRUEBA DONDE NO DEBE: el motor declara ley en 20 de 25 casos sin dinamica, con confianza 1.0. Por
el criterio congelado del propio prerregistro, el estudio de la banda de escala queda NULO.*

---

## 1. LO QUE PASÓ
El prerregistro-45 iba a medir la banda de escala del motor. Antes de correrlo, su **señuelo**
—declarado por escrito— decía:

> *"Un sistema **sin dinámica** (constante más ruido) escalado igual no puede dar ley en ninguna
> escala. Si la da, **NULO**."*

**La dio.** Y no en un caso raro:

| qué se le dio al motor | declara ley |
|---|---|
| **constante + ruido diminuto** (nada que descubrir) | **20 de 25** |
| ruido puro, para comparar | **0 de 15** |

## 2. LO QUE DEVUELVE, QUE ES PEOR QUE EL CONTEO
Sobre una constante, el motor **no** contesta *"la derivada es cero"*. Contesta esto:

```
dx/dt = −49.54·1 − 48.09·x − 195.26·v + 24.77·x² + 50.97·xv − 46.67·v²
dv/dt = −103.35·1 + 20.59·x − 165.85·v + 10.26·x² + 61.74·xv − 21.25·v²
```

**Seis términos por ecuación, coeficientes entre 20 y 195, y confianza 1.0 en casi todos.**

## 3. POR QUÉ PASA, y por qué el nulo de ruido no lo cazaba
Con una señal casi constante, todos los términos de la biblioteca (`1, x, v, x², xv, v²`) son **casi
colineales entre sí**: todos valen casi lo mismo en todas las filas. La regresión queda
**malcondicionada** y encuentra combinaciones enormes que se cancelan entre ellas y ajustan el ruido
diminuto. Y el bootstrap le da **confianza 1.0** porque cada re-muestreo cae en la misma solución
degenerada: *todos los remuestreos se equivocan igual*.

**El ruido puro no dispara esto** porque sus términos sí varían y la regresión está bien
condicionada — por eso el control negativo que teníamos desde siempre pasaba limpio. **El régimen
peligroso no era el ruido: era la quietud.**

## 4. POR QUÉ ESTO IMPORTA MÁS QUE LA BANDA DE ESCALA
**Una señal casi constante no es un caso de laboratorio: es media física.** Un objeto ya asentado,
un sensor saturado, un canal en reposo, **una cantidad que se conserva**. El proyecto entero busca
regularidades, y las regularidades más limpias son justamente las cosas que **no cambian**.

**Lo que sí puedo afirmar hoy:** el motor `sindy3` declara leyes elaboradas, con confianza máxima,
sobre datos donde no hay nada que declarar, siempre que la señal tenga poca variación propia.

**Lo que NO puedo afirmar todavía, y no lo voy a insinuar:** cuáles de nuestros resultados están
tocados. `conservada.py` (que produjo N-004) es una herramienta **distinta**, con su propio nulo
surrogado que sí aprueba la Regla 31. Decir "esto invalida el árbol" sería tan poco riguroso como
decir que no toca nada. **Hay que medirlo, campaña por campaña, y no es lo que se hizo hoy.**

## 5. EL ESTUDIO DE LA BANDA DE ESCALA QUEDA **NULO**
Su propio prerregistro lo dijo: *si el señuelo aprueba, NULO*. **Se cumple sin discutirlo.** La
medida del barrido no se reporta ni se usa, aunque el módulo ya estaba escrito y el barrido habría
corrido en minutos.

**Y por qué no me limito a "arreglar el señuelo":** porque el señuelo funcionó. Detectó un defecto
real y más grave que el que el estudio buscaba. Reescribirlo para que pase sería exactamente lo que
este proyecto existe para no hacer.

**Lo que sí queda anotado como error de diseño mío:** metí en la Regla 31 de mi instrumento una
prueba sobre el **objeto de estudio** (el motor), no sobre **mi procedimiento de medida**. Por eso
un defecto del motor bloquea mi propio módulo. El prerregistro-46 rehace el barrido con esa
separación clara — y ahí el comportamiento del motor será **resultado**, no requisito de entrada.

## 6. LA PREGUNTA QUE ABRE (Regla 18)
> **¿A partir de qué variación propia empieza el motor a alucinar?** Hay un umbral en algún sitio
> entre "casi constante" (alucina) y "oscilador limpio" (acierta). Encontrarlo daría un criterio
> mecánico de *cuándo NO se le puede preguntar al motor* — que es más útil que un arreglo a ciegas.

## 7. LA DECISIÓN QUE LE TOCA AL DIRECTOR
Ninguna urgente, pero sí una que quiero que sepa con todas sus letras: **hoy es el segundo defecto
del motor central que aparece, y los dos aparecieron el mismo día, porque el mismo día empezamos a
examinar cosas que llevaban meses corriendo sin examen.** El primero (la banda de escala) produce
falsos negativos. **Éste produce falsos POSITIVOS**, que es la clase de error que este proyecto se
prohibió desde la primera regla.
