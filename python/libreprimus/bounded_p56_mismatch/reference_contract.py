"""Reference-contract diagnosis for the bounded p56 mismatch."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import (
    OUTPUT_DIR,
    REFERENCE_CONTRACT_PATH,
    REPORT_FILES,
    STAGE5AD_COMPUTED_CUDA_HASH,
    STAGE5AD_EXPECTED_HASH,
    STAGE5X_FORMULA_HASH,
    base_record,
)


def build_reference_contract(
    *, reference_contract_out: Path = REFERENCE_CONTRACT_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    record = base_record(
        "bounded_p56_mismatch_reference_contract_record",
        "schemas/cuda/bounded-p56-mismatch-reference-contract-record-v0.schema.json",
        reference_contract_record_id="stage5ad-fix-reference-contract-bounded-p56-v0",
        stage5ad_expected_hash=STAGE5AD_EXPECTED_HASH,
        stage5ad_computed_cuda_hash=STAGE5AD_COMPUTED_CUDA_HASH,
        stage5x_formula_hash=STAGE5X_FORMULA_HASH,
        cuda_formula_matches_stage5x_formula=STAGE5AD_COMPUTED_CUDA_HASH == STAGE5X_FORMULA_HASH,
        cuda_formula_matches_stage5w_expected=STAGE5AD_COMPUTED_CUDA_HASH == STAGE5AD_EXPECTED_HASH,
        expected_hash_reference_mode="stage5l_bounded_candidate_major_reference_recomputed",
        formula_hash_reference_mode="prime_minus_one_formula_output_tokens",
        contract_status="reference_hash_material_mismatch",
        reference_contract_repair_required=True,
        cuda_kernel_repair_required=False,
        hash_material_policy_repair_required=True,
        interpretation=(
            "The Stage 5AD CUDA/formula hash matches the Stage 5X formula hash, "
            "while the Stage 5AD expected hash points to the Stage 5L candidate-major reference material."
        ),
    )
    records = [record]
    write_records(reference_contract_out, records)
    write_json_report(out_dir, REPORT_FILES["reference_contract"], {"records": records})
    return records
