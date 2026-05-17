"""Load and validate Stage 2H approval-gated execution requests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.approval_execution.models import ApprovalExecutionRequest
from libreprimus.approval_execution.validation import validate_payload
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256

FALSE_FIELDS = [
    "unsolved_execution_allowed",
    "search_execution_enabled",
    "candidate_generation_enabled",
    "scoring_enabled",
    "cuda_enabled",
    "canonical_corpus_active",
    "page_boundaries_final",
    "trusted_as_canonical",
]

SAFE_SCOPES = {
    "synthetic_only",
    "solved_fixture_only",
    "synthetic_and_solved_fixture_only",
    "no_op_review_only",
}


def load_approval_execution_request(path: Path) -> ApprovalExecutionRequest:
    resolved = path if path.is_absolute() else repo_root() / path
    payload = load_request_payload(resolved)
    validate_approval_execution_request_payload(payload, source_text=resolved.read_text(encoding="utf-8"))
    return ApprovalExecutionRequest(payload=payload, path=str(resolved), sha256=compute_sha256(resolved))


def load_request_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    payload = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(payload, dict):
        raise ValueError(f"Approval execution request must be a mapping: {path}")
    return payload


def validate_approval_execution_request_payload(
    payload: dict[str, Any],
    *,
    source_text: str = "",
) -> None:
    validate_payload(payload, "approval-gated-execution-request-v0.schema.json")
    if payload.get("execution_scope") not in SAFE_SCOPES:
        raise ValueError("Approval-gated execution request scope is not allowed in Stage 2H.")
    for field in FALSE_FIELDS:
        if payload.get(field) is not False:
            raise ValueError(f"Stage 2H approval-gated requests require {field}=false.")
    if _looks_like_raw_dump(source_text):
        raise ValueError("Approval-gated request appears to include raw corpus data.")


def _looks_like_raw_dump(text: str) -> bool:
    return len(text) > 30000 or "data/raw/" in text or text.count("\n") > 1400 or "BEGIN RAW" in text

