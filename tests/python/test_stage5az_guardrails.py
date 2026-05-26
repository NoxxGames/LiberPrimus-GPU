from pathlib import Path

import yaml


def test_stage5az_guardrails_keep_all_execution_closed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5az-guardrail.yaml").read_text(encoding="utf-8"))
    false_flags = [
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "llm_vision_token_reading_performed",
        "semantic_image_interpretation_performed",
        "hidden_content_image_forensics_performed",
        "stego_tool_execution_performed",
        "hash_preimage_search_performed",
        "decode_attempt_performed",
        "token_experiments_executed",
        "variant_byte_streams_generated",
        "full_cartesian_product_enumerated",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "cryptanalytic_benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ]

    assert payload["status"] == "passed"
    for flag in false_flags:
        assert payload[flag] is False
