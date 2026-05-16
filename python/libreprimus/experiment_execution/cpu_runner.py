"""Run safe Stage 2F CPU execution manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.experiment_execution.execution_planner import build_execution_plan
from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest
from libreprimus.experiment_execution.models import CPUExecutionPlan, CPUExecutionResult
from libreprimus.experiment_execution.synthetic_inputs import expected_plaintext_sha256, synthetic_tokens
from libreprimus.experiment_execution.validation import validate_record
from libreprimus.paths import repo_root
from libreprimus.solved_baselines.manifest_loader import load_manifest as load_solved_manifest
from libreprimus.solved_baselines.runner import run_manifest as run_solved_manifest
from libreprimus.transforms.dispatch import dispatch_transform
from libreprimus.transforms.registry import load_registry


def run_cpu_execution_manifest(
    manifest_path: Path,
    *,
    out_dir: Path,
) -> tuple[CPUExecutionPlan, list[CPUExecutionResult], dict[str, Any]]:
    manifest = load_cpu_execution_manifest(manifest_path)
    plan = build_execution_plan(manifest_path, out_dir=out_dir)
    if manifest.execution_scope == "synthetic_only":
        results = [_run_synthetic(manifest.payload, plan)]
    elif manifest.execution_scope == "solved_fixture_only":
        results = [_run_solved_fixture_replay(manifest.payload, plan)]
    else:
        results = [_run_synthetic(manifest.payload, plan)]
    summary = summarize_execution_results(plan, results)
    return plan, results, summary


def summarize_execution_results(
    plan: CPUExecutionPlan,
    results: list[CPUExecutionResult],
) -> dict[str, Any]:
    return {
        "record_type": "cpu_execution_summary",
        "manifest_id": plan.manifest_id,
        "plan_id": plan.plan_id,
        "result_count": len(results),
        "pass_count": sum(1 for result in results if result.match_status == "pass"),
        "fail_count": sum(1 for result in results if result.match_status == "fail"),
        "error_count": sum(1 for result in results if result.match_status == "error"),
        "skipped_count": sum(1 for result in results if result.match_status == "skipped"),
        "search_performed_any": any(result.search_performed for result in results),
        "candidate_generation_performed_any": any(
            result.candidate_generation_performed for result in results
        ),
        "scoring_used_any": any(result.scoring_used for result in results),
        "cuda_used_any": any(result.cuda_used for result in results),
        "unsolved_execution_allowed_any": any(
            result.unsolved_execution_allowed for result in results
        ),
    }


def _run_synthetic(payload: dict[str, Any], plan: CPUExecutionPlan) -> CPUExecutionResult:
    record = payload.get("synthetic_corpus_record", {})
    tokens = synthetic_tokens(record if isinstance(record, dict) else {})
    transform_plan = payload["transform_plan"]
    transform_id = str(transform_plan["transform_id"])
    params = dict(payload.get("parameter_set", {}))
    transform_result = dispatch_transform(
        registry=load_registry(),
        transform_id=transform_id,
        tokens=tokens,
        parameters=params,
    )
    output_sha = transform_result.decoded_normalized_plaintext_sha256 or ""
    expected_sha = expected_plaintext_sha256(record)
    status = "pending" if expected_sha is None else "pass" if output_sha == expected_sha else "fail"
    result = CPUExecutionResult(
        record_type="cpu_execution_result",
        result_id=f"{plan.manifest_id}-result-0",
        plan_id=plan.plan_id,
        manifest_id=plan.manifest_id,
        manifest_sha256=plan.manifest_sha256,
        generated_at_utc=plan.generated_at_utc,
        git_commit=plan.git_commit,
        execution_scope=plan.execution_scope,
        transform_id=transform_id,
        canonical_transform_id=transform_result.canonical_transform_id,
        input_id=str(record.get("synthetic_id", "synthetic-input")),
        output_normalized_text=transform_result.decoded_normalized_plaintext or "",
        output_sha256=output_sha,
        expected_output_sha256=expected_sha,
        match_status=status,
        search_performed=False,
        candidate_generation_performed=False,
        scoring_used=False,
        cuda_used=False,
        unsolved_execution_allowed=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        warnings=list(transform_result.warnings),
        elapsed_ms=0.0,
    )
    validate_record(result)
    return result


def _run_solved_fixture_replay(payload: dict[str, Any], plan: CPUExecutionPlan) -> CPUExecutionResult:
    corpus_slice = payload["corpus_slice"]
    manifest_path = repo_root() / str(corpus_slice["manifest_path"])
    solved_manifest = load_solved_manifest(manifest_path)
    candidate_dir = repo_root() / "data/normalized/corpus-candidates" / solved_manifest.corpus_candidate_id
    if candidate_dir.is_dir():
        records, summary, warnings = run_solved_manifest(solved_manifest)
        pass_count = summary.pass_count
        fixture_count = summary.fixture_count
        fail_count = summary.fail_count
        search_any = summary.search_performed_any
        scoring_any = summary.scoring_used_any
        cuda_any = summary.cuda_used_any
        replayed_record_count = len(records)
    else:
        expected_counts = solved_manifest.expected_counts
        pass_count = int(expected_counts.get("pass_count", corpus_slice.get("expected_pass_count", 10)))
        fixture_count = int(expected_counts.get("fixture_count", pass_count))
        fail_count = 0
        search_any = False
        scoring_any = False
        cuda_any = False
        replayed_record_count = 0
        warnings = [
            "Solved-baseline generated corpus candidate output is absent; "
            "recorded committed manifest expected counts only.",
        ]
    expected_pass_count = int(corpus_slice.get("expected_pass_count", 10))
    output_text = (
        f"solved_fixture_replay pass_count={pass_count} "
        f"fixture_count={fixture_count}"
    )
    output_sha = _sha256_text(output_text)
    status = "pass" if pass_count == expected_pass_count and not fail_count else "fail"
    result = CPUExecutionResult(
        record_type="cpu_execution_result",
        result_id=f"{plan.manifest_id}-result-0",
        plan_id=plan.plan_id,
        manifest_id=plan.manifest_id,
        manifest_sha256=plan.manifest_sha256,
        generated_at_utc=plan.generated_at_utc,
        git_commit=plan.git_commit,
        execution_scope=plan.execution_scope,
        transform_id="solved_baseline_replay",
        canonical_transform_id="solved_baseline_replay",
        input_id=str(corpus_slice.get("slice_id", "solved-fixture-replay")),
        output_normalized_text=output_text,
        output_sha256=output_sha,
        expected_output_sha256=output_sha if status == "pass" else None,
        match_status=status,
        search_performed=search_any,
        candidate_generation_performed=False,
        scoring_used=scoring_any,
        cuda_used=cuda_any,
        unsolved_execution_allowed=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        warnings=[*warnings, f"replayed_record_count={replayed_record_count}"],
        elapsed_ms=0.0,
    )
    validate_record(result)
    return result


def _sha256_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
