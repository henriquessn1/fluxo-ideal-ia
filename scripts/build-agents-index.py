#!/usr/bin/env python3
"""Gera agents/times/index.json: o catálogo dos times oficiais que a Central mostra na tela de
importar (chave, nome, descrição, versão, agentes e o caminho do manifesto).

NÃO editar o index.json à mão: é DERIVADO dos manifest.json. Depois de mudar um time, rode
    python scripts/build-agents-index.py
e commite o index.json junto com o manifesto.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TIMES = RAIZ / "agents" / "times"


def main() -> None:
    itens = []
    for m in sorted(TIMES.glob("*/manifest.json")):
        d = json.loads(m.read_text(encoding="utf-8"))
        agentes = d.get("agentes") or []
        itens.append({
            "chave": d["chave"],
            "nome": d.get("nome") or d["chave"],
            "descricao": d.get("descricao") or "",
            "versao": str(d.get("versao") or ""),
            "agentes": len(agentes),
            "tipos": sorted({a.get("tipo") for a in agentes if a.get("tipo")}),
            "manifesto": m.relative_to(RAIZ).as_posix(),
        })
    saida = {"schema_version": 1, "times": itens}
    (TIMES / "index.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"index.json: {len(itens)} times")


if __name__ == "__main__":
    main()
