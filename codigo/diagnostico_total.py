# diagnostico_total.py — LA LISTA DE TODO LO QUE ESTÁ MAL, EN UN SOLO SITIO
#
# ORDEN DEL DIRECTOR (8-ago-2026): "detecta todos los problemas de todos los sistemas y lístalos
# para arreglarlos en base a las pruebas."
#
# Los guardianes dicen SÍ o NO. Este archivo dice **QUÉ ESTÁ MAL Y EN QUÉ ORDEN ARREGLARLO**.
# Corre absolutamente todo lo que el proyecto sabe correr —las Reglas 31 de cada instrumento, los
# tres guardianes, la meta-auditoría de mutación— y devuelve UNA LISTA PRIORIZADA.
#
# Regla de la casa: aquí no se esconde nada. Un problema conocido y escrito vale mil veces más que
# un problema que solo aparece cuando un revisor externo lo encuentra.
#
# Uso: python diagnostico_total.py [--rapido]

import os
import sys
import json
import argparse
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (id, qué es, cómo se comprueba, gravedad)
#   BLOQUEA  = impide producir nodos o publicar; se arregla antes que nada
#   IMPORTA  = degrada la ciencia o la confianza, pero no invalida lo hecho
#   DEUDA    = declarado, conocido, esperando decisión o trabajo
GRAVEDADES = ["BLOQUEA", "IMPORTA", "DEUDA"]


def _correr(cmd, timeout=3600):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIEMPO AGOTADO"


def _py(*args):
    return [sys.executable] + [os.path.join(BASE, "codigo", args[0])] + list(args[1:])


