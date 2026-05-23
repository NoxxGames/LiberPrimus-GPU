"""Build bounded-p56 CUDA parity preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import (
    BOUNDED_P56_CANDIDATE_ID,
    BOUNDED_P56_FIXTURE_ID,
    BOUNDED_P56_MAPPING_ID,
    BOUNDED_P56_PREFLIGHT_PATH,
    BOUNDED_P56_VECTOR_ID,
    DOC_STALENESS_VALIDATION_PATH,
    EXPECTED_BOUNDED_P56_HASH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    REPORT_FILES,
    SOURCE_CONTRACT_STAGE_ID,
    SOURCE_NATIVE_PARITY_STAGE_ID,
    base_record,
)


def build_bounded_p56_preflight(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    doc_staleness_validation: Path = DOC_STALENESS_VALIDATION_PATH,
    bounded_p56_preflight_out: Path = BOUNDED_P56_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = read_records(parity_report)[0]
    doc = read_records(doc_staleness_validation)[0] if doc_staleness_validation.exists() else {}
    parity_clean = parity.get("parity_status") == "passed" and parity.get("stage5aa_hash_match") is True
    docs_clean = doc.get("doc_staleness_strict_check_passed") is True or not doc
    ready = parity_clean and docs_clean
    blockers: list[str] = []
    if not parity_clean:
        blockers.append("stage5aa_synthetic_parity_not_clean")
    if not docs_clean:
        blockers.append("stage5ab_doc_staleness_not_clean")
    records = [
        base_record(
            "bounded_p56_cuda_parity_preflight_record",
            "schemas/cuda/bounded-p56-cuda-parity-preflight-record-v0.schema.json",
            preflight_id="stage5ac-bounded-p56-cuda-preflight-v0",
            bounded_p56_vector_id=BOUNDED_P56_VECTOR_ID,
            mapping_id=BOUNDED_P56_MAPPING_ID,
            fixture_id=BOUNDED_P56_FIXTURE_ID,
            candidate_id=BOUNDED_P56_CANDIDATE_ID,
            expected_output_token_hash=EXPECTED_BOUNDED_P56_HASH,
            output_hash_algorithm="sha256_canonical_json_v1",
            native_reference_stage=SOURCE_NATIVE_PARITY_STAGE_ID,
            cuda_contract_stage=SOURCE_CONTRACT_STAGE_ID,
            synthetic_cuda_parity_stage="stage-5aa",
            bounded_p56_cuda_execution_allowed_current_stage=False,
            bounded_p56_cuda_execution_ready_next_stage=ready,
            requires_explicit_future_stage=True,
            full_p56_required=False,
            full_p56_blocked=True,
            unsolved_page_cuda_allowed=False,
            benchmark_allowed=False,
            scored_experiment_allowed=False,
            preflight_status="ready_for_stage5ad_bounded_p56_cuda_parity" if ready else "blocked_preflight_gap",
            blockers=blockers,
        )
    ]
    write_records(bounded_p56_preflight_out, records)
    write_json_report(out_dir, REPORT_FILES["bounded_p56"], {"records": records})
    return records
