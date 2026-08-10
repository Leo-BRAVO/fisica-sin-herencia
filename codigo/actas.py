# actas.py — EL AUDITOR DE MIS PROPIAS ACTAS
#
# EL HUECO QUE ESTE ARCHIVO TAPA, dicho sin adornos. Hasta hoy el proyecto vigilaba el código
# (banco), la casa (coherencia), las reglas (auditoria_total + reglas), los guardianes
# (guardianes_de_guardianes) y los instrumentos (metodo + sanidad). **Nadie vigilaba lo que yo
# ESCRIBO sobre los resultados.** El evaluador del lazo juzga nuestra ingeniería, no mis
# conclusiones. Así que la cadena entera podía estar impecable y el acta decir otra cosa que los
# datos — y el director, que lee las actas y no los JSON, no habría tenido cómo saberlo.
#
# Es el hueco más peligroso que quedaba, porque es el único donde un error mío llega intacto hasta
# la persona que decide. Y no es hipotético: el 8-ago hubo que corregir el reclamo del nodo N-003
# ("superó al orquestador") porque comparaba reducciones contra bases distintas — el número estaba
# bien y la frase estaba mal.
#
# QUE COMPRUEBA, y qué NO puede comprobar:
#   SI  — que el VEREDICTO escrito en el acta sea el mismo que el veredicto del archivo de datos
#         que ella misma cita. Un acta que dice GANA donde el JSON dice NO CONCLUYENTE se cae.
#   SI  — que las cifras que el acta presenta como medidas EXISTAN en los datos citados.
#   SI  — que toda acta cite al menos una fuente de datos comprobable.
#   NO  — si mi INTERPRETACION es correcta. Ninguna máquina puede juzgar eso, y fingir que sí
#         sería peor que no intentarlo. Lo que se cierra es la puerta a que el acta CONTRADIGA sus
#         propios datos; la puerta a que los lea mal sigue abierta y se declara abierta.
#
# Uso: python actas.py    (y lo llama auditoria_total.py)

import os
import re
import json
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Solo se auditan las actas del régimen nuevo: las anteriores se escribieron sin este contrato y
# reescribirlas para que pasen sería exactamente lo que la Regla 8 prohíbe.
DESDE_INFORME = 48

TOLERANCIA = 0.02        # 2%: las actas redondean, y exigir igualdad exacta sería ruido puro


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _numeros_de(obj, salida=None):
    """Todos los números que hay dentro de un JSON, a cualquier profundidad."""
    salida = [] if salida is None else salida
    if isinstance(obj, dict):
        for v in obj.values():
            _numeros_de(v, salida)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _numeros_de(v, salida)
    else:
        n = _num(obj)
        if n is not None:
            salida.append(n)
    return salida


def _series_por_clave(obj, acc=None, camino=""):
    """Agrupa por RUTA de clave todos los numeros que aparecen en varios JSON hermanos. Sirve para
    reconocer una serie ('puntaje' de cinco semillas) y poder promediarla."""
    acc = {} if acc is None else acc
    if isinstance(obj, dict):
        for k, v in obj.items():
            _series_por_clave(v, acc, f"{camino}.{k}")
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _series_por_clave(v, acc, camino)
    else:
        n = _num(obj)
        if n is not None and not isinstance(obj, bool):
            acc.setdefault(camino, []).append(n)
    return acc


def _medias_por_clave(datos):
    """La media de cada serie de dos o mas valores. Es la unica derivacion que se admite."""
    acc = _series_por_clave(datos)
    return [sum(v) / len(v) for v in acc.values() if len(v) >= 2]


def _veredicto_de(obj):
    """El veredicto declarado por los datos, si lo hay."""
    if isinstance(obj, dict):
        for k in ("veredicto", "fallo", "dictamen"):
            if isinstance(obj.get(k), str):
                return obj[k]
        for v in obj.values():
            r = _veredicto_de(v)
            if r:
                return r
    return None


def _fuentes_citadas(texto):
    """Rutas de `resultados/...` que el acta cita. Es el contrato: si no cita, no se puede auditar."""
    rutas = set()
    for m in re.finditer(r"resultados/[\w\-/\.]+", texto):
        rutas.add(m.group(0).rstrip(".,)`*"))
    return sorted(rutas)


