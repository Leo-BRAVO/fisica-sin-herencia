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
         i.get("estado") in ("pendiente", "hecha", "espera-al-director", "espera-al-metodo"))
    if i.get("estado") != "pendiente":
        continue
    caso(f"cola PENDIENTE '{i['id']}': su tipo lo toma el latido",
         i.get("tipo") in TIPOS_QUE_EL_LATIDO_TOMA, f"tipo={i.get('tipo')}")
    caso(f"cola PENDIENTE '{i['id']}': tiene datos/salida/args",
         all(k in i for k in ("datos", "salida", "args")))
    caso(f"cola PENDIENTE '{i['id']}': la ruta de datos es UNA sola, real",
         isinstance(i.get("datos"), str) and "+" not in i.get("datos", "+"),
         f"datos={i.get('datos')}")

print("== LA PUERTA (metodo.py): ningun estudio pendiente sin sello VALIDO ==")
# Idea del director (10-ago-2026): "unicamente despues de que pasen todas las validaciones puedes
# correr una prueba". Un metodo escrito no es una puerta; esto si. El sello guarda la HUELLA del
# archivo, asi que pasar la puerta y luego editar el modulo INVALIDA el sello.
# Se aplica solo a lo PENDIENTE: los estudios ya hechos se juzgan por sus actas, no retroactivamente.
import metodo as _pu
for _i in cola["items"]:
    if _i.get("estado") != "pendiente":
        continue
    _d = _i.get("datos", "")
    if not _d.startswith("codigo/") or not _d.endswith(".py"):
        continue
    _m = os.path.basename(_d)[:-3]
    _ok, _por = _pu.sello_valido(_m)
    caso(f"cola PENDIENTE '{_i['id']}': su modulo {_m} paso LA PUERTA", _ok, _por)

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

print("== LA FRONTERA DE LA MEMORIA (Regla 34): arbol/ solo tiene hojas, y nadie lo lee entero ==")
# El protocolo de la memoria (registros/PROTOCOLO-MEMORIA.md, 9-ago-2026) separo HOJAS (lo que
# Diego lee/escribe mecanicamente) de CARTELES (documentos humanos). Los carteles se mudaron a
# registros/. Estos tres casos impiden que la frontera se borre por descuido:
CARTELES = ("ANOMALIAS.md", "ECUACIONES-COMPARADAS.md", "INVESTIGACION-LABS.md",
            "CURRICULO-DATOS.md", "PLAN-EDUCACION.md", "PLATAFORMA-Y-FRONTERA.md",
            "DISENO-CONSTRUCCION.md", "FRONTERA-INOBSERVABLE.md",
            # SEGUNDA MUDANZA, 10-ago-2026, por orden del director ("evita que todo cartel este
            # dentro de las hojas"). La primera mudanza los busco por nombre conocido y se dejo
            # DOS dentro de arbol/, los dos peores: GIMNASIO.md es una revision de literatura
            # cientifica humana (y el propio documento advertia en su §1 que nada de eso podia
            # entrar al lado de Diego, mientras vivia en la carpeta que la Regla 29 declara
            # visible para el); GENOMA-DIEGO.md cita cognicion infantil, cognicion comparada y
            # la escalera causal por su nombre. Ninguno era leido por modulo alguno —no hubo
            # fuga— pero una frontera que depende de que nadie deje caer un archivo ahi no es
            # una frontera. Por eso ademas del nombre se anade el candado por CONTENIDO de mas
            # abajo: la lista por nombre solo caza lo que ya sabemos que existe.
            "GIMNASIO.md", "GENOMA-DIEGO.md")
_intrusos = [c for c in CARTELES if os.path.exists(os.path.join(BASE, "arbol", c))]
caso("ningun cartel humano vive dentro de arbol/ (la mudanza se sostiene)",
     not _intrusos, str(_intrusos))

# Ningun modulo de Diego puede ABRIR un cartel como datos. Se permite nombrarlo en un comentario
# (leccion de diseno); se prohibe pasarlo a open()/read_text()/json.load()/glob.
_lectores = []
for _py in sorted(glob.glob(os.path.join(BASE, "codigo", "*.py"))):
    if os.path.basename(_py) in ("coherencia.py", "auditoria_total.py",
                                 "guardianes_de_guardianes.py"):
        continue  # los guardianes NOMBRAN los carteles justamente para vigilarlos
    _src = open(_py, encoding="utf-8", errors="ignore").read()
    _codigo = "\n".join(l.split("#", 1)[0] for l in _src.split("\n"))
    for _c in CARTELES:
        if _c in _codigo:
            _lectores.append(f"{os.path.basename(_py)}->{_c}")
caso("ningun modulo de codigo/ abre un cartel humano como datos (Regla 27 mecanizada)",
     not _lectores, str(_lectores))

# Y nadie puede leer arbol/ como CARPETA COMPLETA: toda lectura declara sus hojas por nombre.
# Un glob de *.md o *.json* sobre arbol/ arrastraria cualquier cartel que alguien deje caer ahi.
_globales = []
for _py in sorted(glob.glob(os.path.join(BASE, "codigo", "*.py"))):
    if os.path.basename(_py) in ("coherencia.py", "auditoria_total.py"):
        continue  # los guardianes SI deben barrer la carpeta: para eso vigilan
    _src = open(_py, encoding="utf-8", errors="ignore").read()
    _codigo = "\n".join(l.split("#", 1)[0] for l in _src.split("\n"))
    for _m in re.findall(r'"arbol",\s*"([^"]+)"', _codigo):
        if _m.startswith("*") or _m in ("*.md", "*.json"):
            _globales.append(f"{os.path.basename(_py)}:{_m}")
