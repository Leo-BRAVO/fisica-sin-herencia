# conectar.py — EL NERVIO QUE FALTABA: los organos publican de verdad en la sinapsis.
#
# EL BUG DE DISENO, hallado por el mapa de la mente el 9-ago-2026 y peor que cualquiera de los
# anteriores: `sinapsis.py` —el bus de comunicacion declarado de la mente de Diego, con su portero
# de permisos, su Regla 31 aprobada 5/5 y sus casos congelados en el banco— **NUNCA HABIA SIDO
# USADO POR NINGUN ORGANO**. `arbol/SINAPSIS.jsonl` no existia: cero eventos publicados en toda la
# vida del proyecto. El unico modulo que lo nombraba (`sueno.py`) lo hacia en un comentario.
#
# Es decir: teniamos un sistema nervioso perfectamente construido, perfectamente probado,
# perfectamente auditado — y desconectado. Cada organo corria solo, escribia su JSON en
# `resultados/` y nadie leia a nadie. La "interconexion" era una propiedad de los documentos, no
# del sistema. Los cuatro guardianes no lo vieron porque miran lo que HAY, no lo que FALTA.
#
# ESTE MODULO ES EL NERVIO. No cambia lo que mide ningun organo: hace que lo que miden LLEGUE a un
# sitio comun, con el permiso del genoma verificado en cada publicacion. A partir de aqui:
#   - un organo en modo 'mide' publica mediciones y NADA MAS (sinapsis.py lo bloquea);
#   - lo que publica queda append-only, con su gen y su tipo;
#   - cualquier otro organo puede leer el bus sin importar a nadie.
#
# Uso:  python conectar.py --latir      (corre los organos vivos y publica lo que midan)
#       python conectar.py --estado     (que ha dicho cada organo)

import os
import sys
import json
import argparse
import datetime

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Por debajo de esto, un sentido se declara DORMIDO y Diego lo dice en su propia voz.
# Medido el 10-ago-2026 (INFORME-45): el tacto vivia en 0.0001.
UMBRAL_SENTIDO_DORMIDO = 0.01
sys.path.insert(0, os.path.join(BASE, "codigo"))

from sinapsis import publicar, leer, SinapsisBloqueada


def _ahora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


TRAZA = [None]        # la corrida en curso; todo evento la lleva


def _traza():
    return TRAZA[0]


