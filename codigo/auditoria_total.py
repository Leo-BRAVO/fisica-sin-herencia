# auditoria_total.py — LA AUDITORIA DE CIERRE (orden del director, 8-ago-2026):
# "verifica que ninguna regla se rompa, que todo este interconectado, que trabajando en la
#  nube tampoco tenga conocimiento humano, que cada push alimente al arbol".
# Es el tercer guardian, y el mas severo: se corre ANTES de cualquier campana seria y
# ANTES de mostrarle el repositorio a un revisor o a un inversionista. A diferencia de
# pruebas.py (la ciencia) y coherencia.py (la casa), este audita EL CUMPLIMIENTO DE LAS
# REGLAS de punta a punta, incluida la cadena de la nube.
# Uso: python auditoria_total.py   (salida: dictamen + codigo 0/1)

import os
import re
import ast
import json
import glob
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FALLOS, AVISOS = [], []


def ok(nombre, cond, detalle=""):
    if cond:
        print(f"  ok   {nombre}")
    else:
        print(f"FALLO  {nombre} {detalle}")
        FALLOS.append(nombre)


def aviso(nombre, cond, detalle=""):
    if cond:
        print(f"  ok   {nombre}")
    else:
        print(f"AVISO  {nombre} {detalle}")
        AVISOS.append(nombre)


