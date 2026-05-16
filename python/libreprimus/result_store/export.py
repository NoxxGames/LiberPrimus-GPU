"""Export helpers for result-store generated outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.result_store.jsonl_sink import write_jsonl
from libreprimus.result_store.schema_validation import validate_record
from libreprimus.solved_fixtures.models import to_jsonable


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    validate_record(payload)
    path.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_result_store_outputs(
    out_dir: Path,
    *,
    run_records: list[Any],
    event_records: list[Any],
    artifact_records: list[Any],
    summary: Any,
) -> dict[str, Path]:
    return {
        "runs": write_jsonl(out_dir / "run_records.jsonl", run_records),
        "events": write_jsonl(out_dir / "event_records.jsonl", event_records),
        "artifacts": write_jsonl(out_dir / "artifact_records.jsonl", artifact_records),
        "summary": write_json(out_dir / "summary.json", summary),
    }
