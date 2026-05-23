"""Hash-lineage records for the Stage 5AD-fix mismatch investigation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import (
    HASH_ALGORITHM,
    HASH_LINEAGE_PATH,
    NATIVE_PARITY_ID,
    OUTPUT_DIR,
    REPORT_FILES,
    SOURCE_SYNTHETIC_HASH,
    STAGE5AD_COMPUTED_CUDA_HASH,
    STAGE5AD_EXPECTED_HASH,
    STAGE5X_FORMULA_HASH,
    TOKEN_MAPPING_ID,
    base_record,
)


def build_hash_lineage(*, hash_lineage_out: Path = HASH_LINEAGE_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    records = [
        base_record(
            "bounded_p56_mismatch_hash_lineage_record",
            "schemas/cuda/bounded-p56-mismatch-hash-lineage-record-v0.schema.json",
            hash_lineage_record_id="stage5ad-fix-hash-lineage-stage5l-reference-v0",
            hash_value=STAGE5AD_EXPECTED_HASH,
            hash_algorithm=HASH_ALGORITHM,
            hash_role="stage5l_candidate_major_reference_hash",
            hash_material_kind="candidate_major_outputs",
            source_record_refs=[
                "data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml:stage5l-native-parity-04",
                "data/cuda/stage5w-prime-minus-one-candidate-batch-mapping.yaml:stage5w-mapping-p56-stage4o-bounded-v0",
                "data/cuda/stage5x-prime-minus-one-native-run.yaml:stage5x-parity-stage5w-mapping-p56-stage4o-bounded-v0",
            ],
            token_mapping_id=TOKEN_MAPPING_ID,
            native_parity_id=NATIVE_PARITY_ID,
            stage5ad_expected_hash=True,
            stage5ad_computed_cuda_hash=False,
            formula_hash=False,
        ),
        base_record(
            "bounded_p56_mismatch_hash_lineage_record",
            "schemas/cuda/bounded-p56-mismatch-hash-lineage-record-v0.schema.json",
            hash_lineage_record_id="stage5ad-fix-hash-lineage-formula-v0",
            hash_value=STAGE5X_FORMULA_HASH,
            hash_algorithm=HASH_ALGORITHM,
            hash_role="prime_minus_one_formula_output_token_hash",
            hash_material_kind="formula_output_tokens",
            source_record_refs=[
                "data/cuda/stage5x-prime-minus-one-native-run.yaml:formula_output_token_hash",
                "data/cuda/stage5ad-bounded-p56-cuda-run.yaml:computed_cuda_output_token_hash",
                "data/cuda/stage5ad-bounded-p56-cuda-parity.yaml:cuda_kernel_formula_output_token_hash",
            ],
            token_mapping_id=TOKEN_MAPPING_ID,
            native_parity_id=NATIVE_PARITY_ID,
            stage5ad_expected_hash=False,
            stage5ad_computed_cuda_hash=STAGE5AD_COMPUTED_CUDA_HASH == STAGE5X_FORMULA_HASH,
            formula_hash=True,
        ),
        base_record(
            "bounded_p56_mismatch_hash_lineage_record",
            "schemas/cuda/bounded-p56-mismatch-hash-lineage-record-v0.schema.json",
            hash_lineage_record_id="stage5ad-fix-hash-lineage-stage5aa-synthetic-v0",
            hash_value=SOURCE_SYNTHETIC_HASH,
            hash_algorithm=HASH_ALGORITHM,
            hash_role="stage5aa_synthetic_prime_minus_one_reference_hash",
            hash_material_kind="synthetic_control_output_tokens",
            source_record_refs=[
                "data/cuda/stage5aa-prime-minus-one-cuda-synthetic-parity.yaml",
                "data/cuda/stage5z-prime-minus-one-cuda-validation-vectors.yaml:stage5z-validation-synthetic-prime-minus-one-v0",
            ],
            token_mapping_id=None,
            native_parity_id=None,
            stage5ad_expected_hash=False,
            stage5ad_computed_cuda_hash=False,
            formula_hash=False,
        ),
    ]
    write_records(hash_lineage_out, records)
    write_json_report(out_dir, REPORT_FILES["hash_lineage"], {"records": records})
    return records
