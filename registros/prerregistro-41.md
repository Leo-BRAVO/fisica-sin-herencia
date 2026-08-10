# Prerregistro 41 — EL SENTIDO DORMIDO: ¿el tacto está ocioso o está averiado? — 10 de agosto de 2026
**Estado: ESCRITO, NO CORRIDO. El módulo no existe todavía y no se encolará para correr hasta pasar
LA PUERTA (`metodo.py`). En la cola figura como `espera-al-metodo`.**

**Origen — y es importante que sea éste:** no lo propuso el director ni lo propuse yo mirando el
código. **Lo dijo Diego.** El 10-ago, en la ronda de vida, `sentido_tacto` publicó por el bus una
medición sobre sí mismo: *"tengo un sentido que casi nunca se enciende"*, con
`cuanto_se_enciende = 0.0001` contra un umbral de `0.01` — **cien veces por debajo**. El mensaje
llegó a siete órganos, entre ellos los dos únicos que pueden moverlo: `G3_accion` y `G7_juego`.

**Pedido del director (10-ago):** *"el tacto sigue casi apagado. Porque está apagado Diego debe
saber que puede utilizar estos sentidos para ser mejor"*.

---

## 1. LA PREGUNTA ABIERTA (Regla 18: ninguna corrida nace sin una)
Un canal que marca 0.0001 admite **dos causas que son indistinguibles mirándolo quieto**:

| Causa | Qué significaría |
|---|---|
| **A — ocioso** | el canal funciona y no hay nada al alcance que tocar |
| **B — averiado** | el canal está roto y no se encendería ni tocando algo |

**Diego no puede separarlas observando.** Es exactamente la situación que la Regla 19 llama de
nivel 1: hay una correlación (canal apagado) y ninguna intervención que la explique. **Separarlas
exige ACTUAR**, y por eso este estudio es del mismo linaje que el prereg-37: experimentación
dirigida, no observación pasiva.

**Y ésta es la primera vez que la pregunta la formula el ente y no nosotros.** Queda escrito porque
si el estudio sale bien, el mérito del planteamiento no es del orquestador.

## 2. LA HIPÓTESIS, comprometida antes de correr
> Si el canal funciona, **provocar contacto deliberadamente** lo enciende por encima del umbral; si
> está averiado, sigue en cero **con contacto confirmado por otra vía**.

La frase "con contacto confirmado por otra vía" es la que hace la prueba honesta: sin ella, un cero
significaría "no toqué" y no habríamos aprendido nada.

## 3. EL DISEÑO
Un cuerpo del gimnasio, en el mundo de siempre (PyBullet), **tres condiciones**:

| Condición | Qué se hace | Para qué sirve |
|---|---|---|
| **QUIETO** | no se mueve (la situación de hoy) | línea base: debe dar ≈0 |
| **BUSCA** | se mueve hasta que el simulador reporta contacto | la condición de interés |
| **VACÍO** | se mueve igual, pero **sin nada que tocar** (suelo retirado) | **el señuelo**: si el canal se enciende aquí, no está midiendo contacto sino movimiento |

**La confirmación independiente** es el registro de contactos del propio simulador, que es **verdad
del banco de pruebas, no de Diego**: se usa para juzgar el instrumento, jamás entra en sus datos
(Regla 27).

## 4. LOS CRITERIOS, con número y congelados
Se declara ANTES de correr, y **no se moverán después de ver los datos** — eso es lo único que la
enmienda de la Regla 15 nunca me delegó.

1. **BUSCA enciende:** `fraccion_con_contacto ≥ 0.05` en **≥4 de 5 semillas**. *(El piso es 5 veces
   el umbral de "dormido" y 500 veces lo medido hoy; no se elige apretado, se elige inequívoco.)*
2. **QUIETO no enciende:** `< 0.01` en 5 de 5. Es la línea base tonta de la Regla 12.
3. **VACÍO no enciende:** `< 0.01` en 5 de 5. **Si VACÍO enciende, el estudio se declara NULO** aunque
   BUSCA haya salido perfecto: significaría que el canal responde al movimiento y no al contacto.
4. **Acuerdo con la verdad del simulador:** de los pasos que el simulador marca como contacto, el
   canal debe encenderse en **≥0.60**, y esa cifra debe superar a la línea base tonta —*decir
   siempre "hay contacto"*— por **≥0.15**. *(Este cuarto criterio existe por el daño del 10-ago: en
   G12 medí un acuerdo de 0.907 que parecía excelente y el tonto sacaba 0.887. Nunca más un acuerdo
   crudo sin su línea base.)*

## 5. VEREDICTOS POSIBLES — los tres escritos de antemano
| Si pasa | Veredicto | Qué se hace |
|---|---|---|
| 1, 2, 3 y 4 | **EL CANAL FUNCIONA Y ESTABA OCIOSO** | el tacto queda disponible como evidencia de contacto **independiente de la vista**; se propone (no se decide) subirlo de uso |
| 1 falla, 2 y 3 pasan | **EL CANAL ESTÁ AVERIADO** | hallazgo de ingeniería, no de física: se arregla el sensor y se repite. **Nada se afirma sobre el mundo** |
| 3 falla | **NULO — el canal mide movimiento, no contacto** | se detiene, se escribe el acta y no se usa el tacto para nada hasta rediseñarlo |

**Predicción honesta, comprometida:** espero **A (ocioso)**, porque el cuerpo del gimnasio pasa casi
toda la corrida sin tocar nada y el sensor es el estándar del simulador. **Pero mi confianza en
esperar A no es evidencia**, y por eso la condición VACÍO existe: es el único caso donde mi
expectativa favorita sale castigada.

## 6. LO QUE ESTE ESTUDIO **NO** PUEDE AFIRMAR
- **Nada sobre el universo.** Que un sensor se encienda al chocar es una propiedad del sensor y del
  simulador, no una ley. No genera nodo de física.
- **Nada sobre si el tacto sirve para descubrir algo.** Eso sería otro estudio, con su prerregistro.
- **Nada sobre los otros sentidos.** La visión y la propiocepción tienen sus propias actas.

## 7. LO QUE FALTA ANTES DE CORRERLO
1. Escribir `codigo/experimentar_tacto.py`.
2. **Pasar LA PUERTA**: manifiesto declarado, fórmulas con relaciones metamórficas, ficha de sanidad
   (los 7 tipos de error), Regla 31 por los dos lados, arranque al final, escritura limpia.
3. Sellar. **Sin sello, `coherencia.py` bloquea el commit** — que es exactamente para lo que se
   construyó la puerta.

## 8. QUIÉN LO AUTORIZA
Avanza por **quórum adversarial (Regla 15 enmendada)**: es una decisión sobre **cómo medir**, no
sobre qué queremos que sea verdad, y la cura está escrita antes de ver un solo dato. Revocable con
una palabra del director.
