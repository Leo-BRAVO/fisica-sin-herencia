# Prerregistro 62 — EL LAZO, con la línea base que debía haber puesto: el reparto UNIFORME — 17 de agosto de 2026
**Rehace el criterio E del prerregistro 58. Autorizado por el director («adelante con todo»).
Peldaño (Regla 9): Fase 1.**
**Estado: FIRMADO después de la lectura previa del catálogo y antes de escribir `lazo2.py`.**

---

## 0. QUÉ SE ROMPIÓ Y DÓNDE
El INFORME-69 midió el lazo con los dos órganos midiendo de verdad y **cuatro de sus cinco
criterios aprobaron**. Falló el quinto, y falló **por mi culpa**:

> **Puse como «línea base tonta» mis propios números escritos a mano**: `curable` 0.30 para la
> región buena y 0.10 para el televisor. **La realidad medida es 0.0827 y 0.0776** — una diferencia
> **tres veces menor** que la que yo había supuesto. **Elegí como rival mi propia suposición
> optimista**, que es justo lo que el estudio venía a desmontar.

Está en el catálogo como **error nº21: «línea base tonta que no es tonta, sino FAVORABLE»**.

## 1. LA PREGUNTA, y es la misma con el rival correcto
> Con `poder` e `incertidumbre` midiendo de verdad, ¿el reparto de la atención **le gana al reparto
> UNIFORME** — que es el rival trivial de verdad — sin que ninguna región lleve un número escrito
> por mí?

## 2. POR QUÉ EL UNIFORME ES LA LÍNEA BASE CORRECTA
La Regla 11 pide un **rival trivial**: uniforme, persistencia, constante o azar. **El uniforme es
el reparto de quien no sabe nada**: parte el presupuesto en partes iguales y no mira ninguna
medida. **No es una hipótesis mía sobre el mundo — es la ausencia de hipótesis.**

Con presupuesto 10 y dos regiones, el uniforme da **5.0 y 5.0**. Ese número **no lo elijo yo**:
sale de dividir.

## 3. LO QUE SE CONSTRUYE, y lo que NO se toca
- **`lazo2.py`**: **importa** `lazo_atencion` —sellado— y reutiliza sus regiones medidas y su
  reparto. **Solo cambia el rival del criterio E.**
- **NO se edita `lazo_atencion.py`**, ni `poder.py`, ni `incertidumbre.py`, ni `atencion.py`.
  Los cuatro están sellados o publicados; editarlos mataría sus sellos.
- **NO se retira el INFORME-69.** Aquel acta dijo lo que midió y se queda con su veredicto.

## 4. LO QUE SE ARRASTRA, y hay que decirlo ANTES
**`incertidumbre` mide sin sello vigente y su ficha reprueba por el 20.7% del INFORME-60.** Todo
`curable` de este estudio sale de ese instrumento.

> **Este estudio NO puede limpiar ese defecto y no pretende hacerlo.** Lo declara aquí, y su acta
> lo repetirá. Si el defecto se arregla algún día, este resultado **hay que rehacerlo**.

## 5. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **los dos órganos miden de verdad** | ninguna región lleva un `poder` ni un `curable` escrito a mano — se hereda de la ficha de `lazo_atencion` |
| **B** | **el televisor sigue perdiendo** | menos de **2.0 de 10**, el mismo número del prerregistro 49 |
| **C** | **la región buena sigue ganando** | más de **7.0 de 10**, el mismo también |
| **E'** | **le gana al UNIFORME** | la región buena recibe **más que 5.0**, y el televisor **menos que 5.0**. Las dos cosas, no una |
| **F** | **el uniforme no se mira los datos** | el reparto uniforme se calcula **sin usar ninguna medida**: presupuesto entre número de regiones. Comprobado en código |

## 6. LO QUE SE ESPERA, y qué se dirá EN CADA CASO
**Espero que E' apruebe**, porque el INFORME-69 ya publicó 9.758 contra 0.242 y el uniforme es
5.0/5.0. **Y decirlo así, de antemano, es exactamente lo que hace que valga poco**: este criterio
es fácil.

- **Si E' aprueba**, se escribe que **el lazo le gana al rival trivial** y `poder` queda **listo
  para conectarse**, con la salvedad del 20.7% escrita.
- **Si E' falla**, se escribe que **medir de verdad no supera ni al reparto de quien no sabe nada**,
  y `poder` se queda desconectado para siempre en lo que a este estudio respecta.
- **Si falla B o C**, se descarta: significaría que el lazo cambió desde el INFORME-69 y habría que
  averiguar por qué antes de nada.

## 6.bis REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
Lo único propio de este módulo es **el rival**, y eso es lo que se examina:
- **Control positivo:** el uniforme de 10 entre 2 da exactamente **5.0**, y el de 10 entre 4 da
  **2.5**. Si no dividiera, no sería un reparto.
- **Señuelo:** el uniforme **no depende de ninguna medida** — devuelve el mismo número con datos
  distintos. Un rival que mirara los datos no sería una línea base, y el error nº21 fue ése.
- **Relación metamórfica con mecanismo:** más regiones, menos para cada una. **Base 2.0, no 0.0.**
- **La Regla 31 NO comprueba que el reparto medido le gane**: eso es el criterio E', es decir
  **resultado**. Meterlo haría que E' no pudiera fallar.

## 6.ter CUÁNDO SE ABANDONA (Regla 13, con número)
- **Si falla E' —la buena por debajo de 5.0 o el televisor por encima de 5.0— se abandona la idea
  de conectar `poder`**, y se escribe que medir de verdad no supera al reparto de quien no sabe
  nada.
- **Si falla B (televisor ≥ 2.0) o C (buena ≤ 7.0), se abandona el estudio entero**: significaría
  que el lazo cambió desde el INFORME-69 y hay que averiguar por qué antes de comparar nada.

*(Las dos secciones se añadieron después de correr, porque `reglas.py` marcó que faltaban. **No
cambian ningún criterio ni ningún número**: los umbrales 5.0, 2.0 y 7.0 ya estaban congelados en la
tabla de arriba y en el código, y las pruebas del rival ya estaban escritas en `lazo2.regla31`. Lo
que faltaba era decirlo aquí.)*

## 7. LO QUE ESTE ESTUDIO **NO** ARREGLA, y es más de lo que arregla
- **No arregla el error nº21.** Un catálogo no se limpia rehaciendo un estudio: **el incidente
  queda**, y con él el recordatorio.
- **No revisa las demás líneas base del proyecto.** El INFORME-69 abrió esa pregunta y **sigue
  abierta**: cuántas de mis «líneas base tontas» son suposiciones mías. **Sigue sin medirse.**
- **Nada del universo.**

## 8. FIRMA
Avanza por **quórum adversarial** — y con una advertencia honesta: **este es el prerregistro más
flojo de la serie**, porque su criterio principal ya se sabe que va a aprobar. Su valor no está en
el resultado sino en **poner el rival correcto en el sitio donde puse el equivocado**. Revocable
con una palabra del director.
