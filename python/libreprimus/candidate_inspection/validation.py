"""Validation helpers for candidate inspection summaries."""

from __future__ import annotations

from typing import Any


def validate_no_full_dump_in_markdown(text: str) -> None:
    if "output_normalized_text" in text or "candidate_records.jsonl contents" in text:
        raise ValueError("Inspection markdown must not include full candidate dumps.")


def validate_summary_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("solve_claim") is not False:
        raise ValueError("Candidate inspection summaries must keep solve_claim=false.")
    if payload.get("cuda_used") is not False:
        raise ValueError("Candidate inspection summaries must keep cuda_used=false.")
    return payload
