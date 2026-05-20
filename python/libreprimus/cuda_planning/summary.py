"""Stage 5A CUDA planning aggregate summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_json, write_yaml
from libreprimus.cuda_planning.loaders import load_stage4o_summary, load_stage4p_summary, load_stage4q_summary
from libreprimus.cuda_planning.models import (
    CUDA_PLANNING_POLICY,
    IMPLEMENTATION_GATES_PATH,
    NON_TARGETS_PATH,
    PARITY_SCAFFOLD_PATH,
    STAGE5A_OUTPUT_DIR,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    TARGET_PLAN_PATH,
)


def build_summary(
    *,
    out_dir: Path = STAGE5A_OUTPUT_DIR,
    target_plan_path: Path = TARGET_PLAN_PATH,
    parity_scaffold_path: Path = PARITY_SCAFFOLD_PATH,
    implementation_gates_path: Path = IMPLEMENTATION_GATES_PATH,
    non_targets_path: Path = NON_TARGETS_PATH,
    summary_out: Path = SUMMARY_PATH,
) -> dict[str, Any]:
    targets = list(read_yaml(target_plan_path).get("records", []))
    scaffolds = list(read_yaml(parity_scaffold_path).get("records", []))
    gates = list(read_yaml(implementation_gates_path).get("records", []))
    non_targets = list(read_yaml(non_targets_path).get("records", []))
    stage4q = load_stage4q_summary()
    stage4o = load_stage4o_summary()
    stage4p = load_stage4p_summary()
    ready_targets = sum(1 for record in targets if record.get("target_status") == "ready_for_planning")
    blocked_targets = sum(1 for record in targets if str(record.get("target_status", "")).startswith("blocked"))
    summary = {
        "record_type": "stage5a_cuda_planning_summary",
        "schema": "schemas/cuda/cuda-planning-summary-v0.schema.json",
        "stage_id": "stage-5a",
        "status": "complete",
        "target_plan_records": len(targets),
        "ready_targets": ready_targets,
        "blocked_targets": blocked_targets,
        "non_cuda_target_plan_records": sum(1 for record in targets if record.get("target_status") == "non_cuda_target"),
        "non_target_records": len(non_targets),
        "parity_scaffold_records": len(scaffolds),
        "implementation_gate_records": len(gates),
        "satisfied_gates": sum(1 for record in gates if record.get("implementation_gate_status") == "satisfied"),
        "blocked_deferred_gates": sum(
            1 for record in gates if record.get("implementation_gate_status") in {"blocked", "deferred"}
        ),
        "stage4o_parity_references_used": int(stage4o.get("parity_expectations_written", 0)),
        "stage4p_unified_result_references_used": int(stage4p.get("records_with_parity_expectations", 0)),
        "stage4q_ready_targets": int(stage4q.get("future_cuda_targets_ready", 0)),
        "stage4q_blocked_targets": int(stage4q.get("future_cuda_targets_blocked", 0)),
        "stage4q_skipped_non_cuda_targets": int(stage4q.get("skipped_non_cuda_targets", 0)),
        "next_stage": "Stage 5B - CUDA parity harness skeleton",
        "website_expansion_stage": "Stage 6",
        "notes": [
            "Stage 5A is CUDA planning and parity scaffolding only.",
            "No CUDA source, kernels, GPU benchmarks, speedup claims, broad experiments, raw-data processing, or solve claims were added.",
            "Future CUDA work must cite Stage 5A target and gate records.",
        ],
        **CUDA_PLANNING_POLICY,
    }
    write_yaml(summary_out, summary)
    write_json(out_dir / SUMMARY_REPORT, summary)
    return summary
