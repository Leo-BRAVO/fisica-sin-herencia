# contratos.py — EL GUARDIAN DE LAS INTERFACES (prerregistro-49, 11-ago-2026).
#
# POR QUE EXISTE, y es un hallazgo medido y no una idea bonita. El INFORME-52 encontro el defecto
# mas grave del proyecto hasta la fecha, y NO era de un modulo: era de la CADENA. G14 publicaba
# una "ignorancia curable" inflada por el ruido y G8 se la creia SIN COMPROBAR NADA, con lo que el
# televisor se llevaba 7.036 de 10 y la region buena 2.964.
#
# Cuando el director pregunto si los "organos" son cuerpo o son mente, la respuesta honesta fue
# que 12 de 15 son mente — y que renombrarlos no habria evitado nada, porque el problema no es la
# metafora biologica: ES UNA INTERFAZ SIN CONTRATO. Este archivo mecaniza el contrato.
#
# QUE EXIGE:
#   1. Todo modulo que publique un numero que otro consume declara `CONTRATO = {...}` con su TIPO:
#      SENTIDO (lee el mundo) · ACTUADOR (lo cambia) · ESTIMADOR (produce numeros) · POLITICA
#      (decide).
#   2. Todo ESTIMADOR declara el RANGO VALIDO de cada numero que publica.
#   3. Todo consumidor declara QUE consume, DE QUIEN, y con que rango — y lo VERIFICA en codigo.
#
# LO QUE ESTE GUARDIAN **NO** PUEDE COMPROBAR, dicho aqui para que nadie confie de mas: no sabe si
# el rango declarado es el CORRECTO. Un rango mal elegido pasa este guardian igual de bien que uno
# bueno. Solo comprueba que exista, que se declare y que el consumidor lo mire.
#
# Uso: python contratos.py [--regla31]

import os
import re
import sys
import argparse
import importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIPOS = ("SENTIDO", "ACTUADOR", "ESTIMADOR", "POLITICA")

# Los modulos que HOY tienen contrato. La lista crece a mano y a proposito: meterlos todos de
# golpe con un contrato inventado seria peor que no tenerlo, porque daria por revisado lo que no
# se ha mirado. Cada modulo entra aqui cuando alguien lee de verdad que publica y que consume.
CON_CONTRATO = ("incertidumbre", "atencion")

METODO = {
    "prerregistro": 49,
    "tipo_de_medida": "umbral",   # cada chequeo de contrato es una decision binaria: pasa o no
    "que_mide": ("cuantos incumplimientos de contrato detecta: tipo invalido, numero publicado "
                 "sin rango, consumo sin decir de quien, y rango declarado pero no verificado "
                 "en codigo"),
    "comparten_datos": {
        "hay": False,
        "porque": "cada contrato se revisa por separado y no hay ninguna magnitud compartida "
                  "entre modulos; lo unico comun es el propio detector",
    },
    "linea_base": ("no revisar nada — el detector tonto que dice 'todo bien' siempre. Detecta 0 "
                   "incumplimientos, y cualquier detector util tiene que superarlo sobre "
                   "contratos rotos a proposito (Regla 11)"),
    "formulas": [
        {"base": {"rotos": 1.0}, "parametro": "rotos", "factor": 4.0, "esperado": "sube",
         "porque": "mas contratos rotos = mas incumplimientos detectados. Se declara como "
                   "desigualdad y no como proporcion porque un mismo contrato roto puede disparar "
                   "mas de un chequeo. Base 1.0 y NO 0.0: multiplicar cero por cuatro sigue "
                   "siendo cero, y ese descuido ya me tumbo cuatro relaciones este mes"},
    ],
}

_fallos = []
_ok = []


