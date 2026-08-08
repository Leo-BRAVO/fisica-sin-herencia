# boleta.py — LA BOLETA DE CALIFICACIONES del Centro (pendiente estrategico nº6, 12-jul-2026).
# La curva de crecimiento en numeros: cuanto sabe, cuanto mejora, cuanto aprende de sus errores.
# Uso: python boleta.py   ->  imprime y guarda registros/BOLETA.json

import os
import json
import glob
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    mem = os.path.join(BASE, "arbol", "MEMORIA-MENTE.jsonl")
    todos = [json.loads(l) for l in open(mem, encoding="utf-8")] if os.path.exists(mem) else []
    # AUD-EXT-01: las pruebas nulas (Regla 11) no son campanas — no entran a la boleta.
    recuerdos = [r for r in todos if not r.get("nulo") and not r["campana"].startswith("nulo")]
    mejoras = [r["cuanto_mejore"] for r in recuerdos if r.get("cuanto_mejore") is not None]
    # AUD-EXT-01: un nodo EN CUARENTENA (Regla 31) no cuenta como vivo.
    nodos_e2 = glob.glob(os.path.join(BASE, "arbol", "N-*-E2.md"))
    en_cuarentena = [n for n in nodos_e2
                     if "EN CUARENTENA" in open(n, encoding="utf-8").read(500)]
    nodos_vivos = len(nodos_e2) - len(en_cuarentena)
    nodos_arch = len(glob.glob(os.path.join(BASE, "arbol", "epoca1", "N-*.md")))
    informes = len(glob.glob(os.path.join(BASE, "resultados", "INFORME-*.md")))
    prerregistros = len(glob.glob(os.path.join(BASE, "registros", "prerregistro-*.md")))
    commits = int(subprocess.run(["git", "-C", BASE, "rev-list", "--count", "HEAD"],
                                 capture_output=True, text=True).stdout.strip() or 0)
    # En un clon superficial (shallow) el conteo miente hacia abajo — se marca None.
    shallow = subprocess.run(["git", "-C", BASE, "rev-parse", "--is-shallow-repository"],
                             capture_output=True, text=True).stdout.strip() == "true"
    if shallow:
        commits = None
    lecciones = sum(1 for l in open(os.path.join(BASE, "MENTE.md"), encoding="utf-8") if l.startswith("- (v"))
    con = os.path.join(BASE, "arbol", "CONECTOMA.json")
    tejidos = len(json.load(open(con)).get("nodos", {})) if os.path.exists(con) else 0

    # AUD-EXT-01: la boleta solo contiene lo que se puede CONTAR desde el disco.
    # Los juicios de valor (cuantas leyes humanas se redescubrieron, cuantas automejoras
    # "valen") viven en los informes y en los veredictos del comparador, firmados por el
    # director — una boleta con notas escritas a mano no es una boleta.
    boleta = {
        "campanas_totales": len(recuerdos),
        "pruebas_nulas_corridas": len(todos) - len(recuerdos),
        "mejora_media": round(sum(mejoras) / len(mejoras), 4) if mejoras else None,
        "mejor_campana": round(max(mejoras), 4) if mejoras else None,
        "huecos_abiertos": sum(1 for r in recuerdos if r.get("hueco")),
        "nodos_vivos_E2": nodos_vivos, "nodos_en_cuarentena": len(en_cuarentena),
        "nodos_archivados_E1": nodos_arch,
        "nodos_en_conectoma": tejidos, "informes": informes,
        "prerregistros": prerregistros, "lecciones_de_metodo": lecciones,
        "commits_genesis": commits,
    }
    with open(os.path.join(BASE, "registros", "BOLETA.json"), "w", encoding="utf-8") as f:
        json.dump(boleta, f, indent=2, ensure_ascii=False)
    print("=== BOLETA DEL CENTRO ===")
    for k, v in boleta.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
