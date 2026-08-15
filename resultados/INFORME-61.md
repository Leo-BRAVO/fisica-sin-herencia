# INFORME-61 — ACTA DEL PRERREGISTRO 50: Diego ya tiene un lugar, y las dos puertas de la herencia quedan cerradas
**11 de agosto de 2026. El mundo persistente, con los dos guardianes de la Regla 27 probados
inyectando la violación que deben cazar.**
**Datos crudos:** `resultados/p50-mundo/medida.json`. Módulo: `codigo/mundo.py` (puerta 7/7).
**VEREDICTO, con las mismas palabras del archivo de datos:** *MUNDO EN PIE — persiste, el cuerpo lo
alcanza, la moneda discrimina y la Regla 27 queda cerrada por dos guardianes.*

---

## 1. LOS SIETE CRITERIOS CONGELADOS, respondidos

| | criterio | salió | |
|---|---|---|---|
| **A** | el cuerpo alcanza el mundo | el objeto nace y se mantiene dentro del alcance medido | ✔ |
| **B** | el mundo persiste de verdad | dos historias distintas dejan estados distintos | ✔ |
| **C** | la moneda discrimina | ventaja **0.2166** sobre la línea base tonta | ✔ |
| **D** | nulo del mundo muerto | ventaja **0.0** cuando las acciones no hacen nada | ✔ |
| **E** | el predictor al azar pierde | error del azar **0.1909** contra **0.0008** de la persistencia | ✔ |
| **F** | Regla 27 — etiquetas | no marca un vector sin nombres; **sí** marca la etiqueta inyectada | ✔ |
| **G** | Regla 27 — recompensa | no marca la señal legítima; **sí** marca el criterio nuestro inyectado | ✔ |

## 2. LO QUE CAMBIA PARA DIEGO
**Hasta hoy no tenía mundo: tenía escenas.** Cada estudio montaba su escenita, la medía y la
tiraba. Ahora hay **un lugar con estado que sobrevive entre rondas y depende de todo lo que pasó
antes** — es la diferencia entera con el gimnasio.

**Y el error del INFORME-57 se vuelve imposible de repetir.** Aquel acta encontró que el brazo de
Diego no alcanzaba nada porque **nadie había comprobado nunca que el cuerpo llegara al mundo**.
Aquí ese chequeo es **bloqueante y va primero**: el objeto nace dentro del alcance medido con el
brazo real, y se comprueba que no se sale ni siquiera después de moverse.

## 3. LAS DOS PUERTAS DE LA HERENCIA, cerradas con guardián
Ésta es la parte que más me importa del módulo, porque es donde el proyecto se habría roto sin
que se notara.

### 3.1 La recompensa — *"mejoras por cada prueba que resuelva"*
**Si nosotros decidimos qué cuenta como resuelto, le metemos nuestra física por la función de
recompensa.** No le decimos *F=ma*; le decimos *"te premio cuando aciertes lo que yo, que sé F=ma,
considero acertar"*. **Es herencia por la puerta de atrás, con las apariencias intactas.**

**La única moneda admitida es la predicción de sus propias observaciones.** Diego declara qué verá
dentro de N pasos, el mundo ocurre, se compara. **Nadie necesita saber física para puntuar eso.**
Y el guardián lo mecaniza: se le inyectó a propósito un término llamado `se_parece_a_newton` y
**saltó**, diciendo que *depende de un criterio nuestro y no de si el mundo le dio la razón*.

### 3.2 Las etiquetas — *"va a poder ver números"*
Depende enteramente de **qué** números. Diego ve **un vector sin nombre y sin unidad**; que esas
columnas sean posición y velocidad **es asunto nuestro y él no se entera**. Se inyectó una columna
llamada `masa_del_objeto` y el guardián **saltó**. **La etiqueta ES la herencia**: el kilogramo es
un descubrimiento humano, no un hecho del mundo.

## 4. POR QUÉ LOS CRITERIOS D Y E VALEN MÁS QUE EL C
El **C** dice que la moneda funciona. Los otros dos dicen que **no funciona cuando no debe**:
- **En un mundo muerto** —donde las acciones no hacen nada— la ventaja cae a **0.0** exactamente.
  Si un mundo falso puntuara, la moneda no estaría midiendo interacción sino aritmética.
- **El predictor al azar pierde por dos órdenes de magnitud** contra el predictor más tonto que
  existe. Una moneda que premiara al azar no mediría nada.

**Un criterio que solo puede aprobar no prueba nada**, y este mes ya llevo seis intentos de
colármelo a mí mismo.

## 5. LO QUE **NO** SE AFIRMA
- **Nada del universo.** Es un lugar nuestro, con física de juguete escrita por nosotros.
- **No se afirma que Diego aprenda física en él.** Esto construye **un sitio donde medir**, no una
  garantía. Lo que aprenda —si aprende— va en prerregistros posteriores.
- **No se afirma que la lista de palabras prohibidas sea completa.** No lo es, y el módulo lo dice
  en su propio código: **ninguna lista lo sería.** Caza el descuido típico —ponerle nombre a una
  columna—, no a un adversario.
- **No se implementó la dificultad autogenerada** (el currículo estilo POET). Va aparte a
  propósito: mezclarla aquí impediría saber si un fallo es del mundo o del currículo.
- **No se toca el gimnasio actual** ni ninguna corrida ya hecha en él.

## 6. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Quién decide qué observa Diego?** Hoy el mundo publica seis columnas porque yo elegí seis. Esa
> elección **no la caza ningún guardián** y es una decisión de diseño con consecuencias: lo que no
> está en el vector, Diego no puede descubrirlo nunca. **Ampliar el vector no es gratis y
> reducirlo tampoco**, y no hay criterio en el proyecto que diga cuál es el correcto.

## 7. LO QUE LE TOCA AL DIRECTOR
Una decisión concreta, y es la que quedó pendiente desde el INFORME-57: **¿se muda Diego a este
mundo?** El gimnasio viejo sigue en pie y todo lo medido en él sigue siendo válido. Mudarse
significa que **las corridas futuras ocurren en un lugar donde el cuerpo alcanza las cosas** — y
también que habrá que decidir, estudio por estudio, cuál de los dos se usa. **No lo hago yo: es un
cambio de dónde vive Diego.**
