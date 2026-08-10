# Prerregistro 42 — ¿Debe el escalón 1 aislar UN canal, o puede declarar varios no-yos? — 10 de agosto de 2026
**Autorizado por el director el 10-ago-2026 ("la 1 sí"), sobre la PENDIENTE 1 de
`registros/FIRMAS-PENDIENTES.md`.**

---

## 0. LA CONFESIÓN QUE VA PRIMERO, PORQUE CAMBIA CÓMO SE DEBE LEER TODO LO DEMÁS
**Esta pregunta se me ocurrió porque un criterio falló.** El prereg-35 pedía que `altura` fuera el
**único** canal apto en el escalón 1; salió **PARCIAL** (INFORME-42): en 3 de 5 mundos se cumplió,
y en 2 el canal `contacto` también pasó — por **0.016 sobre un piso de 0.30**.

Solo entonces pensé: *"un mundo tiene más de una cosa que no soy yo; quizá exigir un único apto era
la exigencia equivocada"*. El argumento es bueno. **Y el momento en que se me ocurrió lo hace
sospechoso**, porque ésa es la definición exacta de una racionalización a posteriori. Por eso esta
decisión no la tomé por quórum y esperó la palabra del director: no es una decisión sobre **cómo
medir**, es sobre **qué queremos que sea verdad**.

**Consecuencia operativa, y es la parte que hace honesto este prerregistro:** los cinco mundos del
prereg-35 **quedan quemados** para esta pregunta. La hipótesis nació mirándolos; volver a usarlos
sería examinar con las respuestas delante. **Se corre sobre cinco semillas nuevas que nunca se han
usado**, declaradas aquí antes de tocarlas: `71, 73, 79, 83, 89`.

---

## 1. LA PREGUNTA, en una frase
> Cuando Diego separa lo que es su cuerpo de lo que no lo es, ¿el instrumento debe exigir que
> **exactamente un** canal quede marcado como suyo, o debe permitir que **varios** canales queden
> marcados como *no-yo* siempre que el suyo gane con margen?

## 2. LAS DOS HIPÓTESIS, y ninguna es la favorita
| | Qué afirma | Qué implicaría si gana |
|---|---|---|
| **H-AISLAR** (el criterio viejo) | el escalón 1 debe dejar **un solo** canal apto | el instrumento es específico: distingue *mi cuerpo* de *todo lo demás* |
| **H-VARIOS** (el criterio nuevo) | basta con que el canal propio **gane con margen**, aunque otros pasen el piso | el mundo tiene varias cosas que no soy yo, y exigir unicidad era una exigencia del diseñador, no del problema |

**Declaro cuál me conviene:** me conviene H-VARIOS, porque convierte un PARCIAL en un limpio. **Por
eso el criterio de abajo está escrito para que H-VARIOS pueda perder**, y por eso hay una condición
donde pierde incluso si los números salen bonitos (§5, el señuelo).

## 3. LA LÍNEA BASE TONTA (Regla 12, obligatoria desde hoy)
El instrumento (`soporte.escalon1`) mira **7 canales**: 3 ángulos del brazo, `altura`, `contacto`,
`vel_z` y un canal de **ruido señuelo**. El predictor ingenuo es **elegir un canal al azar**: acierta
`altura` **1 de 7 veces = 0.143**. Ése es el suelo, y todo puntaje de este estudio se reporta como
**ganancia sobre 0.143**, nunca como acierto crudo.

*(Este párrafo existe por el daño del 10-ago: en G12 medí un acuerdo de 0.907 que parecía excelente
y el tonto sacaba 0.887. Nunca más un puntaje sin su línea base al lado.)*

## 4. EL CRITERIO, congelado antes de correr — y lo que ya sé, declarado
**LO QUE YA SÉ Y NO PUEDO DES-SABER (va aquí para que se pueda descontar al leerme):** en los cinco
mundos quemados, `altura` fue apto **5/5** con autopredictibilidad **0.4175 · 0.5026 · 0.4519 ·
0.6121 · 0.6489**, y `contacto` cruzó el piso solo en dos, con **0.3160 — por 0.016 sobre 0.30**. Es
decir: el margen de `altura` sobre `contacto` en esos mundos fue de **~0.30**. **Cualquier umbral que
yo elija hoy está informado por esos números**, y fingir lo contrario sería peor que decirlo.

Sobre las **5 semillas nuevas** (`71, 73, 79, 83, 89`) se corre `escalon1` y se registra, por mundo:
la lista `candidatos_aptos`, el `candidato` elegido, y la autopredictibilidad de cada apto.

1. **H-AISLAR gana** si en **≥4 de 5** mundos `candidatos_aptos` tiene **exactamente un** elemento
   y ese elemento es `altura`.
