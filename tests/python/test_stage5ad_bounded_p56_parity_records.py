from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.bounded_p56_cuda_parity.models import (
    EXPECTED_OUTPUT_TOKEN_HASH,
    FORMULA_OUTPUT_TOKEN_HASH,
)


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_parity_record_keeps_stage5x_mismatch_explicit() -> None:
    record = _records("data/cuda/stage5ad-bounded-p56-cuda-parity.yaml")[0]

    assert record["parity_status"] == "failed_hash_mismatch"
    assert record["expected_output_token_hash"] == EXPECTED_OUTPUT_TOKEN_HASH
    assert record["computed_cuda_output_token_hash"] == FORMULA_OUTPUT_TOKEN_HASH
    assert record["stage5x_expected_hash_match"] is False
    assert record["stage5aa_synthetic_rerun_in_stage5ad"] is False
    assert "computed_cuda_hash_mismatches_stage5x_expected_hash" in record["blockers"]