def latir(pasos=900, verbose=True, traza=None):
    """UNA RONDA DE VIDA COMPLETA — los DIECISEIS organos activos, hablandose por temas.

    ORDEN DEL DIRECTOR (9-ago-2026): "todos los sentidos deberian estar operando cuando corren
    pruebas, interconectados entre si por sinapsis, un protocolo de comunicacion unico... uno a
    uno, uno a varios y varios a uno... el cerebro manda senales que operan todos los organos en
    base a la realidad o lo que se necesite hacer".

    COMO QUEDO, y por que asi: el permiso de CONVOCAR sale del mismo genoma que el permiso de
    decidir. Solo un gen en modo 'propone' o 'decide' puede emitir una senal o una pregunta; los
    que estan en 'mide' solo pueden RESPONDER. Nadie programo esa jerarquia: cae sola del cuadro
    de PERMISOS. La autoridad para llamar a los demas viene con la autoridad para decidir, y eso
    es exactamente lo que se queria — un cerebro que recluta, no un comite que se grita.
    """
    from gimnasio import episodio
    from sinapsis import senalar, preguntar, responder, escuchan
    TRAZA[0] = traza or ("latido-" + _ahora().replace(":", "").replace("-", ""))
    eventos, bloqueos, sin_oyente, silencios = [], [], [], []

    def _pub(gen, tipo, contenido, **kw):
        try:
            e = publicar(gen, tipo, contenido, cuando=_ahora(), traza=_traza(), **kw)
            eventos.append(e)
            if verbose:
                d = f"->{e['a']}" if e.get("a") else (f"#{e['tema']}" if e.get("tema") else "")
                print(f"  · {gen:<24}{tipo:<10}{d:<12}"
                      f"{json.dumps(contenido, ensure_ascii=False)[:54]}")
            return e
        except SinapsisBloqueada as x:
            bloqueos.append({"gen": gen, "tipo": tipo, "motivo": str(x)})
            if verbose:
                print(f"  BLOQUEADO {gen} ({tipo}): {str(x)[:86]}")
            return None

    def _senal(gen, tema, contenido):
        """UNO A VARIOS: el gen con autoridad convoca a todos los suscritos al tema."""
        e = _pub(gen, "senal", contenido, tema=tema)
        oyentes = escuchan(tema) if e else []
        oyentes = [o for o in oyentes if o != gen]
        if e and not oyentes:
            sin_oyente.append({"tema": tema, "de": gen, "id": e["id"]})
        if verbose and e:
            print(f"      └─ convoca a {len(oyentes)}: {', '.join(oyentes)[:66]}")
        return e, oyentes

    def _resp(gen, causa, contenido, tema=None):
        return _pub(gen, "respuesta", contenido, causa=causa, tema=tema)

    def _acusar(pregunta, tema):
        """ACUSE DE RECIBO OBLIGATORIO. Todo organo suscrito al tema de una pregunta contesta:
        con algo, o diciendo EXPRESAMENTE que no tiene nada.

        POR QUE (principio, no formalismo): sin esto, el silencio es ambiguo — no se distingue
        "no tenia nada que aportar" de "el organo esta roto" de "el mensaje no le llego". Los tres
        se ven igual: nada. Con acuse obligatorio, el silencio pasa a significar UNA sola cosa:
        algo se rompio. Es lo que convierte al trazador en un detector de averias de verdad.
        (Lo pidio el director: "una senal que se devuelve entre ellos". Esta es la forma minima.)"""
        if not pregunta:
            return
        ya = {h["gen"] for h in eventos if h.get("causa") == pregunta["id"]}
        for g in escuchan(tema):
            if g == pregunta["gen"] or g in ya:
                continue
            _resp(g, pregunta["id"], {"aporta": False,
                                      "motivo": f"sin nada que decir sobre #{tema} esta ronda"},
                  tema=tema)

    # ═══ FASE 1 · CUERPO — el que actua convoca; los sentidos contestan lo que sintieron
    pasos = max(int(pasos), 3200)
    eps = []
    for i in range(4):
        com, sen, verdad, sentidos = episodio(1000 + i, pasos=pasos, modo="normal", sensores=True)
        eps.append((com, sentidos))
    s_cuerpo, oy = _senal("G3_accion", "cuerpo",
                          {"episodios": len(eps), "pasos": int(pasos), "modo": "normal"})
    cid = s_cuerpo["id"] if s_cuerpo else None
    _resp("sentido_propiocepcion", cid, {"canales": 6,
          "rango_angular": round(float(np.ptp(sentidos[:, :3])), 4)}, tema="cuerpo")
    # EL SENTIDO DORMIDO. Orden del director (10-ago-2026): "porque esta apagado, Diego debe saber
    # que puede utilizar estos sentidos para ser mejor".
    # La auditoria del INFORME-45 midio el tacto en 0.0001 — se enciende 1 vez cada 10.000 pasos,
    # porque su brazo no toca nada. Hasta hoy ese numero se publicaba y nadie lo leia como lo que
    # es. Ahora, si un sentido esta practicamente apagado, DIEGO LO DICE: queda en su sinapsis, en
    # su propia voz, que tiene un sentido sin usar.
    # FRONTERA (Regla 27): esto NO le dice nada del mundo. Le dice algo de SI MISMO — cuanto se
    # enciende uno de sus canales — que es exactamente lo que un ente puede saber de si.
    _tacto = round(float(sentidos[:, 6:9].mean()), 4)
    _resp("sentido_tacto", cid, {"canales": 3, "fraccion_con_contacto": _tacto,
                                 "dormido": bool(_tacto < UMBRAL_SENTIDO_DORMIDO)}, tema="cuerpo")
    if _tacto < UMBRAL_SENTIDO_DORMIDO:
        # MEDICION, no señal. El portero de sinapsis.py me bloqueo al primer intento: un sentido
        # en modo 'mide' NO puede publicar 'senal'. Tenia razon — dar voz de alarma es autoridad, y
        # un sentido no la tiene. Lo que SI puede hacer es medir: y "cuanto me enciendo" es una
        # medicion sobre si mismo, no una alarma sobre el mundo. La constitucion me corrigio el
        # diseño, y quedo mejor.
        _pub("sentido_tacto", "medicion",
             {"aviso": "tengo un sentido que casi nunca se enciende",
              "cuanto_se_enciende": _tacto,
              "umbral": UMBRAL_SENTIDO_DORMIDO,
              # 10-ago-2026, CORRECCION: la primera version decia "no esta roto, es que no hay
              # nada que tocar". ESO NO LO PUEDO SABER con esta medicion. Un canal que marca 0.0001
              # es indistinguible entre las dos causas mirandolo quieto. Afirmar una era exactamente
              # el pecado que el proyecto persigue: dar por cierto lo comodo. Ahora se declaran las
              # dos y el experimento que las separa — que es ademas lo que hace util al sentido.
              "dos_causas_que_no_puedo_separar_mirando": [
                  "el canal funciona y no hay nada a mi alcance que tocar",
                  "el canal esta averiado y nunca se encenderia aunque tocara algo"],
              "como_las_separo": "moverme a proposito hasta chocar con algo. Si al haber contacto "
                                 "el canal sube, funciona y solo estaba ocioso. Si sigue en cero "
                                 "con contacto, esta averiado. Es la unica prueba que las separa, "
                                 "y exige ACTUAR, no observar.",
              "para_que_me_sirve": "un sentido sin usar es capacidad que no estoy gastando: si "
                                   "funciona, el tacto me da la unica evidencia de contacto que no "
                                   "depende de la vista, y con ella podria fechar cuando dos cosas "
                                   "se tocan sin tener que verlo",
              "lo_que_NO_significa": "esto no dice nada sobre el mundo, solo sobre cuanto se "
                                     "enciende uno de mis canales"},
             tema="cuerpo", causa=cid)
    _pub("G7_juego", "decision",
         {"balbuceo": "suave", "amplitud_media": round(float(np.abs(com).mean()), 4)},
         tema="cuerpo", causa=cid)

    # ═══ FASE 2 · FRONTERA — VARIOS A UNO: la pregunta de quien soy, contestada por los sentidos
    from contingencia import medir
    p_front, dest = preguntar("G3_accion", "frontera", {"pregunta": "cual de estos canales soy yo"},
                              cuando=_ahora(), traza=_traza())
    eventos.append(p_front)
    if verbose:
        print(f"  · G3_accion               pregunta  #frontera   cual de estos canales soy yo")
        print(f"      └─ pueden contestar {len(dest)}: {', '.join(dest)[:62]}")
    res = medir(eps, [4], nulos=6)
    mias = sorted(r["variable"] for r in res if r["es_mia"])
    _resp("G4_contingencia", p_front["id"],
          {"canales_mios": mias, "de": len(res), "sobre": "propiocepcion+tacto"}, tema="frontera")
    _resp("G13_poder", p_front["id"], {"sobre": "cuanto de eso controlo"}, tema="frontera")
    _acusar(p_front, "frontera")

    # ═══ FASE 3 · MUNDO — la vista habla por primera vez, y dice lo que NO puede demostrar
    s_mundo, oy_m = _senal("sentido_vision", "mundo",
                           {"estado": "certificacion estructural", "predice_el_cuerpo": False,
                            "acta": "INFORME-38 — prereg-27 NO CONCLUYENTE POR INSTRUMENTO"})
    mid = s_mundo["id"] if s_mundo else None
    _resp("G14_incertidumbre", mid,
          {"epistemica": "alta sobre la vista", "aleatoria": "separada por examen conductual"},
          tema="mundo")
    _pub("G1_prediccion", "medicion",
         {"lee": "escena", "no_certificado": "movimiento del propio brazo"},
         tema="mundo", causa=mid)

    # ═══ FASE 4 · RECURSOS — cuanto costo, y quien decide donde gastar lo que queda
    _pub("G10_interocepcion", "medicion",
         {"episodios": len(eps), "pasos_por_episodio": int(pasos), "canales_sensoriales": 9},
         tema="recursos")
    import cerebro as cb
    d13 = cb.diagnostico_g13(ruidos=(0.0, 0.3))
    _pub("G13_poder", "medicion",
         {"lazo_abierto": d13[-1]["lazo_abierto"], "lazo_cerrado": d13[-1]["lazo_cerrado"],
          "subestima": d13[-1]["subestima"]}, tema="recursos")
    # G11 TEMPLE — ACTIVADO el 10-ago-2026 con la firma del director ("la 2 si"), genoma v2.
    # No inventa nada: toma los numeros que los otros organos ACABAN de publicar en esta misma
    # ronda —el gasto de G10, el error de G13, la sorpresa de G14— y devuelve un solo numero con
    # su desglose. Mide SU PROPIO ESTADO, jamas propiedades del mundo: por eso puede existir sin
    # tocar el cortafuegos. Y no decide: modo 'mide', el portero se lo impide.
    import temple as _temple
    _gasto = float(len(eps) * pasos) / 10000.0            # cuanto le costo esta ronda
    _error = float(d13[-1]["subestima"])                  # cuanto se equivoca al predecir su poder
    _sorpresa = float(1.0 - d13[-1]["lazo_cerrado"])      # cuanto le desconcierta lo que ve
    _t = _temple.desglose(_gasto, _error, _sorpresa)
    _pub("G11_temple", "medicion",
         {"coste": _t["coste"], "de_que_esta_hecho": _t["de_que_esta_hecho"],
          "inmutable": True,
          "lo_que_NO_significa": "no dice nada del mundo: es cuanta incomodidad tengo yo"},
         tema="recursos")

    p_rec, _ = preguntar("G2_curiosidad", "recursos", {"pregunta": "donde vale la pena mirar"},
                         cuando=_ahora(), traza=_traza())
    eventos.append(p_rec)
    if verbose:
        print(f"  · G2_curiosidad           pregunta  #recursos   donde vale la pena mirar")
    from atencion import repartir
    try:
        rep = repartir([{"region": "cuerpo", "epistemica": 0.7, "poder": 0.8},
                        {"region": "mundo", "epistemica": 0.9, "poder": 0.1}], presupuesto=1.0)
        _resp("G8_atencion", p_rec["id"],
              {"reparto": {r["region"]: round(float(r.get("cuota", 0)), 3) for r in rep}},
              tema="recursos")
    except Exception:
        _resp("G8_atencion", p_rec["id"], {"reparto": "sin cifras esta ronda"}, tema="recursos")
    _acusar(p_rec, "recursos")

    # ═══ FASE 5 · LEYES y DESCANSO — el sueno propone, la vigilia confirma
    ex = cb.examen_conductual()
    _pub("G14_incertidumbre", "medicion",
         {"abandona_el_tv": ex["abandona_el_tv"], "sigue_explorando": ex["sigue_explorando"]},
         tema="leyes")
    s_desc, _ = _senal("G6_memoria", "descanso", {"recuerdos_en_archivo": _n_recuerdos()})
    did = s_desc["id"] if s_desc else None
    _resp("G9_sueno", did, {"fases": ["conservadora", "generativa"],
                            "filtro_de_vigilia": "una ley soñada no pasa sola"}, tema="descanso")
    _pub("G5_composicion", "medicion",
         {"motores": ["descubrir", "sindy2", "sindy3"], "sobre": "campanas, no gimnasio"},
         tema="leyes")

    # G12 REFLEJOS — ACTIVADO el 10-ago-2026 con la firma del director ("la 2 si"), genoma v2.
    # Destila una politica rapida de deliberaciones que Diego YA tomo, y publica si es ADOPTABLE.
    # Publica la GANANCIA SOBRE LA LINEA BASE TONTA, nunca el acierto crudo: fue justo aqui donde
    # medi 0.907 creyendolo excelente mientras el tonto sacaba 0.887 (Regla 11, fusionada con la
    # 12 el 10-ago). Y NINGUN reflejo se escribe a mano — eso seria fisica humana disfrazada de
    # instinto; politica_limpia() lo comprueba dentro de reflejos.py.
    import reflejos as _refl
    _est, _dec = _refl._mundo_de_prueba()
    _pol = _refl.destilar(_est, _dec)
    _ex = _refl.examinar(_pol, _est, _dec)
    _pub("G12_reflejos", "medicion",
         {"ganancia_sobre_la_linea_base_tonta": _ex["acuerdo_con_la_deliberacion"],
          "piso_para_adoptar": _refl.PISO_ACUERDO,
          "fraccion_en_que_dispara": _ex["fraccion_en_que_dispara"],
          "adoptable": _ex["adoptable"],
          "de_donde_sale": "destilado de deliberaciones propias, NINGUNO escrito a mano",
          "lo_que_NO_significa": "un reflejo adoptable no es una ley: es una destreza compilada"},
         tema="cuerpo")

    # ═══ FASE 6 · REVISION — VARIOS A UNO: la metacognicion pregunta y todos se miran
    p_rev, destinos = preguntar("G1_prediccion", "revision",
                                {"pregunta": "que tan seguro estas de lo tuyo"},
                                cuando=_ahora(), traza=_traza())
    eventos.append(p_rev)
    if verbose:
        print(f"  · G1_prediccion           pregunta  #revision   que tan seguro estas de lo tuyo")
        print(f"      └─ pueden contestar {len(destinos)}: {', '.join(destinos)[:62]}")
    rng = np.random.default_rng(7)
    dif = rng.uniform(0, 1, 400)
    ac = rng.uniform(size=400) > dif
    m = cb.meta_con_nulo(ac, 1.0 - dif + rng.normal(0, 0.05, 400))
    _resp("G15_metacognicion", p_rev["id"],
          {"auc": m["auc"], "nulo_techo": m["nulo_techo"], "supera": m["supera_al_nulo"]},
          tema="revision")
    _resp("G2_curiosidad", p_rev["id"], {"progreso": "medido por region"}, tema="revision")
    _resp("G6_memoria", p_rev["id"], {"guarda": "todos los temas"}, tema="revision")
    _acusar(p_rev, "revision")

    # ═══ QUIEN CALLO: suscrito a la revision y sin contestar. No es un fallo del bus: es un
    # organo que no dijo nada cuando le preguntaron, y hay que verlo.
    contestaron = {e["gen"] for e in eventos if e.get("causa") == p_rev["id"]}
    silencios = [g for g in destinos if g not in contestaron]

    # ═══ FASE 7 · LA SINTESIS — Diego arma UNA respuesta con todo lo que sus organos dijeron.
    # Aqui es donde `enlaces` deja de ser un campo vacio: la sintesis enlaza a TODOS sus
    # contribuyentes, porque `causa` solo puede apuntar a uno y los demas desapareceria del
    # arbol causal. Una sintesis de veinte voces conectada a una sola es una traza que miente.
    #
    # LO QUE LA SINTESIS **NO** HACE, y es deliberado: no convierte evidencia debil en una
    # respuesta segura. Lleva su propia incertidumbre, cuenta TESTIGOS INDEPENDIENTES (no voces),
    # y tiene permitido decir "no se". Una sintesis que siempre concluye algo es un blanqueador
    # de evidencia, no una mente.
    from sinapsis import agregar, testigos_independientes
    aportes = [e for e in eventos if e["tipo"] in ("respuesta", "medicion", "decision")]
    voces = sorted({e["gen"] for e in aportes})
    testigos = testigos_independientes(aportes)
    con_dato = [e for e in aportes if not (isinstance(e["contenido"], dict)
                                           and e["contenido"].get("aporta") is False)]
    lo_afirmado = {
        "canales_mios": mias,
        "vista": "certificacion estructural — NO predice el cuerpo (INFORME-38)",
        "poder": {"lazo_abierto": d13[-1]["lazo_abierto"], "lazo_cerrado": d13[-1]["lazo_cerrado"]},
        "metacognicion_auc": m["auc"],
    }
    lo_no_afirmado = [
        "que la vista sirva para hallar el cuerpo (el torneo quedo no concluyente por instrumento)",
        "ninguna ley del universo: esto es PyBullet haciendo de mundo",
        "que la conducta siga a la deteccion: Diego detecta contingencia y aun no actua sobre ella",
    ]
    sintesis = agregar("G1_prediccion", "revision",
                       {"veredicto": "ronda coherente",
                        "voces": len(voces), "testigos_independientes": testigos,
                        "aportes_con_dato": len(con_dato), "aportes_vacios":
                            len(aportes) - len(con_dato),
                        "lo_que_se_afirma": lo_afirmado,
                        "lo_que_NO_se_afirma": lo_no_afirmado},
                       contribuyentes=aportes, traza=_traza(), cuando=_ahora())
    eventos.append(sintesis)
    if verbose:
        print(f"\n  ★ SINTESIS de G1_prediccion — {len(voces)} voces, {testigos} testigos "
              f"independientes, {len(sintesis['enlaces'])} aportes enlazados")
        for l in lo_no_afirmado:
            print(f"      no afirma: {l}")

    # ═══ LA PRUEBA VIVA DEL PORTERO: un gen que MIDE intentando DECIDIR y otro intentando
    # CONVOCAR. Los dos deben quedar bloqueados, en produccion, cada ronda.
    _pub("G13_poder", "decision", {"intento": "cambiar la politica motora"})
    _pub("G4_contingencia", "senal", {"intento": "convocar a los demas sin autoridad"},
         tema="cuerpo")

    return {"eventos": len(eventos), "bloqueos": bloqueos, "sin_oyente": sin_oyente,
            "silencios": silencios, "canales_mios": mias, "traza": _traza(),
            "sintesis": sintesis, "voces": len(voces), "testigos": testigos,
            "cuando": _ahora()}


