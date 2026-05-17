"""Summary helpers for candidate inspection output."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from libreprimus.candidate_inspection.models import InspectionSummary


def to_summary_payload(summary: InspectionSummary) -> dict[str, Any]:
    payload = asdict(summary)
    payload["record_type"] = "candidate_inspection_summary"
    payload["solve_claim"] = False
    payload["cuda_used"] = False
    return payload
