# pruebas.py — EL BANCO DE PRUEBAS CONGELADO (exigido por la Regla 30; construido 12-jul-2026).
# Toda modificacion de codigo (humana o por propuesta de la mente) debe pasar este banco
# ANTES del commit. Los casos son sinteticos y FIJOS: no se tocan jamas — solo se agregan.
# Uso: python pruebas.py   (salida: OK total o el detalle del fallo; codigo de salida 0/1)

import os
import sys
import json
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descubrir import preparar, dividir_por_tiempo, error_linea_base, error_rival_lineal, _mse_suma
from autopsia import evaluar, piso_de_ruido
from canonizar import tarjeta

FALLOS = []


def caso(nombre, cond, detalle=""):
    if cond:
        print(f"  ok  {nombre}")
    else:
        print(f"FALLO {nombre} {detalle}")
        FALLOS.append(nombre)


def csv_temporal(contenido):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="")
    f.write(contenido); f.close()
    return f.name


print("== preparar: formas, retardos, suavizado, objetivo crudo ==")
# senal lineal s(t)=2t: cambios constantes=2; con 12 muestras
csv1 = csv_temporal("t,s1\n" + "\n".join(f"{t},{2*t}" for t in range(12)))
X, Y = preparar(csv1)
caso("forma base 1 senal", X.shape[1] == 2 and Y.shape[1] == 1, f"{X.shape}")
caso("cambio correcto", np.allclose(X[:, 1], 2.0))
caso("objetivo = siguiente", np.allclose(Y[:, 0], X[:, 0] + 2.0))
X2, Y2 = preparar(csv1, retardos=2)
caso("retardos agregan columnas", X2.shape[1] == 4, f"{X2.shape}")
caso("retardo-1 correcto", np.allclose(X2[:, 2], X2[:, 0] - 2.0))
X3, Y3 = preparar(csv1, suavizar=3)
caso("suavizado: objetivo sigue CRUDO (lineal exacto)", np.allclose(Y3[:, 0] - (X3[:, 0] + 2.0), 0.0, atol=1e-9),
     "el suavizado toco al objetivo (leccion INF-11 violada)")

print("== varas: base trivial y rival lineal ==")
rng = np.random.default_rng(7)
Xs = rng.normal(size=(200, 4)); Ys = np.column_stack([Xs[:, 0] + Xs[:, 2], Xs[:, 1] + Xs[:, 3]])
caso("base velocidad exacta cuando el mundo ES velocidad",
     error_linea_base(Xs, Ys) < 1e-20)
caso("rival lineal aprende el mapa lineal",
     error_rival_lineal(Xs[:100], Ys[:100], Xs[100:], Ys[100:]) < 1e-10)
caso("_mse_suma = suma por senal",
     abs(_mse_suma(np.zeros((5, 2)), np.ones((5, 2))) - 2.0) < 1e-12)

print("== autopsia: piso de ruido y evaluar ==")
ruido = rng.normal(0, 3.0, size=5000)
piso = piso_de_ruido(np.cumsum(rng.normal(size=5000)) + ruido)  # camino suave + ruido sigma=3
caso("piso ~ var del ruido (9.0)", 6.0 < piso < 12.5, f"piso={piso:.2f}")
caso("evaluar respeta v-indices", np.allclose(evaluar("v1 + 2*v3", np.array([[1., 0., 5., 0.]])), 11.0))

print("== surrogado IAAFT: la falsificacion perfecta ==")
from descubrir import _iaaft
rng2 = np.random.default_rng(3)
# senales de banda ancha (camino aleatorio suavizado) acopladas — caso realista;
# con ondas puras monocromaticas la decorrelacion por fases es debil por naturaleza
s1 = np.convolve(rng2.normal(size=2100), np.ones(8) / 8, mode="valid")[:2000]
s2 = 0.8 * np.roll(s1, 3) + 0.1 * rng2.normal(size=2000)  # acoplada a s1
f1 = _iaaft(s1, rng2)
esp_o = np.abs(np.fft.rfft(s1)); esp_f = np.abs(np.fft.rfft(f1))
caso("surrogado conserva el espectro",
     np.corrcoef(esp_o, esp_f)[0, 1] > 0.99, f"corr={np.corrcoef(esp_o, esp_f)[0,1]:.3f}")
