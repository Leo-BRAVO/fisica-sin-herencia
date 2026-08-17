# politica_contacto.py — LA POLITICA QUE BUSCA EL CONTACTO (prerregistro-60, 17-ago-2026).
#
# EL HUECO: el INFORME-57 concluyo que el tacto FUNCIONA y esta OCIOSO — se enciende si el brazo
# barre a proposito. Pero ESE BARRIDO LO ESCRIBI YO A MANO: la condicion `busca` de tacto.py es un
# balbuceo programado por mi. Diego no busca nada; yo le muevo el brazo.
#
# LA PREGUNTA: en un mundo donde empujar solo funciona si la mano esta CERCA del objeto, ¿una
# politica movida UNICAMENTE por su propio error de prediccion termina buscando el contacto por su
# cuenta, o el contacto solo aparece si se lo ordenamos?
#
# LA TRAMPA QUE ESTE MODULO EXISTE PARA NO PISAR (Regla 27): la recompensa NO PUEDE decir "toca
# cosas". Si le pagaramos por tocar, el contacto apareceria por construccion y no habriamos medido
# nada. El unico termino admisible es `error_de_prediccion_propio`, y lo comprueba a maquina el
# guardian_de_recompensa de mundo.py.
#
#     EL CONTACTO ES LO QUE MEDIMOS, NUNCA LO QUE PAGAMOS.
#
# La distancia mano-objeto es VERDAD DEL SIMULADOR: juzga desde fuera y no entra jamas en lo que
# Diego recibe. Es el mismo trato que tacto.py le da a la verdad del simulador.
#
# QUE SE IMPORTA Y NO SE COPIA: de `mundo.py` —sellado— vienen el ALCANCE medido del cuerpo y los
# DOS guardianes de la Regla 27. Copiarlos habria creado una segunda verdad que se desincroniza.
#
# Uso: python politica_contacto.py [--regla31] [--salida resultados/p60-politica-contacto/medida.json]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

import mundo                                                                # noqa: E402

# QUE ESTUDIA ESTE MODULO: la politica intrinseca. Por eso su regla31() NO la llama — trabaja con
# el balbuceo y con una politica recta escrita a mano, que son andamios mios. Examinar al sujeto
# dentro de mi propia Regla 31 es el error que dejo NULO al prerregistro-45.
SUJETO = ("POLITICA",)

# ------------------------------------------------------------------ EL PRERREGISTRO, EN CODIGO
SEMILLAS = (1, 2, 3, 4, 5)
# PASOS sale de un calculo, y el calculo estaba MAL la primera vez (ENMIENDA 1). Un paseo de paso
# 0.03 tarda tau ~ (0.88/0.03)^2 ~ 860 pasos en RECORRER la caja, pero recorrerla no es
# MUESTREARLA: en N pasos hay N/tau muestras independientes, y para que la frecuencia de una region
# del 4% se parezca a su valor asintotico hacen falta muchas decenas de muestras independientes.
# N ~ 25*tau ~ 21000. Medido en el banco: a 3000 pasos sale 0.0008 y a 20000 sale 0.0198.
PASOS = 20000
CANDIDATOS = 16            # las tres politicas sortean del MISMO saco; solo cambia como eligen
MODELOS = 5                # cuantos modelos propios se contradicen entre si
RADIO = 0.12               # a que distancia el empuje transfiere
PASO_MANO = 0.03
MINIMAS_A_FAVOR = 4        # de 5 semillas
# ENMIENDA 1: la razon de volumenes se PUBLICA como numero informativo y ya NO tiene poder de veto.
# Ataba la validez del estudio a una prediccion ASINTOTICA que una corrida finita no tiene por que
# cumplir, y ademas no validaba nada: el balbuceo es ciego POR CONSTRUCCION —nunca mira la
# observacion— y el criterio C no depende de la geometria para nada. En su lugar entra EL MUNDO
# SORDO, que es mas duro y puede tumbar el resultado aunque salga a mi favor.

