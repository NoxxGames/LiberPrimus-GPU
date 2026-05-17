"""Stage 3E bounded queue dry-run support."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_queue
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.method_backlog.counts import validate_candidate_count
from libreprimus.method_backlog.models import Stage3EDryRunResult, Stage3EDryRunSummary
from libreprimus.method_backlog.support import classify_executor_support
from libreprimus.method_backlog.validation import validate_stage3e_queue_item
from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable


def dry_run_stage3e_queue(
    *,
    policy_path: Path,
    queue_path: Path,
    out_dir: Path,
) -> Stage3EDryRunSummary:
    policy = load_operator_policy(policy_path)
    queue = load_bounded_queue(queue_path)
    checks = {check.item_id: check for check in check_queue(policy, queue)}
    results: list[Stage3EDryRunResult] = []
    for item in queue.items:
        validate_stage3e_queue_item(item)
        calculated = validate_candidate_count(item)
        support_status, support_reason = classify_executor_support(item)
        check = checks[str(item["item_id"])]
        executable = support_status == "runnable_now" and not check.blocking_reasons
        warnings = list(check.warnings)
        if support_status != "runnable_now":
            warnings.append(support_reason)
        results.append(
            Stage3EDryRunResult(
                item_id=str(item["item_id"]),
                experiment_kind=str(item["experiment_kind"]),
                declared_candidate_count=int(item["candidate_count_upper_bound"]),
                calculated_candidate_count=calculated,
                policy_status=check.status,
                implementation_status=str(item.get("implementation_status", support_status)),
                executor_status=support_status,
                executable_now=executable,
                blocking_reasons=list(check.blocking_reasons),
                warnings=warnings,
            )
        )
    summary = Stage3EDryRunSummary(
        queue_id=queue.queue_id,
        policy_id=policy.policy_id,
        item_count=len(results),
        total_candidate_estimate=sum(result.calculated_candidate_count for result in results),
        runnable_now_count=sum(1 for result in results if result.executor_status == "runnable_now"),
        needs_executor_count=sum(1 for result in results if result.executor_status == "needs_executor"),
        dry_run_only_count=sum(1 for result in results if result.executor_status == "dry_run_only"),
        blocked_count=sum(1 for result in results if result.policy_status == "fail" or result.executor_status == "blocked"),
        executed_count=0,
        results=results,
    )
    output_path = write_dry_run_summary(out_dir, summary)
    return Stage3EDryRunSummary(
        queue_id=summary.queue_id,
        policy_id=summary.policy_id,
        item_count=summary.item_count,
        total_candidate_estimate=summary.total_candidate_estimate,
        runnable_now_count=summary.runnable_now_count,
        needs_executor_count=summary.needs_executor_count,
        dry_run_only_count=summary.dry_run_only_count,
        blocked_count=summary.blocked_count,
        executed_count=summary.executed_count,
        results=summary.results,
        output_path=output_path,
    )


def write_dry_run_summary(out_dir: Path, summary: Stage3EDryRunSummary) -> Path:
    resolved = out_dir if out_dir.is_absolute() else repo_root() / out_dir
    resolved.mkdir(parents=True, exist_ok=True)
    path = resolved / "stage3e_queue_dry_run_summary.json"
    payload = to_jsonable(summary)
    payload["record_type"] = "stage3e_queue_dry_run_summary"
    payload["generated_at_utc"] = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload["git_commit"] = _git_commit()
    payload["solve_claim"] = False
    payload["cuda_used"] = False
    payload["generated_outputs_ignored"] = _is_ignored(path)
    payload.pop("output_path", None)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root(),
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def _is_ignored(path: Path) -> bool:
    try:
        relative = path.relative_to(repo_root())
    except ValueError:
        return False
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", str(relative)],
        cwd=repo_root(),
        check=False,
    )
    return result.returncode == 0
