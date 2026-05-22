"""Schedule shape conformance records for Stage 5V."""

from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import COMMON_FLAGS, OUTPUT_DIR, REPORT_FILES, SCHEDULE_CONFORMANCE_PATH


def build_schedule_conformance(
    *,
    schedule_conformance_out: Path = SCHEDULE_CONFORMANCE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = [
        {
            **COMMON_FLAGS,
            "record_type": "schedule_conformance_record",
            "schema": "schemas/cuda/schedule-conformance-record-v0.schema.json",
            "schedule_id": "stage5v-key-schedule-shape-conformance",
            "schedule_kind": "vigenere_key_schedule",
            "conformance_status": "shape_only",
            "fixture_id": "stage5v-key-schedule-shape-fixture",
            "policy": "key tokens and reset/advance policy fields validate, but Vigenere execution stays pending.",
            "blockers": ["family_specific_vigenere_execution_contract_pending"],
        },
        {
            **COMMON_FLAGS,
            "record_type": "schedule_conformance_record",
            "schema": "schemas/cuda/schedule-conformance-record-v0.schema.json",
            "schedule_id": "stage5v-prime-minus-one-stream-shape-conformance",
            "schedule_kind": "prime_minus_one_stream_schedule",
            "conformance_status": "shape_only",
            "fixture_id": "stage5v-stream-schedule-shape-fixture",
            "policy": "stream values and advance fields validate, but prime-stream execution stays pending.",
            "blockers": ["family_specific_prime_stream_execution_contract_pending"],
        },
    ]
    write_record_set(schedule_conformance_out, records)
    write_report(out_dir, REPORT_FILES["schedule"], {"records": records, "count": len(records)})
    return records
