"""Stage 4Q benchmark planning summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.cpu_smoke import run_cpu_smoke
from libreprimus.benchmark_planning.environment import build_environment_record
from libreprimus.benchmark_planning.export import resolve_repo_path, write_json, write_yaml
from libreprimus.benchmark_planning.models import (
    BENCHMARK_PLAN_TIERS,
    CPU_ONLY_POLICY,
    STAGE4Q_OUTPUT_DIR,
    STAGE4Q_PLAN_PATH,
    STAGE4Q_READINESS_PATH,
    STAGE4Q_SUMMARY_PATH,
    SUMMARY_JSON,
)
from libreprimus.benchmark_planning.parity_readiness import build_parity_readiness
from libreprimus.benchmark_planning.source_loaders import load_stage4o_summary, load_stage4p_summary


def build_benchmark_plan(
    *,
    out_dir: Path = STAGE4Q_OUTPUT_DIR,
    plan_out: Path = STAGE4Q_PLAN_PATH,
    readiness_out: Path = STAGE4Q_READINESS_PATH,
    summary_out: Path = STAGE4Q_SUMMARY_PATH,
) -> dict[str, Any]:
    """Build committed Stage 4Q plan/readiness/summary records plus ignored diagnostics."""

    environment = build_environment_record(out_dir=out_dir)
    smoke_records = run_cpu_smoke(out_dir=out_dir)
    readiness = build_parity_readiness(out_dir=out_dir, readiness_out=readiness_out)
    plan_records = [_plan_record(tier) for tier in BENCHMARK_PLAN_TIERS]
    write_yaml(plan_out, {"records": plan_records})

    stage4o = load_stage4o_summary()
    stage4p = load_stage4p_summary()
    summary = {
        "record_type": "stage4q_benchmark_parity_summary",
        "schema": "schemas/benchmarks/stage4q-benchmark-parity-summary-v0.schema.json",
        "stage_id": "stage-4q",
        "status": "complete",
        "benchmark_plan_records": len(plan_records),
        "parity_readiness_records": len(readiness),
        "cpu_smoke_records": len(smoke_records),
        "cpu_smoke_candidate_count": len(smoke_records),
        "cpu_smoke_result_count": sum(1 for record in smoke_records if record["benchmark_status"] == "smoke_passed"),
        "stage4o_parity_references_used": int(stage4o.get("parity_expectations_written", 0)),
        "stage4p_unified_result_references_used": int(stage4p.get("records_with_parity_expectations", 0)),
        "future_cuda_targets_ready": sum(
            1 for record in readiness if record["parity_gate_status"] == "ready_for_future_cuda_planning"
        ),
        "future_cuda_targets_blocked": sum(1 for record in readiness if record["benchmark_status"] == "blocked"),
        "skipped_non_cuda_targets": sum(
            1 for record in readiness if record["parity_gate_status"] == "skipped_not_cuda_target"
        ),
        "environment_record_written": bool(environment),
        "documentation_hygiene_checks_added": True,
        "readme_duplicates_fixed": True,
        "codex_output_ignored": True,
        "codex_output_staged": False,
        "benchmark_generated_outputs_ignored": True,
        "next_stage": "Stage 5A - CUDA planning and parity scaffolding only",
        "website_expansion_stage": "Stage 6",
        "notes": [
            "Stage 4Q records CPU benchmark and future parity planning only.",
            "Stage 4Q CPU smoke timings are diagnostics, not performance claims.",
            "CUDA implementation remains deferred until Stage 5 explicitly scopes scaffolding.",
        ],
        **CPU_ONLY_POLICY,
    }
    write_yaml(summary_out, summary)
    write_json(resolve_repo_path(out_dir) / SUMMARY_JSON, summary)
    return summary


def _plan_record(tier: dict[str, str]) -> dict[str, Any]:
    return {
        "record_type": "cpu_benchmark_plan",
        "stage_id": "stage-4q",
        "acceptance_gate": "planning_record_only",
        "future_execution_requires": [
            "explicit manifest",
            "raw-data-free input or approved fixture",
            "generated-output boundary verification",
            "no solve claim",
        ],
        **tier,
        **CPU_ONLY_POLICY,
    }
