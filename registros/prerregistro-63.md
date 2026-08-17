# Prerregistro 63 — EL CENSO DE ÓRGANOS, CORREGIDO: un módulo se usa de dos formas, no de una — 17 de agosto de 2026
**Corrige el instrumento del prerregistro 54, cuyo defecto está publicado en CORRECCIÓN-02.
Autorizado por el director («adelante con todo»). Peldaño (Regla 9): Fase 1.**
**Estado: FIRMADO después de la lectura previa del catálogo y antes de escribir `anatomia2.py`.**

---

## 0. EL DEFECTO, ya publicado
`anatomia.py` declara huérfano a todo módulo que nadie **importe**. Pero `interocepcion.py` y
`memoria.py` **se ejecutan después de cada estudio del latido** — corren más que casi cualquier
órgano. **El censo miraba una de las dos formas de usar un módulo.** CORRECCIÓN-02.

## 1. LA PREGUNTA
> Con las **dos** vías contadas —lo que se importa y lo que el proyecto ejecuta—, **¿cuántos
> órganos del genoma están de verdad desconectados?**

## 2. LO QUE SE CONSTRUYE, y lo que NO se toca
- **`anatomia2.py`**: **importa** `anatomia` —sellado— y le añade **la segunda vía**: los módulos
  que los workflows o la cola llaman por su nombre de archivo.
- **NO se edita `anatomia.py`.** Está sellado; editarlo dejaría irreproducible el INFORME-65.
- **NO se retira el INFORME-65.**

## 3. LA LÍNEA BASE TONTA (Reglas 11 y 12)
**El censo viejo**, tal cual. Si contar las invocaciones **no cambia ni un veredicto**, entonces la
CORRECCIÓN-02 estaba equivocada y este módulo sobra — y se dirá así.

## 4. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **cuenta las dos vías** | un módulo importado por nadie pero ejecutado por un workflow sale **CONECTADO** |
| **B** | **no inventa conexiones** | un módulo que ni se importa ni se ejecuta sigue saliendo **HUÉRFANO** |
| **C** | **le gana al censo viejo** | el veredicto cambia para **al menos un** órgano. Si no cambia para ninguno, **este módulo sobra y se dice** |
| **D** | **no acusa por no estar sellado** | igual que el criterio B del prerregistro 54: sello y conexión son cosas distintas |

## 5. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo:** con un grafo y una lista de invocaciones hechos a mano, encuentra
  exactamente los huérfanos plantados.
- **Señuelo:** si **todo** está invocado, no queda ni un huérfano — no puede inventarse uno.
- **`SUJETO` declarado:** los **órganos reales**. La Regla 31 no los toca: trabaja con datos
  sintéticos.
- **Relación metamórfica con MECANISMO:** más módulos invocados = menos huérfanos, porque cada
  invocación solo puede sacar a uno de la lista y nunca meter a ninguno. **Base 1.0, no 0.0.**

## 6. CUÁNDO SE ABANDONA (Regla 13)
Si falla **A** o **B**, el censo miente y se descarta entero. Si falla **C**, se escribe que
**contar las invocaciones no cambia nada** y `anatomia2` queda como código muerto, con esa razón.

## 7. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **Ejecutarse no es funcionar.** Que el latido corra un módulo no dice que mida bien: eso lo dice
  su ficha, y **ninguno de los tres huérfanos ha pasado la puerta**.
- **NO se archiva ni se conecta nada.** El censo mide; el director decide.

## 8. FIRMA
Avanza por **quórum adversarial**: el criterio **C** contempla que la corrección **no sirva de
nada** y obliga a decirlo. Revocable con una palabra del director.
