# guardianes_de_guardianes.py — ¿QUIÉN VIGILA A LOS VIGILANTES?
#
# PREGUNTA DEL DIRECTOR (8-ago-2026): "la mente está hecha para automejorarse, correcto. ¿Pero qué
# automejora lo que está ATRÁS de la mente? El sistema que controla las reglas y todo, ¿existe igual?"
#
# La respuesta honesta hasta hoy era: NO del todo. Diego se automejora dentro de su corral
# (Reglas 28–30). Los tres guardianes lo vigilan a él. Pero **nadie vigilaba a los guardianes**.
# Un guardián que siempre dice "ok" es indistinguible de un guardián que funciona — hasta el día
# en que hace falta, y ese día ya es tarde. De hecho ya nos pasó dos veces esta semana:
#   · el workflow del latido se fusionó con YAML roto y ningún guardián chistó;
#   · la cadena de verificación enmascaraba los códigos de salida y NADA bloqueó nada en toda una
#     sesión — los guardianes "pasaban" porque nunca se leyó su veredicto.
#
# ESTE ARCHIVO ES ESA CAPA QUE FALTABA. No revisa código: **rompe el proyecto a propósito** y
# comprueba que el guardián correspondiente GRITE. Es la Regla 31 aplicada a la propia gobernanza:
#
#     UNA HERRAMIENTA QUE NO FALLA DONDE NO HAY NADA, NO SIRVE.
#     UN GUARDIÁN QUE NO SE PONE ROJO ANTE UN DAÑO REAL, TAMPOCO.
#
# Cada mutación es un daño que YA cometimos o que podríamos cometer. Si el guardián no lo caza,
# el guardián es decorativo y hay que arreglarlo — no el proyecto.
#
# Uso: python guardianes_de_guardianes.py

import os
import re
import sys
import json
import shutil
import subprocess
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FALLOS = []


def _copia():
    """Copia trabajable del proyecto (sin .git ni datos): mutar la copia, jamás el original."""
    d = tempfile.mkdtemp(prefix="mutante_")
    destino = os.path.join(d, "proyecto")
    shutil.copytree(BASE, destino,
                    ignore=shutil.ignore_patterns(".git", "datos", "__pycache__", "*.pt"))
    return d, destino


def _correr(raiz, guardian):
    r = subprocess.run([sys.executable, os.path.join(raiz, "codigo", guardian)],
                       capture_output=True, text=True, cwd=raiz, timeout=1800)
    return r.returncode