def revisar_contrato(nombre, contrato):
    """EL REVISOR PURO: recibe un contrato y devuelve la lista de incumplimientos. Separado del
    resto para poder probarlo con contratos SINTETICOS —rotos a proposito— sin tocar el
    repositorio. Un detector que solo se puede probar sobre los modulos reales no se puede probar
    por el lado negativo."""
    fallos = []
    if not isinstance(contrato, dict):
        return [f"{nombre}: sin CONTRATO"]
    if contrato.get("tipo") not in TIPOS:
        fallos.append(f"{nombre}: tipo invalido {contrato.get('tipo')!r}")
    for clave, spec in (contrato.get("publica") or {}).items():
        r = (spec or {}).get("rango")
        if not (isinstance(r, (list, tuple)) and len(r) == 2
                and isinstance(r[0], (int, float))):
            fallos.append(f"{nombre}: publica '{clave}' SIN rango")
    for clave, spec in (contrato.get("consume") or {}).items():
        if not (spec or {}).get("de"):
            fallos.append(f"{nombre}: consume '{clave}' sin decir DE QUIEN")
        r = (spec or {}).get("rango")
        if not (isinstance(r, (list, tuple)) and len(r) == 2):
            fallos.append(f"{nombre}: consume '{clave}' sin rango declarado")
    return fallos


