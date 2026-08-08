# Prerregistro 24 — La búsqueda del cuerpo: cómo se elige un diseño de Gimnasio sin hacer trampa — 8 de agosto de 2026
**Estado: FIRMADO por el director el 8-ago-2026 ("as tambien esto"). El protocolo se escribió ANTES
de mirar los resultados; la firma llegó después de ejecutarlo y de que su predicción fallara —
lo cual queda, a propósito, como demostración de que el protocolo funciona aunque el que lo
escribió se equivoque.**

---

## El problema que este documento resuelve

El director ordenó: *"repensemos el Gimnasio como nadie lo ha hecho, probemos muchas variables sin
violar las reglas y sigamos hasta tener la mejor."*

Probar muchos diseños es correcto. Pero **elegir el diseño que supera la prueba es, en sí mismo, una
forma de ajuste** — la misma familia de vicio que llevamos toda la semana cazando, solo que un piso
más arriba: en vez de mover la vara, se mueve el mundo hasta que la vara diga que sí.

La diferencia entre ingeniería honesta y autoengaño es el protocolo. Aquí está.

---

## Qué se puede variar y por qué es legal

Todo lo que se varía es **el cuerpo de Diego y su cámara**. Nada es un hecho sobre el mundo, así
que nada contamina (Reglas 1–4). Se confiesa cada perilla:

| Variable | Qué es | Por qué es legal |
|---|---|---|
| **amortiguación** | rozamiento viscoso en sus articulaciones | un miembro real lo tiene; es su cuerpo, no el universo |
| **límite articular** | tope de giro | su cuerpo tiene forma; una articulación que gira infinito es lo raro |
| **suavizado del balbuceo** | cuán lentos son sus impulsos | G7 (juego); el prereg-19 ya autoriza explorarlo |
| **amplitud del balbuceo** | cuán fuertes | ídem, rango {N, 2N} ya firmado |
| **subpasos** | cada cuántos pasos de física observa | su tasa de muestreo, no una propiedad del mundo |

**Lo que NO se toca, ni una coma:** el criterio del prerregistro-23 (h=8, ventana=150, piso 0.02,
fracción 0.40, mínimo 20 ventanas), los episodios-juez congelados, el nulo por desplazamiento
circular, y la verdad cuerpo/mundo que Diego jamás ve.

## Puntuación (fijada antes de mirar)
Por cada uno de los cuatro mundos de control se cuentan las **variables bien clasificadas de las 7**
(cuerpo cuando es cuerpo, mundo cuando es mundo). Máximo 28 puntos. No hay ningún otro criterio:
ni "se ve mejor", ni "el número me gusta más".

---

## EL PROTOCOLO CONTRA EL AUTOENGAÑO (la parte que importa)

1. **La búsqueda corre sobre las semillas 1000–1011.** Ese conjunto queda quemado: cualquier
   número que salga de ahí es exploratorio y **no puede citarse como resultado**.
2. **El ganador se verifica sobre semillas FRESCAS (7000–7011)** que la búsqueda nunca vio. Solo
   ese segundo número cuenta como medición.
3. **Si el ganador cae al verificar, se reporta la caída.** Un diseño que solo funciona en las
   semillas donde se buscó es un diseño sobreajustado, y decirlo es el resultado.
4. **El número de diseños probados se declara.** Probar 8 diseños y quedarse con el mejor infla el
   resultado esperado; el lector tiene que saber cuántas veces se tiró el dado.
5. **El criterio no se toca durante la búsqueda.** Si ningún diseño llega, el veredicto es que
   ningún diseño llegó — no que el criterio era muy exigente.

## Criterio de parada (para no buscar para siempre)
Se declara **antes**: máximo **dos rondas** de barrido. Si tras la segunda ronda ningún diseño
alcanza en semillas frescas el criterio del prerregistro-23 en los cuatro controles, se registra
**FRACASO DEL HITO 0** con su diagnóstico, y se detiene. La Regla 13 existe para esto: abandonar un
enfoque que no funciona no es fracaso del proyecto, es el proyecto funcionando.

## Predicción comprometida
Espero que la **amortiguación** sea la variable dominante, por una razón mecánica declarada antes
de ver nada: sin rozamiento, la velocidad de una articulación es historia acumulada y el par solo
añade un empujón marginal; con rozamiento, la velocidad SIGUE al par (respuesta de primer orden) y
el cuerpo se vuelve aprendible en un solo paso. Espero que el límite articular ayude menos, y que
el suavizado y los subpasos casi no muevan la aguja.

## ANEXO POST-RESULTADOS (registrado el 8-ago-2026, DESPUÉS de ver los números — Regla 8)
El director preguntó: *"ahora que viste los resultados, ¿qué cambiaríamos o mejoraríamos en la
búsqueda de cuerpo?"*. Respuesta con la evidencia delante, para la próxima ronda:

1. **La búsqueda optimizó el cuerpo para el DETECTOR, no para los OJOS.** Ganamos 28/28 sobre el
   estado del simulador y el hito 0 visual siguió fracasando (0.38 contra piso 0.40). La próxima
   búsqueda debe puntuar TAMBIÉN cuán legible es el cuerpo para una cámara: el R² con que unos
   ojos frescos leen las articulaciones. Es una variable de diseño legal — es SU cuerpo y SU
   cámara — y ataca el fallo medido (ojos que leen escena y no brazo).
2. **La visibilidad es una variable de cuerpo y no la exploramos.** Grosor del brazo, contraste
   contra el fondo, encuadre de la cámara: todo eso decide cuántos píxeles cuesta ignorarlo, y la
   pérdida por píxel ignora lo que ocupa poco. Ronda 3 debe barrer visibilidad.
3. **La potencia estadística se decide ANTES.** Dos veces nos mordió el número de ventanas; el
   mínimo de 20 ahora está en el código, pero el diseño de cada ronda debe declarar sus ventanas
   esperadas antes de correr.
4. **Presupuesto declarado:** 8 diseños en ronda 1-2. Toda ronda declara cuántos dados tira.

- **Firmado:** Leo, director — 8-ago-2026, aprobación en conversación ("as tambien esto"), con el
  anexo post-resultados marcado como tal.