caso("surrogado conserva la distribucion", np.allclose(np.sort(f1), np.sort(s1)))
f2 = _iaaft(s2, rng2)
c_orig = abs(np.corrcoef(s1, s2)[0, 1]); c_surr = abs(np.corrcoef(f1, f2)[0, 1])
caso("surrogado DESTRUYE el acople entre senales",
     c_surr < c_orig * 0.35, f"original={c_orig:.2f} surrogado={c_surr:.2f}")

print("== REGLA 31 (agregado 8-ago-2026): el criterio completo A+B de conservada ==")
# Caso congelado: replicas de ruido SUAVIZADO e independientes (nada conservado, nada
# compartido). Con el nulo viejo (barajado) el criterio completo de los prerregistros
# 16-17 ACEPTABA este mundo vacio (score 0.0004 y jueces < 0.2 — habria parido un nodo).
# Con surrogado (IAAFT) los JUECES lo rechazan. Leccion tallada aqui: en senales no
# estacionarias el score de entrenamiento (nivel A) puede sobreajustar; el verdugo
# decisivo es el nivel B con nulo surrogado.
import tempfile as _tmp, shutil as _sh
from regla31_conservada import mundo_vacio as _mv, mundo_lleno as _ml, \
    escribir_replicas as _er, correr_mundo as _cm
# Parametros IDENTICOS a la corrida oficial de regla31_conservada.py (6 replicas, T=600,
# 20 corridas nulas): miniaturizarlo hace trampas — con 2 replicas de entrenamiento y senos
# monocromaticos, el surrogado conserva una combinacion por accidente (leccion documentada).
_dir31 = _tmp.mkdtemp(prefix="p31_")
_csvs_v = _er(os.path.join(_dir31, "v"), _mv(np.random.default_rng(12345)))
_csvs_l = _er(os.path.join(_dir31, "l"), _ml(np.random.default_rng(54321)))
_sv, _nv, _jv = _cm(_csvs_v, "surrogado", 20)
caso("surrogado: el mundo vacio NO pare nodo",
     not (_nv > 0 and _jv), f"score={_sv:.4g} serias={_nv} jueces={_jv}")
_sb, _nb, _jb = _cm(_csvs_v, "barajado", 20)
caso("barajado daba 5 'serias' en el mundo vacio (defecto historico documentado)",
     _nb > 0, f"score={_sb:.4g} serias={_nb}")
_sl, _nl, _jl = _cm(_csvs_l, "surrogado", 20)
caso("surrogado: el mundo lleno SI pare nodo (s1^2+s2^2 encontrada)",
     _nl > 0 and _jl, f"score={_sl:.4g} serias={_nl} jueces={_jl}")
_sh.rmtree(_dir31, ignore_errors=True)

print("== GEN G2 (curiosidad2, metrica 18b FIRMADA): aburrimiento, frescura, records limpios ==")
# NOTA DE GOBERNANZA: estos casos REEMPLAZAN a los del prereg-18 original (8-ago-2026) porque
# prueban la metrica: la 18a fracaso su backtest (INFORME-21) y la 18b fue firmada por el
# director. El ESPIRITU del caso (Regla 31 del gen: sin progreso -> aburrimiento; jamas
# interes inventado) es identico y queda congelado aqui.
from curiosidad2 import prioridades as _prio, UMBRAL as _umb, H as _H
_prefijos = ["oficial-trial1", "peldano2-pendulo46", "dp-morpheus", "p13-latente",
             "caida-libre", "conservadas-x"]
# memoria plana LARGA: dos pasadas por todas las regiones con el MISMO g — los records de
# todas quedan viejos (mas alla del horizonte H) y nada progresa.
_mem_plana = [{"campana": p, "lo_trivial": 4.0, "mi_mejor_esfuerzo": 1.0}
              for _v in range(3) for p in _prefijos]
_pp = _prio(_mem_plana)
caso("memoria sin progreso -> aburrimiento universal (todas <= umbral)",
     all(p <= _umb for p in _pp.values()), f"{_pp}")
_mem_viva = list(_mem_plana) + [{"campana": "oficial-trial1", "lo_trivial": 4.0, "mi_mejor_esfuerzo": 0.25}]
_pv = _prio(_mem_viva)
caso("record que mejora -> progreso positivo SOLO en su region",
     _pv["mendeley"] > _umb and all(_pv[r] <= _umb for r in _pv if r != "mendeley"), f"{_pv}")
# frescura: un record ganado hace mas de H eventos ya no cuenta como progreso
_mem_rancia = list(_mem_viva) + [{"campana": p, "lo_trivial": 4.0, "mi_mejor_esfuerzo": 1.0}
                                 for p in _prefijos[:1] * _H]
