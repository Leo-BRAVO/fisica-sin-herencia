# Prerregistro 44 — ¿POR QUÉ UN BRAZO PROPIO PUEDE PARECER "NO MÍO"? — 10 de agosto de 2026
**Nace del hallazgo no anticipado del prereg-42 (INFORME-48).**
**Peldaño (Regla 9): Fase 1** — sistema con respuesta conocida (el simulador sabe qué es el brazo).
**No se sube de peldaño.**

---

## 0. EL HALLAZGO QUE LO ORIGINA, con su número
Corriendo el prereg-42 sobre cinco mundos nuevos, en el mundo **73** el escalón 1 declaró apto —es
decir, **no-mío**— al canal **`art1`, una articulación del propio brazo de Diego**:

| canal (mundo 73) | autopredictible | obediencia neta | ¿legal? | ¿no-mío? |
|---|---|---|---|---|
| art0 | 1.0000 | 0.1234 | sí | no |
| **art1** | 0.9797 | **0.0297** | sí | **SÍ** ← techo 0.05 |
| art2 | 0.9998 | 0.6559 | sí | no |
| altura | 0.5245 | 0.0000 | sí | sí |

`altura` ganó igual, **pero por desempate**, no porque el criterio excluyera al intruso. Los datos
están en `resultados/p42-unico-apto/veredicto.json`.

**Y ésta es la parte incómoda:** ese hallazgo apareció **por la suerte de una semilla**. Ningún
criterio del prereg-42 lo buscaba. Si el sorteo hubiera dado otros cinco mundos, habríamos cerrado
el estudio con un veredicto limpio y este problema seguiría ahí, invisible.

## 1. LA PREGUNTA
> El techo de obediencia dice: *si tus comandos predicen la variable por encima de 0.05, es tuya*.
> `art1` obedeció **0.0297**. ¿Por qué el mando de Diego a veces **no predice su propio brazo**?

**No es una pregunta sobre cuántos aptos se admiten** — eso se contestó y se cerró. Es sobre si la
señal de mando **captura todo lo que el brazo hace**.

## 2. LAS TRES CAUSAS POSIBLES, y ninguna es la favorita
| | Qué diría | Qué implicaría |
|---|---|---|
| **A — el mando no lo explica todo** | el brazo se mueve también por contacto, gravedad e inercia, y el comando explica solo una parte | el techo de 0.05 es **demasiado bajo para articulaciones muy inerciales** |
| **B — el retardo no alcanza** | el efecto del comando sobre esa articulación tarda más de lo que el instrumento mira | el problema es el **horizonte**, no el techo |
| **C — la articulación estaba casi quieta** | poca varianza propia, así que hay poco que explicar | el problema es de **cobertura del balbuceo**, no del criterio |

**Declaro que no tengo favorita**, y no es cortesía: las tres implican arreglos distintos y ninguna
me conviene más. Si tuviera favorita lo diría, como lo dije en el prereg-42.

## 3. EL DISEÑO
Sobre **cinco semillas nuevas** — `101, 103, 107, 109, 113`, declaradas aquí antes de tocarlas, y
distintas de las del 35 (quemadas) y de las del 42 (ya usadas) — se mide, por articulación:

1. **obediencia neta** (lo que ya se mide hoy),
2. **la misma obediencia con horizonte doble** → separa **B**,
3. **la varianza propia de la articulación** → separa **C**,
4. **la fracción de pasos en que esa articulación está en contacto con algo** → separa **A**.

## 4. LA LÍNEA BASE TONTA (Regla 11)
El predictor ingenuo es **"todas las articulaciones son mías"** — que es la respuesta correcta por
construcción, porque el simulador sabe cuáles son el brazo. Sobre 3 articulaciones × 5 mundos = 15
casos, el tonto acierta **15 de 15 = 1.000**. **El instrumento actual acierta 14 de 15 = 0.933.**

**Y esto hay que decirlo entero: en esta tarea concreta, el detector es PEOR que el tonto.** No es
una paradoja — el tonto no puede encontrar el cuerpo en un mundo donde no lo conoce de antemano, y
el detector sí. Pero como medida de *"¿confunde canales?"*, el tonto es el listón, y hoy lo
perdemos por un caso de quince.

## 5. LOS CRITERIOS, congelados
1. **Se confirma A** si en los casos con `no_mio = True` para una articulación, la **fracción de
   contacto** es mayor que en los casos bien clasificados por **≥0.15**, en **≥4 de 5** mundos.
2. **Se confirma B** si al doblar el horizonte la obediencia de esas articulaciones **sube por
   encima de 0.05** en **≥4 de 5**.
3. **Se confirma C** si la **varianza propia** de las articulaciones mal clasificadas es menor que
   la de las bien clasificadas por **≥30%**, en **≥4 de 5**.
4. **Pueden confirmarse varias.** No son excluyentes, y forzar una sola sería inventar simplicidad.
5. **Si no se confirma ninguna**, veredicto **NO CONCLUYENTE**, y queda escrito que el detector
   tiene un modo de fallo **que no sabemos explicar** — que es peor que tener uno explicado, y por
   eso se dirá con esas palabras.

## 6. REGLA 31 — LOS DOS LADOS
- **Debe fallar donde no hay nada:** con los **motores desconectados** (mundo "sin agencia" que
  `contingencia.py` ya construye), ninguna articulación puede salir "mía". Si alguna sale, el
  instrumento fabrica cuerpo y el estudio se detiene.
- **Debe aprobar donde sí hay:** en el mundo de control positivo, la articulación con agencia
  **debe** salir mía.
- **SEÑUELO:** el canal de **ruido puro** no puede salir mío en ningún mundo. Si sale, **NULO**.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si el control negativo declara **1 o más** articulaciones mías → **se detiene**, no se reporta.
- Si el señuelo aprueba → **NULO**.
- Si sale NO CONCLUYENTE → **no hay segunda vuelta con más semillas**. Se escribe el acta diciendo
  que el modo de fallo queda sin explicar, y **se propone al director bajar el uso del detector**
  hasta que se explique. Declarado aquí para que no exista la tentación de seguir sorteando mundos
  hasta que uno hable.

## 8. LO QUE ESTO **NO** PUEDE AFIRMAR
- Nada del universo: es sobre un instrumento nuestro.
- **No revisa el nodo H-001** (que se apoya en este detector) hasta tener veredicto. Si sale A, B o
  C, entonces sí habrá que releer H-001 con el resultado delante — y eso será otro acta.
- **No cambia ningún umbral.** Mover el techo de 0.05 después de ver estos datos es exactamente lo
  que el director reservó y lo que la Regla 13 endurecida prohíbe.

## 9. FIRMA
Avanza por **quórum adversarial**: la pregunta la abre un dato, no un deseo, y todos los criterios
están congelados antes de correr. Revocable con una palabra del director.