caso("ningun modulo lee arbol/ como carpeta completa (toda lectura nombra su hoja)",
     not _globales, str(_globales))

# EL CANDADO POR CONTENIDO (10-ago-2026). La lista de nombres de arriba solo caza los carteles que
# YA sabemos que existen; el que alguien escriba mañana entraria sin ruido. Este caso mira lo que
# de verdad importa: que ninguna hoja —lo que la Regla 29 hace visible a Diego— CITE ciencia humana.
# Cazo dos fugas mias con esto el mismo dia que lo escribi: dos nodos recien redactados mencionaban
# hallazgos publicados de terceros. El cortafuegos de la Regla 27 no falla por mala fe, falla por
# redaccion comoda — y la comodidad hay que mecanizarla en contra.
_HUELLAS_HUMANAS = ("arxiv", "neurips", "iclr", "icml", " et al", "la literatura",
                    "publicad", "spelke", "baillargeon", "tomasello", "oudeyer", "pearl",
                    "rovee-collier")
_citas = []
for _hoja in sorted(glob.glob(os.path.join(BASE, "arbol", "*.md"))
                    + glob.glob(os.path.join(BASE, "arbol", "epoca1", "*.md"))):
    _t = open(_hoja, encoding="utf-8", errors="ignore").read().lower()
    for _h in _HUELLAS_HUMANAS:
        if _h in _t:
            _citas.append(f"{os.path.basename(_hoja)}:{_h.strip()}")
caso("ninguna hoja de arbol/ cita ciencia humana (Regla 27 mecanizada por CONTENIDO, no por nombre)",
     not _citas, str(_citas))

# EL CANDADO DE LA FIRMA (10-ago-2026, al abrir el LAZO). La Regla 15 dice que Diego y el
# orquestador solo PROPONEN: el director decide y firma. Mientras el trabajo iba prompt a prompt,
# esa regla la sostenia el propio ritmo de la conversacion. En un lazo que corre solo durante dias
# eso deja de ser cierto, asi que la firma pasa de costumbre a comprobacion: TODO nodo del arbol
# debe llevar escrita su aprobacion. Un nodo sin firma es un nodo que el lazo escribio por su
# cuenta, y el guardian lo grita antes de que llegue a main.
_sin_firma = []
for _n in sorted(glob.glob(os.path.join(BASE, "arbol", "N-*.md"))
                 + glob.glob(os.path.join(BASE, "arbol", "H-*.md"))
                 + glob.glob(os.path.join(BASE, "arbol", "epoca1", "*.md"))):
    if not re.search(r"aprobad|aprobaci|firmad", open(_n, encoding="utf-8",
                                                      errors="ignore").read(), re.I):
        _sin_firma.append(os.path.basename(_n))
caso("todo nodo del arbol lleva la firma del director (Regla 15 mecanizada para el LAZO)",
     not _sin_firma, str(_sin_firma))

# QUORUM ADVERSARIAL (enmienda del 10-ago-2026: el director pasa a observador). Un nodo puede
# nacer sin su firma SOLO si declara las siete comprobaciones que lo sostienen. Esto no es
# burocracia: es lo unico que queda en el sitio donde antes estaba un humano diciendo que si. Un
# nodo con FIRMA DELEGADA que no enumere su quorum es exactamente el "hecho consumado sin que
# nadie lo firmara" que la Regla 15 existe para impedir.
_QUORUM = ("prerregistro", "guardian", "regla 31", "semillas", "nulo", "señuelo", "adversarial")
_mal_delegados = []
for _n in sorted(glob.glob(os.path.join(BASE, "arbol", "N-*.md"))
                 + glob.glob(os.path.join(BASE, "arbol", "H-*.md"))):
    _t = open(_n, encoding="utf-8", errors="ignore").read().lower()
    if "firma delegada" in _t:
        _faltan = [q for q in _QUORUM if q not in _t]
        if _faltan:
            _mal_delegados.append(f"{os.path.basename(_n)}: falta {_faltan}")
caso("todo nodo de FIRMA DELEGADA enumera su quorum adversarial completo (Regla 15 enmendada)",
     not _mal_delegados, str(_mal_delegados))

print("== EL METODO (10-ago-2026): sus 8 pasos existen y sus herramientas tambien ==")
# El metodo no sustituye ninguna regla ni las repite: cubre la capa de "¿el instrumento mide lo
# que dice?", que no existia. Aqui se comprueba que no sea solo un documento bonito.
_met = os.path.join(BASE, "registros", "METODO.md")
caso("el METODO existe y vive del lado humano (registros/, no arbol/)", os.path.exists(_met))
if os.path.exists(_met):
    _t = open(_met, encoding="utf-8").read()
    import sanidad as _sn
    for _fn in ("correlaciones", "clasificacion", "tramoya_detectada", "condiciones_distintas",
                "cociente_seguro", "restos_de_versiones", "homoglifos", "texto_para_shell",
                "relaciones_metamorficas", "politica_limpia"):
        caso(f"el METODO cita {_fn}() y la funcion EXISTE en sanidad.py",
             _fn in _t and hasattr(_sn, _fn))
    caso("el METODO declara su hueco abierto (paso 0 sin mecanizar)",
         "hueco" in _t.lower() and "paso 0" in _t.lower())

print("== documentos fundacionales: sus referencias cruzadas existen ==")
genoma_path = os.path.join(BASE, "registros", "GENOMA-DIEGO.md")   # cartel: vive fuera de arbol/
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
