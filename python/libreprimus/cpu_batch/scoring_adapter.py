"""Scoring adapter for CPU batch output records."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from libreprimus.scoring.minimal_triage import score_text


def score_output(output_text: str | None, *, enabled: bool) -> dict[str, Any]:
    """Score text through the existing minimal triage scorer when available."""

    if not enabled:
        return {"score_status": "scoring_disabled"}
    if not output_text:
        return {"score_status": "scoring_not_available", "reason": "no_output_text"}
    score = score_text(output_text)
    payload = asdict(score)
    payload["score_status"] = "scored"
    return payload
