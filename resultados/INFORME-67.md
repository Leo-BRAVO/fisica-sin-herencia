# INFORME-67 — ACTA DEL PRERREGISTRO 57: el codificador de hoy se derrumba con el brazo delgado, y mi criterio usó la media donde no debía
**11 de agosto de 2026. Cinco semillas nuevas (251, 257, 263, 269, 271). Brazo de dos segmentos de
un píxel de grosor, ocupando el 0.0142 de la imagen.**
**Datos crudos:** `resultados/p57-brazo/medida.json`, y para la comparacion de la §3 tambien
`resultados/p56-ojos/medida.json` — la tabla cruza los dos estudios y por eso cita los dos. Módulo: `codigo/ojos_brazo.py` (puerta 8/8).
**VEREDICTO, con las mismas palabras del archivo de datos:** *ERA EL BRAZO DELGADO — la ventaja del
cuello de botella espacial CRECE cuando el objeto es delgado, que es el caso que Diego tiene.*

---

## 1. LOS NÚMEROS, y hay que leerlos enteros

| semilla | 251 | 257 | **263** | 269 | 271 |
|---|---|---|---|---|---|
| **softmax espacial** | 0.7584 | 0.7264 | **-0.0205** | 0.6093 | 0.7519 |
| **píxel (el de hoy)** | 0.3134 | 0.3852 | 0.3072 | 0.1838 | 0.2348 |
| **ventaja** | 0.445 | 0.3412 | **-0.3277** | 0.4255 | 0.5171 |

**Ventaja media 0.2802**, contra el **0.2693** que exigía el criterio B. **Pasó por 0.011.**

## 2. LO PRIMERO, ANTES DEL TITULAR: mi criterio usó la media donde no debía
**El criterio B pedía que la ventaja MEDIA superara el mejor caso del disco. Lo hace, por un pelo.
Y una media es exactamente el estadístico equivocado para este resultado**, porque el resultado no
es uniforme: **es de dos modos.** En cuatro semillas la ventaja va de 0.3412 a 0.5171 — grande y
consistente. **En la quinta se invierte: -0.3277.**

**En la semilla 263 el softmax espacial no falla un poco: falla del todo** (R² -0.0205, es decir,
no recupera nada) **y pierde contra el codificador de hoy.**

> **El veredicto congelado se queda como está** —no muevo un criterio después de verlo pasar, igual
> que no lo moví ayer después de verlo fallar—. **Pero el titular sin esta sección sería
> engañoso**, y elegir la media fue un error de diseño mío, hermano del que ya está en el catálogo:
> *"control de regresión construido con casos parecidos entre sí"*. **Un promedio sobre un
> resultado bimodal esconde justo lo que hay que mirar.** Queda añadido a `disciplina.py` como
> error nº15, con este incidente.

## 3. LO QUE SÍ ES INEQUÍVOCO, y es el hallazgo de verdad
**No está en la comparación entre arquitecturas: está en lo que le pasa al codificador de HOY.**

| | disco compacto (INFORME-66) | **brazo delgado (aquí)** |
|---|---|---|
| píxel — **lo que Diego usa** | 0.6287 a 0.7848 | **0.1838 a 0.3852** |

**El codificador que Diego lleva puesto pierde más de la mitad de su capacidad cuando el objeto es
delgado**, y ese derrumbe es **consistente en las cinco semillas**, sin ninguna excepción.

**Eso confirma el punto de la crítica externa con sus propias palabras:** la pérdida por píxel
*"subpondera las articulaciones delgadas frente al fondo estático"*. **Con el brazo ocupando el
0.0142 de la imagen, reconstruir el fondo es casi todo el trabajo, y el brazo casi no cuenta.**

## 4. Y EL SUSTITUTO TAMPOCO ESTÁ LISTO
El softmax espacial gana en 4 de 5 — **pero se derrumba en una.** Con la escena del disco no falló
ninguna vez; aquí falla una de cinco. **Un codificador que a veces no ve nada no es un
codificador que se pueda poner en producción**, y decir *"gana de media"* sería exactamente el
error que acabo de nombrar.

**Lo honesto es esto: sabemos que el de hoy es malo con brazos delgados, y NO sabemos todavía con
qué sustituirlo.**

## 5. LO QUE **NO** SE AFIRMA
- **NO se cambia el ojo de Diego.** Estaba declarado antes de correr y se cumple. **Y ahora hay una
  razón más:** el candidato falla 1 de cada 5 veces.
- **NO se afirma que el softmax espacial sea el sustituto.** Se afirma que **el de hoy se derrumba
  con objetos delgados**, que es una afirmación sobre el actual, no sobre el nuevo.
- **NO se afirma nada sobre el gimnasio real.** Un brazo dibujado en numpy no es PyBullet con
  sombras, oclusiones y perspectiva.
- **Nada del universo.**

## 6. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Por qué se derrumba el softmax espacial en la semilla 263 y no en las otras cuatro?** No es
> ruido de medida: es un fallo total, de 0.75 a -0.02. La sospecha más simple es que **los dos
> puntos de atención colapsen sobre el mismo sitio** —un mínimo local donde ambos siguen al mismo
> segmento y el otro queda invisible—. **Si es eso, tiene arreglo conocido**, y sería un estudio
> corto. **Y si no es eso, el candidato no sirve.**

## 7. LO QUE LE TOCA AL DIRECTOR
Ninguna decisión urgente. Un aviso: **hoy sabemos por qué Diego no ve bien su propio brazo, y no
sabemos aún cómo arreglarlo.** Es menos de lo que esperaba esta mañana y **es más de lo que
teníamos ayer**, cuando las cuatro arquitecturas puntuaban a ruido y no sabíamos por qué.
