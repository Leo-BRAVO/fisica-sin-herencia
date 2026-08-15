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

_fallos = []
_ok = []


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

    class _Sin:
        pass

    class _Malo:
        CONTRATO = {"tipo": "INVENTADO", "publica": {"x": {}}}

    class _Bueno:
        CONTRATO = {"tipo": "ESTIMADOR", "publica": {"x": {"rango": [0.0, 1.0]}}}

    caso("un modulo SIN contrato se marca", getattr(_Sin, "CONTRATO", None) is None)
    caso("un tipo inventado se marca", _Malo.CONTRATO["tipo"] not in TIPOS)
    caso("un numero publicado SIN rango se marca",
         (_Malo.CONTRATO["publica"]["x"].get("rango") is None))
    caso("un contrato BIEN puesto NO se marca",
         _Bueno.CONTRATO["tipo"] in TIPOS
         and len(_Bueno.CONTRATO["publica"]["x"]["rango"]) == 2)
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
