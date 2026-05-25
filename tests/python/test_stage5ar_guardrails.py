from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ar_guardrails_block_execution_and_interpretation() -> None:
    guardrail = yaml.safe_load(Path("data/token-block/stage5ar-guardrail.yaml").read_text(encoding="utf-8"))
    for key in [
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "semantic_image_interpretation_performed",
        "hidden_content_image_forensics_performed",
        "stego_tool_execution_performed",
        "decode_attempted",
        "hash_preimage_search_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ]:
        assert guardrail[key] is False
    assert guardrail["new_cuda_kernels_added"] == 0
