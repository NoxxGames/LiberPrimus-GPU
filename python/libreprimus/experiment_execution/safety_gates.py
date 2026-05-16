"""Safety gates for Stage 2F bounded CPU execution."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from libreprimus.experiment_execution.models import CPUExecutionManifest, ExecutionSafetyGateResult
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import load_registry, resolve_transform


def evaluate_execution_safety_gates(
    manifest: CPUExecutionManifest,
    *,
    out_dir: Path,
) -> list[ExecutionSafetyGateResult]:
    payload = manifest.payload
    gates: list[ExecutionSafetyGateResult] = []
    gates.append(_gate("execution_enabled", True, payload.get("execution_enabled")))
    gates.append(
        _gate(
            "execution_scope_allowed",
            "synthetic_or_solved_fixture_only",
            payload.get("execution_scope")
            in {"synthetic_only", "solved_fixture_only", "synthetic_and_solved_fixture_only"},
        )
    )
    for field in [
        "unsolved_execution_allowed",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        gates.append(_gate(field, False, payload.get(field)))
    gates.append(_corpus_slice_gate(payload))
    gates.append(_output_path_gate(out_dir))
    gates.extend(_transform_gates(payload))
    return gates


def has_failure(gates: list[ExecutionSafetyGateResult]) -> bool:
    return any(gate.is_failure for gate in gates)


def warning_messages(gates: list[ExecutionSafetyGateResult]) -> list[str]:
    return [gate.message for gate in gates if gate.is_warning]


def _gate(gate_id: str, required_value: Any, actual_value: Any) -> ExecutionSafetyGateResult:
    passed = actual_value == required_value or (
        isinstance(required_value, str) and actual_value is True
    )
    return ExecutionSafetyGateResult(
        gate_id=gate_id,
        gate_name=gate_id.replace("_", " "),
        required_value=required_value,
        actual_value=actual_value,
        status="pass" if passed else "fail",
        severity="info" if passed else "error",
        message=f"{gate_id} {'passed' if passed else 'failed'}.",
    )


def _corpus_slice_gate(payload: dict[str, Any]) -> ExecutionSafetyGateResult:
    corpus_slice = payload.get("corpus_slice", {})
    slice_kind = corpus_slice.get("slice_kind") if isinstance(corpus_slice, dict) else None
    if slice_kind == "future_unsolved_page_candidate":
        passed = False
    elif slice_kind == "page_candidate":
        passed = corpus_slice.get("solved_fixture_only") is True
    else:
        passed = slice_kind in {"synthetic", "solved_fixture_group"}
    return _gate("corpus_slice_safe", "synthetic_or_solved_fixture_only", passed)


def _output_path_gate(out_dir: Path) -> ExecutionSafetyGateResult:
    resolved = out_dir if out_dir.is_absolute() else repo_root() / out_dir
    root = repo_root()
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return ExecutionSafetyGateResult(
            gate_id="output_path_policy",
            gate_name="output path policy",
            required_value="ignored generated directory",
            actual_value=str(resolved),
            status="fail",
            severity="error",
            message="Output path is outside the repository and is not the Stage 2F ignored output area.",
        )
    ignored = _is_ignored(root, str(relative / "summary.json"))
    return ExecutionSafetyGateResult(
        gate_id="output_path_policy",
        gate_name="output path policy",
        required_value="ignored generated directory",
        actual_value=str(relative),
        status="pass" if ignored else "fail",
        severity="info" if ignored else "error",
        message="Output path is ignored." if ignored else "Output path is not ignored.",
    )


def _transform_gates(payload: dict[str, Any]) -> list[ExecutionSafetyGateResult]:
    transform_id = str(payload.get("transform_plan", {}).get("transform_id", ""))
    if transform_id == "solved_baseline_replay":
        return [_gate("transform_registered_or_replay", "registered_or_solved_replay", True)]
    try:
        registry = load_registry()
        definition = resolve_transform(registry, transform_id)
    except Exception as exc:  # noqa: BLE001 - converted into safety gate failure.
        return [
            ExecutionSafetyGateResult(
                gate_id="transform_registered",
                gate_name="transform registered",
                required_value="registered CPU transform",
                actual_value=transform_id,
                status="fail",
                severity="error",
                message=str(exc),
            )
        ]
    return [
        _gate("transform_registered", "registered CPU transform", True),
        _gate("transform_cpu_reference", True, definition.supports_cpu_reference),
        _gate("transform_search_disabled", False, definition.search_enabled),
        _gate("transform_gpu_disabled", False, definition.supports_gpu),
    ]


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

