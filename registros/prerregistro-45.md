# Prerregistro 45 — LA BANDA DE ESCALA DEL MOTOR, y qué campañas cayeron fuera — 10 de agosto de 2026
**Nace del INFORME-50: `sindy3` encuentra la misma ley a ×1 y ×10 y NO la encuentra a ×0.1 ni ×100.**
**Peldaño (Regla 9): Fase 1.** No se sube de peldaño: es una propiedad de nuestro código.

---

## 0. LO QUE YA SE SABE, y por qué no basta
Está medido y guardado en `resultados/p43-escala-sindy3/medida.json`: cuatro escalas, mismo
oscilador, dos veredictos distintos. **Lo que NO se sabe es dónde están los bordes de la banda ni
si alguna campaña nuestra cayó fuera** — y ésa es la pregunta que importa, porque de su respuesta
depende cómo hay que leer todos nuestros resultados negativos.

## 1. LAS DOS PREGUNTAS
1. **¿Dónde están los bordes?** Barrido fino de escala sobre un sistema de respuesta conocida.
2. **¿Alguna campaña nuestra cayó fuera?** El mismo barrido sobre los datos de cada campaña que
   produjo un nodo o un "no concluyente".

## 2. LA LÍNEA BASE TONTA (Regla 11)
El predictor ingenuo es **"el motor encuentra la ley siempre que exista, sin importar las
unidades"** — que es lo que cualquiera supondría de un motor de descubrimiento, y es la hipótesis
que el INFORME-50 ya refutó en cuatro puntos. **La medida de este estudio es cuánto se aparta el
motor de ese ideal**, no un acierto crudo: se reporta como **fracción de escalas en que ve**, sobre
un barrido declarado de antemano.

## 3. EL DISEÑO
- **Barrido:** escalas `10^k` con `k` de −3 a +3 en pasos de 0.25 → **25 puntos**, declarados aquí.
- **Sistema:** el mismo oscilador amortiguado del INFORME-50, y **además** un segundo sistema
  distinto (caída con roce) para no confundir una propiedad del motor con una del oscilador.
- **Cinco semillas** por punto: `2, 3, 5, 7, 11`.
- **La medida:** en cada escala, en cuántas de las 5 semillas el motor declara ley.

## 4. LOS CRITERIOS, congelados
1. **Se confirma que hay banda** si existe un intervalo contiguo de escalas donde el motor ve en
   **≥4 de 5** semillas, y **fuera** de él ve en **≤1 de 5**, en **los dos sistemas**.
2. **Se confirma que la banda es estrecha** —y por tanto grave— si abarca **menos de 3 décadas**.
3. **Si el motor ve en las 25 escalas**, el INFORME-50 queda **contradicho por este estudio** y hay
   que buscar la causa en otra parte. **Ese resultado es posible y sería mi error**, y se escribiría
   con esas palabras.

## 5. REGLA 31 — LOS DOS LADOS
- **Debe fallar donde no hay nada:** sobre **ruido puro** escalado igual, el motor no puede declarar
  ley en ninguna de las 25 escalas. Si la declara en alguna, el estudio se detiene: el hallazgo no
  sería sobre la escala sino sobre un motor que inventa.
- **Debe aprobar donde sí hay:** en la escala ×1, el motor debe declarar ley en **5 de 5** semillas.
- **SEÑUELO:** un sistema **sin dinámica** (constante más ruido) escalado igual no puede dar ley en
  ninguna escala. Si la da, **NULO**.

## 6. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si el control negativo declara ley en **≥1** escala → **se detiene**, no se reporta banda.
- Si el señuelo aprueba → **NULO**.
- **No hay segunda vuelta ampliando el barrido** hasta que aparezca la banda que me gustaría ver.
  Los 25 puntos son los que hay.

## 7. QUÉ SE HARÁ CON EL RESULTADO — y qué NO
- **Si hay banda estrecha:** se escribe un prerregistro **aparte** para el arreglo (normalizar antes
  de ajustar y re-escalar los coeficientes después), con su propia Regla 31. **El arreglo no se
  hace en este estudio**: medir y arreglar en la misma corrida es cómo se acaba arreglando hasta
  que el número salga bonito.
- **Si alguna campaña insignia cayó fuera de la banda:** su acta se **anota**, no se reescribe
  (Regla 8), y el nodo correspondiente pasa a revisión con el director.
- **No se degrada ningún nodo por precaución** antes de tener la medida.

## 8. LO QUE ESTO **NO** PUEDE AFIRMAR
- Nada del universo.
- **No dice que nuestros resultados sean falsos.** Un motor con banda estrecha produce **falsos
  negativos** (leyes que no vio), no falsos positivos. Lo que quedaría en duda son los "no
  concluyente", no los hallazgos.

## 9. FIRMA
Avanza por **quórum adversarial**: es una decisión sobre cómo medir, con el barrido y los criterios
congelados antes de correr, y con un veredicto posible que me deja mal. Revocable con una palabra
del director.
