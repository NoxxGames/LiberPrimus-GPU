"""Guardrail record for Stage 5AD-fix."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import GUARDRAIL_PATH, OUTPUT_DIR, REPORT_FILES, base_record


def build_guardrails(*, guardrail_out: Path = GUARDRAIL_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    record = base_record(
        "bounded_p56_mismatch_guardrail_record",
        "schemas/cuda/bounded-p56-mismatch-guardrail-record-v0.schema.json",
        guardrail_record_id="stage5ad-fix-guardrail-v0",
        full_p56_execution_allowed=False,
        unsolved_page_cuda_allowed=False,
        benchmark_allowed=False,
        scored_experiment_allowed=False,
        raw_data_processing_allowed=False,
        generated_body_publication_allowed=False,
        website_expansion_allowed=False,
        method_status_upgrade_allowed=False,
        cuda_source_modification_allowed=False,
        new_cuda_kernel_allowed=False,
        guardrail_status="all_stage5ad_fix_guardrails_preserved",
        blocked_scopes=[
            "full_p56_cuda",
            "unsolved_page_cuda",
            "benchmarks",
            "scored_experiments",
            "raw_data_processing",
            "generated_body_publication",
            "website_expansion",
            "method_status_upgrade",
            "new_cuda_kernel",
        ],
    )
    records = [record]
    write_records(guardrail_out, records)
    write_json_report(out_dir, REPORT_FILES["guardrail"], {"records": records})
    return records
