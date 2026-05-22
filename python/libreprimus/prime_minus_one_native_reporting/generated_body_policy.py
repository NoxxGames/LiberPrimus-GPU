"""Build Stage 5Y generated-body policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, GENERATED_BODY_POLICY_PATH, OUTPUT_DIR, REPORT_FILES


POLICIES = [
    ("stage5x_generated_native_result_bodies", "ignored_unpublished"),
    ("stage5y_generated_reports", "ignored_unpublished"),
    ("full_output_token_arrays", "not_committed"),
    ("compact_hashes_and_source_ids", "committed_metadata_allowed"),
    ("raw_data_sqlite_and_local_reports", "uncommitted"),
    ("codex_output", "ignored_unpublished"),
    ("future_generated_body_publication", "requires_explicit_new_policy_stage"),
]


def build_generated_body_policy(
    *,
    generated_body_policy_out: Path = GENERATED_BODY_POLICY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = []
    for policy_subject, policy_status in POLICIES:
        records.append(
            {
                **COMMON_RECORD_FLAGS,
                "record_type": "prime_minus_one_generated_body_policy_record",
                "schema": "schemas/cuda/prime-minus-one-generated-body-policy-record-v0.schema.json",
                "policy_record_id": f"stage5y-generated-body-{policy_subject}",
                "policy_subject": policy_subject,
                "policy_status": policy_status,
                "generated_body_publication_allowed": False,
                "generated_outputs_committed": False,
                "raw_data_processed": False,
                "codex_output_committed": False,
                "sqlite_committed": False,
                "future_publication_requires_explicit_policy": True,
            }
        )
    write_records(generated_body_policy_out, records)
    write_json_report(out_dir, REPORT_FILES["generated_body_policy"], {"records": records})
    return records
