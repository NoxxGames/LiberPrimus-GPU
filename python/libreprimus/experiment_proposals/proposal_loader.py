"""Load and validate Stage 2G experiment proposals."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.experiment_proposals.checklist import validate_review_checklist
from libreprimus.experiment_proposals.models import ExperimentProposal
from libreprimus.experiment_proposals.validation import validate_payload
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256

FALSE_FIELDS = [
    "approved_for_execution",
    "execution_enabled",
    "search_execution_enabled",
    "candidate_generation_enabled",
    "scoring_enabled",
    "cuda_enabled",
    "canonical_corpus_active",
    "page_boundaries_final",
    "trusted_as_canonical",
]


def load_experiment_proposal(path: Path) -> ExperimentProposal:
    resolved = path if path.is_absolute() else repo_root() / path
    payload = load_yaml_payload(resolved)
    validate_experiment_proposal_payload(payload, source_text=resolved.read_text(encoding="utf-8"))
    return ExperimentProposal(payload=payload, path=str(resolved), sha256=compute_sha256(resolved))


def load_yaml_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Experiment proposal must be a YAML mapping: {path}")
    return payload


def validate_experiment_proposal_payload(
    payload: dict[str, Any],
    *,
    source_text: str = "",
) -> None:
    validate_payload(payload, "experiment-proposal-v0.schema.json")
    if payload.get("human_approval_required") is not True:
        raise ValueError("Stage 2G proposals require human_approval_required=true.")
    for field in FALSE_FIELDS:
        if payload.get(field) is not False:
            raise ValueError(f"Stage 2G proposals require {field}=false.")
    if "candidate_count_upper_bound" not in payload:
        raise ValueError("Experiment proposal requires candidate_count_upper_bound.")
    if int(payload["candidate_count_estimate"]) > int(payload["candidate_count_upper_bound"]):
        raise ValueError("Proposal candidate_count_estimate exceeds candidate_count_upper_bound.")
    validate_review_checklist(payload["review_checklist"], proposal_id=str(payload["proposal_id"]))
    corpus_slice = payload.get("corpus_slice", {})
    if not isinstance(corpus_slice, dict):
        raise ValueError("corpus_slice must be a mapping.")
    if (
        corpus_slice.get("slice_kind") == "future_unsolved_page_candidate"
        and payload.get("human_approval_required") is not True
    ):
        raise ValueError("Future unsolved page candidate proposals require human_approval_required=true.")
    if corpus_slice.get("slice_kind") == "future_unsolved_page_candidate" and corpus_slice.get("review_required") is not True:
        raise ValueError("Future unsolved page candidate proposals require review_required=true.")
    if _looks_like_raw_dump(source_text):
        raise ValueError("Experiment proposal appears to include raw corpus data.")


def _looks_like_raw_dump(text: str) -> bool:
    return len(text) > 30000 or "data/raw/" in text or text.count("\n") > 1400 or "BEGIN RAW" in text