def _datos_de(rutas):
    """Carga todos los JSON bajo las rutas citadas."""
    datos = []
    for r in rutas:
        p = os.path.join(BASE, r)
        if os.path.isdir(p):
            for f in glob.glob(os.path.join(p, "*.json")):
                try:
                    datos.append((f, json.load(open(f, encoding="utf-8"))))
                except Exception:
                    pass
        elif p.endswith(".json") and os.path.exists(p):
            try:
                datos.append((p, json.load(open(p, encoding="utf-8"))))
            except Exception:
                pass
    return datos


def _cifras_del_acta(texto):
    """Los números que el acta presenta como MEDIDOS: los de sus tablas. Se excluyen a propósito
    los años, los números de regla/informe/prerregistro y los conteos pequeños de prosa, que no
    son mediciones y solo meterían ruido."""
    cifras = []
    for linea in texto.split("\n"):
        if not linea.strip().startswith("|"):
            continue
        if re.search(r"Regla|INFORME|prerregistro|semilla", linea, re.I) and "|" not in linea[1:]:
            continue
        for m in re.finditer(r"[-+]?\d+\.\d+", linea):     # solo decimales: son mediciones
            n = float(m.group(0))
            if 1900 < abs(n) < 2100:
                continue
            cifras.append(n)
    return cifras


def auditar(desde=DESDE_INFORME, verbose=True):
    fallos, avisos = [], []
    actas = sorted(glob.glob(os.path.join(BASE, "resultados", "INFORME-*.md")))
    revisadas = 0
    for ruta in actas:
        m = re.search(r"INFORME-(\d+)", os.path.basename(ruta))
        if not m or int(m.group(1)) < desde:
            continue
        revisadas += 1
        nombre = os.path.basename(ruta)
        texto = open(ruta, encoding="utf-8").read()

        # (1) TODA ACTA CITA SUS DATOS. Sin esto no hay nada que auditar, y un acta sin fuente es
        #     una opinión con formato de informe.
        fuentes = [f for f in _fuentes_citadas(texto)
                   if os.path.exists(os.path.join(BASE, f))]
        if not fuentes:
            fallos.append(f"{nombre}: no cita NINGUNA fuente de datos que exista")
            continue

        datos = _datos_de(fuentes)
        if not datos:
            avisos.append(f"{nombre}: cita fuentes pero ninguna trae JSON auditable")
            continue

        # (2) EL VEREDICTO DEL ACTA ES EL DE LOS DATOS. El fallo más grave posible.
        vered_datos = [v for _, d in datos for v in [_veredicto_de(d)] if v]
        if vered_datos:
            arriba = texto[:4000].upper()
            if not any(v.split("—")[0].strip().upper()[:12] in arriba for v in vered_datos):
                fallos.append(f"{nombre}: los datos dicen '{vered_datos[0]}' y el acta no lo dice "
                              f"en ninguna parte de su encabezado")

        # (3) LAS CIFRAS DE SUS TABLAS EXISTEN EN LOS DATOS.
        del_json = _numeros_de([d for _, d in datos])
        # UN ACTA PUEDE PROMEDIAR: "dirigido 14.4" es la media de cinco semillas y es legitimo que
        # no este escrito tal cual en ningun JSON. Se admiten las MEDIAS de las series por clave —
        # una relajacion acotada y declarada, no un permiso general. Lo que sigue sin admitirse es
        # una cifra que no salga ni de los datos ni de promediarlos: eso es un numero que solo
        # existe en mi cabeza, y el 10-ago publique uno asi (la obediencia 0.0297 del prereg-42,
        # que habia medido a mano y nunca guarde).
        del_json = list(del_json) + _medias_por_clave([d for _, d in datos])
        huerfanas = []
        for c in _cifras_del_acta(texto):
            if not any(abs(c - j) <= TOLERANCIA * max(1.0, abs(j)) for j in del_json):
                huerfanas.append(c)
        if huerfanas:
            fallos.append(f"{nombre}: {len(huerfanas)} cifras de sus tablas NO aparecen en los "
                          f"datos citados: {sorted(set(huerfanas))[:6]}")

    if verbose:
        print(f"=== EL AUDITOR DE LAS ACTAS (desde el INFORME-{desde}) ===")
        print(f"  actas revisadas: {revisadas}")
        for f in fallos:
            print(f"  FALLO {f}")
        for a in avisos:
            print(f"  aviso {a}")
        if not fallos:
            print("  ok    ninguna acta contradice los datos que cita")
        print("  NOTA: esto NO comprueba que mi interpretacion sea correcta — ninguna maquina "
              "puede. Solo que el acta no contradiga sus propios datos.")
    return fallos


if __name__ == "__main__":
    import sys
    sys.exit(1 if auditar() else 0)
