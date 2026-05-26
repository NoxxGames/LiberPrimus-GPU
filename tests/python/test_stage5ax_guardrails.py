from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ax_guardrails_block_cryptanalytic_execution_and_cuda() -> None:
    guardrail = yaml.safe_load(Path("data/ci/stage5ax-guardrail.yaml").read_text(encoding="utf-8"))
    false_fields = [
        "cryptanalytic_execution_performed",
        "token_experiments_executed",
        "variant_byte_streams_generated",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "llm_vision_token_reading_performed",
        "semantic_image_interpretation_performed",
        "hidden_content_image_forensics_performed",
        "stego_tool_execution_performed",
        "decode_attempt_performed",
        "hash_preimage_search_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "cryptanalytic_benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
        "generated_validation_outputs_committed",
    ]
    assert guardrail["infrastructure_stage"] is True
    assert guardrail["parallel_validation_only"] is True
    for field in false_fields:
        assert guardrail[field] is False
