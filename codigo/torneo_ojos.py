# torneo_ojos.py — EL TORNEO DE SUS OJOS (prerregistro-27): A vs B vs C vs Ranuras.
#
# La primera generación de la Regla 33 corrida de verdad: cuatro arquitecturas visuales, mismo
# mundo, mismas semillas, aptitud del lado de los jueces (filogenia.aptitud), acta con
# filogenia.torneo(). Ninguna arquitectura ve su propio puntaje ni el de las demás.
#
# Uso: python torneo_ojos.py [--episodios 12] [--pasos 1500] [--epocas 12] [--semillas 5]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

from gimnasio import correr
from ojos_gimnasio import entrenar_ojos
import percepcion2 as p2
import ranuras as rn
from filogenia import aptitud, torneo
import panel_jueces as pj

COMPETIDORES = ["A-pixel", "B-predictivo", "C-corolario", "R-ranuras"]

# ==========================================================================================
# LA PUERTA (metodo.py) — 10-ago-2026
# ==========================================================================================
# Este modulo llevaba 5 estudios ENCOLADOS Y PARADOS desde que la puerta se encendio: no tenia
# manifiesto, ni formulas comprobables, ni ficha de sanidad, ni Regla 31 propia. Y no es un modulo
# cualquiera — es el que DECIDE cual de las cuatro arquitecturas visuales de Diego gana. Un torneo
# cuyo juez nunca se examino es el sitio mas caro posible para tener un instrumento roto, y ya nos
# paso una vez: la primera vuelta (prereg-27) salio NO CONCLUYENTE POR INSTRUMENTO porque la vara
# aplastaba a los cuatro competidores en 0.0000 EXACTO. La vara no medía a nadie: medía su suelo.
#
# LO QUE SE EXAMINA AQUI ES LA VARA, NO LOS COMPETIDORES. Por eso todo lo de abajo corre sobre
# latentes SINTETICOS cuya relacion con los comandos la fijamos nosotros: es la unica forma de
# saber si la lectura mide lo que dice medir sin preguntarle al que esta siendo medido.
METODO = {
    "prerregistro": 38,
    "tipo_de_medida": "continua",
    "que_mide": ("la lectura de CONTINGENCIA del panel: cuanta obediencia NETA a los comandos "
                 "hay en unos latentes, descontado su propio nulo por comandos barajados"),
    "comparten_datos": {
        "hay": True,
        "porque": "los cuatro competidores se evaluan sobre LOS MISMOS videos y los MISMOS "
                  "comandos, a proposito: un torneo donde cada competidor corre su propio mundo "
                  "no compara arquitecturas, compara suertes. Lo que NO comparten es el "
                  "entrenamiento — cada uno entrena su propio codificador con su propia semilla.",
    },
    "linea_base": ("el nulo por comandos barajados, que ya va restado dentro del puntaje: la "
                   "lectura ES una ganancia sobre su linea base, no un acierto crudo (Regla 11)"),
    "formulas": [
        {"base": {"senal": 0.8, "ruido": 0.3}, "parametro": "senal", "factor": 0.05,
         "esperado": "baja",
         "porque": "si los latentes dejan de seguir a los comandos, la contingencia debe caer. "
                   "Se declara como DESIGUALDAD y no como proporcion porque la ganancia de "
                   "obediencia neta no tiene forma cerrada: poner un factor exacto seria "
                   "inventarselo, y ya me reprobo la puerta una vez por hacer eso"},
        {"base": {"senal": 0.8, "ruido": 0.3}, "parametro": "ruido", "factor": 8.0,
         "esperado": "baja",
         "porque": "mas ruido encima de la misma señal = menos obediencia legible. Si NO bajara, "
                   "la lectura estaria midiendo la escala de los latentes y no su relacion con "
                   "los comandos"},
    ],
}