_pr = _prio(_mem_rancia)
caso("frescura 18b: el record viejo deja de contar como progreso",
     _pr["mendeley"] <= _umb, f"mendeley={_pr['mendeley']}")
# records limpios: una corrida interna (-inner-) con g gigante NO mueve el record
_mem_inner = list(_mem_plana) + [{"campana": "p14-inner-d4", "lo_trivial": 100.0, "mi_mejor_esfuerzo": 0.001}]
_pi = _prio(_mem_inner)
caso("records limpios 18b: las corridas internas no mueven records",
     _pi["dp-latentes-propios"] <= _umb, f"dp-latentes={_pi['dp-latentes-propios']}")

print("== GEN G10 (interocepcion) + el defecto de Goodhart de G2 ==")
# Regla 31 del gen G10: el coste sentido debe CRECER con el esfuerzo y con el territorio,
# y jamas ser constante (un coste plano es el denominador falso que veniamos arrastrando).
from interocepcion import trabajo_del_motor as _tm
caso("G10: mas semillas -> mas coste", _tm(10, 400, 20) > _tm(5, 400, 20))
caso("G10: mas iteraciones -> mas coste", _tm(5, 800, 20) > _tm(5, 400, 20))
caso("G10: la campana unidad vale 1.0", abs(_tm(5, 400, 20) - 1.0) < 1e-9)
caso("G10: el coste NO es constante (el denominador dejo de ser falso)",
     len({_tm(2, 400, 12), _tm(5, 400, 20), _tm(5, 800, 25)}) == 3)

# EL CANAL DE GOODHART Nº2, demostrado en NUESTROS PROPIOS DATOS (ECUACIONES-COMPARADAS §4.2):
# una region que OLVIDA y REAPRENDE farmea interes para siempre si el progreso se recorta con
# max(0,...). Con progreso CON SIGNO, el ciclo se cancela. Caso congelado: es la razon por la
# que la ecuacion de G2 debe corregirse (prerregistro-20).
def _lp_recortado(serie, H):
    return max(0.0, serie[-1] - (serie[-1 - H] if len(serie) > H else 0.0))
def _lp_con_signo(serie, H):
    return serie[-1] - (serie[-1 - H] if len(serie) > H else 0.0)
_oscila = [0.0, 0.5, 0.9, 0.4, 0.9, 0.4, 0.9]      # aprende, olvida, reaprende...
caso("G2/Goodhart nº2: el recorte max(0,.) PREMIA olvidar-y-reaprender",
     _lp_recortado(_oscila, 1) > 0.4, f"lp={_lp_recortado(_oscila,1):.3f}")
caso("G2/Goodhart nº2: el progreso CON SIGNO cancela el ciclo (sobre la vuelta completa)",
     abs(_lp_con_signo(_oscila, 2)) < 1e-9, f"lp={_lp_con_signo(_oscila,2):.3f}")

print("== GANANCIA HONESTA: el instrumento que separa dinamica de textura ==")
# Nace de convertir un fracaso en medidor (INFORME-27). Casos congelados: debe dar ~0 donde
# solo hay textura y >0 donde hay acople real. Si deja de distinguirlos, no puede opinar
# sobre ninguna representacion y el banco lo grita.
from ganancia_honesta import regla31 as _gh31, reduccion as _red
caso("ganancia honesta: reduccion bien definida", abs(_red(1.0, 0.25) - 0.75) < 1e-12)
caso("ganancia honesta: APRUEBA su Regla 31 (separa textura de dinamica)", _gh31() == 0)
# MEDIDO el 8-ago-2026: un solo sorteo de surrogado varia +-0.015 — reportar uno es elegir el
# que salio. La medicion DEBE traer su desviacion o no es medicion.
import inspect as _insp
from ganancia_honesta import medir as _gm
caso("ganancia honesta: promedia N surrogados (no un solo sorteo)",
     _insp.signature(_gm).parameters["surrogados"].default >= 5)
caso("ganancia honesta: reporta su DESVIACION junto al numero",
     "ganancia_honesta_desv" in _insp.getsource(_gm))
# G10: una sensacion anulada o sin tiempo fiable no puede alimentar decisiones
from interocepcion import coste_de as _cd
caso("G10: sin tiempo fiable, coste_de devuelve None (no inventa)",
     _cd("p14-final") is None)

