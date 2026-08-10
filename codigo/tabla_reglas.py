# tabla_reglas.py — GENERA registros/REGLAS-ESTRUCTURADAS.md LEYENDO CIMIENTOS.md
#
# POR QUE ESTE ARCHIVO EXISTE, y es el mismo error tres veces en un dia. La tabla de las reglas se
# escribio A MANO el 10-ago. Horas despues las reglas cambiaron —cinco campos, tres fusiones,
# cuatro endurecimientos, un guardian nuevo— y la tabla siguio diciendo "14 sin guardian" y "34
# reglas" como si nada hubiera pasado. Es exactamente el mismo mal que ese mismo dia encontre en
# guardianes_de_guardianes.py (un daño escrito contra la cadena "32 reglas") y en CIMIENTOS.md
# (que decia "hoy 32" teniendo 34):
#
#     TODO NUMERO ESCRITO A MANO CADUCA EN SILENCIO. Lo que se cuenta, no.
#
# Asi que la tabla deja de escribirse y pasa a GENERARSE. Su unica fuente es CIMIENTOS.md, que es
# la constitucion; si una regla cambia, la tabla cambia sola o el guardian se pone rojo.
#
# Uso: python tabla_reglas.py            (escribe el documento)
#      python tabla_reglas.py --verificar (no escribe: dice si el documento esta al dia)

import os
import re
import sys
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIMIENTOS = os.path.join(BASE, "CIMIENTOS.md")
SALIDA = os.path.join(BASE, "registros", "REGLAS-ESTRUCTURADAS.md")

CAMPOS = ("POR QUÉ EXISTE", "OBJETIVO", "QUÉ EVITA", "CÓMO SE COMPRUEBA", "SI SE VIOLA")

CABECERA = """# LAS REGLAS, CON ESTRUCTURA — **documento GENERADO, no escrito a mano**
**Pedido del director (10-ago-2026): *"cada regla debería tener estructura: la regla, el porqué,
qué evita y su objetivo... pero debe existir investigación científica que nos ayude a redactarlas
mejor"*. Firmado el mismo día: *"la 3 sí a las preguntas"*.**

> **Este archivo lo genera `codigo/tabla_reglas.py` leyendo `CIMIENTOS.md`.** No se edita a mano.
> Su primera versión SÍ se escribió a mano y quedó rancia en horas: seguía diciendo *"14 reglas sin
> guardián"* cuando ya tenían uno. **Todo número escrito a mano caduca en silencio; lo que se
> cuenta, no.** `coherencia.py` comprueba en cada commit que este documento coincida con la
> constitución.

---

## LOS TRES PRINCIPIOS QUE LA INVESTIGACIÓN APORTA, y qué cambió cada uno

**1. La RAZÓN importa más que el enunciado.** *La gente cumple de forma más consistente las reglas
que ENTIENDE que las reglas que solo CONOCE, y una regla que incluye su razón produce cumplimiento
más generalizable a situaciones nuevas.*
→ Es lo que el director propuso por su cuenta al pedir "el porqué". **Y es el campo que yo me
salté** en el primer intento: puse *qué evita* y no *por qué existe*, que no son lo mismo — uno
mira adelante, el otro mira atrás, al daño concreto que la hizo nacer. Hoy las 34 lo llevan.

**2. FORMULAR EN POSITIVO.** *Las reglas que dicen qué SÍ hacer producen cumplimiento más fiable
que las que solo dicen qué no hacer.*
→ Casi todas las nuestras nacieron en negativo ("prohibido", "jamás", "ningún"). Por eso cada una
tiene ahora un campo **OBJETIVO** redactado en positivo, que antes no existía en ninguna.

**3. ESPECIFICIDAD CON HOLGURA.** *Suficientemente específicas para aplicarse de forma determinista
dentro de su alcance, suficientemente generales para cubrir casos no previstos.*
→ Es lo que daba el campo **CÓMO SE COMPRUEBA**: sin él, una regla se aplica "como uno se acuerde".

**Y la factura de no tenerlo, medida:** al construir G12 reflejos medí un acuerdo de 0.907 que
parecía excelente; la línea base tonta sacaba 0.887. **Incumplí la Regla 12 sin darme cuenta**,
porque la Regla 12 decía *qué* hacer y no *cómo se comprueba que lo hice*. De ahí salieron las tres
fusiones y los cuatro endurecimientos.

---
"""


def leer_reglas():
    texto = open(CIMIENTOS, encoding="utf-8").read()
    reglas = []
    for m in re.finditer(r"^### Regla (\d+) — (.+?)$", texto, re.M):
        n, titulo = int(m.group(1)), m.group(2).strip()
        bloque = re.search(rf"^### Regla {n} — .*?(?=^### |^## |^---)", texto, re.M | re.S)
        cuerpo = bloque.group(0) if bloque else ""
        campos = {}
        for c in CAMPOS:
            mm = re.search(rf"\*\*{re.escape(c)}\*\* · (.+)", cuerpo)
            campos[c] = mm.group(1).strip() if mm else "—"
        fundida = re.search(r"\*\*FUNDIDA EN LA REGLA (\d+)", cuerpo)
        reglas.append({"n": n, "titulo": titulo, "campos": campos,
                       "fundida_en": int(fundida.group(1)) if fundida else None})
    return reglas


