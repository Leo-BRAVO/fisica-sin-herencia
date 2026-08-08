# coherencia.py — LA AUTOAUDITORIA PERMANENTE (orden del director, 8-ago-2026).
# Verifica que el repositorio este INTERCONECTADO y diga la verdad sobre si mismo:
# que los numeros que los documentos proclaman coincidan con lo que hay en disco.
# Se corre JUNTO con pruebas.py antes de cada commit (ver GUIA-ORQUESTADOR).
# pruebas.py vigila la ciencia congelada; coherencia.py vigila la casa.
# Uso: python coherencia.py   (salida: OK total o el detalle; codigo de salida 0/1)

import os
import re
import json
import glob
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FALLOS = []


def caso(nombre, cond, detalle=""):
    if cond:
        print(f"  ok  {nombre}")
    else:
        print(f"FALLO {nombre} {detalle}")
        FALLOS.append(nombre)


def leer(rel):
    with open(os.path.join(BASE, rel), encoding="utf-8") as f:
        return f.read()


print("== reglas: el numero que proclamamos es el que existe ==")
cimientos = leer("CIMIENTOS.md")
reglas = [int(n) for n in re.findall(r"### Regla (\d+)", cimientos)]
max_regla = max(reglas)
caso("las reglas son consecutivas 1..N sin huecos",
     sorted(set(reglas)) == list(range(1, max_regla + 1)), f"faltan: {set(range(1,max_regla+1))-set(reglas)}")
readme = leer("README.md")
caso(f"README proclama '{max_regla} reglas' (las que CIMIENTOS contiene)",
     f"{max_regla} reglas" in readme)

print("== arbol: nodos, cuarentena y conectoma cuentan lo mismo ==")
nodos_e2 = sorted(glob.glob(os.path.join(BASE, "arbol", "N-*-E2.md")))
cuarentena = [n for n in nodos_e2 if "EN CUARENTENA" in open(n, encoding="utf-8").read(600)]
con = json.load(open(os.path.join(BASE, "arbol", "CONECTOMA.json")))
for n in cuarentena:
    nombre = os.path.basename(n).replace(".md", "")
    caso(f"nodo en cuarentena {nombre} NO esta en el conectoma",
         not any(nombre.split("-E2")[0] in k and "E2" in k for k in con["nodos"]
                 if nombre.replace("N-", "N-") in k))
boleta = json.load(open(os.path.join(BASE, "registros", "BOLETA.json")))
caso("boleta: vivos + cuarentena = archivos de nodos E2",
     boleta.get("nodos_vivos_E2", -1) + boleta.get("nodos_en_cuarentena", 0) == len(nodos_e2),
     f"boleta={boleta.get('nodos_vivos_E2')}+{boleta.get('nodos_en_cuarentena')} archivos={len(nodos_e2)}")
caso("boleta sin numeros de juicio escritos a mano",
     "leyes_humanas_redescubiertas" not in boleta and "automejoras_validadas" not in boleta)

print("== prerregistros: los borradores se declaran, los firmados no fingen ==")
for p in sorted(glob.glob(os.path.join(BASE, "registros", "prerregistro-*.md"))):
    t = open(p, encoding="utf-8").read()
    nombre = os.path.basename(p)
    if "BORRADOR" in t[:200]:
        caso(f"{nombre} (borrador) declara firma PENDIENTE", "PENDIENTE" in t)

print("== cola de estudios: cada item ejecutable esta completo ==")
cola = json.load(open(os.path.join(BASE, "registros", "COLA-ESTUDIOS.json"), encoding="utf-8"))
for i in cola["items"]:
    if i.get("tipo") == "re-analisis":
        caso(f"cola item '{i['id']}' tiene datos/salida/args",
             all(k in i for k in ("datos", "salida", "args")))
    caso(f"cola item '{i['id']}' tiene estado valido",
         i.get("estado") in ("pendiente", "hecha", "espera-al-director"))

print("== version de la MENTE: coincide donde se proclama ==")
mente = leer("MENTE.md")
v = re.search(r"Versión (\d+)", mente)
caso("MENTE declara version", v is not None)
if v:
    caso(f"README cita la misma version (v{v.group(1)})", f"(v{v.group(1)})" in readme)

print("== documentos fundacionales: sus referencias cruzadas existen ==")
genoma_path = os.path.join(BASE, "arbol", "GENOMA-DIEGO.md")
if os.path.exists(genoma_path):
    genoma = open(genoma_path, encoding="utf-8").read()
    for ref in re.findall(r"prereg(?:istro)?-(\d+)", genoma):
        caso(f"GENOMA cita prerregistro-{ref} y existe",
             os.path.exists(os.path.join(BASE, "registros", f"prerregistro-{ref}.md")))
for doc in ("registros/AUDITORIA-EXTERNA-01.md",):
    t = leer(doc)
    for cod in set(re.findall(r"`codigo/([a-z0-9_]+\.py)`", t)):
        caso(f"{os.path.basename(doc)} cita codigo/{cod} y existe",
             os.path.exists(os.path.join(BASE, "codigo", cod)))

print()
if FALLOS:
    print(f"COHERENCIA: {len(FALLOS)} FALLOS -> NO COMMITEAR: {FALLOS}")
    sys.exit(1)
print("COHERENCIA: TODO OK — la casa dice la verdad sobre si misma")