print("== dimension intrinseca: TwoNN y participacion ==")
from dimension import twonn, participacion
_rngD = np.random.default_rng(4)
# curva 1-D (circulo) embebida en 4 dimensiones: TwoNN debe decir ~1, participacion ~2
_t = _rngD.uniform(0, 2 * np.pi, 800)
_C = np.column_stack([np.cos(_t), np.sin(_t), 0.5 * np.cos(_t), -0.2 * np.sin(_t)])
_d1 = twonn(_C + _rngD.normal(0, 1e-4, _C.shape))
caso("TwoNN ~1 en una curva embebida en 4D", _d1 is not None and 0.7 < _d1 < 1.5, f"d={_d1}")
# nube llena en 3D: TwoNN ~3
_N3 = _rngD.normal(size=(800, 3))
_d3 = twonn(_N3)
caso("TwoNN ~3 en nube llena 3D", _d3 is not None and 2.4 < _d3 < 3.7, f"d={_d3}")
caso("participacion ~3 en nube llena 3D", 2.5 < participacion(_N3) <= 3.05, f"pr={participacion(_N3):.2f}")

print("== LOS DOS CANALES DE MENTIRA DE LA GANANCIA HONESTA (medidos el 8-ago-2026) ==")
# Estos casos NO celebran el instrumento: congelan sus LIMITES, medidos con mundos de verdad
# conocida. Nacen de tres arreglos propuestos que fracasaron uno tras otro (INFORME-30).
import tempfile as _tf, shutil as _sh
from ganancia_honesta import medir as _medir
_tmpd = _tf.mkdtemp(prefix="lim_banco_")
try:
    def _mundo(nombre, reps):
        c = os.path.join(_tmpd, nombre); os.makedirs(c, exist_ok=True)
        for i, (a, b) in enumerate(reps, 1):
            with open(os.path.join(c, f"r{i}.csv"), "w") as f:
                f.write("t,x_px,y_px\n")
                for t_ in range(len(a)):
                    f.write(f"{t_},{a[t_]:.6f},{b[t_]:.6f}\n")
        return c
    _n = 900
    _k9 = np.ones(9) / 9
    _rg = np.random.default_rng(5)
    _t = np.arange(_n)
    # CANAL 1 — FALSO POSITIVO: dos paseos aleatorios INDEPENDIENTES (cero ley) fabrican
    # ganancia honesta porque el IAAFT es circular y destruye la deriva que el real conserva.
    _paseo = [(np.convolve(np.cumsum(_rg.normal(size=_n + 8)), _k9, mode="valid")[:_n],
               np.convolve(np.cumsum(_rg.normal(size=_n + 8)), _k9, mode="valid")[:_n])
              for _ in range(6)]
    _g_falso = _medir(_mundo("paseo", _paseo), [3], surrogados=4, suavizar=3, retardos=2)
    caso("ganancia honesta MIENTE con señales integradas sin ley (canal conocido)",
         _g_falso["ganancia_honesta"] > 0.05,
         f"si este caso se pone rojo el canal se cerro: revisar INFORME-30 (dio {_g_falso['ganancia_honesta']:+.3f})")
    # CANAL 2 — FALSO NEGATIVO: una ley determinista vista con 0.5% de ruido de seguimiento
    # pierde casi toda su ganancia. El instrumento no puede certificar datos de camara real.
    def _osc(ruido):
        r = []
        for j in range(6):
            w = 0.06 + 0.004 * j
            x = 40 * np.cos(w * _t + _rg.uniform(0, 6.3)) + _rg.normal(0, ruido, _n)
            y = 40 * np.sin(1.9 * w * _t + _rg.uniform(0, 6.3)) + _rg.normal(0, ruido, _n)
            r.append((x, y))
        return r
    _limpio = _medir(_mundo("limpio", _osc(0.0)), [3], surrogados=4, suavizar=3, retardos=2)
    _sucio = _medir(_mundo("sucio", _osc(0.4)), [3], surrogados=4, suavizar=3, retardos=2)
    caso("ganancia honesta ve la ley cuando NO hay ruido",
         _limpio["ganancia_honesta"] > 0.10, f"{_limpio['ganancia_honesta']:+.3f}")
    caso("ganancia honesta PIERDE la misma ley con 1% de ruido (canal conocido)",
         _sucio["ganancia_honesta"] < _limpio["ganancia_honesta"] / 2,
         f"limpio {_limpio['ganancia_honesta']:+.3f} vs sucio {_sucio['ganancia_honesta']:+.3f}")
    # LA CONSECUENCIA: los dos canales juntos hacen que (niveles alto, incrementos ~0) sea
    # AMBIGUO — compatible con 'paseo sin ley' Y con 'ley a traves de camara ruidosa'.
    caso("el par (niveles, incrementos) NO desambigua: queda registrado como limite",
         "AMBIGUO" in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "ganancia_honesta.py"), encoding="utf-8").read())
