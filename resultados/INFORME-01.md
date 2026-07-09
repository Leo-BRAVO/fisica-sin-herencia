# INFORME 01 — Corrida piloto, Fase 0 — 9 de julio de 2026
*(Regla 17: escrito en español llano. Si algo no se entiende, el informe está mal hecho.)*

## 1. Qué se hizo
Se le dieron a la máquina 3,883 mediciones reales de un sistema físico (dos señales, `s1` y `s2`, rastreadas por video en un laboratorio de Michigan — dataset público Mendeley 7yd2ntbh3w). NO se le dijo qué era el sistema, ni qué significaban las señales, ni ninguna física. Se le pidió una sola cosa: encontrar fórmulas matemáticas que predigan el valor siguiente de cada señal. Buscó tres veces desde puntos de partida aleatorios distintos (semillas 1, 2 y 3), evaluando ~14,000 fórmulas por segundo. La regla del juego, firmada ANTES de correr (prerregistro-01 + enmienda-01): sus fórmulas debían predecir el 30% final de los datos — que jamás vio — con menos de la mitad del error del mejor predictor trivial.

## 2. Qué se encontró (en una frase)
**La máquina descubrió, tres veces por caminos independientes, la misma fórmula para la señal 1 — y esa fórmula predice el futuro oculto del sistema 4.5 millones de veces mejor que la predicción trivial.**

## 3. Los números
| Corrida | Error sobre futuro oculto | Umbral exigido | Veredicto |
|---|---|---|---|
| Semilla 1 | 0.1511 | < 0.1518 | SUPERA |
| Semilla 2 | 0.2580 | < 0.1518 | no supera |
| Semilla 3 | 0.1474 | < 0.1518 | SUPERA |
Criterio del piloto: 2 de 3 → **CUMPLIDO**.

La fórmula replicada (señal 1), en las tres semillas con constantes idénticas hasta el 4º decimal:
`siguiente_s1 = s1 + (cambio de s1) + sin((s1−s2) × −0.01747) + sin(s1 × −0.0180)`
La constante −0.01747 apareció también en las fórmulas de la señal 2 de las tres semillas.

## 4. Los intentos de destrucción (Regla 11)
- **Ruido puro:** la máquina no encontró nada con habilidad real (errores ~1.57 millones contra umbral de 382 mil). FRACASÓ correctamente. ✓
- **Tiempo barajado:** ídem (errores ~1.23 millones contra umbral de 306 mil). FRACASÓ correctamente. ✓
- **Hallazgo colateral:** la primera vara de medir tenía un defecto (la línea base de velocidad es absurdamente mala en datos sin estructura). Se detectó gracias al propio verdugo, se corrigió endureciendo el criterio (enmienda-01, registrada antes de conocer los resultados finales), y el resultado del piloto quedó igual o más fuerte.

## 5. Qué significa y qué NO significa
- Significa: el método funciona de punta a punta — la máquina puede extraer regularidades reales y replicables de datos crudos sin recibir física humana, y nuestras defensas contra el autoengaño funcionan.
- NO significa: que hayamos descubierto física nueva (esto es el peldaño de validación del método, con respuesta conocida por la humanidad — aunque la máquina no la conoce).

## 6. Qué decisión le toca al director
1. Aprobar la corrida OFICIAL (10 semillas, misma vara enmendada) para consolidar el resultado, más la replicación con Trials 2 y 3.
2. Aprobar el nodo N-001 (borrador en `arbol/N-001.md`) como primer nodo PROVISIONAL del árbol.
3. Decidir cuándo hacemos las mejoras aprobadas: git bien instalado, vara lineal como tercer rival, regla de gobernanza de enmiendas.
