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

# ============================================================================================
# SINAPSIS 2.0 — EL PROTOCOLO UNICO (9-ago-2026, orden del director: "todos interconectados,
# uno a uno, uno a varios y varios a uno; el cerebro manda senales que operan todos los organos
# en base a la realidad o lo que se necesite hacer; y un metodo para detectar cada conexion que
# se realizo durante la prueba").
#
# LO QUE **NO** SE HIZO, Y POR QUE: conectar todos con todos. Un cerebro con todas las neuronas
# conectadas a todas no es mas inteligente: es una crisis epileptica — ruido que se retroalimenta
# hasta que nada significa nada. Los cerebros reales usan SUSCRIPCION POR TEMA (la corteza visual
# no recibe senales del intestino aunque compartan sistema nervioso) y un PORTERO que decide que
# sube (el talamo). Ademas, si todos hablan con todos, se pierde justo lo que el director pide:
# saber QUIEN causo QUE. Aqui cada senal declara su tema y cada evento dice de que otro evento
# nacio. Eso es lo que permite reconstruir el arbol completo de una prueba.
#
# LAS CINCO FORMAS DE HABLAR (todas por el mismo canal, todas con el mismo portero):
#   1. UNO A TODOS      publicar(gen, tipo, contenido, tema=...)      — lo oye quien este suscrito
#   2. UNO A UNO        publicar(..., a="G4_contingencia")            — dirigido a un organo
#   3. UNO A VARIOS     senalar(gen, tema, contenido)                 — el cerebro recluta por tema
#   4. VARIOS A UNO     responder(gen, causa=id_pregunta, ...)        — todos contestan la misma
#   5. IDA Y VUELTA     preguntar(...) -> responder(..., causa=id)    — la senal que se devuelve
#
# CADA EVENTO LLEVA SU PASAPORTE: id propio, traza (que corrida), causa (que evento lo provoco),
# tema, emisor, destinatario. Sin esos cinco campos no hay forma de auditar una mente.
# ============================================================================================

PERMISOS = {"mide": {"medicion", "respuesta"},
            "propone": {"medicion", "respuesta", "propuesta", "pregunta", "senal"},
            "decide": {"medicion", "respuesta", "propuesta", "pregunta", "senal", "decision"},
            "inactivo": set()}

# Los temas del cuerpo de Diego. Un tema que nadie escucha es un error de diseno, y el trazador
# lo caza. Un organo solo recibe lo que declara escuchar en el genoma (campo "escucha").
TEMAS = ("cuerpo", "mundo", "frontera", "leyes", "recursos", "descanso", "revision")


def _genoma():
    return json.load(open(GENOMA, encoding="utf-8"))["genes"]


class SinapsisBloqueada(Exception):
    pass


def _siguiente_id(ruta):
    """Id incremental y legible. No hace falta azar: la sinapsis es append-only y de un solo
    escritor por corrida, y un id predecible se lee mejor en una auditoria."""
    if not os.path.exists(ruta):
        return 1
    n = 0
    for _ in open(ruta, encoding="utf-8"):
        n += 1
    return n + 1


def publicar(gen, tipo, contenido, cuando=None, _ruta=None,
             tema=None, a=None, causa=None, traza=None, deriva_de=None):
    """Publica un evento en la sinapsis. El genoma decide si este gen PUEDE decir esto.

    tema  — de que habla (uno de TEMAS). Quien este suscrito al tema lo recibe.
    a     — destinatario concreto: convierte la publicacion en UNO A UNO.
    causa — id del evento que provoco este. Es lo que permite reconstruir el arbol causal.
    traza — identificador de la corrida entera, para separar una prueba de otra.

    deriva_de — id del evento cuya EVIDENCIA se uso para producir este. NO es lo mismo que
      `causa`, y confundirlos fue un error propio cazado el 9-ago-2026 por este mismo trazador:
        · `causa`      = QUE ME HIZO HABLAR   (conversacional: me preguntaron)
        · `deriva_de`  = DE QUIEN SON LOS DATOS QUE USE  (evidencial: mire lo que el midio)
      Ocho organos contestando la misma pregunta NO son un consenso de un solo testigo: cada uno
      midio lo suyo y respondio por su cuenta. Ocho organos repitiendo lo que dijo un noveno SI
      lo son. La genealogia —lo que cuenta testigos independientes— viaja SOLO por `deriva_de`.
    """
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
    if a is not None and a not in genes:
        raise SinapsisBloqueada(f"no se puede dirigir un evento a '{a}': no existe en el genoma")
    if tema is not None and tema not in TEMAS:
        raise SinapsisBloqueada(
            f"tema '{tema}' desconocido. Los temas son {TEMAS}: inventar temas sueltos es como "
            f"tender un nervio a ninguna parte — nadie lo escucha y nadie lo sabe.")
    ruta = _ruta or SINAPSIS
    # ENTREGA — LA ESCRIBE EL BUS, NUNCA EL EMISOR. Sin este campo es IMPOSIBLE distinguir
    # "nadie estaba escuchando" de "escucharon y se callaron", y ese es el modo de fallo numero
    # uno documentado en la taxonomia MAST (NeurIPS 2025) sobre 1600 trazas reales: un modulo
    # que ignora la entrada de otro. Los dos casos se ven identicos —silencio— y se arreglan en
    # sitios opuestos: uno es error de diseno del mapa, el otro es un organo averiado.
    # (Hallazgo de la investigacion del 9-ago-2026, que encontro este hueco en la version de
    # esta misma manana.)
    if a is not None:
        entrega = [a]
    elif tema is not None:
        entrega = [o for o in escuchan(tema, genes) if o != gen]
    else:
        entrega = []
    # ENLACES — para difusion (uno a varios) y agregacion (varios a uno). La convencion de
    # OpenTelemetry para mensajeria es tajante: el modelo padre-hijo MIENTE en cuanto hay
    # difusion, porque un evento solo puede tener UN padre. Una convocatoria a nueve organos
    # trazada con padre-hijo se ve completa y ha perdido ocho de nueve relaciones causales. Es el
    # fallo mas insidioso que existe en auditoria: produce una autopsia con apariencia de
    # completitud. `causa` queda para las cadenas 1:1; `enlaces` carga el resto.
    evento = {"id": _siguiente_id(ruta), "gen": gen, "tipo": tipo, "contenido": contenido,
              "cuando": cuando, "tema": tema, "a": a, "causa": causa, "traza": traza,
              "entrega": entrega, "enlaces": [], "deriva_de": deriva_de}
    # GENEALOGIA — de que mensajes ORIGINALES desciende esto. Sirve para contar TESTIGOS
    # INDEPENDIENTES, no mensajes: si cuatro organos coinciden pero los cuatro derivan del mismo
    # ancestro, no hay cuatro testigos, hay uno repetido cuatro veces. Es el "consenso falso" que
    # la literatura de cascadas de error (2026) senala como el fallo que se vuelve incorregible.
    if deriva_de is not None:
        padres = [e for e in leer(_ruta=ruta) if e.get("id") == deriva_de]
        evento["genealogia"] = ((padres[0].get("genealogia") or [deriva_de])
                                if padres else [deriva_de])
    else:
        # testigo PROPIO: midio lo suyo. Su genealogia es el mismo, y por eso cuenta como uno.
        evento["genealogia"] = [evento["id"]]
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")
    return evento


