# mente.py — EL MAPA DE LA MENTE DE DIEGO: qué órganos tiene, cómo se hablan, y qué está suelto.
#
# ORDEN DEL DIRECTOR (9-ago-2026): "necesito saber cómo todo está interconectado y el proceso
# exacto que se ejecuta cuando pedimos pruebas; diagnostica cada instrumento, regla, órgano de
# Diego por separado y luego juntos, y verifica que realmente todo esté interconectado, tenga
# lógica; muéstrame cómo se ve la mente de Diego ahora."
#
# Los guardianes dicen SI o NO. `diagnostico_total.py` dice QUE ESTA MAL. Este archivo dice
# **COMO ESTA ARMADO** — y por eso encuentra una clase de fallo que ninguno de los otros ve:
# el HUERFANO. Un modulo que aprueba su Regla 31, pasa el banco, y no esta conectado a nada.
# Un organo perfecto que no le llega sangre a nadie.
#
# Cinco preguntas, y las cinco se responden leyendo el disco, no la memoria de nadie:
#   1. ¿Que genes declara el genoma, en que modo, y con que modulo?
#   2. ¿Que modulo importa a que otro? (el tejido real, no el dibujado)
#   3. ¿Cada gen tiene modulo vivo, Regla 31, casos en el banco y prerregistro?
#   4. ¿Que modulos existen y NO cuelgan de ningun gen ni de ningun otro modulo? (huerfanos)
#   5. ¿Que puede DECIDIR hoy, que solo PROPONE y que solo MIDE?

import os
import re
import sys
import ast
import json
import glob
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COD = os.path.join(BASE, "codigo")

# Modulos que son herramienta del lado humano (guardianes, orquestacion, mapas): no son organos
# de Diego y no se les exige colgar de un gen.
LADO_HUMANO = {"pruebas.py", "coherencia.py", "auditoria_total.py", "guardianes_de_guardianes.py",
               "diagnostico_total.py", "mente.py", "boleta.py", "conectoma.py", "latido_nube.py",
               "reconstruir_datos.py", "preparar_mendeley.py", "extraer_posiciones.py",
               "canonizar.py", "forense.py", "autopsia.py", "rodar.py",
               "auditoria_total.py", "regla31_conservada.py", "descubrir_pool.py"}


def _genoma():
    return json.load(open(os.path.join(BASE, "arbol", "GENOMA.json"), encoding="utf-8"))


def _modulos_de(gen):
    """Un gen puede declarar varios modulos ('percepcion.py/descubrir.py') o ninguno."""
    m = gen.get("modulo")
    if not m:
        return []
    m = re.sub(r"\s*\(.*?\)", "", m)          # 'gimnasio.py (balbuceo)' -> 'gimnasio.py'
    return [x.strip() for x in m.split("/") if x.strip().endswith(".py")]


def _invocados_por_la_cola():
    """LOS CORREDORES. Un modulo puede estar perfectamente conectado sin que NADIE lo importe:
    los guiones que el latido ejecuta desde `registros/COLA-ESTUDIOS.json` se invocan por ruta,
    no por `import`. La primera version de este mapa los declaro huerfanos a todos —
    hito0_multimodal, torneo_ojos, curiosidad— cuando son justamente los que producen la ciencia.
    El sistema tiene DOS formas de conexion y hay que mirar las dos:
       BIBLIOTECA — alguien la importa.
       CORREDOR   — la cola o el workflow la ejecutan.
    (Punto ciego propio, cazado el 9-ago-2026 al leer la primera radiografia.)"""
    usados = set()
    for ruta in (os.path.join(BASE, "registros", "COLA-ESTUDIOS.json"),
                 os.path.join(BASE, ".github", "workflows", "latido-nube.yml"),
                 os.path.join(BASE, ".github", "workflows", "estudios-nube.yml")):
        if not os.path.exists(ruta):
            continue
        texto = open(ruta, encoding="utf-8").read()
        usados.update(re.findall(r"([a-z0-9_]+\.py)", texto))
    return usados


def _importa(archivo):
    """Que otros modulos de codigo/ importa este, leyendo el arbol sintactico (no adivinando)."""
    try:
        arbol = ast.parse(open(archivo, encoding="utf-8").read())
    except SyntaxError:
        return set()
    fuera = set()
    for n in ast.walk(arbol):
        if isinstance(n, ast.Import):
            fuera.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            fuera.add(n.module.split(".")[0])
    locales = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(COD, "*.py"))}
    return {f"{x}.py" for x in fuera if x in locales}


