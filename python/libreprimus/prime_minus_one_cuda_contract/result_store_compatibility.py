"""Build Stage 5Z result-store compatibility records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import OUTPUT_DIR, RESULT_STORE_COMPATIBILITY_PATH, base_record


def build_result_store_compatibility(
    result_store_compatibility_out: Path = RESULT_STORE_COMPATIBILITY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    specs = [
        (
            "stage5z-result-store-stage4p-v0",
            "stage4p",
            "compatible_compact_metadata_only",
            "Stage 5Z records can be represented as compact Stage 4P unified result surfaces without generated bodies.",
        ),
        (
            "stage5z-score-summary-stage4i-v0",
            "stage4i",
            "compatible_triage_only",
            "Future score summaries must preserve Stage 4I finite confidence labels and cannot imply solve evidence.",
        ),
    ]
    records = [
        base_record(
            "prime_minus_one_cuda_result_store_compatibility_record",
            "schemas/cuda/prime-minus-one-cuda-result-store-compatibility-record-v0.schema.json",
            compatibility_record_id=record_id,
            compatibility_contract=contract,
            compatibility_status=status,
            compatibility_notes=notes,
            compact_summary_only=True,
            result_body_publication_allowed=False,
            score_interpretation="triage_only",
        )
        for record_id, contract, status, notes in specs
    ]
    write_records(result_store_compatibility_out, records)
    write_json_report(out_dir, "result_store_compatibility_report.json", {"records": records})
    return records


__all__ = ["build_result_store_compatibility"]
