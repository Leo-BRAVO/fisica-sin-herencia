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
# PUNTO CIEGO CAZADO POR guardianes_de_guardianes.py (8-ago-2026, su PRIMERA corrida): bastaba
# con que UNA mencion siguiera bien para que el chequeo pasara, aunque otra quedara rancia. Un
# documento que se contradice a si mismo confunde a quien audita — igual que el titulo de un
# prerregistro firmado que sigue diciendo BORRADOR.
_rancias = sorted({int(n) for n in re.findall(r"(\d+) reglas", readme)} - {max_regla})
caso("README sin NINGUNA cifra rancia de reglas (ni una mencion vieja)",
     not _rancias, f"menciona tambien: {_rancias}")

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
    titulo, estado = t.split("\n")[0], (t.split("Estado:", 1)[1][:60] if "Estado:" in t else "")
    borrador_titulo = "BORRADOR" in titulo
    firmado = "FIRMADO" in estado
    # HUECO CAZADO 8-ago-2026: tres prerregistros seguian titulandose BORRADOR despues de ser
    # firmados. Un documento que se contradice a si mismo confunde a quien audita.
    caso(f"{nombre}: titulo y estado NO se contradicen",
         not (borrador_titulo and firmado), "dice BORRADOR en el titulo pero esta FIRMADO")
    if borrador_titulo and not firmado:
        caso(f"{nombre} (borrador) declara firma PENDIENTE", "PENDIENTE" in t)

print("== cola de estudios: TODO item pendiente debe poder ejecutarse (INFORME-26) ==")
# HUECO CAZADO 8-ago-2026: un item con tipo que el latido no toma y una ruta imposible
# ("A + B + C") estuvo horas atascado sin que nada avisara — parecia pendiente y nadie
# podia ejecutarlo jamas. Un item inejecutable es peor que un item ausente.
cola = json.load(open(os.path.join(BASE, "registros", "COLA-ESTUDIOS.json"), encoding="utf-8"))
TIPOS_QUE_EL_LATIDO_TOMA = {"re-analisis", "gimnasio"}
for i in cola["items"]:
    caso(f"cola item '{i['id']}' tiene estado valido",
         i.get("estado") in ("pendiente", "hecha", "espera-al-director"))
    if i.get("estado") != "pendiente":
        continue
    caso(f"cola PENDIENTE '{i['id']}': su tipo lo toma el latido",
         i.get("tipo") in TIPOS_QUE_EL_LATIDO_TOMA, f"tipo={i.get('tipo')}")
    caso(f"cola PENDIENTE '{i['id']}': tiene datos/salida/args",
         all(k in i for k in ("datos", "salida", "args")))
    caso(f"cola PENDIENTE '{i['id']}': la ruta de datos es UNA sola, real",
         isinstance(i.get("datos"), str) and "+" not in i.get("datos", "+"),
         f"datos={i.get('datos')}")

print("== version de la MENTE: coincide donde se proclama ==")
mente = leer("MENTE.md")
v = re.search(r"Versión (\d+)", mente)
caso("MENTE declara version", v is not None)
if v:
    caso(f"README cita la misma version (v{v.group(1)})", f"(v{v.group(1)})" in readme)

print("== workflows: el cuerpo de la nube DEBE ser YAML valido y completo ==")
# HUECO CAZADO EL 8-AGO-2026: latido-nube.yml se fusiono con YAML ROTO (un ':' seguido de
# espacio dentro del NOMBRE de un paso hace que YAML lo lea como mapa anidado). GitHub lo
# habria rechazado en silencio: el corazon del proyecto nunca habria latido. Desde hoy,
# ningun workflow entra sin parsear.
_wf = sorted(glob.glob(os.path.join(BASE, ".github", "workflows", "*.yml")))
caso("hay workflows que vigilar", len(_wf) > 0)
try:
    import yaml as _yaml
    _hay_yaml = True
except ImportError:
    _hay_yaml = False
    print("  (aviso: pyyaml no instalado — se usa el chequeo de respaldo, sin parseo completo)")
for _f in _wf:
    _n = os.path.basename(_f)
    _txt = open(_f, encoding="utf-8").read()
    if _hay_yaml:
        try:
            _d = _yaml.safe_load(_txt)
            _job = list(_d["jobs"])[0]
            _pasos = _d["jobs"][_job]["steps"]
            caso(f"{_n}: YAML valido con pasos", isinstance(_pasos, list) and len(_pasos) > 0)
            _nombres = " ".join(str(p.get("name", "")) for p in _pasos)
            caso(f"{_n}: corre los DOS guardianes antes de commitear (Regla 32)",
                 "pruebas.py" in _txt and "coherencia.py" in _txt)
        except Exception as _e:
            caso(f"{_n}: YAML valido", False, str(_e).splitlines()[0])
    else:
        # respaldo sin dependencias: la trampa exacta que nos mordio
        _malos = [l.strip() for l in _txt.splitlines()
                  if l.strip().startswith("- name:") and ": " in l.split("- name:", 1)[1]
                  and not l.split("- name:", 1)[1].strip().startswith(('"', "'"))]
        caso(f"{_n}: ningun nombre de paso con ':' sin comillas (rompe el YAML)",
             not _malos, str(_malos[:1]))
        caso(f"{_n}: corre los DOS guardianes antes de commitear (Regla 32)",
             "pruebas.py" in _txt and "coherencia.py" in _txt)

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
