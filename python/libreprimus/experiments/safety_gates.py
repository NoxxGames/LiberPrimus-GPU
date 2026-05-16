"""Safety gates for Stage 2E dry-run-only exploratory manifests."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from libreprimus.experiments.models import CandidateEstimate, SafetyGateResult
from libreprimus.paths import repo_root


def evaluate_safety_gates(
    manifest_payload: dict[str, Any],
    estimate: CandidateEstimate,
    *,
    out_dir: Path,
) -> list[SafetyGateResult]:
    gates: list[SafetyGateResult] = []
    gates.append(_gate("dry_run_only", True, manifest_payload.get("dry_run_only")))
    for field in [
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        gates.append(_gate(field, False, manifest_payload.get(field)))
    upper_bound = manifest_payload.get("expected_candidate_count_upper_bound")
    gates.append(_gate("candidate_count_upper_bound_present", "present", upper_bound is not None))
    gates.append(
        _gate(
            "candidate_count_within_bound",
            f"<= {upper_bound}",
            estimate.candidate_count <= int(upper_bound or -1),
        )
    )
    corpus_slice = manifest_payload.get("corpus_slice", {})
    review_required = corpus_slice.get("review_required")
    gates.append(
        _gate(
            "future_unsolved_slice_review_required",
            True,
            corpus_slice.get("slice_kind") != "future_unsolved_page_candidate"
            or review_required is True,
        )
    )
    gates.append(_output_path_gate(out_dir))
    result_store_policy = manifest_payload.get("result_store_policy", {})
    gates.append(
        _gate(
            "result_store_preview_only",
            "preview_only",
            result_store_policy.get("mode") in {"preview_only", "dry_run_preview"},
        )
    )
    return gates


def has_failure(gates: list[SafetyGateResult]) -> bool:
    return any(gate.is_failure for gate in gates)


def warning_messages(gates: list[SafetyGateResult]) -> list[str]:
    return [gate.message for gate in gates if gate.is_warning]


def _gate(gate_id: str, required_value: Any, actual_value: Any) -> SafetyGateResult:
    passed = actual_value == required_value or actual_value is True and isinstance(required_value, str)
    return SafetyGateResult(
        gate_id=gate_id,
        gate_name=gate_id.replace("_", " "),
        required_value=required_value,
        actual_value=actual_value,
        status="pass" if passed else "fail",
        severity="info" if passed else "error",
        message=f"{gate_id} {'passed' if passed else 'failed'}.",
    )


def _output_path_gate(out_dir: Path) -> SafetyGateResult:
    resolved = out_dir if out_dir.is_absolute() else repo_root() / out_dir
    root = repo_root()
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return SafetyGateResult(
            gate_id="output_path_policy",
            gate_name="output path policy",
            required_value="ignored generated directory or external temp",
            actual_value=str(resolved),
            status="pass",
            severity="info",
            message="Output path is outside the repository and treated as temporary dry-run output.",
        )
    ignored = _is_ignored(root, str(relative / "summary.json"))
    return SafetyGateResult(
        gate_id="output_path_policy",
        gate_name="output path policy",
        required_value="ignored generated directory",
        actual_value=str(relative),
        status="pass" if ignored else "fail",
        severity="info" if ignored else "error",
        message="Output path is ignored." if ignored else "Output path is not ignored.",
    )


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
