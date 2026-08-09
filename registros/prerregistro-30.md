# Prerregistro 30 — El gemelo y las firmas del bebé: los dos controles de oro del espejo — 9 de agosto de 2026
**Estado: FIRMADO por el director el 9-ago-2026 ("implementemos todo absolutamente todo").**

## Por qué (dos agujeros abiertos en el hito 0)

### Agujero A — el espejo puede ser de apariencia
El hito 0 declaró "el espejo" (coherencia visión↔propiocepción) con 4/5 semillas. Pero ese
resultado no distingue entre dos explicaciones muy distintas:
- **contingencia** — "esto obedece a mis órdenes, luego soy yo" (lo que queremos);
- **apariencia** — "esto tiene forma de brazo, luego soy yo" (un atajo que no es reconocerse).

La única forma de separarlas es poner en la escena un **segundo brazo idéntico** — misma forma,
misma masa, mismo color — que se mueve con **órdenes que no son suyas**. Es el control más duro
publicado en 2026 para distinción yo/otro en humanoides, y nuestro mundo lo monta con un brazo más.

### Agujero B — Diego detecta contingencia pero no la usa
Su balbuceo es ciego: no cambia nada al descubrir que algo obedece. El modelo computacional del
paradigma del móvil (grupo de O'Regan y Hoffmann, 2025) da tres conductas medibles que un ente
con contingencia de verdad exhibe: (1) mueve **más** la parte del cuerpo que produce efectos —
criterio clásico **1.5× sobre línea base**; (2) al desconectarse el efecto, produce una **ráfaga**
de intentos antes de rendirse; (3) distingue desconexión **gradual** de **abrupta**.

**Frontera de contaminación:** nada aquí le dice a Diego que deba moverse más donde hay efecto.
Se construye el instrumento que lo **mide**, y una política contingente **plantada** que sirve de
control positivo del instrumento — jamás un competidor ni un gen.

## Qué se construye (`codigo/espejo2.py`)
- `escena_gemelo` — dos brazos idénticos; el propio obedece a Diego, el ajeno a otra semilla.
- `prueba_gemelo` — mide cuánto obedece una representación a **sus** órdenes y cuánto a las del
  gemelo, con nulo por comandos barajados. Un espejo de apariencia da la misma cifra para ambos.
- `paradigma_movil` — las tres fases (línea base / contingencia / extinción) con el móvil acoplado
  a una articulación, y desconexión abrupta o gradual.
- `firmas` — las tres firmas con el criterio clásico, más una cuarta cifra: **especificidad**
  (¿sube solo la articulación del efecto, o sube todo el cuerpo?).

## Regla 31 declarada antes de correr (seis casos)
1. **Mi cuerpo** se reconoce: obedece a mis órdenes más que a las del gemelo, sobre el nulo.
2. **El gemelo no soy yo**: su cuerpo no puede declararse propio.
3. **Apariencia mezclada** (la media de ambos cuerpos, como vería una vista que no distingue quién
   es quién) discrimina **menos** que el cuerpo propio.
4. **Política contingente plantada** (control positivo) exhibe las firmas, y de forma específica.
5. **Balbuceo ciego** (lo que Diego hace hoy) **no** las exhibe — si el instrumento las ve donde
   no las hay, mide su propio ruido.
6. **Gradual y abrupta** no pueden dar la misma conducta.

## Resultado (corrido el 9-ago-2026)
**APRUEBA 6/6.**
- Mi cuerpo: obedece a mis órdenes **0.3097** vs al gemelo **0.0473** (nulo 0.0303) → se reconoce.
- El gemelo: obedece a mis órdenes 0.0079 vs a las suyas 0.2868 → **no** se declara mío.
- Apariencia mezclada: diferencia **−0.0477** contra +0.2624 del cuerpo propio → no discrimina.
- Política contingente: **2.08×** sobre línea base, otras articulaciones 1.12× → **específica**.
- Balbuceo ciego: 1.21× → no alcanza el 1.5×, **como debe ser**.

## Un hueco propio cazado por su Regla 31
La política contingente con refuerzo independiente por articulación subía **todas** (2.64× la
buena, 2.26× las otras) y perdía la especificidad. Causa real: el brazo es una cadena — mover la
articulación 0 sacude la 1 y la 2. Cura: **presupuesto finito de esfuerzo** repartido en
proporción a la correlación, de modo que subir una es bajar otra. Un bebé tampoco tiene energía
infinita.

## Qué se espera de la corrida oficial (predicción comprometida)
- El gemelo: **espero que la propiocepción se reconozca** (ya lo hace en el banco) y que **la
  visión falle o quede débil** — es coherente con que la visión-que-se-une no replicara (1/5).
- Las firmas: **espero que Diego NO las exhiba hoy**, porque no tiene política contingente. Ese
  resultado negativo es el que justifica construir una, y quiero registrarlo antes de tenerla.

## Qué NO se afirma
- No se afirma que Diego "se reconozca en un espejo" en ningún sentido humano.
- La política contingente **no entra al genoma**: es control positivo del instrumento.
- Umbrales (1.5×, horizonte 8, ganancia 0.6, fases de 400-500 pasos) **congelados aquí**.

## Firmado
Leo, director — 9-ago-2026, aprobación en conversación.
