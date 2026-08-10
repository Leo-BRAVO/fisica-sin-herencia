# INFORME-56 — ACTA DEL PRERREGISTRO 44: Diego pierde la parte de su cuerpo que menos se mueve
**10 de agosto de 2026. Cinco mundos nuevos: 101, 103, 107, 109, 113.**
**Datos crudos:** `resultados/p44-brazo/medida.json`. Módulo sellado: `codigo/brazo_no_mio.py`.
**VEREDICTO, con las mismas palabras que el archivo de datos:** *SE CONFIRMA C y D (acoplamiento,
NO estaba listada).*

---

## 1. LA PREGUNTA, y qué salió
El prereg-42 encontró que en un mundo el escalón 1 declaró **no-mía** a `art1`, una articulación del
propio brazo de Diego. Este estudio pregunta por qué, con tres causas listadas de antemano y
**ninguna favorita**.

**Replica, y con un patrón nítido: 3 de 15 mal clasificadas — y las tres son `art1`.**

| mundo | art0 | **art1** | art2 |
|---|---|---|---|
| 101 | +0.0563 | +0.0624 | +0.6029 |
| 103 | +0.0893 | +0.2223 | +0.5876 |
| 107 | +0.1266 | **+0.0365 ← no-mía** | +0.6995 |
| 109 | +0.1221 | **+0.0444 ← no-mía** | +0.7106 |
| 113 | +0.0852 | **+0.0256 ← no-mía** | +0.7270 |

## 2. LA CAUSA, y es la C con un margen que no admite discusión
| | mal clasificadas | bien clasificadas |
|---|---|---|
| **varianza propia media** | **0.1164** | **155.6459** |
| fracción de contacto media | 0.7556 | 0.7694 |

**La articulación que se pierde tiene MIL VECES menos varianza que las que se conservan.** El
criterio pedía un 30% menos; salió un factor de **1.337**.

**Y la causa A queda descartada limpiamente:** la fracción de contacto es prácticamente idéntica
(0.756 contra 0.769). El contacto no puede explicar una diferencia entre articulaciones porque es la
misma para todas — es una propiedad de la escena, no del canal.

## 3. LA CAUSA D, QUE YO NO HABÍA LISTADO
Desconectando un canal de comando por vez y mirando qué articulación cae:

| canal desconectado | cae la suya | cae más una ajena | ¿atribuye bien? |
|---|---|---|---|
| 0 → art0 | +0.0203 | +0.0090 | sí |
| **1 → art1** | **+0.0062** | **+0.0402** | **NO** |
| 2 → art2 | +0.5175 | +0.0073 | sí |

**Al quitarle a `art1` su propio mando, `art1` casi no se inmuta — y otra articulación cae siete
veces más.** El brazo está **acoplado**: el mando de una mueve a las demás, y la obediencia medida
por articulación no puede atribuir bien.

**Esa causa no estaba en mi lista de tres.** La escribí como A, B y C y la realidad trajo una cuarta.
Queda dicho así, sin reordenar la lista para que parezca que la había previsto.

## 4. LO QUE ESTO SIGNIFICA PARA DIEGO
**No es un fallo aleatorio: tiene una dirección.** El detector de "esto es mi cuerpo" **pierde
sistemáticamente las partes que menos se mueven**. Un miembro quieto —o sujeto, o apoyado, o
simplemente poco usado en ese episodio— tiende a salir clasificado como *no mío*.

Dicho de otro modo: **Diego reconoce mejor las partes de su cuerpo que agita.** Es una limitación
del instrumento, pero también una afirmación comprobable sobre cómo se construye su frontera yo/mundo.

## 5. LO QUE **NO** SE HACE
- **No se toca el techo de 0.05.** Moverlo con este resultado delante es exactamente lo que la
  Regla 13 endurecida prohíbe, y lo que el director reservó.
- **No se revisa el nodo H-001 todavía.** Se apoya en este detector, y ahora sabemos que tiene un
  sesgo con dirección conocida. **Releerlo es otro acta**, con su propio criterio, y hacerlo hoy
  con el hallazgo caliente sería el error que este proyecto persigue.
- **No se declara nodo.** Es sobre un instrumento nuestro.

## 6. UN ERROR DE DISEÑO MÍO, EL MISMO DE HACE UNA HORA
La medida del acoplamiento la escribí primero **dentro de la ficha de sanidad** — es decir, dentro
de la Regla 31 de mi propio instrumento. Resultado: un defecto del **objeto de estudio** bloqueaba el
módulo que existe para estudiarlo, y la puerta me cerró con razón.

**Es exactamente el error que mató al prerregistro-45 esta misma tarde** (INFORME-54). Dos veces el
mismo día. La regla que queda escrita: **la Regla 31 examina el PROCEDIMIENTO DE MEDIDA; lo que haga
el sujeto es RESULTADO.** La medida no se borró: se movió a donde le tocaba, y es la §3 de este acta.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **Si el detector pierde lo que no se mueve, ¿cómo reconocería Diego una parte de su cuerpo que
> está inmovilizada?** Un humano sabe que su brazo dormido sigue siendo suyo. Diego, hoy, no —y no
> por falta de datos, sino porque su criterio es *"lo que responde a mi mando"* y un miembro quieto
> no responde a nada. Es una pregunta sobre qué es el cuerpo, no sobre el umbral.

## 8. LA DECISIÓN QUE LE TOCA AL DIRECTOR
Ninguna urgente. Pero conviene que sepa que **el hallazgo del prereg-42 no era casualidad de una
semilla: replica en 3 de 5 mundos nuevos, siempre en la misma articulación, y con una causa medida.**
Lo que empezó como una rareza es un sesgo con dirección conocida.
