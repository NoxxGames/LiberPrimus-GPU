"""Write generated Stage 3A candidate records to ignored output paths."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from libreprimus.bounded_execution.models import BoundedCandidateRecord, BoundedRunSummary
from libreprimus.bounded_execution.validation import validate_candidate_record, validate_run_summary
from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable


def resolve_out_dir(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_jsonl(path: Path, records: Iterable[Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(to_jsonable(record), sort_keys=True))
            handle.write("\n")
    return path


def write_candidate_outputs(
    out_dir: Path,
    records: list[BoundedCandidateRecord],
    top_records: list[BoundedCandidateRecord],
    summary: BoundedRunSummary,
    warnings: list[str],
) -> dict[str, Path]:
    resolved = resolve_out_dir(out_dir)
    candidate_payloads = [validate_candidate_record(record) for record in records]
    top_payloads = [validate_candidate_record(record) for record in top_records]
    summary_payload = validate_run_summary(summary)
    paths = {
        "candidate_records": write_jsonl(resolved / "candidate_records.jsonl", candidate_payloads),
        "top_candidates": write_jsonl(resolved / "top_candidates.jsonl", top_payloads),
        "summary": write_json(resolved / "summary.json", summary_payload),
        "result_store_preview": write_json(resolved / "result_store_preview.json", summary.result_store_preview),
    }
    if warnings:
        warning_records = [
            {"record_type": "bounded_run_warning", "run_id": summary.run_id, "warning": warning}
            for warning in warnings
        ]
        paths["warnings"] = write_jsonl(resolved / "warnings.jsonl", warning_records)
    return paths