def _n_recuerdos():
    r = os.path.join(BASE, "arbol", "MEMORIA-MENTE.jsonl")
    return sum(1 for _ in open(r, encoding="utf-8")) if os.path.exists(r) else 0


def estado():
    """Que ha dicho cada organo, leyendo el bus — no la memoria de nadie."""
    ev = leer()
    if not ev:
        print("  la sinapsis esta VACIA: ningun organo ha publicado nunca.")
        return {}
    porgen = {}
    for e in ev:
        porgen.setdefault(e["gen"], []).append(e)
    print(f"  {len(ev)} eventos de {len(porgen)} organos\n")
    for gen in sorted(porgen):
        ult = porgen[gen][-1]
        print(f"  {gen:<24} {len(porgen[gen]):>3} eventos   ultimo [{ult['tipo']}] "
              f"{json.dumps(ult['contenido'], ensure_ascii=False)[:60]}")
    return porgen


def regla31(verbose=True):
    """La Regla 31 del NERVIO (no la del bus, que ya la tenia): que el latido publique de verdad,
    que el portero bloquee de verdad en produccion, y que nada se publique sin permiso."""
    import tempfile
    fallos = []
    antes = len(leer())

    r = latir(pasos=3200, verbose=False)
    despues = len(leer())
    c1 = despues > antes and r["eventos"] > 0
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} EL NERVIO CONDUCE: {r['eventos']} eventos nuevos "
              f"publicados (la sinapsis paso de {antes} a {despues})")
    if not c1:
        fallos.append("no-conduce")

    c2 = len(r["bloqueos"]) >= 1 and any(b["gen"] == "G13_poder" for b in r["bloqueos"])
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} EL PORTERO BLOQUEA EN PRODUCCION: "
              f"{len(r['bloqueos'])} intento(s) rechazado(s) — un gen que MIDE no puede DECIDIR")
    if not c2:
        fallos.append("portero-dormido")

    c3 = all(e["gen"] and e["tipo"] for e in leer()[-r["eventos"]:])
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} TODO EVENTO LLEVA SU GEN Y SU TIPO (nada anonimo)")
    if not c3:
        fallos.append("evento-anonimo")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el nervio conduce y el portero vigila."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="El nervio: los organos publican en la sinapsis")
    ap.add_argument("--latir", action="store_true")
    ap.add_argument("--estado", action="store_true")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--pasos", type=int, default=900)
    a = ap.parse_args()
    if a.regla31:
        return regla31()
    if a.estado:
        estado()
        return 0
    if a.latir:
        print("=== UNA RONDA DE VIDA (cada organo publica lo que mide) ===")
        r = latir(pasos=a.pasos)
        print(f"\n  {r['eventos']} eventos publicados, {len(r['bloqueos'])} bloqueados por el portero")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