def mutacion(nombre, guardian, danar):
    """Aplica un daño conocido y exige que el guardián se ponga ROJO."""
    tmp, raiz = _copia()
    try:
        if not danar(raiz):
            # 10-ago-2026: SALTADA ERA UN APROBADO DISFRAZADO. Si el daño no se puede aplicar,
            # la meta-auditoria perdio esa cobertura y NADIE se enteraba: el veredicto final
            # seguia diciendo "los 9 daños fueron cazados" contando 8. Un daño que caduca es
            # exactamente el punto ciego que este archivo existe para cazar, aplicado a si mismo.
            print(f"  FALLO {nombre}  ->  el DAÑO ya no se puede aplicar: la prueba caduco")
            FALLOS.append(f"{nombre} (daño caducado, no se pudo aplicar)")
            return
        codigo = _correr(raiz, guardian)
        if codigo != 0:
            print(f"  ok    {nombre}  ->  {guardian} lo cazó")
        else:
            print(f"  FALLO {nombre}  ->  {guardian} dijo OK sobre un proyecto ROTO")
            FALLOS.append(f"{nombre} ({guardian})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------- los daños, uno por uno ----------------------------

def _editar(raiz, rel, viejo, nuevo):
    p = os.path.join(raiz, rel)
    t = open(p, encoding="utf-8").read()
    if viejo not in t:
        return False
    open(p, "w", encoding="utf-8").write(t.replace(viejo, nuevo, 1))
    return True


def borra_una_regla(raiz):
    """Daño: desaparece una regla del medio. Las reglas dejarían de ser consecutivas."""
    p = os.path.join(raiz, "CIMIENTOS.md")
    t = open(p, encoding="utf-8").read()
    m = re.search(r"### Regla 21 —.*?(?=### Regla 22 —)", t, re.S)
    if not m:
        return False
    open(p, "w", encoding="utf-8").write(t.replace(m.group(0), "", 1))
    return True


def boleta_miente(raiz):
    """Daño: la boleta proclama más nodos vivos de los que hay en disco."""
    p = os.path.join(raiz, "registros", "BOLETA.json")
    d = json.load(open(p, encoding="utf-8"))
    d["nodos_vivos_E2"] = d.get("nodos_vivos_E2", 0) + 7
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return True


def workflow_roto(raiz):
    """Daño REAL que ya cometimos: un ':' sin comillas dentro del nombre de un paso rompe el YAML
    y GitHub rechaza el workflow en silencio — el corazón del proyecto no latiría."""
    import glob
    for f in glob.glob(os.path.join(raiz, ".github", "workflows", "*.yml")):
        t = open(f, encoding="utf-8").read()
        m = re.search(r"( +- name: )([^\n\"']+)\n", t)
        if m:
            open(f, "w", encoding="utf-8").write(
                t.replace(m.group(0), f"{m.group(1)}{m.group(2)}: roto\n", 1))
            return True
    return False


def cola_inejecutable(raiz):
    """Daño REAL que ya cometimos: un item pendiente que el latido no puede ejecutar jamás —
    parece pendiente y nadie lo corre nunca."""
    p = os.path.join(raiz, "registros", "COLA-ESTUDIOS.json")
    d = json.load(open(p, encoding="utf-8"))
    d["items"].append({"id": "mutante-inejecutable", "estado": "pendiente",
                       "tipo": "tipo-que-nadie-toma", "datos": "A + B + C",
                       "salida": "x", "args": ""})
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return True


def readme_desfasado(raiz):
    """Daño: el README proclama un número de reglas distinto del que CIMIENTOS contiene.

    10-ago-2026 — POR QUE ESTE DAÑO SE LEE SOLO Y YA NO SE ESCRIBE A MANO: durante semanas el daño
    buscaba la cadena literal "32 reglas". Cuando las reglas pasaron de 32 a 34 el texto dejo de
    existir, el daño dejo de aplicarse, y la meta-auditoria lo reporto como SALTADA — es decir,
    perdio una cobertura sin ponerse roja. Un daño escrito a mano CADUCA. Ahora se lee el numero
    que el README proclame hoy, sea cual sea, y se le resta uno."""
    ruta = os.path.join(raiz, "README.md")
    if not os.path.exists(ruta):
        return False
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    m = re.search(r"(\d+)\s+reglas", texto)
    if not m:
        return False
    viejo = m.group(0)
    nuevo = f"{int(m.group(1)) - 1} reglas"
    return _editar(raiz, "README.md", viejo, nuevo)


def suavizar_el_objetivo(raiz):
    """Daño CIENTÍFICO: suavizar también el objetivo Y hace descubrible al propio filtro. Es el
    error más sutil que cometimos (INFORME-11) y está congelado en el banco."""
    return _editar(raiz, "codigo/descubrir.py",
                   "        crudas = [s[off:off + len(entradas[0])] for s in señales]",
                   "        crudas = [e for e in entradas]")


def base_trivial_debil(raiz):
    """Daño CIENTÍFICO: quitarle a la línea base uno de sus dos predictores la vuelve más fácil
    de vencer — todos los veredictos se inflan."""
    return _editar(raiz, "codigo/descubrir.py",
                   "    return min(mse_vel, mse_media)", "    return mse_vel * 3.0")


def nulo_que_no_destruye(raiz):
    """Daño CIENTÍFICO: un 'nulo' que devuelve el mundo intacto. Todo pasaría la Regla 11."""
    return _editar(raiz, "codigo/descubrir.py",
                   "    if nulo == \"barajado\":\n        perm = rng.permutation(len(señales[0]))\n"
                   "        señales = [s[perm] for s in señales]",
                   "    if nulo == \"barajado\":\n        señales = [s for s in señales]")


def contingencia_sin_nulo(raiz):
    """Daño CIENTÍFICO nuevo: que el detector de contingencia declare cuerpo sin superar su nulo.
    Volvería a inventar un 'yo' donde los motores están desconectados."""
    return _editar(raiz, "codigo/contingencia.py",
                   '"es_mia": bool(real[d] > techo[d] and real[d] > fraccion),',
                   '"es_mia": bool(real[d] >= 0.0),')


MUTACIONES = [
    ("desaparece una regla del medio",            "coherencia.py",      borra_una_regla),
    ("la boleta proclama nodos que no existen",   "coherencia.py",      boleta_miente),
    ("el workflow del latido con YAML roto",      "coherencia.py",      workflow_roto),
    ("un item de cola imposible de ejecutar",     "coherencia.py",      cola_inejecutable),
    ("el README proclama otras reglas",           "coherencia.py",      readme_desfasado),
    ("se suaviza tambien el objetivo",            "pruebas.py",         suavizar_el_objetivo),
    ("la linea base se vuelve facil de vencer",   "pruebas.py",         base_trivial_debil),
    ("el nulo por barajado no destruye nada",     "pruebas.py",         nulo_que_no_destruye),
    ("la contingencia declara cuerpo sin nulo",   "pruebas.py",         contingencia_sin_nulo),
]


if __name__ == "__main__":
    print("=== LOS GUARDIANES DE LOS GUARDIANES ===")
    print("Se rompe el proyecto A PROPÓSITO, una vez por daño, y se exige que el guardián grite.")
    print("Un guardián que dice OK sobre un proyecto roto es decoración, no gobernanza.\n")
    for nombre, guardian, danar in MUTACIONES:
        mutacion(nombre, guardian, danar)
    print()
    if FALLOS:
        print(f"META-AUDITORÍA: {len(FALLOS)} GUARDIANES CIEGOS -> arreglarlos antes que nada:")
        for f in FALLOS:
            print(f"   · {f}")
        sys.exit(1)
    print(f"META-AUDITORÍA: los {len(MUTACIONES)} daños fueron cazados. "
          "Los guardianes no son decoración.")
