"""Validation helpers for Stage 3V OutGuess regression."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.stego.outguess_export import read_json, resolve_path
from libreprimus.stego.outguess_manifest import validate_manifest_and_artifacts


def validate_results(results_dir: Path, *, allow_missing: bool = False) -> tuple[dict[str, Any], list[str]]:
    """Validate generated OutGuess regression result files."""
    resolved = resolve_path(results_dir)
    if not resolved.exists():
        if allow_missing:
            return {"results_present": False}, []
        return {}, [f"results directory missing: {resolved}"]
    summary_path = resolved / "summary.json"
    if not summary_path.is_file():
        if allow_missing:
            return {"results_present": False}, []
        return {}, [f"summary missing: {summary_path}"]
    summary = read_json(summary_path)
    errors: list[str] = []
    if summary.get("record_type") != "outguess_regression_summary":
        errors.append("summary record_type must be outguess_regression_summary")
    for key in ("raw_payloads_committed", "solve_claim", "cuda_used"):
        if summary.get(key) is not False:
            errors.append(f"summary {key} must be false")
    return summary, errors


__all__ = ["validate_manifest_and_artifacts", "validate_results"]