def _latentes_sinteticos(n_ep=6, pasos=1400, dim=8, senal=0.8, ruido=0.3, semilla=7):
    """Latentes de juguete con obediencia CONTROLADA por nosotros: cada canal sigue al comando
    con peso `senal` y lleva `ruido` encima. Es la unica forma de examinar la vara sin preguntarle
    al competidor — la verdad la ponemos nosotros.

    1400 pasos x 6 episodios y no menos: `contingencia.medir` usa ventanas de 150 y EXIGE al menos
    20 para dar un veredicto — con menos, ese criterio "fabrica cuerpo donde no lo hay" (medido el
    8-ago-2026, y por eso LANZA en vez de devolver un numero flojo). Mi primer intento usaba 120
    pasos y la puerta lo tumbo en el paso 1. Tenia razon: habria examinado la vara con una medicion
    que la propia herramienta declara invalida.
    """
    rng = np.random.default_rng(int(semilla))
    comandos, latentes = [], []
    for _ in range(int(n_ep)):
        u = rng.normal(size=(int(pasos), 3))
        z = np.zeros((int(pasos), int(dim)))
        for d in range(int(dim)):
            fuente = u[:, d % 3]
            z[:, d] = float(senal) * np.cumsum(fuente) / max(1.0, np.sqrt(pasos))
            z[:, d] += rng.normal(0.0, float(ruido), size=int(pasos))
        comandos.append(u)
        latentes.append(z)
    return comandos, latentes