finally:
    _sh.rmtree(_tmpd, ignore_errors=True)

print("== horizonte: retrocompatibilidad exacta ==")
from descubrir import preparar as _prep
_csvh = os.path.join(_tmpd, "x")  # ruta ya borrada: se usa un csv sintetico en memoria
import tempfile as _tf2
_fd = _tf2.mkdtemp(prefix="hz_")
_p = os.path.join(_fd, "a.csv")
with open(_p, "w") as _f:
    _f.write("t,s1,s2\n")
    for _i in range(300):
        _f.write(f"{_i},{np.sin(_i*0.1):.6f},{np.cos(_i*0.07):.6f}\n")
_X1, _Y1 = _prep(_p, suavizar=3, retardos=2)
_X2, _Y2 = _prep(_p, suavizar=3, retardos=2, horizonte=1)
caso("horizonte=1 reproduce EXACTAMENTE el comportamiento historico",
     np.array_equal(_X1, _X2) and np.array_equal(_Y1, _Y2))
_X4, _Y4 = _prep(_p, suavizar=3, retardos=2, horizonte=4)
caso("horizonte=4 predice 4 cuadros al futuro (Y desplazada, no recortada al azar)",
     len(_Y4) == len(_Y1) - 3 and abs(_Y4[0, 0] - _Y1[3, 0]) < 1e-12)
_sh.rmtree(_fd, ignore_errors=True)

print("== contingencia (G4): el detector de la frontera yo/mundo ==")
# Congela las DOS lecciones que costaron una tarde de corridas contra el simulador:
# (1) a un cuadro vista un cuerpo es casi invisible -> el horizonte importa;
# (2) un objeto manipulable TAMBIEN es contingente -> lo que separa es la CONSISTENCIA.
from contingencia import medir as _cmedir, _mundos_regla31 as _cmundos
_cm = _cmundos(n_ep=14, T=1600, semilla=3)
_cjueces = [13, 14]
_sin_ag = _cm["1 SIN AGENCIA (motores desconectados)"][0]
_pos = _cm["2 CONTROL POSITIVO (solo la var 0 obedece)"][0]
_trampa = _cm["4 DERIVA FUERTE, CERO AGENCIA (la trampa del INF-30)"][0]
_r_sin = _cmedir(_sin_ag, _cjueces, nulos=5, horizonte=8, ventana=150)
_r_pos = _cmedir(_pos, _cjueces, nulos=5, horizonte=8, ventana=150)
_r_tra = _cmedir(_trampa, _cjueces, nulos=5, horizonte=8, ventana=150)
caso("contingencia: NO inventa cuerpo donde los motores estan desconectados",
     not any(r["es_mia"] for r in _r_sin),
     str([r["variable"] for r in _r_sin if r["es_mia"]]))
caso("contingencia: encuentra EXACTAMENTE el grado de libertad conectado",
     [r["variable"] for r in _r_pos if r["es_mia"]] == [0],
     str([(r["variable"], r["obedece_en"]) for r in _r_pos]))
caso("contingencia: la deriva fuerte con comandos suaves NO fabrica cuerpo (trampa INF-30)",
     not any(r["es_mia"] for r in _r_tra),
     str([r["variable"] for r in _r_tra if r["es_mia"]]))
caso("contingencia: el nulo es DESPLAZAMIENTO circular, no barajado (regla 31 enmendada)",
     "roll" in _insp.getsource(__import__("contingencia")._desplazar))
# HUECO CAZADO POR EL PROPIO BANCO (8-ago-2026): con pocas ventanas el criterio firmado
# fabrica cuerpo donde no lo hay. Ahora la medicion se NIEGA a opinar bajo el minimo.
try:
    _cmedir(_cmundos(n_ep=6, T=300, semilla=3)["1 SIN AGENCIA (motores desconectados)"][0],
            [5, 6], nulos=2, horizonte=8, ventana=150)
    _rechaza = False
except SystemExit:
    _rechaza = True
caso("contingencia: se NIEGA a medir con menos ventanas del minimo (no opina sin potencia)",
     _rechaza)
