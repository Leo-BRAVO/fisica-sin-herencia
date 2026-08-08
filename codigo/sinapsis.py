# sinapsis.py — EL SISTEMA NERVIOSO: por donde los organos se hablan, con el genoma de portero.
#
# AUDITORIA DE INTERCONEXION (8-ago-2026, orden del director: "la interconexion debe ser
# increiblemente mejor"): hasta hoy los organos se comunicaban leyendo archivos sueltos cada uno
# a su manera — eso no es un sistema nervioso, es un pueblo sin telefono. Y la disciplina
# "mide-no-decide" vivia en COMENTARIOS: nada la hacia cumplir mecanicamente.
#
# DESDE HOY:
#   1. Todo organo publica sus mediciones en UNA sinapsis comun (arbol/SINAPSIS.jsonl,
#      append-only como la memoria) con formato tipado: quien, tipo, que, cuando.
#   2. EL GENOMA ES EL PORTERO (patron de banderas ejecutables, adaptado de la arquitectura de
#      permisos-por-invocacion que revisamos): arbol/GENOMA.json declara el MODO de cada gen
#      ('mide' / 'propone' / 'decide' / 'inactivo') y esta sinapsis lo HACE CUMPLIR:
#        - un gen en modo 'mide' NO PUEDE publicar decisiones ni propuestas: se bloquea aqui,
#          mecanicamente, no por buena conducta;
#        - un gen 'inactivo' no puede publicar nada;
#        - 'decide' exige prerregistro anotado en el genoma.
#      Cambiar un modo = editar GENOMA.json = commit visible + firma (Regla 33).
#
# Uso: from sinapsis import publicar, leer   |   python sinapsis.py --regla31

import os
import sys
import json
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SINAPSIS = os.path.join(BASE, "arbol", "SINAPSIS.jsonl")
GENOMA = os.path.join(BASE, "arbol", "GENOMA.json")

PERMISOS = {"mide": {"medicion"},
            "propone": {"medicion", "propuesta"},
            "decide": {"medicion", "propuesta", "decision"},
            "inactivo": set()}


def _genoma():
    return json.load(open(GENOMA, encoding="utf-8"))["genes"]


class SinapsisBloqueada(Exception):
    pass


def publicar(gen, tipo, contenido, cuando=None, _ruta=None):
    """Publica un evento en la sinapsis. El genoma decide si este gen PUEDE decir esto."""
    genes = _genoma()
    if gen not in genes:
        raise SinapsisBloqueada(f"'{gen}' no existe en el genoma: nadie habla sin estar en el")
    modo = genes[gen]["modo"]
    if tipo not in PERMISOS.get(modo, set()):
        raise SinapsisBloqueada(
            f"'{gen}' esta en modo '{modo}' y NO puede publicar '{tipo}'. "
            f"Subirle el modo exige editar GENOMA.json: commit visible + firma (Regla 33).")
    if tipo == "decision" and not genes[gen].get("prerregistro"):
        raise SinapsisBloqueada(
            f"'{gen}' esta en modo 'decide' pero SIN prerregistro anotado: una decision sin "
            f"prerregistro es exactamente lo que este proyecto existe para impedir.")
    evento = {"gen": gen, "tipo": tipo, "contenido": contenido, "cuando": cuando}
    with open(_ruta or SINAPSIS, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")
    return evento


def leer(gen=None, tipo=None, _ruta=None):
    ruta = _ruta or SINAPSIS
    if not os.path.exists(ruta):
        return []
    out = []
    for linea in open(ruta, encoding="utf-8"):
        e = json.loads(linea)
        if (gen is None or e["gen"] == gen) and (tipo is None or e["tipo"] == tipo):
            out.append(e)
    return out


def regla31(verbose=True):
    """1. Un gen medidor NO puede publicar una decision (bloqueo mecanico, no cortesia).
       2. Un gen inactivo no puede publicar nada.
       3. Lo publicado se lee integro y en orden (append-only).
       4. Un gen que no esta en el genoma no habla."""
    import tempfile
    tmp = tempfile.mktemp(suffix=".jsonl")
    fallos = []
    def caso(nombre, cond):
        if verbose:
            print(f"  {'ok  ' if cond else 'FALLO'} {nombre}")
        if not cond:
            fallos.append(nombre)
    try:
        publicar("G13_poder", "medicion", {"r2": 0.4}, _ruta=tmp)
        caso("un medidor SI publica mediciones", True)
    except SinapsisBloqueada:
        caso("un medidor SI publica mediciones", False)
    try:
        publicar("G13_poder", "decision", {"hacer": "x"}, _ruta=tmp)
        caso("un medidor NO publica decisiones (bloqueo mecanico)", False)
    except SinapsisBloqueada:
        caso("un medidor NO publica decisiones (bloqueo mecanico)", True)
    try:
        publicar("G11_temple", "medicion", {}, _ruta=tmp)
        caso("un gen inactivo no habla", False)
    except SinapsisBloqueada:
        caso("un gen inactivo no habla", True)
    try:
        publicar("gen_inventado", "medicion", {}, _ruta=tmp)
        caso("un gen fuera del genoma no habla", False)
    except SinapsisBloqueada:
        caso("un gen fuera del genoma no habla", True)
    ev = leer(_ruta=tmp)
    caso("lo publicado se lee integro y en orden", len(ev) == 1 and ev[0]["gen"] == "G13_poder")
    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el genoma es portero, no comentario."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="La sinapsis: bus de organos con el genoma de portero")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31")
