"""Export Stage 2F CPU execution outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.experiment_execution.models import CPUExecutionPlan, CPUExecutionResult
from libreprimus.solved_fixtures.models import to_jsonable


def write_execution_outputs(
    out_dir: Path,
    plan: CPUExecutionPlan,
    results: list[CPUExecutionResult],
    summary: dict[str, Any],
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    plan_path = out_dir / f"{plan.manifest_id}-execution-plan.json"
    results_path = out_dir / f"{plan.manifest_id}-execution-results.jsonl"
    summary_path = out_dir / f"{plan.manifest_id}-summary.json"
    plan_path.write_text(
        json.dumps(to_jsonable(plan), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    results_path.write_text(
        "".join(json.dumps(to_jsonable(result), sort_keys=True) + "\n" for result in results),
        encoding="utf-8",
    )
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "execution_plan": plan_path,
        "execution_results": results_path,
        "summary": summary_path,
    }


def write_aggregate_summary(out_dir: Path, summaries: list[dict[str, Any]]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "record_type": "cpu_execution_aggregate_summary",
        "manifest_count": len(summaries),
        "result_count": sum(int(summary.get("result_count", 0)) for summary in summaries),
        "pass_count": sum(int(summary.get("pass_count", 0)) for summary in summaries),
        "fail_count": sum(int(summary.get("fail_count", 0)) for summary in summaries),
        "error_count": sum(int(summary.get("error_count", 0)) for summary in summaries),
        "skipped_count": sum(int(summary.get("skipped_count", 0)) for summary in summaries),
        "search_performed_any": any(summary.get("search_performed_any") for summary in summaries),
        "candidate_generation_performed_any": any(
            summary.get("candidate_generation_performed_any") for summary in summaries
        ),
        "scoring_used_any": any(summary.get("scoring_used_any") for summary in summaries),
        "cuda_used_any": any(summary.get("cuda_used_any") for summary in summaries),
        "unsolved_execution_allowed_any": any(
            summary.get("unsolved_execution_allowed_any") for summary in summaries
        ),
        "summaries": summaries,
    }
    path = out_dir / "summary.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

