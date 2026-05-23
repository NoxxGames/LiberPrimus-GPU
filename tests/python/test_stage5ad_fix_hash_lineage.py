from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.bounded_p56_mismatch.models import STAGE5AD_COMPUTED_CUDA_HASH, STAGE5AD_EXPECTED_HASH, STAGE5X_FORMULA_HASH


def test_stage5ad_fix_hash_lineage_distinguishes_expected_and_formula_hashes() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-hash-lineage.yaml").read_text())["records"]
    by_role = {record["hash_role"]: record["hash_value"] for record in records}

    assert by_role["stage5l_candidate_major_reference_hash"] == STAGE5AD_EXPECTED_HASH
    assert by_role["prime_minus_one_formula_output_token_hash"] == STAGE5AD_COMPUTED_CUDA_HASH
    assert by_role["prime_minus_one_formula_output_token_hash"] == STAGE5X_FORMULA_HASH
    assert STAGE5AD_EXPECTED_HASH != STAGE5AD_COMPUTED_CUDA_HASH