def main():
    ap = argparse.ArgumentParser(description="La lista priorizada de todo lo que está mal")
    ap.add_argument("--rapido", action="store_true",
                    help="omite lo que tarda minutos (Gimnasio y meta-auditoría)")
    a = ap.parse_args()

    problemas = []
    def anotar(gravedad, sistema, que, evidencia, arreglo):
        problemas.append({"gravedad": gravedad, "sistema": sistema, "problema": que,
                          "evidencia": evidencia, "arreglo": arreglo})

    print("=== DIAGNÓSTICO TOTAL — corriendo todo lo que el proyecto sabe correr ===\n")

    # ---------- 1. los tres guardianes ----------
    for guardian, nombre in (("pruebas.py", "banco congelado"),
                             ("coherencia.py", "coherencia de la casa"),
                             ("auditoria_total.py", "dictamen de prevuelo")):
        c, salida = _correr(_py(guardian))
        print(f"  {'ok   ' if c == 0 else 'FALLO'} {nombre}")
        if c != 0:
            anotar("BLOQUEA", guardian, f"{nombre} en rojo",
                   salida.strip().splitlines()[-1][:200] if salida.strip() else "sin salida",
                   "arreglar antes de cualquier commit (Regla 32)")

    # ---------- 2. la Regla 31 de cada instrumento ----------
    instrumentos = [("contingencia.py", "detector de la frontera yo/mundo (G4)"),
                    ("verdugo_escala.py", "verdugo por reescalado"),
                    ("ganancia_honesta.py", "ganancia honesta (sonda, degradada)"),
                    # los seis del 9-ago-2026: cada uno con su prerregistro firmado
                    ("sindy3.py", "SINDy forma debil + bootstrap (prereg-28)"),
                    ("soporte.py", "escalera de soporte + examen VOE (prereg-29)"),
                    ("espejo2.py", "el gemelo y las firmas del bebe (prereg-30)"),
                    ("panel_jueces.py", "panel de jueces diversos (prereg-31)"),
                    ("observador_pasivo.py", "control del observador pasivo (prereg-32)"),
                    ("cerebro.py", "cerebro motivacional G13/G14/G2/G15 (prereg-33)")]
    if not a.rapido:
        instrumentos.append(("gimnasio.py", "el mundo con sus cuatro controles"))
    for mod, nombre in instrumentos:
        c, salida = _correr(_py(mod, "--regla31"))
        print(f"  {'ok   ' if c == 0 else 'FALLO'} Regla 31 — {nombre}")
        if c != 0:
            anotar("BLOQUEA", mod, f"{nombre} REPRUEBA su Regla 31",
                   [l for l in salida.splitlines() if "REPRUEBA" in l or "FALLO" in l][:2],
                   "el instrumento no puede producir nodos hasta corregirse")

    # ---------- 3. quién vigila a los vigilantes ----------
    if not a.rapido:
        c, salida = _correr(_py("guardianes_de_guardianes.py"))
        print(f"  {'ok   ' if c == 0 else 'FALLO'} meta-auditoría (mutación de los guardianes)")
        if c != 0:
            ciegos = [l.strip() for l in salida.splitlines() if l.strip().startswith("·")]
            anotar("BLOQUEA", "guardianes_de_guardianes.py",
                   "hay guardianes CIEGOS: dicen OK sobre un proyecto roto", ciegos,
                   "arreglar el guardián, no el proyecto")

    # ---------- 4. los resultados científicos que quedaron abiertos ----------
    print("\n  (leyendo los resultados de las corridas)")
    hito0 = os.path.join(BASE, "resultados", "p19-hito0-normal", "resumen.json")
    if os.path.exists(hito0):
        d = json.load(open(hito0, encoding="utf-8"))
        if not d.get("cuerpo"):
            anotar("IMPORTA", "ojos_gimnasio.py",
                   "HITO 0 nivel A FRACASA sobre los latentes visuales: no encuentra ningún cuerpo",
                   "0 de 8 latentes superan su nulo; el mismo detector acierta 4/4 sobre el estado "
                   "del simulador, luego el fallo está en los OJOS, no en el detector",
                   "sus ojos apenas codifican el brazo (R2 de los ángulos: -0.09, +0.03, +0.21) "
                   "mientras leen bien la escena (+0.66): la pérdida por píxel pesa igual todos "
                   "los píxeles y el brazo es fino. Candidata medida: ponderar la reconstrucción "
                   "por cuánto cambia cada píxel. Exige enmienda de prerregistro.")
        nb = d.get("nivel_b")
        if nb and not nb.get("supera_al_nulo"):
            anotar("IMPORTA", "ojos_gimnasio.py",
                   "HITO 0 nivel B (el primer no-yo) no supera su nulo",
                   f"fuerza {nb.get('fuerza')} contra techo del nulo {nb.get('nulo_techo')}",
                   "depende del nivel A: sin cuerpo identificado no hay 'no-yo' que aislar")

    # ---------- 5. las deudas declaradas ----------
    c, salida = _correr(_py("auditoria_total.py"))
    for linea in salida.splitlines():
        if linea.strip().startswith("·"):
            anotar("DEUDA", "gobernanza", linea.strip().lstrip("· "),
                   "declarada por el dictamen de prevuelo", "decisión del director o trabajo pendiente")

    # ---------- 6. la lista ----------
    problemas.sort(key=lambda p: GRAVEDADES.index(p["gravedad"]))
    print("\n" + "=" * 78)
    print(f"PROBLEMAS DETECTADOS: {len(problemas)}")
    for g in GRAVEDADES:
        de_ese = [p for p in problemas if p["gravedad"] == g]
        if not de_ese:
            continue
        print(f"\n--- {g} ({len(de_ese)}) ---")
        for i, p in enumerate(de_ese, 1):
            print(f" {i}. [{p['sistema']}] {p['problema']}")
            print(f"    evidencia: {p['evidencia']}")
            print(f"    arreglo:   {p['arreglo']}")
    print("=" * 78)

    out = os.path.join(BASE, "registros", "DIAGNOSTICO-TOTAL.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"problemas": problemas,
                   "bloquean": sum(1 for p in problemas if p["gravedad"] == "BLOQUEA")},
                  f, indent=2, ensure_ascii=False)
    print(f"guardado en {out}")
    # Solo lo que BLOQUEA hace fallar: las deudas están declaradas, no ocultas.
    return 1 if any(p["gravedad"] == "BLOQUEA" for p in problemas) else 0


if __name__ == "__main__":
    sys.exit(main())
