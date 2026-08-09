# Prerregistro 33 — El cerebro motivacional, el sueño en dos fases y los dos blindajes del motor — 9 de agosto de 2026
**Estado: FIRMADO por el director el 9-ago-2026 ("implementemos todo absolutamente todo... avanza
uno por uno hasta terminar todo lo solicitado").**

Reúne seis mejoras que nacen de literatura 2025–2026 leída ese mismo día. Todas son matemática o
método: **ni un dato del mundo humano entra a Diego** (Regla 27 intacta).

---

## 1. G13 (poder) — diagnóstico de lazo abierto
Los creadores del concepto de *empowerment* (Polani/Salge/Tiomkin, 2025) publicaron que estimarlo
con secuencias de órdenes **fijas** subestima el control real en mundos con ruido, porque el
agente real corrige sobre la marcha. **No se arregló a ciegas: primero se midió.**

Mundo de juguete con verdad conocida donde el efecto de la orden **depende del estado**:

| Ruido | Lazo abierto | Lazo cerrado | Subestimación |
|---|---|---|---|
| 0.0 | +0.0404 | +0.0545 | +0.0141 |
| 0.1 | +0.0350 | +0.0473 | +0.0122 |
| 0.3 | +0.0191 | +0.0297 | +0.0106 |
| 0.6 | +0.0084 | **+0.0169** | +0.0084 |

**Confirmado en nuestro propio mundo:** con ruido 0.6 el lazo cerrado ve **el doble** de poder.
G13 sigue en modo `mide`; el arreglo queda medido y disponible, no impuesto.

## 2. G14 (incertidumbre) — examen conductual
La separación epistémica/aleatoria está cuestionada (position paper 2025: los métodos de segundo
orden son incompletos y se contradicen entre sí). **La defensa de la casa no puede ser el número:
tiene que ser la conducta.** El examen pone a la vez un televisor ruidoso **y** una zona aprendible
y exige **las dos cosas**: abandonar el televisor **y seguir explorando** lo aprendible. Teníamos
la mitad; ahora está la otra. Resultado: fracción TV final 0.00, aprendible 1.00, error 0.0033.

## 3. G2 (curiosidad) — modelo del propio error
LPM (ICLR 2026) prueba que llevar además un modelo de *cuánto espero equivocarme aquí*, y calcular
la curiosidad contra esa expectativa, da **cero ante lo inaprendible por construcción** — con
garantía formal, no por suerte. Medido: ante ruido irreducible la curiosidad media da **−5.3e−16**
(cero de máquina); con estructura real distingue puntos (desviación 0.0481).

## 4. G15 metacognición — GEN NUEVO, modo `mide`
¿Su confianza sabe cuándo acierta? Se mide con el estándar de la psicofísica humana (sensibilidad
metacognitiva, aquí como AUC de tipo 2). **Nulo natural perfecto:** con la confianza barajada debe
dar 0.5. Resultado: confianza informada **AUC 0.874** vs nulo 0.547; confianza ciega **0.513**, que
no supera su nulo 0.539 — sin conocimiento, sin crédito.
Entra a `arbol/GENOMA.json` en modo **`mide`**: `sinapsis.py` le impide decidir nada hasta que un
prerregistro firmado suba su modo.

## 5. Sueño (G9) en DOS FASES con guardián
- **Conservadora** — re-minería sobre episodios realmente vividos. Riesgo bajo: es repaso.
- **Generativa** — el modelo genera episodios imaginados y se mina también ahí.
- **FILTRO DE VIGILIA, mecánico:** una ley soñada solo pasa si su **soporte** coincide con una ley
  hallada despierto. No es una promesa escrita: está en el código y el banco lo vigila.

### La historia honesta de este guardián, porque el hallazgo cambió de forma
1. La primera corrida encontró **4 leyes** en los sueños de un modelo ajustado a ruido puro. Alarma.
2. Al perseguir la causa, **no era el mecanismo del sueño**: era `sindy3` declarando leyes sobre
   series cortas. Medido en 6 semillas de ruido: n=600 → **2/6 falsas**, n=1000 → 1/6, n=1500 → 1/6,
   n=2000 → **0/6**. Se le puso a `sindy3` una guarda de **MUESTRAS_MINIMAS = 2000** y la alarma se
   apagó.
3. **El filtro se conserva igual, como defensa en profundidad.** Un modelo lineal ajustado a
   cualquier cosa *es* un sistema lineal, y soñado hacia adelante genera trayectorias con
   estructura — la estructura **del modelo**, no la del mundo. Que hoy el guardián dé cero no
   significa que el riesgo no exista: significa que la primera puerta lo detuvo.

**Este es un hallazgo que corrige un módulo ya firmado (prereg-28) tres horas después de firmarlo.**
Queda escrito así, sin suavizar.

## 6. Los dos blindajes del motor simbólico
- **Residuos en Koopman.** Está demostrado que la discretización finita del operador produce
  **fantasmas**: autovalores espurios que son artefactos del truncamiento. Ahora cada candidato
  lleva su residuo `‖(K−λI)g‖/‖g‖` y solo pasa por debajo de 0.10. Medido: el invariante real
  tiene residuo **0.000**; vectores al azar, **0.134–0.255** — todos rechazados.
- **Chaperón causal.** El consenso 2024–2026 es que un método causal bivariado produce aristas
  indirectas. Ahora existe `TE(U→Y|Z)`. Medido en una cadena a→b→c construida a propósito: la
  bivariada declaraba **+1.4774 bits** de a a c (flecha **falsa**, a no toca a c) y el chaperón la
  dejó en **+0.0111** — una reducción del **99.2%**.
  **Honestidad sobre su límite:** el chaperón **no anula** la arista espuria, la derrumba. Por eso
  el criterio de la casa es *"reduce ≥90%"*, no *"da cero"*. Y como la tabla condicional tiene
  bins⁴ celdas, se añadió guarda de muestras: por debajo de 40 por celda **se niega a opinar**.

---

## Regla 31 de todo lo anterior (declarada antes de correr)
| Módulo | Casos | Resultado |
|---|---|---|
| `cerebro.py` | 6 (lazo, examen doble, curiosidad ante ruido y ante estructura, meta positiva y ciega) | **APRUEBA 6/6** |
| `sueno.py` dos fases | 4 (conservadora, guardián, generativa, mundo de ruido) | **APRUEBA 4/4** |
| `koopman.py` residuos | 2 (invariante real ≈0, vector al azar rechazado) | **APRUEBA** |
| `entropia_transferencia.py` | 2 (derrumbe ≥90%, guarda de muestras) | **APRUEBA** |

**11 casos nuevos congelados en el banco.**

## Qué NO se afirma
- Ningún gen cambia de modo aquí. G13, G14 y el nuevo G15 siguen **midiendo**. Subirlos a
  `propone` o `decide` exige su propio prerregistro firmado, y `sinapsis.py` lo impide mientras
  tanto.
- El sueño **propone**; la vigilia confirma; el director firma. Ninguna ley soñada será nodo.
- Todos los umbrales (residuo 0.10, reducción 0.90, 40 muestras/celda, 2000 muestras mínimas,
  piso de inclusión 0.9) quedan **congelados aquí**.

## Firmado
Leo, director — 9-ago-2026, aprobación en conversación.
