"""Export generated Stage 2H approval-gated execution records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.approval_execution.models import ApprovalGatedExecutionPlan, ApprovalGatedExecutionResult
from libreprimus.approval_execution.validation import validate_record
from libreprimus.solved_fixtures.models import to_jsonable


def write_approval_execution_outputs(
    out_dir: Path,
    plan: ApprovalGatedExecutionPlan,
    result: ApprovalGatedExecutionResult | None,
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    plan_path = out_dir / f"{plan.request_id}-plan.json"
    _write_json(plan_path, validate_record(plan))
    paths = {"plan": plan_path}
    if result is not None:
        result_path = out_dir / f"{plan.request_id}-result.json"
        _write_json(result_path, validate_record(result))
        paths["result"] = result_path
    return paths


def write_summary(out_dir: Path, results: list[ApprovalGatedExecutionResult]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = summarize_approval_execution_results(results)
    path = out_dir / "summary.json"
    _write_json(path, summary)
    return path


def summarize_approval_execution_results(results: list[ApprovalGatedExecutionResult]) -> dict[str, Any]:
    return {
        "record_type": "approval_gated_execution_summary",
        "request_count": len(results),
        "execution_result_count": len(results),
        "pass_count": sum(1 for item in results if item.execution_status == "pass"),
        "fail_count": sum(1 for item in results if item.execution_status == "fail"),
        "blocked_count": sum(1 for item in results if item.execution_status == "blocked"),
        "skipped_count": sum(1 for item in results if item.execution_status == "skipped"),
        "approved_synthetic_pass_count": sum(
            1 for item in results if item.execution_scope == "synthetic_only" and item.execution_status == "pass"
        ),
        "approved_solved_pass_count": sum(
            1 for item in results if item.execution_scope == "solved_fixture_only" and item.execution_status == "pass"
        ),
        "search_performed_any": any(item.search_performed for item in results),
        "candidate_generation_performed_any": any(item.candidate_generation_performed for item in results),
        "scoring_used_any": any(item.scoring_used for item in results),
        "cuda_used_any": any(item.cuda_used for item in results),
        "unsolved_execution_allowed_any": any(item.unsolved_execution_allowed for item in results),
    }


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")

