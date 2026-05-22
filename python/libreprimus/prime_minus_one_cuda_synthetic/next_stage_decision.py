"""Next-stage decision records for Stage 5AA."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_IF_MISMATCH,
    NEXT_STAGE_IF_PASSED,
    NEXT_STAGE_IF_SKIPPED,
    OUTPUT_DIR,
    PARITY_PATH,
    REPORT_FILES,
    base_record,
)


def build_next_stage_decision(
    *,
    parity: Path = PARITY_PATH,
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity_status = read_records(parity)[0].get("parity_status")
    selected_option = _selected_option(str(parity_status))
    options = [
        (
            "stage5ab_prime_minus_one_synthetic_reporting_bounded_p56_preflight",
            NEXT_STAGE_IF_PASSED,
            "Select only if the synthetic CUDA hash matches Stage 5Z.",
        ),
        (
            "stage5aa_followup_toolchain_repair",
            NEXT_STAGE_IF_SKIPPED,
            "Select when CUDA build/run cannot complete locally.",
        ),
        (
            "stage5aa_fix_hash_mismatch",
            NEXT_STAGE_IF_MISMATCH,
            "Select when CUDA executes but mismatches the Stage 5Z expected hash.",
        ),
        (
            "blocked_benchmark_or_scored_experiment",
            "Do not select benchmark, scored experiment, website expansion, or unsolved CUDA.",
            "Benchmarks, scored experiments, website expansion, and unsolved-page CUDA remain out of scope.",
        ),
    ]
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_next_stage_decision_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-next-stage-decision-record-v0.schema.json",
            decision_record_id=f"stage5aa-next-stage-decision-{index:02d}",
            option_id=option_id,
            recommended_stage_title=title,
            rationale=rationale,
            selected=option_id == selected_option,
            parity_status=parity_status,
            deep_research_recommended_next=False,
            benchmark_selected=False,
            scored_experiment_selected=False,
            unsolved_cuda_selected=False,
            website_expansion_selected=False,
            blockers=[] if option_id == selected_option else ["not_selected"],
        )
        for index, (option_id, title, rationale) in enumerate(options, start=1)
    ]
    write_records(next_stage_decision_out, records)
    write_json_report(out_dir, REPORT_FILES["next_stage"], {"records": records})
    return records


def _selected_option(parity_status: str) -> str:
    if parity_status == "passed":
        return "stage5ab_prime_minus_one_synthetic_reporting_bounded_p56_preflight"
    if parity_status == "failed_hash_mismatch":
        return "stage5aa_fix_hash_mismatch"
    return "stage5aa_followup_toolchain_repair"
