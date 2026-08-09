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
sys.path.insert(0, os.path.join(BASE, "codigo"))

from sinapsis import publicar, leer, SinapsisBloqueada


def _ahora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def latir(pasos=900, verbose=True):
    """UNA RONDA DE VIDA: cada organo vivo mide lo suyo sobre el mismo mundo y lo publica.
    Ningun organo decide nada aqui — el genoma no se lo permite, y `sinapsis.py` lo impone."""
    from gimnasio import episodio
    eventos, bloqueos = [], []

    def _pub(gen, tipo, contenido):
        try:
            e = publicar(gen, tipo, contenido, cuando=_ahora())
            eventos.append(e)
            if verbose:
                print(f"  · {gen:<24} {tipo:<10} {json.dumps(contenido, ensure_ascii=False)[:76]}")
        except SinapsisBloqueada as x:
            bloqueos.append({"gen": gen, "tipo": tipo, "motivo": str(x)})
            if verbose:
                print(f"  BLOQUEADO {gen} ({tipo}): {str(x)[:90]}")

    # --- el mundo y el cuerpo: una vida corta, con sus sentidos.
    # CUATRO episodios, no uno: el detector de contingencia exige episodios de ENTRENAMIENTO y de
    # JUEZ separados (la muralla del prereg-19). Con un solo episodio se niega a opinar, y hace
    # bien — cazado en la primera ronda de este nervio, el 9-ago-2026.
    # PASOS MINIMOS: el detector exige >=20 ventanas de 150 pasos por episodio-juez. Con menos se
    # NIEGA a opinar (y hace bien). Un latido que no alcanza ese minimo no es un latido corto: es
    # un latido que miente. Cazado en la segunda ronda de este nervio.
    pasos = max(int(pasos), 3200)
    eps, sentidos_todos = [], []
    for i in range(4):
        com, sen, verdad, sentidos = episodio(1000 + i, pasos=pasos, modo="normal", sensores=True)
        eps.append((com, sentidos))
        sentidos_todos.append(sentidos)
    _pub("G3_accion", "decision",
         {"episodio": "normal", "pasos": int(pasos), "articulaciones": 3})
    _pub("G7_juego", "decision",
         {"balbuceo": "suave", "amplitud_media": round(float(np.abs(com).mean()), 4)})
    _pub("sentido_propiocepcion", "medicion",
         {"canales": 6, "rango_angular": round(float(np.ptp(sentidos[:, :3])), 4)})
    _pub("sentido_tacto", "medicion",
         {"canales": 3, "fraccion_con_contacto": round(float(sentidos[:, 6:9].mean()), 4)})

    # --- la frontera yo/mundo sobre los sentidos del cuerpo (no sobre la vista: ver INFORME-38)
    from contingencia import medir
    res = medir(eps, [4], nulos=6)          # el episodio 4 es el JUEZ; los otros, entrenamiento
    mias = sorted(r["variable"] for r in res if r["es_mia"])
    _pub("G4_contingencia", "medicion",
         {"canales_mios": mias, "de": len(res), "sobre": "propiocepcion+tacto"})

    # --- el gasto: cuanto le costo esta ronda
    _pub("G10_interocepcion", "medicion",
         {"episodios": len(eps), "pasos_por_episodio": int(pasos), "canales_sensoriales": 9})

    # --- el cerebro motivacional: los cuatro que MIDEN
    import cerebro as cb
    d13 = cb.diagnostico_g13(ruidos=(0.0, 0.3))
    _pub("G13_poder", "medicion",
         {"lazo_abierto": d13[-1]["lazo_abierto"], "lazo_cerrado": d13[-1]["lazo_cerrado"],
          "subestima": d13[-1]["subestima"]})
    ex = cb.examen_conductual()
    _pub("G14_incertidumbre", "medicion",
         {"abandona_el_tv": ex["abandona_el_tv"], "sigue_explorando": ex["sigue_explorando"],
          "fraccion_tv_final": ex["fraccion_tv_final"]})
    rng = np.random.default_rng(7)
    dif = rng.uniform(0, 1, 400)
    ac = rng.uniform(size=400) > dif
    m = cb.meta_con_nulo(ac, 1.0 - dif + rng.normal(0, 0.05, 400))
    _pub("G15_metacognicion", "medicion",
         {"auc": m["auc"], "nulo_techo": m["nulo_techo"], "supera": m["supera_al_nulo"]})

    # --- LA PRUEBA VIVA DEL PORTERO: un gen en modo 'mide' intentando DECIDIR.
    # Debe quedar bloqueado, y el bloqueo se registra como parte del latido: un portero que
    # nadie prueba en produccion es un portero que nadie sabe si funciona.
    _pub("G13_poder", "decision", {"intento": "cambiar la politica motora"})

    return {"eventos": len(eventos), "bloqueos": bloqueos,
            "canales_mios": mias, "cuando": _ahora()}


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
    ruta = os.path.join(BASE, "arbol", "SINAPSIS.jsonl")
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
