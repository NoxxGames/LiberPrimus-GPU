"""Build generated-body publication policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import GENERATED_BODY_POLICY_PATH, OUTPUT_DIR, REPORT_FILES, base_record

POLICY_SUBJECTS = (
    ("stage5aa_synthetic_cuda_result_body", "ignored_generated_output_only"),
    ("future_bounded_p56_cuda_result_body", "blocked_until_explicit_future_stage_and_stays_generated"),
)


def build_generated_body_policy(
    *,
    generated_body_policy_out: Path = GENERATED_BODY_POLICY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_generated_body_policy_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-generated-body-policy-record-v0.schema.json",
            policy_record_id=f"stage5ac-generated-body-policy-{subject}",
            policy_subject=subject,
            policy_status=status,
            generated_body_publication_allowed=False,
            generated_outputs_committed=False,
            raw_data_processed=False,
            codex_output_committed=False,
            sqlite_committed=False,
            publication_policy="compact_metadata_only",
        )
        for subject, status in POLICY_SUBJECTS
    ]
    write_records(generated_body_policy_out, records)
    write_json_report(out_dir, REPORT_FILES["generated_body_policy"], {"records": records})
    return records
