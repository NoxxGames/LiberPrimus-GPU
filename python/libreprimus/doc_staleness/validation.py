"""Validation helpers for doc-staleness records."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_record(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return payload


def validate_stage5ab_summary(path: Path) -> list[str]:
    payload = load_record(path)
    errors: list[str] = []
    expected_false = (
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
        "website_expansion_performed",
        "raw_data_processed",
        "generated_outputs_committed",
        "codex_output_committed",
        "solve_claim",
    )
    for key in expected_false:
        if payload.get(key) is not False:
            errors.append(f"{key} must be false")
    if payload.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added must be 0")
    if payload.get("next_selected_stage") != "Stage 5AC - selected from Stage 5AA outcome after stale-doc repair":
        errors.append("next_selected_stage must be Stage 5AC selected from Stage 5AA outcome")
    return errors