caso("contingencia: sus constantes las fija el prerregistro-23, no el codigo",
     "PRERREGISTRO-23" in _insp.getsource(_cmedir) and "SIN AJUSTAR" in _insp.getsource(_cmedir))

print("== verdugo por reescalado: le importa la escala o no ==")
# Congela las DOS versiones que se cayeron antes de la que sirve (INFORME-32):
# comparar contra la base trivial dejaba un mundo SIN LEY a 0.484 de un umbral de 0.5, y un nulo
# con el tiempo revuelto era tan destructivo que TODO lo superaba.
from verdugo_escala import sensibilidad_de_escala as _sens, regla31 as _ve31
_tt = np.arange(400)
_caida = lambda k: [np.column_stack([k * (5.0 - 0.5 * 0.004 * (_tt + f) ** 2) for f in (0, 7, 13)])
                    for _ in range(6)]
_rngE = np.random.default_rng(11)
_paseo = lambda k: [np.column_stack([k * np.cumsum(_rngE.normal(size=400)) for _ in range(3)])
                    for _ in range(6)]
_con = _sens(_caida(1.0), _caida(3.0), 3.0, 1.0)
_sin = _sens(_paseo(1.0), _paseo(3.0), 3.0, 1.0)
caso("verdugo escala: un mundo CON ley es sensible a la escala",
     _con["sensibilidad"] > 0.5 and _con["sobrevive"], f"{_con['sensibilidad']:+.3f}")
caso("verdugo escala: un mundo SIN ley NO es sensible a la escala",
     abs(_sin["sensibilidad"]) < 0.05 and not _sin["sobrevive"], f"{_sin['sensibilidad']:+.4f}")
caso("verdugo escala: la persistencia sola YA transfiere (por eso la vara vieja no servia)",
     0.3 < _sin["transferencia_escala_deshecha"] < 0.7,
     f"{_sin['transferencia_escala_deshecha']:.3f} — si esto baja de 0.3 revisar INFORME-32")
caso("verdugo escala: APRUEBA su Regla 31", _ve31(verbose=False) == 0)

print("== G13 (poder) y G14 (incertidumbre): activados por el director, congelados aqui ==")
from poder import regla31 as _p31, medir as _pmedir
from incertidumbre import regla31 as _i31, medir as _imedir
caso("G13 poder: APRUEBA su Regla 31 (control real, no varianza ni casualidad)", _p31(verbose=False) == 0)
# (corregido en el acto: la primera version de este caso terminaba en "or True" — un caso que
# no puede fallar es decoracion, no vigilancia)
_src_poder = _insp.getsource(__import__("poder"))
caso("G13 poder: es MEDIDOR — no importa curiosidad2 ni escribe en la cola de estudios",
     "import curiosidad2" not in _src_poder and "COLA-ESTUDIOS" not in _src_poder)
caso("G14 incertidumbre: APRUEBA su Regla 31 (separa 'es azar' de 'aun no aprendo')", _i31(verbose=False) == 0)
# la firma falsable de G14, congelada como numero: doblar datos reduce la epistemica
_rngU = np.random.default_rng(9)
_XU = _rngU.normal(size=(12, 2)); _YU = 2 * _XU[:, 0] - _XU[:, 1] + _rngU.normal(0, 0.5, 12)
_XU2 = _rngU.normal(size=(48, 2)); _YU2 = 2 * _XU2[:, 0] - _XU2[:, 1] + _rngU.normal(0, 0.5, 48)
_XtU = _rngU.normal(size=(200, 2))
_eA = _imedir(_XU, _YU, _XtU); _eB = _imedir(_XU2, _YU2, _XtU)
caso("G14: la ignorancia curable CAE al doblar los datos (su firma falsable)",
     _eB["epistemica"] < 0.7 * _eA["epistemica"],
     f"{_eA['epistemica']:.3f} -> {_eB['epistemica']:.3f}")

print("== los sistemas del plan biologico: sueño, atencion, filogenia (Reglas 31 rapidas) ==")
from sueno import regla31 as _s31
from atencion import regla31 as _a31, repartir as _rep
from filogenia import regla31 as _f31, torneo as _torneo
caso("G9 sueño: APRUEBA su Regla 31 (sueña donde hay algo, calla donde no)", _s31(verbose=False) == 0)
caso("G8 atencion: APRUEBA su Regla 31 (la fovea huye del televisor)", _a31(verbose=False) == 0)
caso("Regla 33 filogenia: el estadio empata gemelos y corona oraculos", _f31(verbose=False) == 0)
# la propiedad anti-Goodhart de la atencion, congelada como numero:
_regs = [{"id": "tv", "epistemica": 0.05, "aleatoria": 5.0, "poder": 0.0, "coste": 10},
         {"id": "buena", "epistemica": 0.8, "aleatoria": 0.1, "poder": 0.5, "coste": 10}]