def escuchan(tema, _genes=None):
    """QUIEN OYE ESTE TEMA. La suscripcion vive en el genoma (campo 'escucha'), no en el codigo:
    cambiar quien oye que es un cambio de genoma, con commit visible."""
    genes = _genes or _genoma()
    return sorted(g for g, v in genes.items()
                  if tema in (v.get("escucha") or []) and v.get("modo") != "inactivo")


def senalar(gen, tema, contenido, cuando=None, traza=None, causa=None, _ruta=None):
    """UNO A VARIOS — el cerebro recluta a todos los organos suscritos a un tema.
    Devuelve el evento y a quienes les toca responder. Si no hay nadie suscrito, la senal se
    publica igual (para que el trazador la vea) y la lista sale vacia: una senal sin oyente es un
    error de diseno que debe quedar registrado, no silenciado."""
    ev = publicar(gen, "senal", contenido, cuando=cuando, _ruta=_ruta,
                  tema=tema, causa=causa, traza=traza)
    return ev, ev["entrega"]


def preguntar(gen, tema, contenido, a=None, cuando=None, traza=None, _ruta=None):
    """IDA Y VUELTA — una pregunta que espera respuesta. `a` la hace UNO A UNO; sin `a` la
    escucha todo el que este suscrito al tema (y entonces sera VARIOS A UNO al contestar)."""
    ev = publicar(gen, "pregunta", contenido, cuando=cuando, _ruta=_ruta,
                  tema=tema, a=a, traza=traza)
    return ev, ev["entrega"]


def responder(gen, causa, contenido, cuando=None, traza=None, tema=None, a=None, _ruta=None,
              deriva_de=None):
    """La senal que se devuelve. `causa` es el id de la pregunta o senal que la provoco — sin eso
    la respuesta es huerfana y el trazador la marca como fallo de protocolo."""
    return publicar(gen, "respuesta", contenido, cuando=cuando, _ruta=_ruta,
                    tema=tema, a=a, causa=causa, traza=traza, deriva_de=deriva_de)


def leer(gen=None, tipo=None, _ruta=None, tema=None, traza=None, causa=None, a=None):
    """Lee el bus con filtros. Sin argumentos devuelve todo, en orden de llegada."""
    ruta = _ruta or SINAPSIS
    if not os.path.exists(ruta):
        return []
    out = []
    for linea in open(ruta, encoding="utf-8"):
        if not linea.strip():
            continue
        e = json.loads(linea)
        if gen is not None and e["gen"] != gen:
            continue
        if tipo is not None and e["tipo"] != tipo:
            continue
        if tema is not None and e.get("tema") != tema:
            continue
        if traza is not None and e.get("traza") != traza:
            continue
        if causa is not None and e.get("causa") != causa:
            continue
        if a is not None and e.get("a") != a:
            continue
        out.append(e)
    return out


def recibidos_por(gen, traza=None, _ruta=None):
    """QUE LE LLEGO A ESTE ORGANO: lo dirigido a el, mas todo lo de los temas que escucha.
    Es la vista del mundo desde dentro de un organo — la que el organo usaria para actuar."""
    genes = _genoma()
    mios = set(genes.get(gen, {}).get("escucha") or [])
    return [e for e in leer(_ruta=_ruta, traza=traza)
            if e["gen"] != gen and (e.get("a") == gen or (e.get("tema") in mios and not e.get("a")))]


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


def testigos_independientes(eventos):
    """CUANTOS TESTIGOS DE VERDAD hay detras de un conjunto de eventos que coinciden.
    Cuenta genealogias distintas, no mensajes. Cuatro organos que dicen lo mismo derivando todos
    del mismo ancestro son UN testigo repetido cuatro veces — y tratarlo como cuatro es como se
    fabrica un consenso falso que despues nadie puede corregir."""
    raices = set()
    for e in eventos:
        g = e.get("genealogia") or []
        raices.add(tuple(g) if g else ("propio", e["id"]))
    return len(raices)
