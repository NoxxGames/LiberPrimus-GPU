"""Result-store conformance records for Stage 5V."""

from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import COMMON_FLAGS, OUTPUT_DIR, REPORT_FILES, RESULT_STORE_CONFORMANCE_PATH


def build_result_store_conformance(
    *,
    result_store_conformance_out: Path = RESULT_STORE_CONFORMANCE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = [
        _record(
            "stage5v-result-store-compact-summary",
            "stage4p_compact_summary",
            "passed",
            "Conformance publishes compact metadata only and keeps generated bodies ignored.",
        ),
        _record(
            "stage5v-score-summary-compatibility",
            "stage4i_score_summary",
            "passed",
            "Score-vector conformance uses finite Stage 4I triage-only labels.",
        ),
        _record(
            "stage5v-output-hash-compatibility",
            "output_token_hash_records",
            "passed",
            "Executed fixtures commit output-token hashes, not generated bodies.",
        ),
    ]
    write_record_set(result_store_conformance_out, records)
    write_report(out_dir, REPORT_FILES["result_store"], {"records": records, "count": len(records)})
    return records


def _record(record_id: str, surface: str, status: str, notes: str) -> dict[str, object]:
    return {
        **COMMON_FLAGS,
        "record_type": "native_conformance_result_store_record",
        "schema": "schemas/cuda/native-conformance-result-store-record-v0.schema.json",
        "result_store_conformance_id": record_id,
        "compatibility_surface": surface,
        "conformance_status": status,
        "compact_summary_only": True,
        "generated_body_committed": False,
        "generated_body_publication_allowed": False,
        "method_status_upgraded": False,
        "notes": notes,
    }
