# EL ÁRBOL — mapa visual del conocimiento del proyecto
**ÉPOCA 2 EN CURSO (11-jul-2026, orden del director):** el árbol de la Época 1 (N-001, N-002, N-003) fue ARCHIVADO en `arbol/epoca1/` con la confianza retirada — la rederivación total con la tubería mejorada (prerregistro-12) decidirá qué se reconfirma, qué se refina y qué se poda. El diagrama de abajo muestra la Época 1 como referencia histórica; el árbol vivo de la Época 2 nace vacío y sus leyes deben VENCER a las viejas para entrar.

**Se actualiza con cada nodo nuevo. GitHub renderiza el diagrama automáticamente al abrir este archivo. Verde = nodo validado provisional; amarillo = pregunta abierta (candidata a nodo); gris = pregunta respondida o en curso.**

```mermaid
graph TD
    RAIZ(("FÍSICA SIN HERENCIA<br/>27 reglas · MENTE v4")):::raiz

    N001["N-001 · 9-jul-2026<br/>Regularidad replicada en Mendeley-DP<br/>estructura: valor + cambio + sin(acople×k)<br/>10/10 semillas · sobrevivió 2 verdugos"]:::nodo
    N002["N-002 · 9-jul-2026<br/>k ≈ 0.01746 pertenece al SISTEMA<br/>3 corridas físicas · 30/30 ecuaciones<br/>hijo de N-001"]:::nodo

    P1{"¿La fórmula RUEDA<br/>multi-paso?"}:::pregunta
    P3{"¿Hay cantidad<br/>CONSERVADA?"}:::pregunta
    P4{"¿Video coincide<br/>con encoder?"}:::pregunta
    P5{"¿Por qué resiste<br/>la señal 2?"}:::pregunta

    N003["N-003 · 9-jul-2026<br/>La fórmula TRANSFIERE sin re-entrenar<br/>Trial1→Trial2 y Trial1→Trial3 bajo umbral<br/>hijo de N-001 y N-002"]:::nodo

    Q1{"¿k depende de las UNIDADES?<br/>re-escalado ×100: evidencia parcial SÍ<br/>(INFORME-04, resultado C con traza de A)"}:::parcial
    Q3{"¿k sobrevive a un APARATO distinto?<br/>peldaño 2: caída y vuelo<br/>+ péndulo propio del director"}:::pregunta
    Q4{"¿Cuánto RUEDA la fórmula<br/>multi-paso antes de degradarse?"}:::pregunta

    E2N001["N-001-E2 · 11-jul-2026<br/>Ley de retardos Mendeley — 8× sobre É1<br/>k reapareció espontáneamente<br/>PRIMER NODO DEL ÁRBOL VIVO"]:::nodo

    RAIZ --> E2N001
    RAIZ --> N001
    N001 --> N002
    N001 --> P1
    N001 --> P3
    N001 --> P4
    N001 --> P5
    N002 --> Q1
    N002 --> N003
    N002 --> Q3
    N003 --> Q4

    classDef parcial fill:#4a3d1a,stroke:#e67e22,color:#fff

    classDef raiz fill:#1a1a2e,stroke:#e94560,color:#fff,stroke-width:3px
    classDef nodo fill:#0f3d2e,stroke:#2ecc71,color:#fff,stroke-width:2px
    classDef pregunta fill:#3d3d1a,stroke:#f1c40f,color:#fff
    classDef encurso fill:#2c2c54,stroke:#818cf8,color:#fff,stroke-dasharray: 5 5
```

## Cómo leerlo
- **Nodos verdes:** conocimiento validado (provisional hasta subir la escalera de la Regla 19).
- **Rombos amarillos:** preguntas abiertas — el combustible de la Regla 18. Cada corrida nueva debe nacer de uno de estos.
- **Rombos punteados:** investigación en curso con prerregistro firmado.
- Los detalles de cada nodo viven en su archivo (`N-001.md`, `N-002.md`); este mapa es el índice visual.

## Cómo se actualiza
Al aprobar un nodo o abrir/cerrar una pregunta, el orquestador edita el diagrama y commitea. Verlo renderizado: abrir este archivo en GitHub (lo dibuja solo).
