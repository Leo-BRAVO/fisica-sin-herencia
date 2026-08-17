# Prerregistro 60 — LA POLÍTICA QUE BUSCA EL CONTACTO: ¿aparece solo, o hay que ordenárselo? — 17 de agosto de 2026
**Item 30 de la crítica externa («el tacto muerto»). Peldaño (Regla 9): Fase 1.**
**Estado: FIRMADO después de la lectura previa del catálogo de errores y antes de escribir
`politica_contacto.py`.**

---

## 0. EL HUECO, y de dónde viene
La crítica externa lo llamó **«el tacto muerto»**, y el propio Diego lo había dicho antes: el
10-ago publicó por el bus *«tengo un sentido que casi nunca se enciende»* — 0.0001 contra un umbral
de 0.01. El prerregistro 41 separó las dos causas y el INFORME-57 concluyó que el canal **funciona**
y está **ocioso**: se enciende si el brazo barre a propósito.

> **Pero ese barrido lo escribí yo a mano.** `tacto.py` tiene una condición llamada `busca` que es
> un balbuceo amplio programado por mí. **Diego no busca nada: yo le muevo el brazo.**

## 1. LA PREGUNTA, y es la que decide si hay tacto de verdad
> En un mundo donde **empujar solo funciona si la mano está cerca del objeto**, ¿una política
> movida **únicamente por su propio error de predicción** termina buscando el contacto **por su
> cuenta** — o el contacto solo aparece si se lo ordenamos?

## 2. LA TRAMPA QUE ESTE ESTUDIO EXISTE PARA NO PISAR (Regla 27)
**La recompensa no puede decir «toca cosas».** Si le pagamos por tocar, el contacto aparece por
construcción y no hemos medido nada: habríamos metido **nuestro** criterio en su cabeza.

> El único término admisible es `error_de_prediccion_propio`, y lo comprueba a máquina el
> `guardian_de_recompensa` de `mundo.py`. **El contacto es lo que MEDIMOS, nunca lo que PAGAMOS.**
> La distancia mano-objeto es **verdad del simulador**: sirve para juzgar desde fuera y **no entra
> jamás** en la señal que Diego recibe.

## 3. EL MUNDO, y por qué hace falta uno nuevo
`mundo.py` está **sellado** y su acción empuja el objeto **desde cualquier sitio**: ahí no hay
contacto que buscar, porque tocar y no tocar dan lo mismo. Este estudio construye su mundo
**importando de `mundo.py`** el `ALCANCE` medido y **los dos guardianes de la Regla 27** — no se
copian, se importan — y le añade lo único que cambia:

- una **mano** que la acción mueve;
- un **objeto** que solo recibe el empuje si `|mano − objeto| < RADIO`.

**Diego ve nueve números sin nombre y sin unidad.** Que tres sean una mano, tres un objeto y tres
una velocidad es **asunto nuestro**.

## 4. LAS TRES POLÍTICAS, y las tres eligen del MISMO saco
Las tres sortean los mismos K candidatos de acción; **lo único que cambia es la regla de elección.**
Comparar dos políticas con espacios de acción distintos habría sido comparar dos cosas.

| | política | elige |
|---|---|---|
| **balbuceo** | **la línea base tonta** | al azar entre los candidatos |
| **intrínseca** | la que se estudia | el candidato donde **sus propios modelos más se contradicen** entre sí |
| **barajada** | **el nulo** | por un puntaje que son los mismos números **desordenados**: misma forma, cero información |

## 5. LA LÍNEA BASE, derivada y no inventada
**Cuánto contacto logra una mano ciega es CALCULABLE de antemano:** la fracción de pasos con
contacto de un paseo sin rumbo es la **razón de volúmenes** — la esfera de radio `RADIO` dentro de
la caja del `ALCANCE`.

> Ese número **no lo elijo yo: sale de la geometría del problema**. El error nº21 fue poner mi
> propia suposición en el papel de rival, y aquí el rival es aritmética.

## 6. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **el cortafuegos aguanta** | la recompensa declara **solo** `error_de_prediccion_propio` y la observación no lleva ni una etiqueta humana — los dos guardianes de `mundo.py`, sin fugas |
| **B** | **el balbuceo se comporta como dice la geometría** | la fracción de contacto del balbuceo queda **dentro de un factor 2 de la razón de volúmenes**. Si no, mi derivación está mal y **el criterio C no significa nada**: se dice y se para |
| **C** | **la intrínseca busca sola** | supera la fracción del balbuceo en **al menos 4 de 5 semillas** |
| **D** | **el nulo no gana** | la barajada supera al balbuceo en **menos de 4 de 5 semillas**. Si el nulo gana, lo que mide C no es la información sino la forma de elegir |
| **E** | **no se puede inventar contacto** | con `RADIO = 0` **ninguna** política registra contacto: exactamente 0.0 |