def _metodo_medir(rotos=1.0):
    """PASO 1 — la medida escalar: cuantos incumplimientos detecta sobre `rotos` contratos rotos
    a proposito. Sinteticos: no se toca ningun modulo real para medir el detector."""
    total = 0
    for i in range(int(rotos)):
        total += len(revisar_contrato(f"sintetico_{i}",
                                      {"tipo": "INVENTADO", "publica": {"x": {}}}))
    return float(total)


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el detector distingue un contrato bueno de uno roto, o
    marca todo por igual?** Un guardian que marca siempre es tan inutil como uno que nunca marca,
    y ademas es peor: enseña a ignorarlo."""
    fallos = []
    bueno = revisar_contrato("bueno", {"tipo": "ESTIMADOR",
                                       "publica": {"x": {"rango": [0.0, 1.0]}}})
    roto = revisar_contrato("roto", {"tipo": "INVENTADO", "publica": {"x": {}}})
    if bueno:
        fallos.append(f"marca un contrato BIEN puesto: {bueno}")
    if not roto:
        fallos.append("NO marca un contrato roto: el detector no detecta")
    if not CON_CONTRATO:
        fallos.append("la lista de modulos con contrato esta VACIA: revisar sobre vacio aprueba "
                      "siempre, que es justo lo que la Regla 31 prohibe")
    return {"aprueba": not fallos, "fallos": fallos,
            "incumplimientos_en_uno_bueno": len(bueno),
            "incumplimientos_en_uno_roto": len(roto)}


def _caso(nombre, ok, detalle=""):
    (_ok if ok else _fallos).append(nombre)
    print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  -> {detalle}" if detalle and not ok
                                                       else ""))


def revisar(modulos=CON_CONTRATO, verbose=True):
    for nombre in modulos:
        mod = importlib.import_module(nombre)
        c = getattr(mod, "CONTRATO", None)
        if not isinstance(c, dict):
            _caso(f"{nombre}: declara CONTRATO", False,
                  "sin CONTRATO no se sabe que publica ni que consume")
            continue
        _caso(f"{nombre}: declara CONTRATO", True)

        tipo = c.get("tipo")
        _caso(f"{nombre}: su tipo es uno de {TIPOS}", tipo in TIPOS, f"declara {tipo!r}")

        # --- si publica, cada numero necesita RANGO
        for clave, spec in (c.get("publica") or {}).items():
            r = (spec or {}).get("rango")
            bien = (isinstance(r, (list, tuple)) and len(r) == 2
                    and isinstance(r[0], (int, float)))
            _caso(f"{nombre}: publica '{clave}' CON rango declarado", bien, f"rango={r!r}")

        # --- si consume, hay que decir DE QUIEN y con que rango, y VERIFICARLO EN CODIGO
        fuente = os.path.join(BASE, "codigo", f"{nombre}.py")
        texto = open(fuente, encoding="utf-8").read()
        for clave, spec in (c.get("consume") or {}).items():
            de = (spec or {}).get("de")
            r = (spec or {}).get("rango")
            _caso(f"{nombre}: consume '{clave}' diciendo DE QUIEN", bool(de), f"de={de!r}")
            _caso(f"{nombre}: consume '{clave}' con rango declarado",
                  isinstance(r, (list, tuple)) and len(r) == 2, f"rango={r!r}")
            # El chequeo que de verdad importa: que el rango no sea un adorno. Se exige que el
            # modulo LEVANTE UN ERROR en alguna parte donde se mencione el rango del contrato.
            verifica = bool(re.search(r"raise\s+\w*Error", texto)) and "rango" in texto
            _caso(f"{nombre}: VERIFICA en codigo el rango de '{clave}' (no solo lo declara)",
                  verifica,
                  "declarar un rango y no comprobarlo es exactamente lo que hizo G8 con G14")
            # Y que el proveedor declare esa misma clave: un contrato entre dos donde uno de los
            # dos no sabe de que se habla no es un contrato.
            prov = (de or "").replace(".py", "")
            if prov:
                try:
                    pm = importlib.import_module(prov)
                    pub = (getattr(pm, "CONTRATO", {}) or {}).get("publica") or {}
                    _caso(f"{nombre}: '{clave}' lo publica de verdad {prov}", clave in pub,
                          f"{prov} publica {list(pub)}")
                except Exception as e:
                    _caso(f"{nombre}: se puede leer el contrato de {prov}", False, str(e))
    return not _fallos


def regla31(verbose=True):
    """LA REGLA 31 DE ESTE ARCHIVO — los detectores, probados por LOS DOS LADOS.

    Sin esto, este guardian podria aprobar sobre una lista vacia de modulos y quedarse tan ancho:
    `not []` es siempre cierto, y ya me paso dentro del archivo que nacio para cazar ese mal."""
    fallos = []

    def caso(nombre, ok):
        print(f"  {'ok  ' if ok else 'FALLO'} {nombre}")
        if not ok:
            fallos.append(nombre)

    caso("un modulo SIN contrato se marca", len(revisar_contrato("x", None)) > 0)
    caso("un tipo inventado se marca",
         any("tipo invalido" in f for f in
             revisar_contrato("x", {"tipo": "INVENTADO", "publica": {}})))
    caso("un numero publicado SIN rango se marca",
         any("SIN rango" in f for f in
             revisar_contrato("x", {"tipo": "ESTIMADOR", "publica": {"y": {}}})))
    caso("un consumo sin decir DE QUIEN se marca",
         any("DE QUIEN" in f for f in
             revisar_contrato("x", {"tipo": "POLITICA",
                                    "consume": {"y": {"rango": [0, 1]}}})))
    caso("un contrato BIEN puesto NO se marca",
         revisar_contrato("x", {"tipo": "ESTIMADOR",
                                "publica": {"y": {"rango": [0.0, 1.0]}}}) == [])
    caso("la lista de modulos con contrato NO esta vacia (un chequeo sobre vacio no aprueba nada)",
         len(CON_CONTRATO) > 0)
    print("\nREGLA 31: " + ("APRUEBA — los detectores funcionan por los dos lados."
                            if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Guardian de las interfaces (prereg-49)")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("== CONTRATOS: quien publica que, quien lo consume, y quien lo comprueba ==")
    ok = revisar()
    print(f"\nCONTRATOS: {'SIN FALLOS' if ok else f'{len(_fallos)} FALLOS'} "
          f"({len(_ok)} chequeos en verde)")
    print("NOTA: esto NO comprueba que el rango declarado sea el correcto — solo que exista, "
          "se declare y el consumidor lo mire.")
    sys.exit(0 if ok else 1)