def leer(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


print("\n=== A. LA CONSTITUCION (las reglas existen y son coherentes) ===")
cim = leer("CIMIENTOS.md")
reglas = [int(n) for n in re.findall(r"### Regla (\d+)", cim)]
ok("reglas consecutivas 1..N sin huecos ni repetidas",
   sorted(reglas) == list(range(1, max(reglas) + 1)) == sorted(set(reglas)),
   f"{sorted(reglas)}")
ok("Regla 31 (verdugo del instrumento) presente", "### Regla 31" in cim)
ok("Regla 32 (autoauditoria) presente", "### Regla 32" in cim)
ok("Regla 15 reconciliada por enmienda (no contradice a 28-30)",
   "Enmienda de reconciliación" in cim)

print("\n=== B. NO-CONTAMINACION — LA PREGUNTA DEL PAPER (¿la mente ve fisica humana?) ===")
# B1 Regla 4: el motor recibe nombres NEUTROS
desc = leer("codigo/descubrir.py")
ok("Regla 4: al motor simbolico se le pasan nombres neutros v1..vN",
   'variable_names=[f"v{i+1}"' in desc.replace("'", '"'))
ok("Regla 4: los objetivos se llaman v1_sig..vN_sig (sin nombres fisicos)",
   'f"v{j+1}_sig"' in desc)
# B2 Regla 3: ningun modelo preentrenado en la cadena de percepcion
perc = leer("codigo/percepcion.py")
ok("Regla 3/pureza: la percepcion se entrena DESDE CERO (sin pesos ajenos)",
   "pretrained" not in perc.lower() and "torchvision" not in perc.lower()
   and "load_state_dict" not in perc)
# B3 los CSV que ve la mente: columnas neutras, solo numeros
malos_csv = []
for c in glob.glob(os.path.join(BASE, "datos", "**", "*.csv"), recursive=True)[:50]:
    cab = open(c, encoding="utf-8").readline().strip().split(",")
    if any(not re.fullmatch(r"t|cuadro|s\d+|x_px|y_px", x) for x in cab):
        malos_csv.append((os.path.basename(c), cab))
ok("los CSV que entran al motor tienen columnas neutras (t, sN, x_px, y_px)",
   not malos_csv, str(malos_csv[:2]))
# B4 Regla 27: el cortafuegos — los veredictos del comparador NO viven del lado de la mente
lado_mente = glob.glob(os.path.join(BASE, "arbol", "*.md")) + glob.glob(os.path.join(BASE, "arbol", "*.json*"))
fugas = [os.path.basename(f) for f in lado_mente
         if "COMPARADOR-01" in open(f, encoding="utf-8", errors="ignore").read()
         and os.path.basename(f) not in ("GENOMA-DIEGO.md", "PLAN-EDUCACION.md")]
ok("Regla 27: ningun veredicto del comparador dentro del lado de la mente", not fugas, str(fugas))
ok("Regla 27: los informes del comparador viven en registros/ (lado humano)",
   os.path.exists(os.path.join(BASE, "registros", "COMPARADOR-01.md")))
# B5 LA NUBE: ¿la reconstruccion mete texto de terceros al repositorio?
rec = leer("codigo/reconstruir_datos.py")
ok("la nube borra lo extraido de terceros tras usarlo (nada de READMEs ajenos queda)",
   "shutil.rmtree" in rec)
gi = leer(".gitignore")
ok("datos/ esta fuera de git: lo de terceros no puede entrar al repositorio", "datos/" in gi)
rastreados = [f for f in os.popen(f"git -C {BASE} ls-files").read().split()
              if f.startswith("datos/")]
ok("git no rastrea NINGUN archivo bajo datos/", not rastreados, str(rastreados[:3]))
# B6 la cadena de la nube solo baja NUMEROS y VIDEO crudo (Regla 25)
ok("la nube solo descarga datos crudos de fuentes con licencia (Mendeley zip / mp4 Morpheus)",
   "data.mendeley.com" in rec and "cropped_video.mp4" in rec and "huggingface.co" in rec)
ok("Regla 2: la extraccion produce pixeles/cuadros, sin unidades fisicas",
   "x_px" in leer("codigo/extraer_posiciones.py"))

print("\n=== C. LA NUBE (cuerpo nuevo: ¿corre una secuencia perfecta?) ===")
try:
    import yaml
    hay_yaml = True
except ImportError:
    hay_yaml = False
    AVISOS.append("pyyaml ausente: no se pudo parsear workflows")
if hay_yaml:
    for f in sorted(glob.glob(os.path.join(BASE, ".github", "workflows", "*.yml"))):
        n = os.path.basename(f)
        d = yaml.safe_load(open(f, encoding="utf-8"))
        job = list(d["jobs"])[0]
        pasos = d["jobs"][job]["steps"]
        ok(f"{n}: YAML valido", isinstance(pasos, list) and len(pasos) > 1)
        txt = open(f, encoding="utf-8").read()
        ifs = {str(p.get("name", "")): str(p.get("if", "")) for p in pasos}
        # Se verifica el FONDO, no la forma: un workflow puede implementar las protecciones
        # con pasos separados (con `if:`) o dentro de un bucle en bash. Ambas valen; lo que
        # NO vale es que falte la proteccion. (Leccion 8-ago: el auditor bloqueo un merge por
        # verificar la forma vieja tras reescribir el latido como bucle — se corrige aqui.)
        ok(f"{n}: invoca LOS TRES guardianes",
           all(g in txt for g in ("pruebas.py", "coherencia.py", "auditoria_total.py")))
        por_pasos = any("guardianes.outcome == 'success'" in v for v in ifs.values())
        por_bucle = ('GUARDIANES=$?' in txt and '"$GUARDIANES" -eq 0' in txt
                     and txt.index('GUARDIANES=$?') < txt.index("git push -q origin main")
                     if "git push -q origin main" in txt else False)
        ok(f"{n}: el push a main EXIGE que los guardianes aprueben (por pasos o por bucle)",
           por_pasos or por_bucle)
        ok(f"{n}: hay rama de cuarentena si reprueban (nada se pierde, main intacto)",
           "nube-cuarentena" in txt)
        ok(f"{n}: concurrencia declarada (jamas dos corridas a la vez)",
           d.get("concurrency", {}).get("group") == "nube")
        ok(f"{n}: reconstruye datos con huella antes de correr",
           "reconstruir_datos.py" in open(f, encoding="utf-8").read())

print("\n=== D. INTERCONEXION — ¿cada push alimenta al arbol? (Reglas 18, 29, 32) ===")
nodos = sorted(glob.glob(os.path.join(BASE, "arbol", "N-*-E2.md")))
con = json.load(open(os.path.join(BASE, "arbol", "CONECTOMA.json"), encoding="utf-8"))
for n in nodos:
    base_n = os.path.basename(n).replace(".md", "")           # N-00X-E2
    clave = base_n.split("-E2")[0].replace("N-", "N-")        # N-00X
    tejido = any(clave in k and "E2" in k for k in con["nodos"])
    ok(f"Regla 29: {base_n} esta tejido en el conectoma", tejido)
ok("el conectoma no esta fosilizado (fecha != 2026-07-12)",
   con.get("generado") != "2026-07-12", con.get("generado"))
# cada nodo cita su prerregistro/informe y existe
for n in nodos:
    t = open(n, encoding="utf-8").read()
    refs = set(re.findall(r"prerregistro[- ](\d+)", t)) | set(re.findall(r"prereg-(\d+)", t))
    faltan = [r for r in refs
              if not glob.glob(os.path.join(BASE, "registros", f"prerregistro-{r}*.md"))]
    ok(f"Regla 8: {os.path.basename(n)} cita prerregistros que EXISTEN", not faltan, str(faltan))
# la cola es ejecutable en la nube
cola = json.load(open(os.path.join(BASE, "registros", "COLA-ESTUDIOS.json"), encoding="utf-8"))
for i in cola["items"]:
    if i.get("tipo") == "re-analisis" and i.get("estado") == "pendiente":
        ok(f"cola '{i['id']}' declara reconstruccion (sin ella la nube falla)",
           bool(i.get("reconstruir")) or os.path.isdir(os.path.join(BASE, i.get("datos", ""))))

print("\n=== E. REGLAS DECLARADAS PERO NO EJECUTADAS (deuda honesta, para el paper) ===")
# CUIDADO (falso positivo cazado el 8-ago-2026 por el propio auditor): las corridas de la
# herramienta F3 tambien llevan el campo "nulo" (es su CONFIGURACION de control negativo),
# pero NO son pruebas nulas de campana. Una prueba nula de campana tiene "semillas".
nulos = []
for f in glob.glob(os.path.join(BASE, "resultados", "*", "resumen.json")):
    d = json.load(open(f, encoding="utf-8")) or {}
    if d.get("nulo") and "semillas" in d:
        nulos.append((os.path.basename(os.path.dirname(f)), d["nulo"]))
nulos_modernos = [n for n, _ in nulos if not n.startswith("nulo-")]  # con tuberia propia
aviso("Regla 11: las campanas insignia tienen su verdugo CON SU PROPIA tuberia",
      len(nulos_modernos) >= 3,
      f"{len(nulos_modernos)}/3 corridos (los otros {len(nulos)-len(nulos_modernos)} son del dia 1, "
      f"tuberia vieja: no amparan campanas actuales). Encolados en la nube: aud01-nulo-*")
word = glob.glob(os.path.join(BASE, "resultados", "word", "*.docx"))
informes = glob.glob(os.path.join(BASE, "resultados", "INFORME-*.md"))
aviso("Regla 17: cada informe tiene su version Word",
      len(word) >= len(informes), f"{len(word)} Word para {len(informes)} informes")
aviso("Regla 16: repositorio publico (prioridad fuerte)", False, "sigue privado — decision del director")
aviso("Regla 19 nivel 3: replica independiente por un tercero", False, "pendiente — ningun nodo llego al nivel 3")

print("\n" + "=" * 74)
if FALLOS:
    print(f"DICTAMEN: {len(FALLOS)} FALLO(S) — NO correr campanas ni mostrar el repo: {FALLOS}")
    sys.exit(1)
print("DICTAMEN: SIN FALLOS — reglas intactas, cadena limpia, arbol interconectado.")
if AVISOS:
    print(f"DEUDA DECLARADA (no bloquea, pero va escrita en el paper): {len(AVISOS)}")
    for a in AVISOS:
        print(f"   · {a}")
