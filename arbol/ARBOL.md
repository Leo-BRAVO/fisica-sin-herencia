# EL ÁRBOL — mapa visual del conocimiento del proyecto
**ÉPOCA 2 EN CURSO. Actualizado el 8-ago-2026 (INFORME-22): E2-N-004 salió de cuarentena REDUCIDO — Michigan refutado por el nulo honesto, la caída sobrevive con una candidata distinta validada contra el verdugo que aprueba la Regla 31. La Época 1 vive archivada en `arbol/epoca1/` con la confianza retirada.**

**GitHub renderiza el diagrama automáticamente al abrir este archivo. Verde = nodo validado provisional; naranja = en cuarentena (Regla 31); amarillo = pregunta abierta; gris punteado = en curso.**

```mermaid
graph TD
    RAIZ(("FÍSICA SIN HERENCIA<br/>32 reglas · MENTE v12")):::raiz

    E2N001["N-001-E2 · 11-jul-2026<br/>Ley de retardos Mendeley — 8× sobre É1<br/>k = 0.017454 reapareció espontáneamente<br/>5/5 semillas"]:::nodo
    E2N002["N-002-E2 · 12-jul-2026<br/>Percepción propia: 8 variables autoinventadas<br/>ley acoplada replicada a la 4ª–6ª cifra<br/>5/5 · el dp Morpheus por fin cedió"]:::nodo
    E2N003["N-003-E2 · 12-jul-2026<br/>Primera automejora: ojos autoelegidos<br/>latente 4 (la más simple) · 5/5 criterio cumplido<br/>reclamo 'supera al humano' corregido (AUD-EXT-01)"]:::nodo
    E2N004["N-004-E2 · 13-jul, REDUCIDO 8-ago<br/>UNA conservada de la caída sobrevive al<br/>verdugo honesto (jueces 0.004, rompe solo<br/>en el video corrupto) · Michigan REFUTADO"]:::nodo

    E1["ÉPOCA 1 (archivada)<br/>N-001 · N-002 · N-003<br/>k invariante · transferencia entre trials<br/>la caída retiene su corona É1"]:::archivo

    P1{"¿Nulos surrogados de las campañas<br/>insignia? (mendeley: se corre en la<br/>NUBE vía Actions; p14 espera ojos)"}:::pregunta
    P2{"Dimensión intrínseca: MEDIDA 2/3<br/>(Michigan ~3 · caída ~2.3, INF-22)<br/>falta dp Morpheus (rastreo 2 cuerpos)"}:::parcial
    P3{"¿Los latentes canonizan a los<br/>ángulos físicos o son una carta<br/>alternativa tipo Columbia?"}:::pregunta
    P4{"¿Ojos con pérdida de conservación<br/>verían lo eterno directamente?<br/>(N-004 ya resuelto — pregunta ABIERTA)"}:::pregunta
    P5{"¿El bucle multi-perilla (latente+<br/>tubería junta) mejora más?"}:::pregunta

    RAIZ --> E2N001
    RAIZ -.-> E1
    E2N001 --> E2N002
    E2N002 --> E2N003
    E2N001 --> E2N004
    E2N002 --> E2N004
    RAIZ --> P1
    RAIZ --> P2
    E2N002 --> P3
    E2N004 --> P4
    E2N003 --> P5

    classDef parcial fill:#4a3d1a,stroke:#e67e22,color:#fff
    classDef raiz fill:#1a1a2e,stroke:#e94560,color:#fff,stroke-width:3px
    classDef nodo fill:#0f3d2e,stroke:#2ecc71,color:#fff,stroke-width:2px
    classDef cuarentena fill:#4a2d1a,stroke:#e67e22,color:#fff,stroke-width:2px
    classDef pregunta fill:#3d3d1a,stroke:#f1c40f,color:#fff
    classDef archivo fill:#2c2c2c,stroke:#7f8c8d,color:#ccc,stroke-dasharray: 5 5
```

## Cómo leerlo
- **Verde:** conocimiento validado provisional (nivel 1 de la Regla 19 — falta corroboración física y réplica independiente).
- **Naranja (cuarentena):** la Regla 31 encontró un defecto en el instrumento que lo validó; ni muerto ni vivo hasta la re-corrida. No entra al conectoma ni sirve de rival.
- **Amarillo:** preguntas abiertas — cada corrida nueva debe nacer de una (Regla 18).
- **Gris:** la Época 1, archivada con confianza retirada; sus leyes solo regresan venciendo.

## Cómo se actualiza
Al aprobar un nodo o abrir/cerrar una pregunta, el orquestador edita el diagrama y commitea. Verlo renderizado: abrir este archivo en GitHub.
