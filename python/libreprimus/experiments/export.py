"""Export generated Stage 2E dry-run plan outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.experiments.models import DryRunPlan
from libreprimus.solved_fixtures.models import to_jsonable


def write_dry_run_outputs(out_dir: Path, plan: DryRunPlan) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = to_jsonable(plan)
    plan_path = out_dir / f"{plan.manifest_id}-dry-run-plan.json"
    gates_path = out_dir / f"{plan.manifest_id}-safety-gates.jsonl"
    plan_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    gates_path.write_text(
        "".join(
            json.dumps(gate, sort_keys=True) + "\n"
            for gate in payload["safety_gate_results"]
        ),
        encoding="utf-8",
    )
    return {"dry_run_plan": plan_path, "safety_gates": gates_path}


def write_summary(out_dir: Path, plans: list[DryRunPlan]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "record_type": "exploratory_dry_run_summary",
        "plan_count": len(plans),
        "manifest_ids": [plan.manifest_id for plan in plans],
        "candidate_count_total": sum(plan.candidate_count_estimate for plan in plans),
        "safety_gate_pass_count": sum(
            1
            for plan in plans
            for gate in plan.safety_gate_results
            if gate.get("status") == "pass"
        ),
        "safety_gate_fail_count": sum(
            1
            for plan in plans
            for gate in plan.safety_gate_results
            if gate.get("status") == "fail"
        ),
        "execution_enabled_any": any(plan.execution_enabled for plan in plans),
        "search_execution_enabled_any": any(plan.search_execution_enabled for plan in plans),
        "scoring_enabled_any": any(plan.scoring_enabled for plan in plans),
        "cuda_enabled_any": any(plan.cuda_enabled for plan in plans),
    }
    path = out_dir / "summary.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