METODO = {
    "prerregistro": 60,
    "tipo_de_medida": "mixta",   # la fraccion es continua; el criterio cuenta semillas por umbral
    "que_mide": ("que fraccion de los pasos acaba con la mano dentro del radio de contacto del "
                 "objeto, para tres politicas que sortean los mismos candidatos y solo se "
                 "diferencian en la REGLA DE ELECCION"),
    "comparten_datos": {
        "hay": False,
        "porque": "cada semilla corre su propio mundo y su propia politica de principio a fin; "
                  "nada se reutiliza entre semillas ni entre politicas",
    },
    "linea_base": ("el balbuceo: elegir al azar entre los mismos candidatos. Y su valor esperado "
                   "es CALCULABLE de antemano —la razon entre el volumen de la esfera de contacto "
                   "y el volumen de la caja del ALCANCE—, asi que la linea base no la elijo yo: "
                   "sale de la geometria del problema. El error nº21 fue poner mi propia "
                   "suposicion en el papel de rival"),
    "formulas": [
        {"base": {"radio": 0.05}, "parametro": "radio", "factor": 3.0, "esperado": "sube",
         "porque": "el volumen tocable crece con el CUBO del radio, asi que una mano que se pasea "
                   "sin rumbo cae dentro mas a menudo. Es geometria y se sabe A PRIORI, no "
                   "intuicion. Base 0.05 y NO 0.0: multiplicar cero por tres sigue siendo cero, y "
                   "ese descuido ya me tumbo cuatro relaciones este mes"},
    ],
}

# LO QUE DIEGO RECIBE. Se declara aqui, arriba y a la vista, para que el guardian lo lea.
TERMINOS_DE_LA_SEÑAL = ("error_de_prediccion_propio",)


# ------------------------------------------------------------------------------------ el mundo
class MundoConMano:
    """El mundo de `mundo.py` con LO UNICO QUE CAMBIA: una mano que la accion mueve, y un objeto
    que solo recibe el empuje si la mano esta dentro del radio.

    En `mundo.Mundo` la accion empuja el objeto DESDE CUALQUIER SITIO: alli no hay contacto que
    buscar, porque tocar y no tocar dan lo mismo. Esa es la razon entera de este mundo."""

    def __init__(self, semilla=1, radio=RADIO, sordo=False):
        rng = np.random.default_rng(int(semilla))
        self.radio = float(radio)
        # EL MUNDO SORDO (ENMIENDA 1): el contacto ocurre y NO HACE NADA. Alli el contacto no lleva
        # informacion, asi que una politica movida por su propio error de prediccion NO DEBE
        # buscarlo. Es el control que puede anular el criterio C aunque salga a mi favor.
        self.sordo = bool(sordo)
        self.obj = np.array([rng.uniform(*mundo.ALCANCE[e]) for e in ("x", "y", "z")])
        self.mano = np.array([rng.uniform(*mundo.ALCANCE[e]) for e in ("x", "y", "z")])
        self.vel = np.zeros(3)
        self._roce = 0.92

    def _dentro(self, p):
        for i, eje in enumerate(("x", "y", "z")):
            lo, hi = mundo.ALCANCE[eje]
            p[i] = min(max(p[i], lo), hi)
        return p

    def hay_contacto(self):
        """VERDAD DEL SIMULADOR. Juzga desde fuera; NO entra en lo que Diego observa ni recibe."""
        return bool(np.linalg.norm(self.mano - self.obj) < self.radio)

    def paso(self, accion):
        a = np.asarray(accion, dtype=float)[:3]
        self.mano = self._dentro(self.mano + a * PASO_MANO)
        if self.hay_contacto() and not self.sordo:
            self.vel = self.vel * self._roce + a * 0.02
        else:
            self.vel = self.vel * self._roce
        self.obj = self._dentro(self.obj + self.vel * 0.02)
        return self.observar()

    def observar(self):
        """LO QUE DIEGO VE: nueve numeros SIN NOMBRE Y SIN UNIDAD. Que tres sean una mano, tres un
        objeto y tres una velocidad es asunto NUESTRO."""
        return np.concatenate([self.mano, self.obj, self.vel]).astype(float)


# --------------------------------------------------------------------------------- los modelos
_PARES = None


def _expandir(V):
    """LA BASE DE LOS MODELOS: los doce numeros crudos, TODOS sus productos de dos en dos, y un uno.

    POR QUE CUADRATICA Y NO LINEAL, y es una decision con consecuencia: en este mundo el empuje
    solo transfiere cuando la mano esta cerca, y ESO UN MODELO LINEAL NO PUEDE REPRESENTARLO NI
    AUNQUE TOQUE MIL VECES. Con una base lineal, la politica intrinseca no podria descubrir el
    contacto AUNQUE QUISIERA, y el estudio habria estado amañado en su contra desde la primera
    linea.

    POR QUE TODOS LOS PRODUCTOS Y NO 'la distancia mano-objeto': meterle la distancia seria
    DECIRLE cual es la variable que importa. Una expansion polinomica completa es generica —no
    señala nada— y deja que la dependencia sea representable sin nombrarsela. La diferencia entre
    dar una BASE y dar una PISTA es justo lo que la Regla 27 protege."""
    global _PARES
    V = np.atleast_2d(V)
    if _PARES is None or _PARES[0] != V.shape[1]:
        i, j = np.triu_indices(V.shape[1])
        _PARES = (V.shape[1], i, j)
    _, i, j = _PARES
    return np.hstack([V, V[:, i] * V[:, j], np.ones((len(V), 1))])


