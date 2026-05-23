from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ad_fix_guardrails_block_widened_scope() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-guardrail.yaml").read_text())["records"][0]

    assert record["full_p56_execution_allowed"] is False
    assert record["unsolved_page_cuda_allowed"] is False
    assert record["benchmark_allowed"] is False
    assert record["scored_experiment_allowed"] is False
    assert record["new_cuda_kernel_allowed"] is False
