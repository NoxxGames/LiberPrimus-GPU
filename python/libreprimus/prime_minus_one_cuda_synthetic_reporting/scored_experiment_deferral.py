"""Build scored-experiment deferral records for Stage 5AC."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import OUTPUT_DIR, REPORT_FILES, SCORED_EXPERIMENT_DEFERRAL_PATH, base_record

DEFERRALS = (
    ("bounded_cpu_native_scored_experiment", "deferred_manifest_gate_required"),
    ("bounded_solved_fixture_score_regression", "deferred_manifest_gate_required"),
    ("bounded_unsolved_page_micro_pilot", "blocked"),
    ("cuda_scored_experiment", "blocked_pending_cuda_contract_and_parity"),
    ("benchmark_experiment", "blocked_pending_benchmark_planning_stage"),
    ("website_expansion", "deferred_future_unnumbered_project"),
)


def build_scored_experiment_deferral(
    *,
    scored_experiment_deferral_out: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = []
    for index, (experiment_class, status) in enumerate(DEFERRALS, start=1):
        records.append(
            base_record(
                "prime_minus_one_cuda_synthetic_scored_experiment_deferral_record",
                "schemas/cuda/prime-minus-one-cuda-synthetic-scored-experiment-deferral-record-v0.schema.json",
                deferral_record_id=f"stage5ac-scored-deferral-{index:02d}",
                experiment_class=experiment_class,
                deferral_status=status,
                website_expansion_status="deferred_future_unnumbered_project" if experiment_class == "website_expansion" else "not_applicable",
                execution_enabled=False,
                benchmark_execution_allowed=False,
                scored_experiment_execution_allowed=False,
                scored_experiment_executed=False,
                requires_manifest_gate=experiment_class in {"bounded_cpu_native_scored_experiment", "bounded_solved_fixture_score_regression"},
                requires_null_controls=experiment_class not in {"benchmark_experiment", "website_expansion"},
                requires_operator_approval=True,
                blockers=[] if status.startswith("deferred") else [status],
            )
        )
    write_records(scored_experiment_deferral_out, records)
    write_json_report(out_dir, REPORT_FILES["scored_deferral"], {"records": records})
    return records
