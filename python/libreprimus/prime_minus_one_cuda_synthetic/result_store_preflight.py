"""Result-store and score-summary preflight records for Stage 5AA."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    OUTPUT_DIR,
    REPORT_FILES,
    RESULT_STORE_PREFLIGHT_PATH,
    base_record,
)


def build_result_store_preflight(
    *,
    result_store_preflight_out: Path = RESULT_STORE_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    records = [
        _record("stage4p", "stage5aa-result-store-preflight-stage4p-v0"),
        _record("stage4i", "stage5aa-score-summary-preflight-stage4i-v0"),
    ]
    write_records(result_store_preflight_out, records)
    write_json_report(out_dir, REPORT_FILES["result_store"], {"records": records})
    return records


def _record(contract: str, record_id: str) -> dict[str, object]:
    return base_record(
        "prime_minus_one_cuda_synthetic_result_store_preflight_record",
        "schemas/cuda/prime-minus-one-cuda-synthetic-result-store-preflight-record-v0.schema.json",
        preflight_record_id=record_id,
        compatibility_contract=contract,
        result_body_publication_allowed=False,
        generated_body_publication_allowed=False,
        compact_metadata_only=True,
        source_generated_report_path="experiments/results/prime-minus-one-cuda-synthetic/stage5aa/",
        source_generated_report_committed=False,
        score_summary_contract="stage4i" if contract == "stage4i" else None,
        result_store_contract="stage4p" if contract == "stage4p" else None,
        preflight_status="ready_for_compact_metadata_if_synthetic_parity_passes",
        blockers=[],
    )
