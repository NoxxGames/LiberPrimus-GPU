from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.bounded_p56_cuda_parity.cuda_execution import run_bounded_p56_cuda
from libreprimus.bounded_p56_cuda_parity.models import (
    EXPECTED_OUTPUT_TOKEN_HASH,
    FORMULA_OUTPUT_TOKEN_HASH,
    VALIDATION_VECTOR_ID,
)


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_committed_run_record_preserves_hash_mismatch() -> None:
    record = _records("data/cuda/stage5ad-bounded-p56-cuda-run.yaml")[0]

    assert record["validation_vector_id"] == VALIDATION_VECTOR_ID
    assert record["cuda_execution_status"] == "failed_hash_mismatch"
    assert record["expected_output_token_hash"] == EXPECTED_OUTPUT_TOKEN_HASH
    assert record["computed_cuda_output_token_hash"] == FORMULA_OUTPUT_TOKEN_HASH
    assert record["cuda_attempted_count"] == 1
    assert record["cuda_pass_count"] == 0
    assert record["cuda_fail_count"] == 1
    assert record["cuda_skip_count"] == 0
    assert record["full_p56_cuda_executed"] is False
    assert record["unsolved_page_cuda_used"] is False


def test_stage5ad_skip_path_is_no_gpu_safe(tmp_path: Path) -> None:
    records = run_bounded_p56_cuda(
        cuda_run_out=tmp_path / "run.yaml",
        out_dir=tmp_path / "out",
        build_dir=tmp_path / "build",
        skip_cuda=True,
    )
    record = records[0]

    assert record["cuda_execution_status"] == "skipped_cuda_unavailable"
    assert record["cuda_execution_performed"] is False
    assert record["cuda_attempted_count"] == 0
    assert record["cuda_skip_count"] == 1
    assert "cuda_run_skipped_by_option" in record["blockers"]
