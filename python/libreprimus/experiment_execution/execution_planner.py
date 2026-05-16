"""Build Stage 2F bounded CPU execution plans."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest
from libreprimus.experiment_execution.models import CPUExecutionPlan
from libreprimus.experiment_execution.safety_gates import (
    evaluate_execution_safety_gates,
    has_failure,
    warning_messages,
)
from libreprimus.experiment_execution.validation import validate_record
from libreprimus.solved_fixtures.models import to_jsonable

DETERMINISTIC_EXECUTION_TIMESTAMP = "1970-01-01T00:00:00Z"


def build_execution_plan(manifest_path: Path, *, out_dir: Path) -> CPUExecutionPlan:
    manifest = load_cpu_execution_manifest(manifest_path)
    gates = evaluate_execution_safety_gates(manifest, out_dir=out_dir)
    payload = manifest.payload
    manifest_id = manifest.manifest_id
    plan = CPUExecutionPlan(
        record_type="cpu_execution_plan",
        plan_id=f"{manifest_id}-execution-plan-{manifest.sha256[:12]}",
        manifest_id=manifest_id,
        manifest_sha256=manifest.sha256,
        generated_at_utc=DETERMINISTIC_EXECUTION_TIMESTAMP,
        git_commit=_git_commit(),
        execution_enabled=True,
        execution_scope=str(payload["execution_scope"]),
        unsolved_execution_allowed=False,
        search_execution_enabled=False,
        candidate_generation_enabled=False,
        scoring_enabled=False,
        cuda_enabled=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        transform_summary=_transform_summary(payload),
        input_summary=_input_summary(payload),
        safety_gate_results=[to_jsonable(gate) for gate in gates],
        output_paths=_output_paths(manifest_id, out_dir),
        result_store_preview=_result_store_preview(payload),
        warnings=warning_messages(gates),
        elapsed_ms=0.0,
    )
    validate_record(plan)
    if has_failure(gates):
        failed = [gate.gate_id for gate in gates if gate.is_failure]
        raise ValueError(f"CPU execution safety gates failed: {failed}")
    return plan


def _transform_summary(payload: dict[str, Any]) -> dict[str, Any]:
    transform_plan = payload["transform_plan"]
    return {
        "transform_id": transform_plan.get("transform_id"),
        "canonical_transform_id": transform_plan.get(
            "canonical_transform_id",
            transform_plan.get("transform_id"),
        ),
        "registered_cpu_reference_only": True,
    }


def _input_summary(payload: dict[str, Any]) -> dict[str, Any]:
    corpus_slice = payload["corpus_slice"]
    synthetic = payload.get("synthetic_corpus_record")
    return {
        "slice_id": corpus_slice.get("slice_id"),
        "slice_kind": corpus_slice.get("slice_kind"),
        "execution_scope": payload.get("execution_scope"),
        "synthetic_id": synthetic.get("synthetic_id") if isinstance(synthetic, dict) else None,
        "fixture_manifest": corpus_slice.get("manifest_path"),
        "expected_pass_count": corpus_slice.get("expected_pass_count"),
    }


def _output_paths(manifest_id: str, out_dir: Path) -> dict[str, str]:
    return {
        "execution_plan": str(out_dir / f"{manifest_id}-execution-plan.json"),
        "execution_results": str(out_dir / f"{manifest_id}-execution-results.jsonl"),
        "summary": str(out_dir / f"{manifest_id}-summary.json"),
        "aggregate_summary": str(out_dir / "summary.json"),
    }


def _result_store_preview(payload: dict[str, Any]) -> dict[str, Any]:
    policy = payload.get("result_store_policy", {})
    return {
        "mode": policy.get("mode", "preview_only"),
        "import_enabled": False,
        "committed_outputs": False,
    }


def _git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"

