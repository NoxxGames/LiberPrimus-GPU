"""Export generated Stage 2J bounded auto-run records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.bounded_experiments.models import BoundedAutoRunResult, PolicyCheckResult
from libreprimus.bounded_experiments.validation import (
    validate_bounded_auto_run_result,
    validate_policy_check_result,
)
from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable


def _resolve_output_dir(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_policy_check_results(out_dir: Path, checks: list[PolicyCheckResult]) -> Path:
    resolved = _resolve_output_dir(out_dir)
    payload = [validate_policy_check_result(check) for check in checks]
    return write_json(resolved / "policy-check-results.json", payload)


def write_run_result(out_dir: Path, result: BoundedAutoRunResult) -> Path:
    resolved = _resolve_output_dir(out_dir)
    payload = validate_bounded_auto_run_result(result)
    return write_json(resolved / f"{result.item_id}-bounded-auto-run-result.json", payload)


def write_summary(
    out_dir: Path,
    results: list[BoundedAutoRunResult],
    checks: list[PolicyCheckResult],
    *,
    filename: str = "summary.json",
) -> Path:
    resolved = _resolve_output_dir(out_dir)
    payload = build_summary_payload(results, checks)
    return write_json(resolved / filename, payload)


def build_summary_payload(results: list[BoundedAutoRunResult], checks: list[PolicyCheckResult]) -> dict[str, Any]:
    return {
        "record_type": "bounded_auto_run_summary",
        "item_count": len(checks),
        "policy_pass_count": sum(1 for check in checks if check.status in {"pass", "warning"} and not check.blocking_reasons),
        "policy_blocked_count": sum(1 for check in checks if check.blocking_reasons),
        "executed_count": sum(1 for result in results if result.execution_performed),
        "deferred_count": sum(1 for result in results if result.execution_status == "deferred"),
        "blocked_count": sum(1 for result in results if result.execution_status == "blocked"),
        "result_count": len(results),
        "candidate_count_total": sum(result.candidate_count for result in results),
        "search_performed": any(result.search_performed for result in results),
        "scoring_used": any(result.scoring_used for result in results),
        "cuda_used": False,
        "solve_claim_made": False,
        "results": [
            {
                "item_id": result.item_id,
                "execution_status": result.execution_status,
                "execution_performed": result.execution_performed,
                "deferred_reason": result.deferred_reason,
                "candidate_count": result.candidate_count,
            }
            for result in results
        ],
    }
