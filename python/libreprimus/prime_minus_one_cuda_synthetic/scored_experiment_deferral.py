"""Scored experiment deferrals for Stage 5AA."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    OUTPUT_DIR,
    REPORT_FILES,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    base_record,
)

EXPERIMENT_CLASSES = (
    "p56_scored_cuda_experiment",
    "full_p56_scored_cuda_experiment",
    "unsolved_page_micro_pilot",
    "broad_solved_fixture_cuda_campaign",
    "gpu_benchmark_campaign",
    "website_expansion",
)


def build_scored_experiment_deferral(
    *,
    scored_experiment_deferral_out: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_scored_experiment_deferral_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-scored-experiment-deferral-record-v0.schema.json",
            deferral_record_id=f"stage5aa-scored-deferral-{index:02d}",
            experiment_class=experiment_class,
            readiness_status="deferred_manifest_gate_required",
            execution_enabled=False,
            scored_experiment_executed=False,
            benchmark_allowed=False,
            website_expansion_allowed=False,
            no_solve_claim=True,
            blockers=["not_in_stage5aa_scope"],
        )
        for index, experiment_class in enumerate(EXPERIMENT_CLASSES, start=1)
    ]
    write_records(scored_experiment_deferral_out, records)
    write_json_report(out_dir, REPORT_FILES["scored_deferral"], {"records": records})
    return records
