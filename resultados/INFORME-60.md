# INFORME-60 — ACTA DEL PRERREGISTRO 49: el televisor pierde de forma total, y aun así la cadena NO está reparada
**11 de agosto de 2026. La cadena G14 → G8 medida de punta a punta, con datos reales y sin un solo
número puesto a mano.**
**Datos crudos:** `resultados/p49-cadena/medida.json`. Módulos: `codigo/incertidumbre.py`,
`codigo/atencion.py`, `codigo/contratos.py`, `codigo/cadena_g14g8.py` (los cuatro con la puerta
abierta 7/7).
**VEREDICTO, con las mismas palabras del archivo de datos:** *ARREGLA UNO SOLO — la cadena NO está
reparada; fallan A_G14_no_confunde.*

---

## 1. LOS SEIS CRITERIOS CONGELADOS, respondidos

| | criterio | salió | |
|---|---|---|---|
| **A** | G14 deja de confundir ruido con ignorancia | varianza extra del ruido **0.207** sobre un techo de 0.15 | ✘ |
| **B1** | el contrato rechaza el número inflado | *"CONTRATO ROTO ... fuera del rango declarado"* — el mensaje entero está en el archivo de datos | ✔ |
| **B2** | pierde con la ignorancia máxima legal | tv **0.3846**, buena **9.6154** | ✔ |
| **C** | poder cero no puntúa | prioridad exactamente cero | ✔ |
| **D** | no se rompió lo que servía | **buena 10.0, tv 0.0** | ✔ |
| **E** | más ruido no sube la cuota | **0.0** en ×1, ×2, ×5 y ×10 | ✔ |
| **F** | distingue ley de ruido | **0.1459** contra **0.0** (ganancias 0.9657 y 0.0) | ✔ |

Los dos umbrales del criterio B2 —el techo del televisor y el piso de la región buena— están
congelados en el prerregistro 49 y en `codigo/cadena_g14g8.py`; el techo de confusión del
criterio A viene de `codigo/sanidad.py` y no se escribió para esta ocasión.

## 2. LO QUE SÍ SE CONSIGUIÓ, y es grande
**La cadena entera, con dos regiones de verdad, G14 real midiéndolas y G8 real repartiendo:**

**El televisor se lleva `0.0` de 10 y la región buena `10.0` de 10.** Antes —INFORME-52, con las
cifras que aquel acta publicó— el reparto era justo el contrario: el televisor se llevaba la
mayoría y la región buena el resto.

**El televisor no se lleva "poco": se lleva exactamente cero, en las cuatro amplitudes de ruido
probadas.** Y hay tres defensas independientes detrás, no una:
1. **El contrato lo rechaza en la puerta.** `curable` es una fracción acotada, así que **una
   epistémica de 20 ya no puede llegar a G8** — el ataque del INFORME-52 dejó de ser
   representable.
2. **Aun con la ignorancia máxima legal** (`curable = 1.0`), el televisor se lleva 0.3846 de 10.
   **Esto es lo que impide que lo anterior sea un truco de tipos.**
3. **Con datos reales, su `curable` es 0.0000**, porque no hay nada que aprender ahí.

## 3. POR QUÉ EL VEREDICTO ES «ARREGLA UNO SOLO» Y NO LO SUBO
**El criterio A pedía ≤15% y salió 20.7%.** Bajó de 43.3%, pero **no bajó lo suficiente**, y el
umbral no lo invento hoy: es el `TECHO_CONFUSION` que ya estaba en `sanidad.py`.

**No lo subo porque tres de siete me parezcan pocos ni porque seis de siete me parezcan muchos.**
Mover el criterio después de ver los datos es lo único que el director se reservó.

**Y estaba escrito antes de correr.** La enmienda 3 del prerregistro dice, palabra por palabra:
> *"declaro lo que puede salir mal: esa corrección vuelve a meter una dependencia del ruido... Es
> la dirección segura pero no es invariancia, así que el criterio A tiene que seguir cumpliéndose
> con el techo de confusión de `sanidad.py`, y si no se cumple, **el arreglo no vale y se dice**."*

**Se dice.**

## 4. EL HALLAZGO DE FONDO: **A y F están en tensión, y puede que no sea un fallo mío**
Los dos diseños que probé caen en lados opuestos, y **ninguno de los dos es un descuido**:

