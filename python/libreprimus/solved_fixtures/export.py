"""Export helpers for generated solved-fixture reproduction outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from libreprimus.solved_fixtures.models import to_jsonable


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(to_jsonable(record), sort_keys=True, ensure_ascii=False))
            handle.write("\n")


def write_reproduction_outputs(out_dir: Path, records: list[Any], summary: Any, warnings: list[str]) -> dict[str, Path]:
    paths = {
        "records": out_dir / "reproduction_records.jsonl",
        "summary": out_dir / "summary.json",
        "warnings": out_dir / "warnings.jsonl",
    }
    write_jsonl(paths["records"], records)
    write_json(paths["summary"], summary)
    write_jsonl(paths["warnings"], [{"warning": warning} for warning in warnings])
    return paths