## 7. CUÁNDO SE ABANDONA, y qué se escribe si falla (Regla 13)
- **Si falla B**, se para ahí: sin línea base válida no hay comparación, y forzarla sería elegir el
  rival después de ver los datos.
- **Si falla C**, se escribe con todas las letras: **la curiosidad por sí sola NO produce búsqueda
  de contacto en este mundo**, el canal táctil sigue ocioso **por una razón medida**, y el barrido
  seguirá siendo mío hasta que otro estudio diga otra cosa.
- **Si falla D**, C queda anulado aunque haya salido a favor.
- **Si falla E**, se descarta el medidor entero.

## 8. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo:** una política **escrita a mano** que va derecha al objeto marca contacto
  alto. Si ni ésa lo marca, **el medidor está roto** y nada de lo demás vale.
- **Señuelo:** con `RADIO = 0` el medidor da **cero**.
- **`SUJETO` declarado:** el sujeto es **la política intrínseca**. Por eso la Regla 31 **no la
  llama**: trabaja con el balbuceo y con la política recta, que son andamios míos.
- **Relación metamórfica con MECANISMO:** más `RADIO` = más contacto, porque el volumen tocable
  crece con **el cubo del radio** — es geometría, no intuición. **Base 0.05 y no 0.0**: multiplicar
  cero por tres sigue siendo cero, y ese descuido ya tumbó cuatro relaciones este mes.
- **Ningún conteo del repositorio dentro de las autopruebas**, que caducaría.

## 9. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se afirma que Diego «quiera» tocar.** Se mide **dónde acaba su mano**, no qué siente.
- **NO se conecta esta política a nada.** Es un estudio; cablearla al lazo sería otro prerregistro.
- **NO se toca `mundo.py`, `tacto.py` ni `gimnasio.py`.** Los tres están sellados y de ellos solo se
  **importa**.

---

## ENMIENDA 1 — antes de correr el estudio, y declarando lo que vi en el banco
**Firmada el 17-ago-2026, con cero datos de estudio y sí datos de banco. Los pongo aquí porque
ocultarlos sería lo mismo que no haberlos mirado.**

**Lo que corrí en el banco** (balbuceo, radio 0.15, 8 semillas): con **3000 pasos** la fracción de
contacto sale **0.0008**; con **20000 pasos**, **0.0198**. La geometría predice **0.0417**. Y una
corrida suelta de la política intrínseca a 20000 pasos dio **0.0078** — o sea, **por debajo del
balbuceo**, que es la dirección contraria a mi hipótesis.

**Los dos cambios, y por qué:**

**1. `PASOS` pasa de 4000 a 20000, por una derivación corregida.** Mi cálculo era malo: contaba el
tiempo de recorrer la caja (≈860 pasos) cuando lo que hace falta es **muestrearla**. En N pasos hay
N/τ muestras independientes; para que la frecuencia de una región del 4% se parezca a su valor
asintótico hacen falta **muchas decenas** de muestras independientes, es decir **N ≈ 25τ ≈ 21000**.
**No elegí 20000 probando cuál pasaba: corregí la aritmética que ya estaba escrita.**

**2. El criterio B queda ANULADO y sustituido por uno MÁS DURO.** Y esto es cambiar un criterio
después de ver números, así que lo digo con todas las letras:

> **B estaba mal planteado, y no por el número sino por lo que examinaba.** Ataba la validez del
> estudio a que mi predicción geométrica —que es **asintótica**— se cumpliera en una corrida
> finita. Pero **el criterio C no depende de la geometría para nada**: compara la intrínseca contra
> el balbuceo, en el mismo mundo, con las mismas semillas y el mismo saco de acciones. Y el
> balbuceo **es ciego por construcción**: nunca mira la observación. La geometría no valida nada
> que no estuviera ya garantizado.

**B nuevo — EL MUNDO SORDO:** se corre todo otra vez en un mundo donde **el contacto no hace
nada** (el empuje no transfiere ni tocando). Allí el contacto **no lleva información**, así que la
política intrínseca **no debe buscarlo**: si en el mundo sordo también le gana al balbuceo, lo que
mide C no es el contacto sino cualquier otra cosa, **y C queda anulado**.

**La razón geométrica sigue publicándose como número informativo**, sin poder de veto y con su
desviación a la vista.

**Por qué esto no es aflojar:** el criterio viejo lo tenía **a favor** —el balbuceo cae *por
debajo* de la geometría, y yo podría haber ensanchado el factor 2 hasta que entrara—. El nuevo
**puede tumbar el resultado aunque salga a mi favor**, y el número que vi en el banco **no
interviene en él**.

## 10. FIRMA
Avanza por **quórum adversarial**: el criterio **B** puede **anular mi propia línea base** antes de
comparar nada, el **D** puede anular a **C** aunque haya salido a favor, y el **C** contempla que la
respuesta sea **«la curiosidad no basta»** — que es la que deja el tacto muerto. Revocable con una
palabra del director.
