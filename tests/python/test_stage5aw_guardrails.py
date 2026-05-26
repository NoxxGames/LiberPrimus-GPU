from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_guardrails_block_execution_interpretation_and_cuda() -> None:
    guardrail = yaml.safe_load(
        (ROOT / "data/token-block/stage5aw-guardrail.yaml").read_text(encoding="utf-8")
    )
    assert guardrail["parser_repair_only"] is True
    false_flags = [
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "llm_vision_token_reading_performed",
        "semantic_image_interpretation_performed",
        "hidden_content_image_forensics_performed",
        "stego_tool_execution_performed",
        "decode_attempt_performed",
        "hash_preimage_search_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ]
    assert all(guardrail[name] is False for name in false_flags)
    assert guardrail["new_cuda_kernels_added"] == 0