_r = {x["id"]: x["asignado"] for x in _rep(_regs, presupuesto=10)}
caso("atencion: la varianza pura NO compra fovea (anti-televisor por construccion)",
     _r["buena"] > 4 * _r["tv"], str(_r))
caso("filogenia: dos puntajes a 0.001 EMPATAN (no se fabrican linajes)",
     _torneo([{"nombre": "a", "puntaje": 0.500}, {"nombre": "b", "puntaje": 0.501}])["veredicto"] == "EMPATE")

print("== la sinapsis: el genoma es portero, no comentario ==")
from sinapsis import regla31 as _sin31, publicar as _pub, SinapsisBloqueada as _SB
caso("sinapsis: APRUEBA su Regla 31 (bloqueos mecanicos de modo)", _sin31(verbose=False) == 0)
import tempfile as _tf3
_tmp3 = _tf3.mktemp(suffix=".jsonl")
try:
    _pub("G14_incertidumbre", "decision", {}, _ruta=_tmp3); _blq = False
except _SB:
    _blq = True
caso("sinapsis: G14 (medidor) no puede decidir ni queriendo", _blq)
import json as _js
_gj = _js.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arbol", "GENOMA.json"), encoding="utf-8"))
caso("GENOMA.json: todo gen en modo 'decide' tiene prerregistro anotado",
     all(g.get("prerregistro") for g in _gj["genes"].values() if g["modo"] == "decide"))
caso("GENOMA.json: los genes nuevos del dia nacen como MEDIDORES (cuarentena de activacion)",
     all(_gj["genes"][k]["modo"] == "mide" for k in
         ("G13_poder", "G14_incertidumbre", "G8_atencion", "G9_sueno", "G4_contingencia")))

print("== las cinco ecuaciones nuevas (orden del director: implementa todo) ==")
from koopman import regla31 as _k31
from sindy2 import regla31 as _sy31, descubrir as _sydesc
from entropia_transferencia import regla31 as _te31
from energia_libre import regla31 as _el31
from intermodal import regla31 as _im31
caso("Koopman: APRUEBA (halla lo conservado, calla ante lo que decae o vaga)", _k31(verbose=False) == 0)
caso("SINDy: APRUEBA (segundo motor; sin replicacion no hay ley)", _sy31(verbose=False) == 0)
caso("entropia de transferencia: APRUEBA (ve el flujo no lineal que el lineal no ve)", _te31(verbose=False) == 0)
caso("energia libre: APRUEBA (una moneda debajo de todos los impulsos)", _el31(verbose=False) == 0)
caso("espejo intermodal: APRUEBA (refleja al que se mueve, no al que se parece)", _im31(verbose=False) == 0)
caso("SINDy: una ley vacia no es una ley replicada (hueco cazado y congelado)",
     "no es vacío" in _insp.getsource(_sydesc) or "sop_a.sum() == 0" in _insp.getsource(_sydesc))

print("== ranuras: entra al torneo (frontera gris), no al genoma ==")
from ranuras import regla31 as _rn31
caso("ranuras: APRUEBA su Regla 31 (una ranura por cosa, o nada)", _rn31(epocas=3, verbose=False) == 0)
_gd = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arbol", "GENOMA-DIEGO.md"),
           encoding="utf-8").read()
caso("ranuras: el genoma sigue SIN activarla como gen (solo torneo)",
     "G13" in _gd and "ranuras" in _gd.lower() and "NO ENTRA AL GENOMA" in _gd)

print("== SINDy en forma debil + bootstrap (prereg-28): la cura del ruido de sensor ==")
import sindy3 as _s3
caso("sindy3: APRUEBA su Regla 31 (4/4, incluido el oscilador con sensor ruidoso)",
     _s3.regla31(verbose=False) == 0)
# LA LECCION QUE JUSTIFICA EL MODULO, CONGELADA: la derivada numerica muere con 0.5% de ruido de
# sensor; la forma debil sobrevive. Si alguien "simplifica" sindy3 volviendo a derivar, esto grita.
_Xr, _dtr = _s3._oscilador(ruido=0.02)
caso("sindy3: recupera la ley con ruido de sensor donde la derivada numerica ya fracasa",
     _s3._es_la_ley(_s3.descubrir(_Xr, dt=_dtr)) and not (
         lambda l: l is not None and [n for n, _ in l["dx/dt"]] == ["v"]
     )(_sydesc(_Xr, dt=_dtr)))
