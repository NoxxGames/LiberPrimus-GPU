from pathlib import Path

import yaml


def test_stage5ay_guardrails_block_execution_and_cuda() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-guardrail.yaml").read_text(encoding="utf-8"))

    for key in [
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "llm_vision_token_reading_performed",
        "semantic_image_interpretation_performed",
        "hidden_content_image_forensics_performed",
        "stego_tool_execution_performed",
        "hash_preimage_search_performed",
        "decode_attempt_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "cryptanalytic_benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ]:
        assert payload[key] is False
    assert payload["new_cuda_kernels_added"] == 0
