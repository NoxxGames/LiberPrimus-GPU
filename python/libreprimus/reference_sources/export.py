"""Export helpers for generated reference-source summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from libreprimus.reference_sources.models import to_jsonable


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_jsonable(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, records: Iterable[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(to_jsonable(record), sort_keys=True, ensure_ascii=False))
            handle.write("\n")