def _ajustar(S, Y, rng, cuantos=MODELOS):
    """CUANTOS modelos propios, cada uno sobre un remuestreo distinto de la experiencia. Que se
    contradigan entre si es la unica señal que mueve a la politica intrinseca."""
    A = _expandir(S)
    n = len(A)
    return [np.linalg.lstsq(A[idx], Y[idx], rcond=None)[0]
            for idx in (rng.integers(0, n, n) for _ in range(cuantos))]


def _desacuerdo(modelos, entradas):
    """CUANTO SE CONTRADICEN los modelos propios sobre lo que va a pasar, para cada candidato de
    golpe. Sin verdad de nadie: solo Diego contra Diego."""
    E = _expandir(entradas)
    pred = np.stack([E @ W for W in modelos])
    return pred.var(axis=0).sum(axis=1)


# ------------------------------------------------------------------------------ las politicas
def _candidatos(rng, k=CANDIDATOS):
    a = rng.normal(size=(k, 3))
    return a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-9)


def corrida(semilla, politica="balbuceo", pasos=PASOS, radio=RADIO, sordo=False):
    """Una vida entera. Las tres politicas sortean los MISMOS candidatos; solo cambia como eligen.

    Comparar dos politicas con espacios de accion distintos habria sido comparar dos cosas."""
    rng = np.random.default_rng(int(semilla))
    m = MundoConMano(semilla=semilla, radio=radio, sordo=sordo)
    S, Y, tocados = [], [], 0
    modelos = None
    for t in range(pasos):
        # el estado vive en el mundo, no en una variable de esta funcion: asi `obs` se asigna en un
        # solo sitio y no hay forma de confundir el arrastre de estado con un pisoton
        obs = m.observar()
        cand = _candidatos(rng)
        if politica == "balbuceo" or modelos is None:
            elegida = cand[rng.integers(0, len(cand))]
        else:
            puntajes = _desacuerdo(modelos, np.hstack([np.tile(obs, (len(cand), 1)), cand]))
            if politica == "barajada":
                puntajes = rng.permutation(puntajes)     # misma forma, cero informacion
            elegida = cand[int(np.argmax(puntajes))]
        nueva = m.paso(elegida)
        S.append(np.concatenate([obs, elegida]))
        Y.append(nueva - obs)
        tocados += int(m.hay_contacto())
        if politica != "balbuceo" and t >= 40 and t % 20 == 0:
            modelos = _ajustar(np.array(S[-400:]), np.array(Y[-400:]), rng)
    return {"fraccion_de_contacto": tocados / float(pasos), "pasos": int(pasos)}


def _politica_recta(semilla, pasos=300, radio=RADIO):
    """CONTROL POSITIVO, escrito a mano: la mano va derecha al objeto. Si NI ESTA marca contacto,
    el medidor esta roto y nada de lo demas vale. No es una politica que se estudie: es el patron
    con el que se comprueba el METRO."""
    m = MundoConMano(semilla=semilla, radio=radio)
    tocados = 0
    for _ in range(pasos):
        d = m.obj - m.mano
        n = np.linalg.norm(d)
        m.paso(d / n if n > 1e-9 else np.zeros(3))
        tocados += int(m.hay_contacto())
    return tocados / float(pasos)


def razon_de_volumenes(radio=RADIO):
    """LO QUE LA GEOMETRIA PREDICE PARA UNA MANO CIEGA: la esfera de contacto sobre la caja del
    ALCANCE. Este numero NO LO ELIJO YO — sale del problema."""
    caja = 1.0
    for eje in ("x", "y", "z"):
        lo, hi = mundo.ALCANCE[eje]
        caja *= (hi - lo)
    return float((4.0 / 3.0) * np.pi * radio ** 3 / caja)


