"""Build Stage 4I calibration-profile records from existing Stage 3C data."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.scoring_consolidation.models import (
    CALIBRATION_PROFILE_ID,
    SCORER_ID,
    SCORER_VERSION,
    STAGE3C_GENERATED_SUMMARY,
    STAGE3C_RESEARCH_LOG,
)


def build_calibration_profile(*, prefer_generated: bool = True) -> dict[str, Any]:
    """Build a committed calibration profile from existing Stage 3C evidence."""

    summary = _load_generated_summary() if prefer_generated else None
    source = "generated_summary" if summary else "research_log_summary"
    if summary is None:
        summary = _parse_research_log()
    thresholds = dict(summary.get("thresholds", {}))
    return {
        "record_type": "scoring_calibration_profile",
        "calibration_profile_id": CALIBRATION_PROFILE_ID,
        "scorer_id": SCORER_ID,
        "scorer_version": SCORER_VERSION,
        "calibration_source": source,
        "source_ref": _source_ref(source),
        "positive_control_count": int(summary.get("positive_control_count", 0)),
        "null_control_count": int(summary.get("null_control_count", 0)),
        "negative_control_count": int(summary.get("negative_control_count", 0)),
        "candidate_count": int(summary.get("candidate_count", summary.get("stage3_candidate_count", 0))),
        "positive_score_range": summary.get("positive_score_range", {}),
        "null_score_range": summary.get("null_score_range", {}),
        "negative_score_range": summary.get("negative_score_range", {}),
        "thresholds": thresholds,
        "stage3a_top_classification": summary.get("stage3a_top_classification", "noisy"),
        "stage3b_top_classification": summary.get("stage3b_top_classification", "noisy"),
        "limitations": [
            "Stage 3C calibration is small and local.",
            "Labels are triage metadata, not plaintext verification.",
            "Generated calibration detail records remain ignored and are not committed.",
        ],
        "solve_claim": False,
        "trusted_as_canonical": False,
        "cuda_used": False,
    }


def _load_generated_summary() -> dict[str, Any] | None:
    path = repo_root() / STAGE3C_GENERATED_SUMMARY
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _parse_research_log() -> dict[str, Any]:
    path = repo_root() / STAGE3C_RESEARCH_LOG
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    counts = {
        "positive_control_count": _int_after(text, r"Positive controls: `(\d+)`"),
        "null_control_count": _int_after(text, r"Null controls: `(\d+)`"),
        "negative_control_count": _int_after(text, r"Negative controls: `(\d+)`"),
        "candidate_count": _int_after(text, r"Stage 3 candidate records calibrated: `(\d+)`"),
    }
    return {
        **counts,
        "positive_score_range": _range_after(text, r"Positive-control length-normalized score range: `([^`]+)` to `([^`]+)`, mean `([^`]+)`"),
        "null_score_range": _range_after(text, r"Null-control length-normalized score range: `([^`]+)` to `([^`]+)`, mean `([^`]+)`"),
        "negative_score_range": _range_after(text, r"Negative-control length-normalized score range: `([^`]+)` to `([^`]+)`, mean `([^`]+)`"),
        "thresholds": {},
        "stage3a_top_classification": "noisy",
        "stage3b_top_classification": "noisy",
    }


def _int_after(text: str, pattern: str) -> int:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else 0


def _range_after(text: str, pattern: str) -> dict[str, float | int]:
    match = re.search(pattern, text)
    if not match:
        return {"count": 0, "min": 0.0, "max": 0.0, "mean": 0.0}
    return {
        "min": float(match.group(1)),
        "max": float(match.group(2)),
        "mean": float(match.group(3)),
    }


def _source_ref(source: str) -> str:
    path: Path = STAGE3C_GENERATED_SUMMARY if source == "generated_summary" else STAGE3C_RESEARCH_LOG
    return str(path)