- **Diseño 1** — `epistemica/(epistemica+aleatoria)`: **perfecto en A**, sin ninguna dependencia
  del ruido, y **suspende F** — con los mismos datos, el televisor puntuaba **más alto** que la
  región con ley. Las cifras exactas están en la enmienda 3 del `prerregistro-49`, medidas antes
  de tocar el código.
- **Diseño 2** — el anterior multiplicado por la ganancia predictiva fuera de bolsa: **perfecto en
  F** (`0.1459` contra `0.0`) y **suspende A** (varianza extra `0.207`).

**Y hay una razón para sospechar que la tensión es real y no un accidente de implementación:**
para saber si una ignorancia **se puede curar** hay que saber si **hay estructura que aprender**; y
detectar estructura es, por definición, **separar señal de ruido** — lo que hace que la lectura
dependa del nivel de ruido. **Una medida perfectamente ciega al ruido es también ciega a si hay
ley.** Eso es exactamente lo que le pasó al diseño 1, y lo celebré como un acierto sin verlo.

**No se afirma que la tensión sea insalvable.** Se afirma que **mis dos intentos cayeron uno a
cada lado**, y que quien intente el tercero tiene que atacarla de frente en vez de tropezar con
ella.

## 5. LO QUE LA PUERTA CAZÓ, y sin lo cual esto habría salido mal
**Cuatro correcciones de diseño antes de que existiera un solo dato del estudio**, y las cuatro
quedan escritas en el prerregistro con su fecha:
1. **El empowerment puro borraba una distinción ya medida.** Con `curable · poder`, una región
   *intocable pero informativa* y el televisor recibían lo mismo — y el prerregistro 32 midió que
   **la observación pasiva construye modelo**. → dos presupuestos con dos criterios.
2. **Mi propia enmienda reabrió la fuga por la otra puerta.** Escribí `_ignorancia()` aceptando la
   `epistemica` cruda *"por compatibilidad"*: **el mismo agujero que estaba tapando, construido
   dentro del arreglo.** Una interfaz con una excepción amable no es un contrato.
3. **La trampa de la base cero**, heredada del prerregistro 43 (`poder_tv = 0.0` ×20 = 0). Cuarta
   vez en un mes.
4. **La ficha de G14 seguía leyendo la lectura vieja** después de arreglarla, y por eso daba
   **exactamente el mismo 43.3%**. *Un instrumento arreglado del que nadie cambia el medidor sigue
   leyendo el defecto.*

## 6. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **No se afirma que la cadena esté reparada.** Seis criterios de siete no son siete.
- **No se afirma que G14 esté validado.** `atencion.py`, `incertidumbre.py`, `contratos.py` y
  `cadena_g14g8.py` **pasan la puerta 7/7**, que es un paso — pero el criterio A del estudio
  falla, y las dos cosas conviven: la puerta comprueba que el módulo hace lo que quise; el
  criterio comprueba si lo que quise era suficiente.
- **No se toca `temple.py`.** Sigue leyendo `epistemica`, que **no se ha quitado ni cambiado**, así
  que su comportamiento es idéntico al de ayer.
- **No se cambia ningún umbral, ni el techo del 15%, ni el veredicto.**

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Se puede medir "ignorancia curable" sin que el ruido entre en la medida?** El diseño 1 dice
> que sí y resulta ciego; el diseño 2 ve y deja entrar un 20.7%. **Puede que la respuesta correcta
> no sea un número sino dos** —una lectura de *cuánta estructura hay* y otra de *cuántos datos
> faltan*, publicadas por separado y consumidas por separado— en vez de un solo escalar que
> pretende ser las dos cosas. Es la misma lección que el proyecto ya aprendió con la epistémica y
> la aleatoria: **fusionar dos preguntas en un número es lo que hizo mirar el televisor.**

## 8. LO QUE LE TOCA AL DIRECTOR
Ninguna decisión urgente, y una noticia buena y una mala que van juntas:
- **La conducta ya cambió.** Diego deja de mirar la pared que parpadea: de 7.036 a 0.0 de 10.
- **Y la cadena sigue sin estar reparada según su propio criterio.** El tercer intento va en un
  prerregistro nuevo, no en una edición de éste — y con la tensión de la §4 declarada de frente.
