"""Load Stage 2H approval-gated execution summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_summary(results_dir: Path) -> dict[str, Any]:
    path = results_dir / "summary.json"
    if not path.is_file():
        return {
            "record_type": "approval_gated_execution_summary",
            "request_count": 0,
            "execution_result_count": 0,
            "pass_count": 0,
            "fail_count": 0,
            "blocked_count": 0,
            "skipped_count": 0,
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Approval execution summary must be a JSON object: {path}")
    return payload


def load_result_records(results_dir: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted(results_dir.glob("*-result.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"Approval execution result must be a JSON object: {path}")
        records.append(payload)
    return records