caso("sindy3: una ley vacia jamas cuenta como replicada (bootstrap sobre ruido puro calla)",
     _s3.descubrir(__import__("numpy").random.default_rng(3).normal(size=(4000, 2)), dt=0.02) is None)

print("== panel de jueces diversos (prereg-31): ningun juez unico corona ==")
import panel_jueces as _pj
caso("panel: APRUEBA su Regla 31 (5/5: gemelos, oraculo, asterisco, ruido, sin suelo)",
     _pj.regla31(verbose=False) == 0)
# EL BUG DE LA CORRIDA 13, CONGELADO: la aptitud vieja recorta el margen a cero con max(.,0),
# asi que CUALQUIER par de representaciones bajo el piso empata en 0.0000 exacto. Si alguien
# vuelve a poner un suelo en el ordenamiento del panel, esto grita.
_cero = _pj.veredicto([{"nombre": "a", "puntajes": {"contingencia": 0.0, "flecha": 0.0,
                                                    "robustez": 0.0}},
                       {"nombre": "b", "puntajes": {"contingencia": 0.0, "flecha": 0.0,
                                                    "robustez": 0.0}}])
caso("panel: cuatro ceros identicos JAMAS producen un ganador (el torneo viejo si lo hacia)",
     "ganador" not in _cero or "EMPATE" in _cero["fallo"])
caso("panel: gana con ASTERISCO quien gana una lectura y pierde otra (no reemplaza los ojos)",
     "ASTERISCO" in _pj.veredicto(
         [{"nombre": "x", "puntajes": {"contingencia": 1.0, "flecha": 0.0, "robustez": 0.0}},
          {"nombre": "y", "puntajes": {"contingencia": 0.0, "flecha": 1.0, "robustez": 1.0}}]
     )["fallo"] or "GANA y" in _pj.veredicto(
         [{"nombre": "x", "puntajes": {"contingencia": 1.0, "flecha": 0.0, "robustez": 0.0}},
          {"nombre": "y", "puntajes": {"contingencia": 0.0, "flecha": 1.0, "robustez": 1.0}}]
     )["fallo"])

print("== la escalera de soporte (prereg-29): el primer no-yo por definicion POSITIVA ==")
import soporte as _sop
caso("soporte: APRUEBA su Regla 31 (7/7: escalones, senuelo, sin gravedad, VOE, nulos)",
     _sop.regla31(verbose=False) == 0)
# LA LECCION DEL NIVEL B FRACASADO, CONGELADA: definir el no-yo solo como "no me obedece" deja
# entrar al ruido puro. El senuelo de ruido debe ser rechazado por ILEGAL (impredecible), no por
# obediente. Si alguien quita el requisito de legalidad, esto grita.
_c, _x, _n, _k = _sop.escena("cae", semilla=1, pasos=_sop.PASOS_MINIMOS)
_e1 = _sop.escalon1(_c, _x, _n, cortes=_k)
caso("soporte: el ruido puro NO puede ser el primer no-yo (legalidad exigida, no solo ausencia)",
     "ruido" not in (_e1.get("candidatos_aptos") or []) and _e1["candidato"] == "altura")
caso("soporte: sin potencia estadistica no hay veredicto (guarda de pasos minimos)",
     _sop.PASOS_MINIMOS >= 900)

print("== canonizar: tarjeta de identidad ==")
t = tarjeta("(v1 + v2) * 0.5 + 3.0", 4)
caso("desplazamiento = f(0)", abs(t["desplazamiento"] - 3.0) < 1e-6)
caso("gradiente correcto", abs(t["gradiente"][0] - 0.5) < 1e-4 and abs(t["gradiente"][2]) < 1e-6)
caso("estable marcada estable", not t["explota_con_entradas_grandes"])
t2 = tarjeta("exp(exp(v1))", 2)
caso("explosiva marcada fragil", t2.get("explota_con_entradas_grandes", False) or "error" in t2)

print()
if FALLOS:
    print(f"BANCO: {len(FALLOS)} FALLOS -> NO COMMITEAR: {FALLOS}")
    sys.exit(1)
print("BANCO: TODO OK — el codigo respeta las lecciones congeladas")
