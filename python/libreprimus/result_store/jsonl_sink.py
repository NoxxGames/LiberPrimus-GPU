"""JSONL sink for generated experiment result-store records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from libreprimus.result_store.schema_validation import validate_record


def write_jsonl(path: Path, records: Iterable[Any]) -> Path:
    """Write validated records as deterministic UTF-8 JSONL using a temp file replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.tmp")
    with tmp_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            payload = validate_record(record)
            handle.write(json.dumps(payload, sort_keys=True, ensure_ascii=False))
            handle.write("\n")
    tmp_path.replace(path)
    return path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