2. **H-VARIOS gana** si se cumplen **las dos** condiciones:
   **(a)** `candidato == "altura"` en **5 de 5** — sin excepción: si el instrumento no elige bien
   ni una vez, no hay nada que discutir sobre cuántos aptos admite; y
   **(b)** la autopredictibilidad de `altura` supera a la del **mejor apto ajeno** por **≥0.10** en
   **≥4 de 5** mundos.
   **Por qué 0.10 y no otro número:** es **6 veces** el 0.016 que provocó el PARCIAL —así el
   aprobado raspado queda excluido sin ambigüedad— y **un tercio** del ~0.30 que vi en los mundos
   quemados, para no fijar el listón pegado a lo observado. Si lo hubiera puesto en 0.25 estaría
   copiando el resultado; si lo pusiera en 0.02 estaría regalando el aprobado.
3. **Si ganan las dos**, gana **H-AISLAR**. El criterio viejo se mantiene salvo que el nuevo lo
   supere sin empate: **el que propone el cambio carga con la prueba.**
4. **Si no gana ninguna**, veredicto **NO CONCLUYENTE**, y el prereg-35 **se queda PARCIAL** como
   está hoy. Ése es un resultado legítimo, no un fracaso.

**Dónde puede perder H-VARIOS, que es lo que hace que esto sea una prueba:** si en los mundos nuevos
`altura` deja de ser el elegido aunque sea una vez (2a), o si el margen se estrecha por debajo de
0.10 en dos mundos (2b). Las dos son posibles: los mundos nuevos sortean mesa, altura de soltada,
masa y posición, y ya se vio que **la geometría mueve la autopredictibilidad de `contacto`** — fue
exactamente lo que la hizo cruzar el piso en las semillas 4 y 5.

## 5. REGLA 31 — LOS DOS LADOS, y el señuelo que puede matar el estudio
- **Debe fallar donde no hay nada:** con los canales **barajados entre sí** (ningún canal es el
  propio), ningún criterio puede declarar un apto. Si alguno lo declara, el instrumento está roto y
  el estudio se detiene **antes** de mirar el resultado real.
- **Debe aprobar donde sí hay:** con un canal propio **amplificado a propósito** (señal limpia),
  los dos criterios deben encontrarlo. Un instrumento que no ve lo evidente no sirve para juzgar lo
  sutil.
- **EL SEÑUELO:** se incluye un mundo donde **dos canales son propios de verdad** (dos partes del
  mismo cuerpo). Ahí **H-AISLAR debe fallar por construcción** — y si aun así "acierta", es que el
  criterio no mide lo que dice medir, y **el estudio se declara NULO completo**, gane quien gane.

## 6. CUÁNDO SE ABANDONA (Regla 13 endurecida — con número, no con adjetivos)
- Si el control negativo del §5 declara **1 o más** aptos → **se detiene**, no se reporta nada.
- Si el señuelo del §5 aprueba a H-AISLAR → **NULO**, se escribe el acta y se cierra la pregunta.
- Si tras las 5 semillas el veredicto es NO CONCLUYENTE → **no hay tercera vuelta**. La pregunta se
  archiva con el prereg-35 en PARCIAL. **Se declara aquí para que no exista la tentación de seguir
  intentándolo hasta que salga.**

## 7. LA PREDICCIÓN, comprometida
Espero que gane **H-VARIOS**, y ya dije por qué eso me conviene. **Mi expectativa no es evidencia**,
y el §5 está construido para castigarla: si el canal propio no gana por 0.10 —seis veces el margen
que vi— pierdo, y el prereg-35 se queda PARCIAL para siempre.

## 8. LO QUE ESTE ESTUDIO **NO** PUEDE AFIRMAR
- **Nada sobre el universo.** Es sobre un instrumento nuestro y sobre cómo se debe leer.
- **No revive el prereg-35.** Gane lo que gane, aquel estudio se queda como quedó: su acta no se
  reescribe (Regla 8). Lo que cambia, si acaso, es el criterio de los estudios **futuros**.

## 9. EN QUÉ PELDAÑO ESTAMOS (Regla 9)
**Fase 1 — sistemas con respuesta conocida.** El mundo es PyBullet y la respuesta la conoce el
simulador; lo que se examina es **nuestro instrumento**, no el universo. **No se sube de peldaño con
este estudio**, y no se subirá mientras la Fase 1 no funcione de punta a punta: hoy no funciona —
el prereg-39 acaba de salir negativo.

## 10. NIVEL Y FIRMA
**Nivel 1** — correlación en simulador. No sube de nivel: no hay experimento físico aquí.
**Firmado por el director** (10-ago-2026, *"la 1 sí"*), que es lo que lo hace legítimo: el criterio
lo movió quien tenía potestad para moverlo, y no yo después de ver los datos.
