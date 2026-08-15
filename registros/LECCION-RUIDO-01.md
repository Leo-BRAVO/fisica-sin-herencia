# LECCIÓN DE MÉTODO — los dos ruidos no son el mismo, y confundirlos nos falsificó tres módulos
**11 de agosto de 2026. No es un hallazgo sobre Diego: es un error nuestro, repetido tres veces,
que tres guardianes distintos dejaron pasar y que la puerta acabó cazando.**

---

## 1. LA CONFUSIÓN, en una frase
**Dábamos por hecho que "más ruido ⇒ menos ley que hallar". Es falso para el ruido que estábamos
usando.**

| | dónde entra | qué le hace a la ley |
|---|---|---|
| **Ruido de PROCESO** | **dentro** de la integración: `x[t] = x[t-1] + dt·f(x) + ruido` | **EXCITA el sistema.** La ley determinista queda **intacta** y se vuelve **más fácil** de identificar |
| **Ruido de MEDIDA** | **sobre la trayectoria ya ocurrida**, como un sensor | **ENTIERRA la señal** sin tocar la dinámica. Es el único que puede destruir una ley |

**El ruido de proceso sacude al oscilador y le hace recorrer más de su espacio de estados.** Un
sistema más excitado se identifica mejor, no peor. Nosotros escribimos tres veces lo contrario.

## 2. LAS TRES VECES, con sus números
| módulo | qué declaró | qué pasó de verdad |
|---|---|---|
| **`sueno.py`** (prereg 43) | *"con el mundo enterrado en ruido, la vigilia deja de hallar leyes"*, sobre `ruido` de proceso ×30 | La desviación del mundo sube de **0.658 a 13.686** — no se entierra, se amplifica. Las leyes pasan de **3.0 a 4.0** con `sindy4` |
| **`escala.py`** (prereg 46) | la misma relación, sobre `ruido_rel` ×200 | La desviación sube de **0.404 a 6.369**; `sindy4` sigue hallando la ley con margen fuera de muestra de **0.71** |
| **`arreglo_motor.py`** (prereg 47, primer borrador) | la misma relación otra vez | La puerta la midió **×1.000** antes de que existiera un dato |

## 3. LO QUE MÁS DUELE: **las dos primeras APROBARON**
Y aprobaron **por el motivo equivocado.**

`sindy3` pierde leyes cuando sube el ruido de proceso — **pero por fragilidad suya, no porque no
hubiera ley que hallar.** El chequeo *"la medida responde al ruido"* estaba **midiendo un defecto
del instrumento y creyéndolo una propiedad del mundo.**

> **Un chequeo que aprueba por el motivo equivocado es peor que uno que falla**, porque no deja
> rastro. Los dos prerregistros pasaron su Regla 31, se firmaron y produjeron actas. El error solo
> salió a la luz **cuando arreglamos el motor** y el instrumento dejó de fallar de la forma que
> tapaba la mentira.

**Corolario incómodo, y hay que decirlo:** cada vez que reparamos un instrumento, **cualquier
chequeo que aprobaba gracias a su defecto queda en duda.** No es paranoia: es lo que acaba de
pasar tres veces seguidas.

## 4. LA REGLA QUE SALE DE AQUÍ
> **Al declarar una relación metamórfica sobre "ruido", hay que decir CUÁL de los dos, y
> justificar el efecto con el mecanismo — no con la intuición.** El ruido de proceso pertenece al
> mundo; el de medida, al sensor. Solo el segundo destruye información.

Y la que ya teníamos, que esto vuelve a confirmar por cuarta vez:
> **Una relación metamórfica solo puede declarar lo que se sabe A PRIORI.** Las tres veces creímos
> saberlo y ninguna lo sabíamos: estábamos declarando una intuición sobre la palabra "ruido".

## 5. QUÉ SE CORRIGIÓ Y QUÉ NO
- **`arreglo_motor.py`** nació ya corregido (enmienda 5 del prerregistro 47), antes de correr.
- **`sueno.py`** queda corregido: `_mundo_soñable` distingue ahora los dos ruidos, y la relación se
  declara sobre el de medida. Comprobado que discrimina: **4.0 leyes con ruido de sensor 0.05 y
  0.0 al multiplicarlo por 30.** Base distinta de cero.
- **`escala.py` NO se toca.** Está sellado y produjo el INFORME-55. **Su barrido no dependía de esa
  relación** —los tramos se miden sin ella— así que **el INFORME-55 sigue en pie**. Lo que queda
  anotado es que **uno de sus chequeos de Regla 31 aprobaba por el motivo equivocado**, y eso vive
  aquí y en la enmienda 5 del prerregistro 47, no en una edición del acta.

## 6. LO QUE **NO** SE AFIRMA
- **No se afirma que ningún resultado publicado sea falso.** Ninguna de las tres relaciones
  participaba en el cálculo de ningún veredicto: eran chequeos de instrumento.
- **No se afirma que ésta sea la última vez.** Es la cuarta aparición del mismo mal en un mes.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuántos otros chequeos nuestros aprueban por el motivo equivocado?** Un chequeo que pasa no
> deja evidencia de *por qué* pasó. La única forma de saberlo es la que funcionó aquí sin
> proponérselo: **cambiar el instrumento y ver cuáles dejan de aprobar.** Es un examen que se
> podría hacer a propósito, y no lo hemos hecho nunca.
