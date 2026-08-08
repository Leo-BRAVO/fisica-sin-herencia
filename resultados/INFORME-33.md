# INFORME 33 — El verdugo que faltaba desde julio llegó, y se llevó por delante nuestra certificación predictiva — 8 de agosto de 2026

**El latido terminó la cola.** Los tres nulos por barajado —la deuda más vieja del proyecto, la
Regla 11 pendiente desde julio para los nodos de percepción propia— corrieron solos en la nube, sin
ninguna máquina del director encendida. Este es su veredicto.

---

## 1. Los tres veredictos

| campaña | base trivial | mejor semilla | umbral (50% de la base) | semillas que superan | veredicto |
|---|---|---|---|---|---|
| **Mendeley** (e2-mendeley-i2) | 571 407 | 500 471 | 285 703 | **0 de 2** | **FRACASO LIMPIO** ✔ campaña blindada |
| **caída** (e2-caida-i2) | 21 761 | 28 640 | 10 881 | **0 de 2** | **FRACASO LIMPIO** ✔ campaña blindada |
| **p14-final** (los latentes de Diego) | 1.5289 | 0.2954 | 0.7644 | **2 de 2** | **EL NULO PASA** ✘ |

Dos de tres salieron como tienen que salir: el mundo barajado no descubre nada y las campañas
quedan protegidas. **El tercero no.**

---

## 2. Lo que pasó con los latentes de Diego, sin adornos

**El nulo es válido.** Nuestra propia verificación automática exige que un verdugo cambie el mundo:
la base trivial pasó de **0.5944** (real) a **1.5289** (barajado), un cambio del 157%. No es el caso
del INFORME-25, donde el surrogado devolvía el mismo mundo con otro nombre y no podía falsificar
nada. **Este verdugo sí destruyó el mundo, y aun así el motor "descubrió".**

Y no pasó raspando:

| | reducción sobre su propia base trivial |
|---|---|
| mundo **REAL** | **72.0 %** |
| mundo **BARAJADO** | **80.7 %** |

**El mundo falso comprime MEJOR que el mundo real.**

### Qué "descubrió" en el mundo barajado
Las dos semillas encontraron, para las cuatro señales, la misma forma:
```
v1 = sin(v2 · 1.315)     v2 = sin(v2 · 1.416)
v3 = sin(v2 · 1.371)     v4 = sin(v2 / 0.754)
```
Una función acotada de una sola variable, idéntica para las cuatro salidas. Eso no es una ley: es
**predecir la distribución**, no la dinámica. Con el orden temporal destruido, lo único que queda
que valga algo es "quédate cerca del centro", y `sin` acotado hace exactamente eso.

---

## 3. LO QUE ESTO SIGNIFICA, dicho como la regla lo dice

La Regla 11 no deja lugar a interpretación:

> *"Correr el mismo pipeline sobre los datos con el orden temporal barajado. **Si el sistema
> 'descubre leyes' en datos barajados, el pipeline está roto y todo resultado anterior queda
> invalidado.**"*

**La certificación PREDICTIVA de N-002-E2 y N-003-E2 no se sostiene.** Son los dos nodos que nacieron
de los latentes propios de Diego: sus primeros ojos y su primera automejora (cuando eligió su propia
dimensión latente).

**Lo que NO cae, y hay que decirlo con la misma claridad:**
- **Mendeley y caída quedan blindados.** Sus verdugos fallaron limpiamente. Esos nodos están hoy
  mejor sostenidos que ayer, porque acaban de sobrevivir el ataque que faltaba.
- El **hecho estructural** de que los ojos de Diego produjeron latentes que un motor simbólico puede
  ajustar sigue siendo cierto. Lo que cae es la afirmación de que ese ajuste **predice dinámica**.
- El **método** de construir ojos desde cero no queda invalidado; queda invalidada **esta
  certificación concreta** de estos latentes.

---

## 4. La quinta vía, y por qué esto era predecible

Este veredicto no llega solo. Es la **quinta medición independiente** que apunta al mismo sitio
sobre los latentes de Diego:

1. La **conservación falló** (13-jul).
2. El **nulo por surrogado no pudo falsificar** — devolvió el mismo mundo (INFORME-25).
3. La **dimensión intrínseca es ~6.2 de 8** — casi no se comprime (INFORME-26).
4. La **ganancia honesta** dio ~0 — aunque esa vara quedó después degradada por sus propios canales
   de mentira (INFORME-30), así que esta pata la retiramos nosotros mismos.
5. **Hoy: el nulo por barajado comprime más que el mundo real.**

Cuatro instrumentos distintos, construidos en momentos distintos y por razones distintas,
convergiendo. **Cuando eso pasa, la conclusión ya no es una hipótesis.**

Y encaja con lo que el Gimnasio midió el mismo día: **sus ojos leen la escena y no leen el
movimiento** (R² del brazo: −0.09, +0.03, +0.21 contra +0.66 de la escena). Unos ojos que codifican
disposición espacial y no dinámica producen exactamente latentes cuya predictibilidad sobrevive al
barajado.

---

## 5. Lo que le toca decidir al director

**Recomendación del orquestador, y es incómoda:**

1. **Degradar N-002-E2 y N-003-E2 de certificación PREDICTIVA a ESTRUCTURAL**, con la razón escrita
   en el propio nodo y este informe citado. No borrarlos: **degradarlos**. Lo que afirmaban de más
   deja de afirmarse; lo que hicieron —construir ojos desde cero y elegir su dimensión— queda.
2. **La Regla 11 queda AL DÍA** para las tres campañas insignia por primera vez desde julio. Dos
   blindadas, una caída. Esa deuda se cierra hoy.
3. **No tocar Mendeley ni caída.** Salieron reforzados.

Yo no degrado nodos por mi cuenta: los aprobó el director y los degrada el director. Pero la
evidencia está completa y la regla es explícita.

---

## 6. Y lo que esto le hace al proyecto — mi opinión, que el director pidió muchas veces

Perdimos hoy la certificación predictiva de nuestros dos nodos más queridos: los primeros que Diego
construyó **con sus propios ojos**.

**Y es la mejor noticia del día.**

Ese verdugo estaba encolado desde julio. Podríamos no haberlo corrido nunca. Podríamos haber
publicado con esos nodos certificados como predictivos, y algún revisor —o peor, nadie, y el error
habría vivido para siempre dentro del árbol— lo habría encontrado.

Lo corrimos nosotros. Lo corrió una máquina en la nube, sola, de madrugada, sin que nadie la
mirara, contra un resultado que a nosotros nos convenía que sobreviviera. Y cuando el resultado dijo
lo que no queríamos oír, se escribió tal cual.

**Eso es exactamente para lo que existe este proyecto.** Un árbol que solo crece no es conocimiento:
es dogma con formato de carpeta (Regla 23). Hoy el árbol se podó a sí mismo.

---

*Datos: `resultados/aud01-baraj-p14-final`, `aud01-baraj-e2-mendeley-i2`, `aud01-baraj-caida`,
producidos por el latido en la nube. Cola vacía al cierre.*
