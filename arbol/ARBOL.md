# EL ÁRBOL — mapa visual del conocimiento del proyecto
**ÉPOCA 2 EN CURSO. Actualizado el 10-ago-2026 (tarde): H-002 pasa a REPLICADO — el empate sobrevive en cinco mundos distintos (INFORME-43). H-001 sigue en pie y su mitad pendiente (las firmas conductuales) queda cerrada en NO CONCLUYENTE PERMANENTE: ninguna duración hace fiable la vara (INFORME-44). La escalera de soporte replica su escalón 2 y su examen 5/5 pero queda PARCIAL por la cláusula "único apto" (INFORME-42). La rama de física del universo (N-00X-E2) queda como estaba desde el 8-ago (INFORME-22).**

**GitHub renderiza el diagrama automáticamente al abrir este archivo. Verde = nodo validado provisional; azul = nodo de CAPACIDAD (qué puede hacer el ente, no qué es cierto del universo — marcado `sobre-el-simulador`); rojo = capacidad medida que RECORTA una tesis nuestra; naranja = en cuarentena (Regla 31); amarillo = pregunta abierta; gris punteado = archivado.**

```mermaid
graph TD
    RAIZ(("FÍSICA SIN HERENCIA<br/>34 reglas · MENTE v12")):::raiz

    E2N001["N-001-E2 · 11-jul-2026<br/>Ley de retardos Mendeley — 8× sobre É1<br/>k = 0.017454 reapareció espontáneamente<br/>5/5 semillas"]:::nodo
    E2N002["N-002-E2 · 12-jul-2026<br/>Percepción propia: 8 variables autoinventadas<br/>ley acoplada replicada a la 4ª–6ª cifra<br/>5/5 · el dp Morpheus por fin cedió"]:::nodo
    E2N003["N-003-E2 · 12-jul-2026<br/>Primera automejora: ojos autoelegidos<br/>latente 4 (la más simple) · 5/5 criterio cumplido<br/>reclamo 'supera al humano' corregido (AUD-EXT-01)"]:::nodo
    E2N004["N-004-E2 · 13-jul, REDUCIDO 8-ago<br/>UNA conservada de la caída sobrevive al<br/>verdugo honesto (jueces 0.004, rompe solo<br/>en el video corrupto) · Michigan REFUTADO"]:::nodo

    E1["ÉPOCA 1 (archivada)<br/>N-001 · N-002 · N-003<br/>k invariante · transferencia entre trials<br/>la caída retiene su corona É1"]:::archivo

    H000["H-000 · 9-ago-2026 · sobre-el-simulador<br/>EL NACIMIENTO: la frontera yo/mundo emerge<br/>6/6 propiocepciones declaradas suyas · 5/5<br/>control de motores desconectados LIMPIO 5/5"]:::capacidad
    H001["H-001 · 10-ago-2026 · sobre-el-simulador<br/>Se reconoce por CONTINGENCIA, no por apariencia<br/>gemelo idéntico: +0.20 el suyo / −0.20 el otro · 5/5<br/>SOLO propiocepción — la visión no lo sostiene"]:::capacidad
    H002["H-002 · 10-ago-2026 · REPLICADO en 5 mundos<br/>La física de soporte NO necesita cuerpo<br/>empate 5/5 y otra vez 5/5 al variar la caída<br/>RECORTA nuestra tesis · se publicó como se firmó"]:::recorte

    PB{"¿Dónde SÍ gana el cuerpo?<br/>candidata: EXPERIMENTACIÓN DIRIGIDA<br/>(elegir qué hacer para resolver una duda)<br/>si tampoco ahí, sería noticia mayor"}:::pregunta
    PC{"¿Sobrevive el empate si el cuerpo puede<br/>TOCAR lo que observa? Hoy no puede:<br/>ésa es la diferencia entre mirar y experimentar"}:::pregunta
    PD["Firmas conductuales: CERRADO en no<br/>concluyente PERMANENTE (prereg-36)<br/>ninguna duración hace fiable la vara"]:::archivo
    PE{"Escalera de soporte: PARCIAL<br/>escalón 2 y examen replican 5/5, pero con<br/>mesa alta el contacto también pasa el piso<br/>¿debe el escalón 1 aislar UN canal, o varios?"}:::parcial

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

    RAIZ --> H000
    H000 --> H001
    H000 --> H002
    H002 --> PB
    H002 --> PC
    H001 --> PD
    H000 --> PE

    classDef capacidad fill:#12304d,stroke:#3498db,color:#fff,stroke-width:2px
    classDef recorte fill:#4d1a1a,stroke:#e74c3c,color:#fff,stroke-width:2px
    classDef parcial fill:#4a3d1a,stroke:#e67e22,color:#fff
    classDef raiz fill:#1a1a2e,stroke:#e94560,color:#fff,stroke-width:3px
    classDef nodo fill:#0f3d2e,stroke:#2ecc71,color:#fff,stroke-width:2px
    classDef cuarentena fill:#4a2d1a,stroke:#e67e22,color:#fff,stroke-width:2px
    classDef pregunta fill:#3d3d1a,stroke:#f1c40f,color:#fff
    classDef archivo fill:#2c2c2c,stroke:#7f8c8d,color:#ccc,stroke-dasharray: 5 5
```

## Cómo leerlo
- **Verde:** conocimiento validado provisional (nivel 1 de la Regla 19 — falta corroboración física y réplica independiente).
- **Azul (capacidad):** qué puede hacer el ente, no qué es cierto del universo. Nacen en el Gimnasio y llevan `sobre-el-simulador` de por vida: la gravedad de PyBullet es una ecuación que escribimos nosotros. **Jamás entran a la rama de física.**
- **Rojo (recorte):** una capacidad medida cuyo resultado **contradice una tesis nuestra**. Vale exactamente igual que un nodo verde y se escribe con el mismo detalle — es lo que separa un árbol de conocimiento de un folleto.
- **Naranja (cuarentena):** la Regla 31 encontró un defecto en el instrumento que lo validó; ni muerto ni vivo hasta la re-corrida. No entra al conectoma ni sirve de rival.
- **Amarillo:** preguntas abiertas — cada corrida nueva debe nacer de una (Regla 18).
- **Gris:** la Época 1, archivada con confianza retirada; sus leyes solo regresan venciendo.

## Cómo se actualiza
Al aprobar un nodo o abrir/cerrar una pregunta, el orquestador edita el diagrama y commitea. Verlo renderizado: abrir este archivo en GitHub.
