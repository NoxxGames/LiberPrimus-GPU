"""Export helpers for generated corpus candidate records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from libreprimus.corpus_candidate.models import to_jsonable


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(to_jsonable(record), sort_keys=True, ensure_ascii=False))
            handle.write("\n")


def write_corpus_candidate_outputs(out_dir: Path, result: dict[str, Any]) -> dict[str, Path]:
    paths = {
        "manifest": out_dir / "corpus_candidate_manifest.json",
        "tokens": out_dir / "tokens.jsonl",
        "lines": out_dir / "lines.jsonl",
        "page_candidates": out_dir / "page_candidates.jsonl",
        "warnings": out_dir / "warnings.jsonl",
        "separator_inventory": out_dir / "observed_separator_inventory.json",
        "summary": out_dir / "summary.json",
    }
    write_json(paths["manifest"], result["manifest"])
    write_jsonl(paths["tokens"], result["tokens"])
    write_jsonl(paths["lines"], result["lines"])
    write_jsonl(paths["page_candidates"], result["page_candidates"])
    write_jsonl(paths["warnings"], result["warnings"])
    write_json(paths["separator_inventory"], result["separator_inventory"])
    write_json(paths["summary"], result["summary"])
    return paths