# ---------------------------------------------------------------- la ficha y las autopruebas
def _metodo_medir(radio=0.05):
    """La medida que la relacion metamorfica mueve: contacto de una mano SIN RUMBO.

    TRES SEMILLAS Y PASOS LARGOS POR RESOLUCION, no por conveniencia: con 300 pasos la medida daba
    0.0000 en los dos extremos y la relacion 'sube' era indecidible. Una relacion que no se puede
    decidir por falta de muestra no es una relacion falsa: es una medida sin resolucion, y lo que
    se arregla es la medida. Con 3000 pasos seguia dando 0.0000 en los dos extremos; la resolucion
    la fija el mismo calculo que fija PASOS, asi que se usa PASOS."""
    return float(np.mean([corrida(s, politica="balbuceo", pasos=PASOS, radio=radio)
                          ["fraccion_de_contacto"] for s in (1, 2, 3)]))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el medidor de contacto mide contacto, o mide cualquier
    cosa?** Se comprueba por los dos lados: con radio de verdad tiene que encenderse para una mano
    que va derecha, y con radio cero tiene que dar exactamente cero para todas."""
    fallos = []
    if _politica_recta(1, pasos=200) <= 0.0:
        fallos.append("la politica que va DERECHA al objeto no marca contacto: el medidor no mide")
    if _politica_recta(1, pasos=200, radio=0.0) != 0.0:
        fallos.append("con radio 0 el medidor marca contacto: se lo esta inventando")
    if corrida(1, politica="balbuceo", pasos=200, radio=0.0)["fraccion_de_contacto"] != 0.0:
        fallos.append("con radio 0 el balbuceo marca contacto: se lo esta inventando")
    if not SEMILLAS:
        fallos.append("no hay ni una semilla que correr: el estudio aprobaria sobre nada")
    if not TERMINOS_DE_LA_SEÑAL:
        fallos.append("la señal no declara terminos: no se puede auditar de que depende")
    return {"aprueba": not fallos, "fallos": fallos,
            "razon_de_volumenes": razon_de_volumenes(), "semillas": len(SEMILLAS)}


def regla31(verbose=True):
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok   ' if ok else 'FALLO'} {nombre}{('  -> ' + extra) if extra else ''}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("REGLA 31 de politica_contacto — sobre MI PROCEDIMIENTO, sin tocar al sujeto\n")

    recta = _politica_recta(1, pasos=300)
    caso("control positivo: la mano que va derecha al objeto marca contacto alto",
         recta > 0.5, f"{recta:.3f}")

    caso("señuelo: con radio 0 la mano derecha no marca NADA",
         _politica_recta(1, pasos=200, radio=0.0) == 0.0)
    caso("señuelo: con radio 0 el balbuceo tampoco marca NADA",
         corrida(1, politica="balbuceo", pasos=200, radio=0.0)["fraccion_de_contacto"] == 0.0)

    f = METODO["formulas"][0]
    base = f["base"]["radio"]
    antes, despues = _metodo_medir(base), _metodo_medir(base * f["factor"])
    caso(f"metamorfica: mas radio = mas contacto (base {base}, x{f['factor']})",
         despues > antes, f"{antes:.4f} -> {despues:.4f}")

    caso("el cortafuegos: la señal declarada pasa el guardian de recompensa",
         mundo.guardian_de_recompensa(list(TERMINOS_DE_LA_SEÑAL)) == [])
    caso("el cortafuegos: una señal que pagara por tocar SERIA RECHAZADA",
         len(mundo.guardian_de_recompensa(["error_de_prediccion_propio", "hubo_contacto"])) == 1)

    con_nombres = {f"c{i}": 0.0 for i in range(9)}
    caso("el cortafuegos: la observacion no lleva etiquetas humanas",
         mundo.guardian_de_etiquetas(con_nombres) == [])

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el medidor mide contacto y no se lo inventa"
                                if not fallos else f"REPRUEBA en {len(fallos)}: {fallos}"))
    return 0 if not fallos else 1


# ------------------------------------------------------------------------------- la corrida
def correr(salida=None, verbose=True):
    geo = razon_de_volumenes()
    filas = []
    for s in SEMILLAS:
        fila = {"semilla": int(s)}
        for p in ("balbuceo", "intrinseca", "barajada"):
            fila[p] = corrida(s, politica=p)["fraccion_de_contacto"]
        filas.append(fila)
        if verbose:
            print(f"  semilla {s}: balbuceo {fila['balbuceo']:.4f} · intrinseca "
                  f"{fila['intrinseca']:.4f} · barajada {fila['barajada']:.4f}")

    med_balbuceo = float(np.median([f["balbuceo"] for f in filas]))
    gana_intrinseca = sum(1 for f in filas if f["intrinseca"] > f["balbuceo"])
    gana_barajada = sum(1 for f in filas if f["barajada"] > f["balbuceo"])
    # EL MUNDO SORDO (criterio B de la ENMIENDA 1): el contacto ocurre y no hace nada. Alli no
    # lleva informacion, asi que la intrinseca NO DEBE buscarlo mas que el balbuceo.
    sordas = [{"semilla": int(s),
               "balbuceo": corrida(s, "balbuceo", sordo=True)["fraccion_de_contacto"],
               "intrinseca": corrida(s, "intrinseca", sordo=True)["fraccion_de_contacto"]}
              for s in SEMILLAS]
    gana_sorda = sum(1 for f in sordas if f["intrinseca"] > f["balbuceo"])

    a = (mundo.guardian_de_recompensa(list(TERMINOS_DE_LA_SEÑAL)) == []
         and mundo.guardian_de_etiquetas({f"c{i}": 0.0 for i in range(9)}) == [])
    e = all(corrida(s, politica=p, pasos=150, radio=0.0)["fraccion_de_contacto"] == 0.0
            for s in SEMILLAS[:2] for p in ("balbuceo", "intrinseca", "barajada"))

    datos = {
        "prerregistro": 60,
        "razon_de_volumenes_informativa": geo,
        "mediana_balbuceo": med_balbuceo,
        "desviacion_de_la_geometria": (med_balbuceo / geo) if geo else None,
        "mundo_sordo": sordas,
        "semillas_en_que_gana_la_intrinseca_en_el_mundo_sordo": gana_sorda,
        "semillas_en_que_gana_la_intrinseca": gana_intrinseca,
        "semillas_en_que_gana_la_barajada": gana_barajada,
        "de": len(SEMILLAS),
        "filas": filas,
        "criterios": {
            "A_el_cortafuegos_aguanta": bool(a),
            "B_en_el_mundo_sordo_la_intrinseca_no_busca": bool(gana_sorda < MINIMAS_A_FAVOR),
            "C_la_intrinseca_busca_sola": bool(gana_intrinseca >= MINIMAS_A_FAVOR),
            "D_el_nulo_no_gana": bool(gana_barajada < MINIMAS_A_FAVOR),
            "E_no_se_puede_inventar_contacto": bool(e),
        },
    }
    c = datos["criterios"]
    if not c["A_el_cortafuegos_aguanta"]:
        datos["veredicto"] = ("SE DESCARTA EL ESTUDIO — el cortafuegos de la Regla 27 tiene una "
                              "fuga, y el fallo es NUESTRO no suyo")
    elif not c["E_no_se_puede_inventar_contacto"]:
        datos["veredicto"] = "SE DESCARTA EL MEDIDOR — marca contacto donde no puede haberlo"
    elif not c["B_en_el_mundo_sordo_la_intrinseca_no_busca"]:
        datos["veredicto"] = ("ANULADO POR EL MUNDO SORDO — la intrinseca tambien se acerca mas "
                              "que el balbuceo donde el contacto NO HACE NADA, asi que lo que "
                              "mide C no es el contacto sino otra cosa")
    elif not c["D_el_nulo_no_gana"]:
        datos["veredicto"] = ("ANULADO POR EL NULO — la politica barajada tambien le gana al "
                              "balbuceo, asi que lo que se mide no es la informacion sino la "
                              "forma de elegir")
    elif c["C_la_intrinseca_busca_sola"]:
        datos["veredicto"] = (f"LA POLITICA BUSCA EL CONTACTO SOLA — le gana al balbuceo en "
                              f"{gana_intrinseca} de {len(SEMILLAS)} semillas sin que nadie le "
                              f"pague por tocar")
    else:
        datos["veredicto"] = (f"LA CURIOSIDAD POR SI SOLA NO PRODUCE BUSQUEDA DE CONTACTO — gana "
                              f"en {gana_intrinseca} de {len(SEMILLAS)} semillas y hacian falta "
                              f"{MINIMAS_A_FAVOR}. El canal tactil sigue ocioso por una razon "
                              f"medida, y el barrido sigue siendo mio")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nmundo sordo: la intrinseca gana en {gana_sorda} de {len(SEMILLAS)}")
        print(f"geometria (informativa, sin veto): {geo:.5f} · mediana del balbuceo: "
              f"{med_balbuceo:.5f}")
        for k, v in c.items():
            print(f"  {'ok   ' if v else 'FALLO'} {k}")
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 60: la politica que busca el contacto")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p60-politica-contacto/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