def _metodo_medir(senal=0.8, ruido=0.3):
    """PASO 1 — la medida escalar sobre la que se comprueban las relaciones metamorficas."""
    com, lat = _latentes_sinteticos(senal=senal, ruido=ruido)
    return float(pj.lectura_contingencia(lat, com, jueces=[1, 2, 3], nulos=4)["puntaje"])


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta que contesta: **¿la lectura sigue a la obediencia real de
    los latentes, o sigue a otra cosa (su escala, su suavidad, su dimension)?**

    Se fabrican 8 mundos en los que la obediencia se sortea, y se comprueba que la lectura
    correlacione con ELLA y no con el ruido, que se sortea aparte. Es el error de tipo CRUCE: una
    vara que sube cuando sube el ruido coronaria al competidor mas ruidoso, no al que mejor ve.
    """
    import sanidad as S
    # DOS INTENTOS FALLIDOS ANTES DE ESTE, Y LOS DOS ERAN MIOS, NO DE LA VARA:
    #   1) sortee obediencia Y ruido juntos y correlacione la lectura contra la obediencia sola:
    #      0.234 contra un piso de 0.6. Con dos causas moviendose a la vez, una correlacion simple
    #      contra una de ellas esta diluida POR CONSTRUCCION.
    #   2) le di a S.correlaciones() dos "lecturas" que venian de experimentos DISTINTOS. Esa
    #      funcion asume que todas las lecturas son del MISMO conjunto de objetos; cruzarlas no
    #      significa nada, y me contesto que la obediencia explicaba un 21.6% extra del ruido.
    #
    # LA RAZON DE FONDO: S.correlaciones() esta hecha para instrumentos de VARIAS propiedades
    # (masa, roce, ...). Este da UN SOLO NUMERO. La pregunta correcta para un instrumento de una
    # sola lectura no es "¿cada lectura mide lo suyo?" sino "¿esta unica lectura sigue a la
    # propiedad que dice, y es SORDA a la que no?". Se escribe explicita, con los MISMOS umbrales
    # publicados de la ficha para no inventarme una vara mas blanda a mitad de camino.
    rng = np.random.default_rng(19)
    senales, ruidos, lect = [], [], []
    for _ in range(8):
        s = float(rng.uniform(0.2, 1.6))
        r = float(rng.uniform(0.1, 0.9))
        senales.append(s)
        ruidos.append(r)
        lect.append(_metodo_medir(senal=s, ruido=r))

    fallos = []
    # (a) SIGUE a la obediencia — descontando el ruido, que se movio a la vez.
    solo_senal = [_metodo_medir(senal=s, ruido=0.3) for s in senales]
    r_propia = S.correlaciones({"obediencia": solo_senal}, {"obediencia": senales})
    fallos += r_propia["fallos"]
    # (b) ES SORDA a la escala del ruido cuando la obediencia no cambia. Si subiera con el ruido,
    #     el torneo coronaria al competidor mas ruidoso en vez de al que mejor ve — que es
    #     exactamente el modo de fallo que un juez de arquitecturas NO se puede permitir.
    solo_ruido = [_metodo_medir(senal=0.8, ruido=r) for r in ruidos]
    import numpy as _np
    c_ruido = abs(float(_np.corrcoef(solo_ruido, ruidos)[0, 1]))
    if c_ruido > 0.0 and _np.corrcoef(solo_ruido, ruidos)[0, 1] > 0.0:
        fallos.append(f"la lectura SUBE con el ruido (corr {c_ruido:.3f}): coronaria al mas ruidoso")
    return {"aprueba": not fallos, "fallos": fallos,
            "corr_con_obediencia": r_propia.get("tabla", {}),
            "corr_con_ruido": round(c_ruido, 3)}


def regla31(verbose=True):
    """LOS DOS LADOS de la vara del torneo, mas el señuelo que ya nos costo un estudio entero.

    El precedente no es hipotetico: la primera vuelta de este mismo torneo (prereg-27) quedo NO
    CONCLUYENTE porque la vara daba 0.0000 EXACTO a los cuatro competidores. Estos casos existen
    para que eso se cace ANTES de gastar cinco semillas, no despues.
    """
    fallos = []

    def caso(nombre, ok, extra=""):
        print(f"  {'ok  ' if ok else 'FALLO'} {nombre} {extra}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 de la VARA del torneo (no de los competidores) ==")

    # LADO NEGATIVO — latentes de puro ruido: no obedecen a nadie. La lectura debe quedar ~0.
    com, lat_ruido = _latentes_sinteticos(senal=0.0, ruido=1.0, semilla=3)
    p_vacio = float(pj.lectura_contingencia(lat_ruido, com, jueces=[1, 2, 3], nulos=4)["puntaje"])
    caso("con latentes de PURO RUIDO la contingencia no despega", abs(p_vacio) < 0.05,
         f"puntaje {p_vacio:+.5f}")

    # LADO POSITIVO — latentes que siguen a los comandos: la lectura DEBE verlo.
    com2, lat_buenos = _latentes_sinteticos(senal=1.5, ruido=0.1, semilla=4)
    p_lleno = float(pj.lectura_contingencia(lat_buenos, com2, jueces=[1, 2, 3], nulos=4)["puntaje"])
    caso("con latentes que SI obedecen, la contingencia lo ve", p_lleno > 0.05,
         f"puntaje {p_lleno:+.5f}")

    # DISCRIMINA — y esto es lo que fallo en la primera vuelta.
    caso("la vara SEPARA el lleno del vacio (no aplasta a todos en el mismo numero)",
         (p_lleno - p_vacio) > 0.05, f"separacion {p_lleno - p_vacio:+.5f}")

    # SIN SUELO — el defecto exacto del prereg-27: un max(x, 0) que convierte todo en 0.0000.
    peores = [float(pj.lectura_contingencia(l, c, jueces=[1, 2, 3], nulos=4)["puntaje"])
              for l, c in ((lat_ruido, com), (_latentes_sinteticos(senal=0.0, ruido=2.0,
                                                                   semilla=9)[1], com))]
    caso("la vara NO tiene suelo: dos mundos vacios distintos no dan el MISMO numero exacto",
         len(set(round(x, 6) for x in peores)) > 1 or all(x != 0.0 for x in peores),
         f"{[round(x, 6) for x in peores]}")

    # LA TUBERIA ENTERA, NO SOLO LA VARA. Este caso nace de un fallo real del 10-ago: el torneo
    # paso la puerta 7/7 y aun asi REVENTO en la primera semilla — `corromper()` convertia los
    # videos a float64 y los codificadores son float32, asi que la lectura de ROBUSTEZ nunca se
    # habia podido correr con video de verdad. Mi Regla 31 examinaba la vara sobre latentes
    # sinteticos y no tocaba la cadena. LECCION: el sello certifica el modulo, no la tuberia en la
    # que vive — asi que la tuberia se prueba aparte, barata, antes de gastar cinco semillas.
    import numpy as _np
    _v32 = [_np.zeros((6, 16, 16), dtype=_np.float32)]
    _c = pj.corromper(_v32)
    caso("corromper() CONSERVA el tipo del video (float32 sigue siendo float32)",
         _c[0].dtype == _np.float32, str(_c[0].dtype))

    # EL VEREDICTO NO PUEDE CORONAR SIN EVIDENCIA: cuatro competidores identicos deben EMPATAR.
    iguales = [{"nombre": n, "puntajes": {"contingencia": 0.3, "flecha": 0.2, "robustez": 0.1}}
               for n in COMPETIDORES]
    v = pj.veredicto(iguales)
    caso("cuatro competidores IDENTICOS no coronan a nadie por evidencia",
         "EMPATE" in v["fallo"], v["fallo"][:60])

    if verbose:
        print("REGLA 31: " + ("APRUEBA" if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def codificar_competidor(nombre, videos, jidx, epocas, semilla, comandos=None):
    if nombre == "A-pixel":
        m = entrenar_ojos(videos, jidx, latente=8, epocas=epocas, semilla=semilla)
        return p2.codificar(m, videos, jidx)
    if nombre == "B-predictivo":
        m = p2.entrenar(videos, jidx, latente=8, epocas=epocas, semilla=semilla)
        return p2.codificar(m, videos, jidx)
    if nombre == "C-corolario":
        m = p2.entrenar(videos, jidx, latente=8, epocas=epocas, semilla=semilla, comandos=comandos)
        return p2.codificar(m, videos, jidx)
    if nombre == "R-ranuras":
        m = rn.entrenar(videos, jidx, k_ranuras=4, epocas=epocas, semilla=semilla)
        return rn.codificar(m, videos, jidx)
    raise ValueError(nombre)


def una_semilla_panel(semilla, episodios, pasos, epocas, jueces):
    """SEGUNDA VUELTA (prereg-38). Misma competencia, OTRA VARA.

    La primera vuelta quedo NO CONCLUYENTE POR INSTRUMENTO (INFORME-38): la aptitud del prereg-27
    aplastaba a los cuatro competidores en 0.0000 EXACTO porque el `max(margen, 0)` es un suelo, y
    el margen mismo satura en -0.4000 cuando ningun latente alcanza el piso de contingencia. La
    vara no medía a los competidores: medía su propio suelo.

    El panel del prereg-31 no tiene suelo, y mira TRES cosas distintas en vez de una: contingencia
    (¿sirven para hallar el cuerpo?), flecha (¿llevan dentro el sentido del tiempo?) y robustez
    (¿cuanto sobrevive al mundo mal visto?). Un competidor gana solo si gana o empata en LAS TRES.
    """
    jidx = {j - 1 for j in jueces}
    eps, verdad, videos = correr(episodios, pasos, "normal", render=True,
                                 semilla0=1000 + 5000 * semilla)
    comandos = [c for c, _ in eps]
    filas = []
    for nombre in COMPETIDORES:
        def _cod(vs, _n=nombre):
            return codificar_competidor(_n, vs, jidx, epocas, semilla, comandos)
        r = pj.evaluar(nombre, _cod, videos, comandos, jueces, nulos=8)
        filas.append(r)
        print(f"  [{nombre}] semilla {semilla}: contingencia {r['puntajes']['contingencia']:+.5f}  "
              f"flecha {r['puntajes']['flecha']:+.5f}  robustez {r['puntajes']['robustez']:+.5f}",
              flush=True)
    return filas


def una_semilla(semilla, episodios, pasos, epocas, jueces):
    jidx = {j - 1 for j in jueces}
    eps, verdad, videos = correr(episodios, pasos, "normal", render=True, semilla0=1000 + 5000 * semilla)
    comandos = [c for c, _ in eps]
    fila = {}
    for nombre in COMPETIDORES:
        lat = codificar_competidor(nombre, videos, jidx, epocas, semilla, comandos)
        r = aptitud(lat, comandos, jueces, verdad, nulos=8)
        fila[nombre] = r
        print(f"  [{nombre}] semilla {semilla}: puntaje {r['puntaje']:.4f} "
              f"(mías {r['n_mias']}, margen {r['margen_medio']:.4f})", flush=True)
    return fila


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodios", type=int, default=12)
    ap.add_argument("--pasos", type=int, default=1500)
    ap.add_argument("--epocas", type=int, default=12)
    ap.add_argument("--semilla", type=int, default=None,
                    help="si se da, corre SOLO esta semilla (para encolar por partes en el latido)")
    ap.add_argument("--semillas", type=int, default=5,
                    help="usado solo si --semilla no se da: cuenta semillas 1..N en una sola corrida")
    ap.add_argument("--jueces", nargs="+", type=int, default=[10, 11, 12])
    ap.add_argument("--panel", action="store_true",
                    help="prereg-38: SEGUNDA VUELTA con el panel de tres lecturas del prereg-31, "
                         "en lugar de la aptitud del prereg-27 que quedo no concluyente por "
                         "instrumento (INFORME-38). La vara vieja NO se toca.")
    a = ap.parse_args()

    rango = [a.semilla] if a.semilla is not None else list(range(1, a.semillas + 1))

    if a.panel:
        if a.semilla is None:
            raise SystemExit("la segunda vuelta se encola semilla por semilla: usa --semilla N")
        filas = una_semilla_panel(a.semilla, a.episodios, a.pasos, a.epocas, a.jueces)
        out = os.path.join(BASE, "resultados", f"p38-torneo-panel-s{a.semilla}")
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
            json.dump({"prerregistro": 38, "semilla": a.semilla, "episodios": a.episodios,
                       "pasos": a.pasos, "epocas": a.epocas, "lecturas": list(pj.LECTURAS),
                       "resultados": filas,
                       "nota": "SIN veredicto: el veredicto exige las 5 semillas juntas, y mirarlas "
                               "antes de tiempo es exactamente el vicio que el prereg-27 cazo"},
                      f, indent=2, ensure_ascii=False)
        print(f"guardado en {out}/resumen.json (parcial — el veredicto se calcula con las 5)")
        return
    print(f"=== TORNEO DE OJOS (prereg-27) — semillas {rango} x "
          f"{a.episodios} ep x {a.pasos} cuadros ===", flush=True)
    por_semilla = []
    for s in rango:
        print(f"\n--- semilla {s} ---", flush=True)
        por_semilla.append(una_semilla(s, a.episodios, a.pasos, a.epocas, a.jueces))

    if a.semilla is not None:
        # UNA SOLA SEMILLA: se guarda sin veredicto (el veredicto exige verlas todas juntas,
        # y verlas juntas antes de tiempo seria exactamente el vicio que cazamos toda la semana).
        out = os.path.join(BASE, "resultados", f"p27-torneo-ojos-s{a.semilla}")
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
            json.dump({"prerregistro": 27, "semilla": a.semilla, "episodios": a.episodios,
                       "pasos": a.pasos, "epocas": a.epocas, "resultados": por_semilla[0]},
                      f, indent=2, ensure_ascii=False)
        print(f"guardado en {out}/resumen.json (parcial — el veredicto se calcula con las 5)")
        return

    variantes = []
    for nombre in COMPETIDORES:
        puntajes = [f[nombre]["puntaje"] for f in por_semilla]
        variantes.append({"nombre": nombre, "puntaje": float(np.mean(puntajes)),
                          "puntaje_desv": float(np.std(puntajes)),
                          "puntajes_por_semilla": puntajes})

    veredicto = torneo(variantes, empate=0.0)  # el margen real lo aplica el criterio del prereg-27
    p1 = sorted(variantes, key=lambda v: -v["puntaje"])
    p_star, p_2 = p1[0], p1[1]
    separado = (p_star["puntaje"] - p_2["puntaje"]) > (p_star["puntaje_desv"] + p_2["puntaje_desv"])
    if p_star["puntaje"] <= 0:
        fallo = "NINGUNO SIRVE — ni el mejor supera 0 con margen"
    elif separado:
        fallo = f"GANA {p_star['nombre']} — separación real"
    else:
        orden_parsimonia = {"A-pixel": 0, "B-predictivo": 1, "C-corolario": 2, "R-ranuras": 3}
        empatados = [v for v in p1 if v["puntaje"] > 0
                    and p_star["puntaje"] - v["puntaje"] <= p_star["puntaje_desv"] + v["puntaje_desv"]]
        ganador_navaja = min(empatados, key=lambda v: orden_parsimonia[v["nombre"]])
        fallo = f"EMPATE TÉCNICO — gana {ganador_navaja['nombre']} por parsimonia (navaja, no evidencia)"

    print("\n" + "=" * 70)
    print("TABLA FINAL (media ± desviación entre semillas):")
    for v in sorted(variantes, key=lambda x: -x["puntaje"]):
        print(f"  {v['nombre']:<14} {v['puntaje']:+.4f} ± {v['puntaje_desv']:.4f}   "
              f"{v['puntajes_por_semilla']}")
    print(f"\nVEREDICTO DEL PRERREG-27: {fallo}")
    print("=" * 70)

    out = os.path.join(BASE, "resultados", "p27-torneo-ojos")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump({"prerregistro": 27, "semillas": a.semillas, "episodios": a.episodios,
                   "pasos": a.pasos, "epocas": a.epocas, "variantes": variantes,
                   "veredicto_estadio": veredicto, "veredicto_prereg27": fallo},
                  f, indent=2, ensure_ascii=False)
    print(f"guardado en {out}/resumen.json")


if __name__ == "__main__":
    main()
