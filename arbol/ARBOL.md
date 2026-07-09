# EL ÁRBOL — mapa visual del conocimiento del proyecto
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

    Q1{"¿k depende de las UNIDADES?<br/>test re-escalado ×100<br/>— EN CURSO (prereg-04)"}:::encurso
    Q2{"¿TRANSFERENCIA directa<br/>entre trials sin re-entrenar?<br/>— siguiente (aprobada)"}:::pregunta
    Q3{"¿k sobrevive a un SISTEMA distinto?<br/>peldaño 2: caída y vuelo<br/>+ péndulo propio del director"}:::pregunta

    RAIZ --> N001
    N001 --> N002
    N001 --> P1
    N001 --> P3
    N001 --> P4
    N001 --> P5
    N002 --> Q1
    N002 --> Q2
    N002 --> Q3

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
