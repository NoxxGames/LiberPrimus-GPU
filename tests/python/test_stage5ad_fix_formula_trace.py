from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.bounded_p56_mismatch.models import STAGE5AD_COMPUTED_CUDA_HASH, STAGE5AD_EXPECTED_HASH


def test_stage5ad_fix_formula_trace_recomputes_stage5x_formula_hash() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-formula-trace.yaml").read_text())["records"][0]

    assert record["formula_output_token_hash"] == STAGE5AD_COMPUTED_CUDA_HASH
    assert record["formula_output_token_hash"] != STAGE5AD_EXPECTED_HASH
    assert record["formula_matches_stage5x_formula"] is True
    assert record["formula_matches_stage5ad_cuda_hash"] is True
    assert record["formula_matches_stage5ad_expected_hash"] is False
