"""Build the Stage 4I calibration report from existing ledgers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root
from libreprimus.scoring_consolidation.models import (
    CALIBRATION_PROFILE_ID,
    METHOD_RETIREMENT_RECORDS,
    METHOD_STATUS_RECORDS,
)


def build_calibration_report(profile: dict[str, Any]) -> dict[str, Any]:
    """Return a durable calibration report summary."""

    method_statuses = _records(repo_root() / METHOD_STATUS_RECORDS)
    retirements = _records(repo_root() / METHOD_RETIREMENT_RECORDS)
    known_noisy = sorted(
        str(record["method_family_id"])
        for record in method_statuses
        if str(record.get("status")) == "noisy"
    )
    known_negative_or_deprioritised = sorted(
        {
            str(record["method_family_id"])
            for record in method_statuses
            if str(record.get("status")) == "negative"
        }
        | {
            str(record["method_family_id"])
            for record in retirements
            if str(record.get("retired_status")) == "deprioritised"
        }
    )
    return {
        "record_type": "scoring_calibration_report",
        "report_id": "stage4i-scorer-consolidation-calibration-report-v0",
        "calibration_profile_id": str(profile.get("calibration_profile_id", CALIBRATION_PROFILE_ID)),
        "positive_controls_available": int(profile.get("positive_control_count", 0)) > 0,
        "null_controls_available": int(profile.get("null_control_count", 0)) > 0,
        "negative_controls_available": int(profile.get("negative_control_count", 0)) > 0,
        "positive_control_count": int(profile.get("positive_control_count", 0)),
        "null_control_count": int(profile.get("null_control_count", 0)),
        "negative_control_count": int(profile.get("negative_control_count", 0)),
        "known_noisy_families": known_noisy,
        "known_negative_or_deprioritised_families": known_negative_or_deprioritised,
        "score_label_interpretation": "Scores rank review leads only and cannot verify plaintext.",
        "limitations": [
            "Stage 4I consolidates existing scoring behavior and does not invent a new scorer.",
            "No score label can imply solved or plaintext verified.",
            "Future CUDA must match CPU output text and score-summary semantics before being trusted.",
        ],
        "solve_claim": False,
        "trusted_as_canonical": False,
        "cuda_used": False,
    }


def _records(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return [dict(item) for item in payload["records"] if isinstance(item, dict)]
    return []
