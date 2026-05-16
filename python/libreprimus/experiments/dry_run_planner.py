"""Stage 2E exploratory experiment dry-run planner."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from libreprimus.experiments.candidate_estimator import estimate_candidate_count
from libreprimus.experiments.manifest_loader import load_exploratory_manifest
from libreprimus.experiments.models import DryRunPlan
from libreprimus.experiments.safety_gates import evaluate_safety_gates, has_failure, warning_messages
from libreprimus.experiments.validation import validate_record
from libreprimus.solved_fixtures.models import to_jsonable

DETERMINISTIC_DRY_RUN_TIMESTAMP = "1970-01-01T00:00:00Z"


def build_dry_run_plan(manifest_path: Path, *, out_dir: Path) -> DryRunPlan:
    manifest = load_exploratory_manifest(manifest_path)
    estimate = estimate_candidate_count(manifest.payload)
    gates = evaluate_safety_gates(manifest.payload, estimate, out_dir=out_dir)
    manifest_id = manifest.manifest_id
    plan = DryRunPlan(
        record_type="exploratory_dry_run_plan",
        plan_id=f"{manifest_id}-dry-run-{manifest.sha256[:12]}",
        manifest_id=manifest_id,
        manifest_sha256=manifest.sha256,
        generated_at_utc=DETERMINISTIC_DRY_RUN_TIMESTAMP,
        git_commit=_git_commit(),
        dry_run_only=True,
        execution_enabled=False,
        search_execution_enabled=False,
        candidate_generation_enabled=False,
        scoring_enabled=False,
        cuda_enabled=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        corpus_slice_summary=_corpus_slice_summary(manifest.payload),
        transform_space_summary=_transform_space_summary(manifest.payload, estimate),
        candidate_count_estimate=estimate.candidate_count,
        candidate_count_upper_bound=int(manifest.payload["expected_candidate_count_upper_bound"]),
        safety_gate_results=[to_jsonable(gate) for gate in gates],
        warnings=warning_messages(gates),
        output_paths=_output_paths(manifest_id, out_dir),
        result_store_preview=_result_store_preview(manifest.payload),
        elapsed_ms=0.0,
    )
    validate_record(plan)
    if has_failure(gates):
        failed = [gate.gate_id for gate in gates if gate.is_failure]
        raise ValueError(f"Exploratory dry-run safety gates failed: {failed}")
    return plan


def _corpus_slice_summary(payload: dict[str, Any]) -> dict[str, Any]:
    corpus_slice = payload["corpus_slice"]
    return {
        "slice_id": corpus_slice["slice_id"],
        "slice_kind": corpus_slice["slice_kind"],
        "corpus_candidate_id": corpus_slice["corpus_candidate_id"],
        "review_required": corpus_slice["review_required"],
        "canonical_corpus_active": corpus_slice["canonical_corpus_active"],
        "page_boundaries_final": corpus_slice["page_boundaries_final"],
    }


def _transform_space_summary(payload: dict[str, Any], estimate) -> dict[str, Any]:
    transform_plan = payload["transform_plan"]
    return {
        "transform_space_id": transform_plan["transform_space_id"],
        "transform_family": transform_plan["transform_family"],
        "registered_transform_id": transform_plan.get("registered_transform_id"),
        "execution_supported": transform_plan["execution_supported"],
        "dry_run_supported": transform_plan["dry_run_supported"],
        "candidate_count_formula": estimate.candidate_count_formula,
        "parameter_summary": estimate.parameter_summary,
    }


def _output_paths(manifest_id: str, out_dir: Path) -> dict[str, str]:
    return {
        "dry_run_plan": str(out_dir / f"{manifest_id}-dry-run-plan.json"),
        "safety_gates": str(out_dir / f"{manifest_id}-safety-gates.jsonl"),
        "summary": str(out_dir / "summary.json"),
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
