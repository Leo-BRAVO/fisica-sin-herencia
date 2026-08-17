# Prerregistro 59 — EL CENSO DE LOS MUERTOS: qué código del repositorio no lo usa nadie, y cuál de ése se puede archivar de verdad — 17 de agosto de 2026
**Item 28 de la crítica externa. Peldaño (Regla 9): Fase 1.**
**Estado: FIRMADO después de la lectura previa del catálogo de errores y antes de escribir
`censo_muertos.py`.**

---

## 0. EL HUECO, y el número real es otro
La crítica externa dio una lista de **9 módulos huérfanos**. La lista salió de `mente.py`, que solo
mira los módulos que ella misma conoce. **Medido hoy contra el genoma completo: los módulos que no
son órganos ni guardianes son 54, no 9.**

Y de esos 9 de la lista, tres ya no son huérfanos: `contratos.py` es un guardián de la puerta,
`invariantes.py` y `mundo.py` son estudios que se escribieron esta semana. **La lista estaba
vieja.** Actuar sobre ella habría sido archivar lo que acabo de conectar.

## 1. LA PREGUNTA
> De los módulos que no son órganos del genoma ni guardianes, **¿cuántos están realmente muertos**
> —nadie los importa y ninguna acta ni registro los cita— **y de ésos, cuántos se pueden mover
> sin romper nada auditable?**

## 2. LA TRAMPA QUE ESTE ESTUDIO EXISTE PARA EVITAR
**El sello se guarda por NOMBRE y se comprueba abriendo `codigo/<nombre>.py`.** Mover un módulo
sellado a otra carpeta **mata su sello igual que editarlo**: `sello_valido` deja de encontrar el
archivo. Y un sello muerto deja **irreproducible el acta que ese módulo publicó**.

> Por eso este censo tiene dos salidas y no una: **muerto** y **archivable** son cosas distintas.
> Un módulo puede estar muerto y ser **inmovible**. Eso es peso muerto que se queda, y se queda
> con la razón escrita.

## 3. CÓMO SE MIDE (todo mecánico, nada de juicio)
Un módulo está **VIVO** si se cumple al menos una:
- **por importación**: algún otro `.py` de `codigo/` lo importa;
- **por cita**: algún archivo de `resultados/` o `registros/` lo nombra **con su extensión**
  (`x.py`), no por la palabra suelta.

La cita se exige **con extensión** a propósito: los nombres sueltos de este proyecto son palabras
comunes del castellano —`memoria`, `mente`, `escala`, `temple`, `rodar`, `dimension`— y buscarlas
sueltas daría por vivo a cualquiera que aparezca en una frase.

**MUERTO** = ninguna de las dos. **ARCHIVABLE** = muerto **y sin sello vigente**.

## 4. LA LÍNEA BASE TONTA (Reglas 11 y 12), y esta vez tonta de verdad
**`grep` del nombre pelado**: muerto si su nombre no aparece en ningún otro archivo del
repositorio. Es trivial, es generoso, y **no es una suposición mía** — el error nº21 fue poner mi
propia hipótesis en el papel de rival, y no se repite.

**Declaro la contención antes de medir:** todo lo que el grep llame muerto, el censo también lo
llamará muerto. La diferencia solo puede ir en un sentido. **Por eso el criterio C nombra los dos
desenlaces posibles y uno va en mi contra.**

## 5. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **el censo encuentra lo plantado** | sobre un árbol sintético hecho a mano con muertos plantados, los encuentra **exactamente** a ésos |
| **B** | **no acusa a quien tiene cita** | sobre un árbol sintético donde un módulo solo aparece citado por un acta, el censo lo declara **VIVO** |
| **C** | **le gana a la línea base tonta, o no le gana y se dice** | si el censo halla muertos que el grep da por vivos, **cada discrepancia sale con archivo y línea** para que cualquiera la compruebe. **Si no hay ni una discrepancia, el censo no aporta nada sobre un `grep` y así se escribe en el acta** |
| **D** | **ni un sellado entre los archivables** | **cero**. Si el censo propone mover aunque sea un módulo con sello vigente, **se descarta el censo entero** |
| **E** | **no toca nada** | el censo no mueve, no borra y no edita: su única escritura es su propio JSON de salida |

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo:** árbol sintético con muertos plantados → los encuentra.
- **Señuelo:** árbol sintético donde **todos** están importados → encuentra **cero**. No puede
  inventarse un cadáver.
- **`SUJETO` declarado:** el sujeto son **los módulos del repositorio real**. Por eso la Regla 31
  **no puede tocarlos** y trabaja con árboles sintéticos hechos a mano.
- **Relación metamórfica con MECANISMO:** más muertos plantados = más muertos hallados. El factor
  es **3**, y no sale de mi intuición: el conteo es **exactamente lineal** en lo plantado, porque
  el detector recorre nodos y cuenta los que no tienen entrada. **Base 1.0, no 0.0** — duodécima
  vez que lo escribo, y está en el catálogo con cuatro incidentes.
- **Ningún número del repositorio real dentro de las autopruebas.** Escribir «son 54» dentro de una
  prueba la haría caducar el día que se añada un módulo: ése es el error «prueba que caduca», y el
  guardián lo comprueba a máquina.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si falla **A** o **B**, el censo miente y **se descarta entero**: no se ajusta el detector
  después de verlo fallar.
- Si falla **D**, se descarta: proponer mover un sellado es proponer romper un acta.
- Si falla **C** por el lado del empate, **el censo se queda pero se degrada a lo que es**: una
  forma cara de hacer `grep`, y el acta lo dirá con esas palabras.

## 8. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se archiva nada en este estudio.** El censo produce una lista; **mover archivos es un acto
  aparte** y va a su propio commit, después de leer la lista.
- **NO se afirma que un módulo muerto sobre.** Igual que en el prerregistro 54: muerto es
  **desconectado hoy**, no **indigno de existir**. Varios de estos módulos son instrumentos que
  publicaron un acta y luego se quedaron quietos; eso es exactamente lo que debe pasarles.
- **NO se toca ningún módulo sellado.** Ni editándolo ni moviéndolo.

## 9. FIRMA
Avanza por **quórum adversarial**: el criterio **C** contempla que el censo **no valga más que un
`grep`** y lo obliga a decirlo, el **D** lo manda descartar entero si propone mover un sellado, y
la línea base es un `grep` de tres líneas — no una suposición mía. Revocable con una palabra del
director.
