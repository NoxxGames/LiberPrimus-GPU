"""Scored-experiment and adjacent deferral records for Stage 5AD."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import OUTPUT_DIR, REPORT_FILES, SCORED_EXPERIMENT_DEFERRAL_PATH, base_record

DEFERRALS = [
    ("bounded_cpu_native_scored_experiment", "deferred_manifest_gate_required"),
    ("bounded_solved_fixture_score_regression", "deferred_manifest_gate_required"),
    ("bounded_unsolved_page_micro_pilot", "blocked"),
    ("cuda_scored_experiment", "blocked_pending_cuda_parity_and_manifest_gate"),
    ("benchmark_experiment", "blocked_pending_benchmark_planning_stage"),
    ("website_expansion", "deferred_future_unnumbered_project"),
    ("visual_clue_deep_research", "deferred_future_review"),
]


def build_scored_experiment_deferral(
    *, scored_experiment_deferral_out: Path = SCORED_EXPERIMENT_DEFERRAL_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    records = [
        base_record(
            "bounded_p56_cuda_scored_experiment_deferral_record",
            "schemas/cuda/bounded-p56-cuda-scored-experiment-deferral-record-v0.schema.json",
            deferral_id=f"stage5ad-deferral-{experiment_class}",
            experiment_class=experiment_class,
            deferral_status=status,
            execution_enabled=False,
            cuda_execution_allowed=False,
            benchmark_execution_allowed=False,
            scored_experiment_execution_allowed=False,
            generated_body_publication_allowed=False,
            rationale="Stage 5AD is limited to exact bounded p56 CUDA parity metadata.",
        )
        for experiment_class, status in DEFERRALS
    ]
    write_records(scored_experiment_deferral_out, records)
    write_json_report(out_dir, REPORT_FILES["scored_deferral"], {"records": records})
    return records
