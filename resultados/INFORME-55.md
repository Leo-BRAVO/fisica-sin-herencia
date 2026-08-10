# INFORME-55 — ACTA DEL PRERREGISTRO 46: el motor no tiene banda de escala. Tiene **agujeros**.
**10 de agosto de 2026. 25 escalas × 5 semillas × 2 sistemas. Semillas nuevas: 23, 29, 31, 37, 41.**
**Datos crudos:** `resultados/p46-banda/medida.json`. Módulo sellado: `codigo/escala.py`.
**VEREDICTO, con las mismas palabras que el archivo de datos:** *ERRATICO — el motor ve y deja de
ver en tramos SEPARADOS, no en una banda.*

---

## 1. EL BARRIDO, entero
En cuántas de 5 semillas el motor declara ley, para cada escala. Lo único que cambia entre columnas
es un factor multiplicativo; la relación señal/ruido es **idéntica** en las 25 (se midió, §5).

**Oscilador amortiguado**
```
escala 10^ -3  -2.75 -2.5 -2.25 -2  -1.75 -1.5 -1.25 -1  -0.75 -0.5 -0.25  0
ve en   5    5    5    4    2    0    0     0    0    1    3    5    5
escala 10^ 0.25  0.5  0.75  1   1.25  1.5  1.75  2   2.25  2.5  2.75  3
ve en   5    5    5    5    5    3    2    2    1    3    3    4
```

**Caída con roce**
```
escala 10^ -3  -2.75 -2.5 -2.25 -2  -1.75 -1.5 -1.25 -1  -0.75 -0.5 -0.25  0
ve en   4    4    4    5    4    2    2    1    1    2    5    5    5
escala 10^ 0.25  0.5  0.75  1   1.25  1.5  1.75  2   2.25  2.5  2.75  3
ve en   4    5    3    3    4    4    5    5    5    5    5    5
```

| | oscilador | caída con roce |
|---|---|---|
| **tramos contiguos donde ve** | **3** | **3** |
| tramo más largo | 1.5 décadas | 1.75 décadas |

## 2. EL VEREDICTO: **ERRÁTICO**
El criterio congelado decía: *banda* si hay **exactamente un** tramo contiguo en los dos sistemas;
*errático* si hay **más de uno** en alguno. **Hay tres en cada uno.**

**Y lo más informativo no son los tramos, sino dónde está el agujero.** En los dos sistemas —con
leyes de forma distinta, semillas distintas y trayectorias distintas— la zona muerta cae **en el
mismo sitio: alrededor de 10⁻¹·⁵ a 10⁻¹**. Que dos sistemas independientes se apaguen en la misma
franja apunta a **un umbral interno del motor**, no a una propiedad de los sistemas.

## 3. MI PREDICCIÓN, y por qué la declaré antes
El prerregistro-46 dice, escrito antes de correr: *"declaro mi expectativa, para que se me pueda
descontar: espero **ERRÁTICO**. Si sale una banda limpia, mi lectura era ruido de siete puntos y lo
diré con esas palabras."*

**Salió errático.** Acerté — y lo único que hace creíble ese acierto es que estaba escrito antes,
sobre **cinco semillas nuevas**, porque las que me dieron la intuición (2, 3, 5, 7, 11) quedaron
quemadas y no se volvieron a usar.

## 4. POR QUÉ "ERRÁTICO" ES PEOR QUE "BANDA ESTRECHA"
**Una banda se rodea.** Si el motor viera solo entre 10⁰ y 10², bastaría normalizar los datos a esa
franja antes de preguntarle, y el problema quedaría resuelto de forma comprobable.

**Un patrón con agujeros no se rodea**, porque no hay una transformación que garantice caer en zona
buena: normalizar podría meterte justo en el hueco. **El veredicto del motor depende de las unidades
de una forma que no se puede corregir sin arreglar el motor.**

## 5. LO QUE ESTE ESTUDIO CONTROLÓ, para que no se lea de más
- **La relación señal/ruido es la misma en las 25 escalas** (ruido relativo, verificado: las tres
  razones medidas coinciden dentro del 1%). Sin esto, el estudio habría medido el ruido.
- **Control positivo:** a escala ×1 ve en 5 de 5 — hay anclaje.
- **Control negativo:** sobre ruido puro no declara ley en ninguna escala.
- **Dos sistemas con leyes de forma distinta**, para no confundir una propiedad del motor con una
  del oscilador. Los dos dan lo mismo.

## 6. LO QUE **NO** SE AFIRMA
- **Nada del universo.** Es una propiedad de nuestro código.
- **No se dice qué resultados nuestros están tocados.** Un motor con agujeros produce **falsos
  negativos**; lo que queda en duda son los *"no concluyente"*, no los hallazgos. Cuáles y cuánto
  exige medirlo campaña por campaña, y **no es lo que se hizo aquí**.
- **No se arregla el motor.** Va en su propio prerregistro, con su propia Regla 31 — y ahora se sabe
  que el arreglo tiene que atacar **dos** defectos, no uno: los agujeros (falsos negativos) y la
  alucinación sobre señal casi constante (falsos positivos, INFORME-54).

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Qué umbral interno del motor se apaga alrededor de 10⁻¹·⁵?** Los dos sistemas se apagan en la
> misma franja, así que hay un número concreto en el código —un corte de coeficiente, una
> tolerancia, un criterio de parada— que se vuelve incomparable con los datos a esa escala.
> Encontrarlo convierte "arreglar el motor" en un cambio localizado y comprobable, en vez de una
> reescritura a ciegas.

## 8. LA DECISIÓN QUE LE TOCA AL DIRECTOR
Ninguna urgente. Pero el balance del día sobre el motor central ya es éste: **dos defectos medidos,
independientes, y en direcciones opuestas.** Uno le hace perder leyes que están (agujeros de
escala); el otro le hace declarar leyes que no están (señal casi constante). Los dos aparecieron el
mismo día, **y los dos porque empezamos a examinar cosas que llevaban meses corriendo sin examen.**