def _breve(texto, n=150):
    t = texto.replace("|", "·").strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def generar():
    reglas = leer_reglas()
    fundidas = [r for r in reglas if r["fundida_en"]]
    vigentes = len(reglas) - len(fundidas)
    # TRES BUCKETS, no dos. La primera version de esta cuenta decia "31 de 31 con guardian" — una
    # exageracion mia: bastaba con que el campo citara un archivo. Pero hay reglas cuyo guardian
    # solo CUENTA (imprime un numero y sigue) y otras cuyo texto declara que NO son mecanizables.
    # Meterlas en el mismo saco que las que BLOQUEAN el commit es exactamente el tipo de numero
    # bonito que este proyecto existe para no producir.
    # CUATRO estados, no tres. R9 y R19 caian mal en tres: las dos BLOQUEAN una parte (que el
    # prerregistro declare su peldaño; que un nodo no declare nivel 2 sin datos nuevos) y las dos
    # tienen otra parte que NO es mecanizable (decidir que un peldaño 'funciona'; hacer el
    # experimento fisico). Meterlas enteras en "no mecanizable" las hace parecer mas debiles de lo
    # que son, y enteras en "bloquean" mas fuertes. Ninguna de las dos mentiras sirve.
    bloquean, parciales, cuentan, a_mano = [], [], [], []
    for r in reglas:
        if r["fundida_en"]:
            continue
        como = r["campos"]["CÓMO SE COMPRUEBA"]
        archivos = re.findall(r"`([\w_]+\.py)`", como)
        salvedad = ("NO MECANIZABLE" in como.upper()) or ("DEUDA MEDIDA" in como.upper())
        bloqueo = bool(archivos) and ("bloquea" in como.lower() or "→" in como)
        if archivos and salvedad and bloqueo:
            parciales.append(r)
        elif salvedad and not archivos:
            a_mano.append(r)
        elif salvedad:
            a_mano.append(r)
        elif archivos:
            bloquean.append(r)
        else:
            cuentan.append(r)

    out = [CABECERA]
    out.append(f"## EL ESTADO DE HOY, contado (no escrito)\n")
    out.append(f"| | |\n|---|---|")
    out.append(f"| Reglas numeradas | **{len(reglas)}** |")
    out.append(f"| Vigentes | **{vigentes}** |")
    _fus = ", ".join("R%d→R%d" % (r["n"], r["fundida_en"]) for r in fundidas)
    out.append(f"| Fundidas (conservan su número para no romper referencias) | "
               f"**{len(fundidas)}** — {_fus} |")
    out.append(f"| **BLOQUEAN el commit** si se incumplen | **{len(bloquean)} de {vigentes}** |")
    out.append(f"| **BLOQUEAN EN PARTE** — una mitad mecanizada, la otra es un juicio | "
               f"**{len(parciales)}** — {', '.join('R%d' % r['n'] for r in parciales) or 'ninguna'} |")
    out.append(f"| Solo se **CUENTAN** (deuda medida, no bloquea) | **{len(cuentan)}** "
               f"— {', '.join('R%d' % r['n'] for r in cuentan) or 'ninguna'} |")
    out.append(f"| **NO MECANIZABLES**, declarado y no fingido | **{len(a_mano)}** "
               f"— {', '.join('R%d' % r['n'] for r in a_mano) or 'ninguna'} |")
    out.append("")
    out.append("**Decir NO MECANIZABLE es honesto y útil: marca dónde el proyecto depende de "
               "disciplina humana. Fingir que todo se comprueba solo sería peor que no "
               "comprobarlo.** La Regla 22 (doble uso) es el ejemplo claro: es del director, no es "
               "delegable, y una revisión moral que una máquina firma no es una revisión moral.\n")

    out.append("---\n\n## LA TABLA\n")
    out.append("| # | LA REGLA | POR QUÉ EXISTE | OBJETIVO (en positivo) | QUÉ EVITA | CÓMO SE COMPRUEBA | SI SE VIOLA |")
    out.append("|---|---|---|---|---|---|---|")
    for r in reglas:
        c = r["campos"]
        marca = f"**{r['n']}**" if not r["fundida_en"] else f"~~{r['n']}~~"
        out.append(f"| {marca} | {_breve(r['titulo'], 70)} | {_breve(c['POR QUÉ EXISTE'])} | "
                   f"{_breve(c['OBJETIVO'], 90)} | {_breve(c['QUÉ EVITA'], 90)} | "
                   f"{_breve(c['CÓMO SE COMPRUEBA'], 170)} | {_breve(c['SI SE VIOLA'], 60)} |")
    out.append("")
    out.append("*Las filas tachadas son las tres fusiones: el número se conserva vacío porque "
               "renumerar rompería toda referencia del código, los nodos y los informes.*\n")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verificar", action="store_true")
    a = ap.parse_args()
    nuevo = generar()
    if a.verificar:
        viejo = open(SALIDA, encoding="utf-8").read() if os.path.exists(SALIDA) else ""
        if viejo != nuevo:
            print("REGLAS-ESTRUCTURADAS.md NO esta al dia: correr `python codigo/tabla_reglas.py`")
            sys.exit(1)
        print("REGLAS-ESTRUCTURADAS.md coincide con CIMIENTOS.md")
        return
    open(SALIDA, "w", encoding="utf-8").write(nuevo)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
