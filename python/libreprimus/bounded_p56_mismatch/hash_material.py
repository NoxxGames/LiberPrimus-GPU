"""Hash-material trace for Stage 5AD-fix."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256

from .export import write_json_report, write_records
from .models import (
    FORMULA_OUTPUT_TOKENS,
    HASH_ALGORITHM,
    HASH_MATERIAL_PATH,
    OUTPUT_DIR,
    REPORT_FILES,
    STAGE5AD_COMPUTED_CUDA_HASH,
    STAGE5AD_EXPECTED_HASH,
    STAGE5L_CANDIDATE_MAJOR_LAST_OUTPUT_TOKENS,
    base_record,
)


def build_hash_material(*, hash_material_out: Path = HASH_MATERIAL_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    formula_material_hash = stable_json_sha256(FORMULA_OUTPUT_TOKENS)
    records = [
        base_record(
            "bounded_p56_mismatch_hash_material_record",
            "schemas/cuda/bounded-p56-mismatch-hash-material-record-v0.schema.json",
            hash_material_record_id="stage5ad-fix-hash-material-formula-output-v0",
            hash_material_kind="formula_output_tokens",
            hash_material=FORMULA_OUTPUT_TOKENS,
            output_token_hash=formula_material_hash,
            expected_hash_match=formula_material_hash == STAGE5AD_EXPECTED_HASH,
            cuda_formula_hash_match=formula_material_hash == STAGE5AD_COMPUTED_CUDA_HASH,
            hash_algorithm=HASH_ALGORITHM,
            material_status="matches_stage5x_formula_and_stage5ad_cuda_formula",
        ),
        base_record(
            "bounded_p56_mismatch_hash_material_record",
            "schemas/cuda/bounded-p56-mismatch-hash-material-record-v0.schema.json",
            hash_material_record_id="stage5ad-fix-hash-material-stage5l-candidate-major-v0",
            hash_material_kind="stage5l_candidate_major_reference_outputs",
            hash_material=[
                {
                    "candidate_index": 4,
                    "shift": 28,
                    "output_tokens": STAGE5L_CANDIDATE_MAJOR_LAST_OUTPUT_TOKENS,
                }
            ],
            output_token_hash=STAGE5AD_EXPECTED_HASH,
            expected_hash_match=True,
            cuda_formula_hash_match=False,
            hash_algorithm=HASH_ALGORITHM,
            material_status="stage5l_reference_hash_is_not_formula_hash_material",
        ),
    ]
    write_records(hash_material_out, records)
    write_json_report(out_dir, REPORT_FILES["hash_material"], {"records": records})
    return records
