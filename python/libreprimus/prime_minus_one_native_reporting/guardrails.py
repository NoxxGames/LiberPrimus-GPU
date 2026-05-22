"""Build Stage 5Y reporting guardrail records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, GUARDRAIL_PATH, OUTPUT_DIR, REPORT_FILES


GUARDRAILS = [
    "no_native_execution",
    "no_cuda_execution",
    "no_cuda_source_modification",
    "no_new_cuda_kernels",
    "no_benchmarks_or_speedup_claims",
    "no_unsolved_page_cuda_or_real_lp_cuda",
    "no_raw_data_or_generated_body_publication",
    "no_method_status_upgrade_or_solve_claim",
    "no_cpp_launches_python_workers",
]


def build_guardrails(
    *,
    guardrail_out: Path = GUARDRAIL_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = []
    for guardrail_id in GUARDRAILS:
        records.append(
            {
                **COMMON_RECORD_FLAGS,
                "record_type": "prime_minus_one_native_reporting_guardrail_record",
                "schema": "schemas/cuda/prime-minus-one-native-reporting-guardrail-record-v0.schema.json",
                "guardrail_id": f"stage5y-{guardrail_id}",
                "guardrail_status": "passed",
                "rationale": "Stage 5Y is reporting/readiness metadata only.",
            }
        )
    write_records(guardrail_out, records)
    write_json_report(out_dir, REPORT_FILES["guardrail"], {"records": records})
    return records