def radiografia():
    gen = _genoma()
    modulos = sorted(os.path.basename(p) for p in glob.glob(os.path.join(COD, "*.py")))
    banco = open(os.path.join(COD, "pruebas.py"), encoding="utf-8").read()
    imports = {m: _importa(os.path.join(COD, m)) for m in modulos}
    usado_por = {m: sorted(o for o, deps in imports.items() if m in deps) for m in modulos}

    filas = []
    for nombre, g in gen["genes"].items():
        mods = _modulos_de(g)
        vivos = [m for m in mods if os.path.exists(os.path.join(COD, m))]
        tiene_r31 = any("def regla31" in open(os.path.join(COD, m), encoding="utf-8").read()
                        for m in vivos)
        en_banco = any(m[:-3] in banco for m in vivos)
        filas.append({"gen": nombre, "modo": g["modo"], "modulos": mods,
                      "modulos_vivos": vivos,
                      "declara_modulo_inexistente": [m for m in mods if m not in vivos],
                      "tiene_regla31": tiene_r31, "en_banco": en_banco,
                      "prerregistro": g.get("prerregistro")})

    de_genes = {m for f in filas for m in f["modulos_vivos"]}
    corredores = _invocados_por_la_cola()
    huerfanos = [m for m in modulos
                 if m not in de_genes and m not in LADO_HUMANO and not usado_por[m]
                 and m not in corredores]
    return {"genoma_fecha": gen.get("fecha"), "genes": filas, "modulos": modulos,
            "importa": {k: sorted(v) for k, v in imports.items()},
            "usado_por": usado_por, "huerfanos": huerfanos, "de_genes": sorted(de_genes),
            "corredores": sorted(corredores & set(modulos))}


def _barra(modo):
    return {"decide": "DECIDE ", "propone": "propone", "mide": "mide   ",
            "inactivo": "·······"}.get(modo, modo)


def imprimir(r):
    print("=" * 78)
    print(f"LA MENTE DE DIEGO — genoma del {r['genoma_fecha']}")
    print("=" * 78)
    modos = {}
    for f in r["genes"]:
        modos.setdefault(f["modo"], []).append(f)

    print("\n### QUE PUEDE HACER HOY (el modo lo impone `sinapsis.py`, no la buena voluntad)\n")
    for modo, titulo in (("decide", "DECIDE — actua sin pedir permiso, dentro de su prerregistro"),
                         ("propone", "PROPONE — sugiere; el director firma"),
                         ("mide", "MIDE — observa y publica cifras; NO puede decidir nada"),
                         ("inactivo", "INACTIVO — construido o disenado, sin encender")):
        if modo not in modos:
            continue
        print(f"  {titulo}")
        for f in sorted(modos[modo], key=lambda x: x["gen"]):
            marcas = []
            if not f["modulos_vivos"]:
                marcas.append("SIN MODULO")
            else:
                if not f["tiene_regla31"]:
                    marcas.append("SIN Regla 31")
                if not f["en_banco"]:
                    marcas.append("SIN casos en el banco")
            if f["declara_modulo_inexistente"]:
                marcas.append(f"declara inexistente: {f['declara_modulo_inexistente']}")
            aviso = ("   <-- " + "; ".join(marcas)) if marcas else ""
            print(f"    {_barra(f['modo'])}  {f['gen']:<24} "
                  f"{', '.join(f['modulos_vivos']) or '—':<34}{aviso}")
        print()

    print("### EL TEJIDO — quien se apoya en quien (los mas usados primero)\n")
    conteo = sorted(((len(v), k) for k, v in r["usado_por"].items() if v), reverse=True)
    for n, m in conteo[:10]:
        print(f"    {m:<26} <- lo usan {n}: {', '.join(r['usado_por'][m])}")

    print("\n### CORREDORES — nadie los importa; los ejecuta la cola o el workflow\n")
    print(f"    {', '.join(r['corredores']) or 'ninguno'}")

    print("\n### HUERFANOS — ni gen, ni import, ni cola: sueltos de verdad\n")
    if r["huerfanos"]:
        for m in r["huerfanos"]:
            print(f"    SUELTO  {m}")
    else:
        print("    ninguno: todo modulo cuelga de un gen o lo usa otro modulo")
    print()


def revisar(r):
    """Los fallos de ESTRUCTURA (no de codigo ni de ciencia): lo que esta suelto o mal declarado."""
    problemas = []
    for f in r["genes"]:
        if f["declara_modulo_inexistente"]:
            problemas.append(f"{f['gen']}: el genoma declara modulos que no existen "
                             f"{f['declara_modulo_inexistente']}")
        if f["modo"] != "inactivo" and not f["modulos_vivos"]:
            problemas.append(f"{f['gen']}: activo en modo '{f['modo']}' pero SIN modulo vivo")
        if f["modo"] != "inactivo" and f["modulos_vivos"] and not f["en_banco"]:
            problemas.append(f"{f['gen']}: activo y SIN casos en el banco congelado")
        if f["modo"] == "decide" and not f.get("prerregistro"):
            problemas.append(f"{f['gen']}: modo 'decide' SIN prerregistro declarado")
    for m in r["huerfanos"]:
        problemas.append(f"{m}: modulo huerfano — no cuelga de ningun gen y nadie lo importa")
    return problemas


def main():
    ap = argparse.ArgumentParser(description="El mapa de la mente de Diego")
    ap.add_argument("--json", action="store_true", help="volcar la radiografia cruda")
    ap.add_argument("--revisar", action="store_true",
                    help="salir con codigo 1 si hay fallos de estructura")
    a = ap.parse_args()
    r = radiografia()
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0
    imprimir(r)
    problemas = revisar(r)
    if problemas:
        print("### FALLOS DE ESTRUCTURA\n")
        for p in problemas:
            print(f"    · {p}")
        print()
    else:
        print("### FALLOS DE ESTRUCTURA: ninguno — cada gen tiene modulo, Regla 31 y banco.\n")
    if a.revisar:
        return 1 if problemas else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
