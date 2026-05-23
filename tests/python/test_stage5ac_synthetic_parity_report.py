from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

EXPECTED_HASH = "06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab"


def _yaml(path: str) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_stage5ac_reports_stage5aa_synthetic_parity() -> None:
    record = _yaml("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml")["records"][0]
    source_summary = _yaml("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-summary.yaml")

    assert record["source_stage_id"] == "stage-5aa"
    assert record["synthetic_vector_id"] == "stage5z-validation-synthetic-prime-control-v0"
    assert record["expected_output_token_hash"] == EXPECTED_HASH
    assert record["computed_output_token_hash"] == EXPECTED_HASH
    assert source_summary["expected_output_token_hash"] == EXPECTED_HASH
    assert source_summary["computed_output_token_hash"] == EXPECTED_HASH
    assert record["parity_status"] == "passed"
    assert record["stage5aa_hash_match"] is True


def test_stage5ac_does_not_execute_or_modify_cuda() -> None:
    record = _yaml("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml")["records"][0]
    assert record["cuda_execution_performed"] is False
    assert record["cuda_execution_performed_in_stage5ac"] is False
    assert record["cuda_source_modified"] is False
    assert record["cuda_source_modified_in_stage5ac"] is False
    assert record["new_cuda_kernels_added"] == 0
    assert record["new_cuda_kernels_added_in_stage5ac"] == 0
