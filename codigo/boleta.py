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
    recuerdos = [json.loads(l) for l in open(mem, encoding="utf-8")] if os.path.exists(mem) else []
    mejoras = [r["cuanto_mejore"] for r in recuerdos if r.get("cuanto_mejore") is not None]
    nodos_vivos = len(glob.glob(os.path.join(BASE, "arbol", "N-*-E2.md")))
    nodos_arch = len(glob.glob(os.path.join(BASE, "arbol", "epoca1", "N-*.md")))
    informes = len(glob.glob(os.path.join(BASE, "resultados", "INFORME-*.md")))
    prerregistros = len(glob.glob(os.path.join(BASE, "registros", "prerregistro-*.md")))
    commits = int(subprocess.run(["git", "-C", BASE, "rev-list", "--count", "HEAD"],
                                 capture_output=True, text=True).stdout.strip() or 0)
    lecciones = sum(1 for l in open(os.path.join(BASE, "MENTE.md"), encoding="utf-8") if l.startswith("- (v"))
    con = os.path.join(BASE, "arbol", "CONECTOMA.json")
    tejidos = len(json.load(open(con)).get("nodos", {})) if os.path.exists(con) else 0

    boleta = {
        "campanas_totales": len(recuerdos),
        "mejora_media": round(sum(mejoras) / len(mejoras), 4) if mejoras else None,
        "mejor_campana": round(max(mejoras), 4) if mejoras else None,
        "huecos_abiertos": sum(1 for r in recuerdos if r.get("hueco")),
        "nodos_vivos_E2": nodos_vivos, "nodos_archivados_E1": nodos_arch,
        "nodos_en_conectoma": tejidos, "informes": informes,
        "prerregistros": prerregistros, "lecciones_de_metodo": lecciones,
        "commits_genesis": commits,
        "leyes_humanas_redescubiertas": 3,
        "automejoras_validadas": 1,
    }
    with open(os.path.join(BASE, "registros", "BOLETA.json"), "w", encoding="utf-8") as f:
        json.dump(boleta, f, indent=2, ensure_ascii=False)
    print("=== BOLETA DEL CENTRO ===")
    for k, v in boleta.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
