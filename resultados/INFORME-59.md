# INFORME-59 — ACTA DEL PRERREGISTRO 48: el órgano del sueño se recupera, y no estaba roto
**11 de agosto de 2026. La ficha de sanidad de `sueno.py` corrida con los dos motores, sobre el
mismo mundo y las mismas semillas.**
**Datos crudos:** `resultados/p48-sueno/medida.json`. Módulo sellado: `codigo/sueno_motor.py`
(puerta 7/7).
**VEREDICTO, con las mismas palabras del archivo de datos:** *RECUPERADO — con sindy4 la ficha de
sanidad aprueba entera y el señuelo de escala da el mismo numero con el mundo x1 y x10.*

---

## 1. LOS NÚMEROS, y el criterio que yo no escribí
El señuelo de escala **no se redactó para este estudio**: está en la ficha del propio órgano desde
el **prerregistro 43** y dice *"multiplicar el mundo por 10 no puede cambiar cuántas leyes pasan"*.
Aquí solo se cambió el instrumento y se volvió a correr.

| | leyes con el mundo ×1 | leyes con el mundo ×10 | ¿pasa el señuelo? |
|---|---|---|---|
| **`sindy3`** | **3.0** | **0.0** | ✘ |
| **`sindy4`** | **3.0** | **3.0** | ✔ |

**La línea base tonta se sostiene con los dos motores:** soñar sobre un modelo ajustado a ruido
puro da **0** leyes en ambos casos. El suelo es cero, como exigía el prerregistro 43.

## 2. LA FICHA ENTERA, y algo que yo no había predicho
`sindy3` reprobaba la ficha por **dos** cosas, no por una:

```
estructura: correlaciona 0.327 con lo suyo (piso 0.6) — la lectura no mide lo que dice medir
ESCALA: con el mundo x10 pasan 0.0 leyes en vez de 3.0 — el filtro lee amplitud, no estructura
```

Con `sindy4` **la ficha aprueba entera: cero fallos.** No solo se arregló el señuelo de escala
—que era lo que yo esperaba y declaré antes de correr— sino también **la correlación con la
estructura del mundo**, que estaba en 0.327 sobre un piso de 0.6.

**Y tiene sentido hacia atrás:** si el motor pierde leyes de forma errática según la escala de cada
mundo, la cuenta de leyes que sobreviven **deja de seguir a la estructura** aunque el filtro de
vigilia funcione perfectamente. **Los dos fallos eran el mismo fallo, visto por dos ventanas.**

## 3. LO QUE ESTO SIGNIFICA PARA EL ÓRGANO: **no estaba roto**
El ledger de reprobados decía, el 10 de agosto: *"REPROBÓ la ficha ... La causa **NO es suya** — es
que `sindy3` no es invariante a la escala"*. **Ese diagnóstico queda confirmado con una prueba que
podía desmentirlo.**

**El mecanismo del sueño —soñar hacia adelante y filtrar contra la vigilia— nunca falló.** Lo que
fallaba era el motor con el que minaba sus propios sueños. **El órgano estaba sano dentro de un
instrumento roto**, que es el mismo patrón que el tacto de Diego: sano dentro de un cuerpo que no
alcanza nada.

## 4. EL CONTROL POSITIVO — por qué este resultado es creíble
La Regla 31 del estudio exigía, **antes de correr**, que con `sindy3` se **reprodujera el REPROBADO
ya publicado**. Se reprodujo exactamente: `3.0 → 0.0`, las mismas cifras del INFORME-50. **Si mi
montaje no hubiera reproducido el fallo viejo, el estudio se detenía**, porque no habría estado
midiendo lo mismo.

Es lo que separa "arreglamos algo" de "medimos otra cosa y salió bonito".

## 5. LO QUE **NO** SE AFIRMA
- **Nada del universo.** Es un órgano nuestro, en un mundo de juguete nuestro.
- **No se afirma que `sindy4` sea un buen motor.** El INFORME-58 midió que **calla por completo en
  la caída con roce**. Aquí funciona porque **el mundo de juguete de `sueno.py` es un oscilador
  amortiguado**, que es justo la familia donde el arreglo funcionó. **Un órgano que viviera en un
  mundo con una coordenada no acotada podría empeorar con este cambio.**
- **No se afirma que `sueno.py` esté validado.** Pasa **su ficha de sanidad**, que es un paso; la
  puerta entera son siete.
- **No se edita ni se borra el INFORME-50.** Se queda como está: describía correctamente lo que se
  medía entonces.

## 6. LA DECISIÓN QUE ESTE ACTA HABILITA, y que se toma aparte
El prerregistro 48 dejó escrito que **cambiar el motor por defecto de `sueno.py` es un cambio del
órgano y no de este estudio**, y que se decide después, con el acta delante. **El acta ya está
delante y la evidencia sostiene el cambio**: cero fallos en la ficha, señuelo superado, línea base
en cero. Se hace en un paso propio, con la puerta corrida sobre el órgano y con el ledger de
reprobados actualizado **solo hasta donde los hechos lleguen** — pasar la ficha no es pasar la
puerta.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuántos de nuestros "defectos de órgano" son en realidad defectos de instrumento?** De los
> tres órganos reprobados, **éste no era suyo y ya está demostrado**. El de `atencion.py` tampoco
> es suyo: es de la cadena, y viene de `incertidumbre.py`. **Puede que la lista de reprobados sea
> más corta de lo que parece y que el problema esté concentrado en unas pocas piezas compartidas.**

## 8. LO QUE LE TOCA AL DIRECTOR
Ninguna decisión urgente. Un dato para el balance: **la Fase 2 del plan termina con un órgano
recuperado y sin ningún hallazgo caído.** El caso incómodo que dejamos declarado antes de mirar
—que un resultado nuestro se cayera— **no se dio esta vez**.
