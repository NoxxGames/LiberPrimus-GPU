"""Scoring adapter for CPU batch output records."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring_consolidation.confidence_labels import map_legacy_label
from libreprimus.scoring_consolidation.models import CALIBRATION_PROFILE_ID, SCORER_ID, SCORER_VERSION


def score_output(output_text: str | None, *, enabled: bool) -> dict[str, Any]:
    """Score text through the existing minimal triage scorer when available."""

    if not enabled:
        return {"score_status": "scoring_disabled"}
    if not output_text:
        return {"score_status": "scoring_not_available", "reason": "no_output_text"}
    score = score_text(output_text)
    payload = asdict(score)
    legacy_label = str(payload.get("confidence_label", "inconclusive"))
    payload["legacy_confidence_label"] = legacy_label
    payload["confidence_label"] = map_legacy_label(legacy_label)
    payload["scorer_id"] = SCORER_ID
    payload["scorer_version"] = SCORER_VERSION
    payload["calibration_profile_id"] = CALIBRATION_PROFILE_ID
    payload["trusted_as_canonical"] = False
    payload["cuda_used"] = False
    payload["score_status"] = "scored"
    return payload
