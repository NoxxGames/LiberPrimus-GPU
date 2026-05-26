from pathlib import Path

import yaml


def test_stage5bb_no_execution_proof_blocks_real_work() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-no-execution-proof.yaml").read_text())

    for key in [
        "real_token_block_byte_streams_generated",
        "real_variant_byte_streams_generated",
        "hash_search_performed",
        "hash_comparison_performed",
        "decode_attempt_performed",
        "scoring_performed",
        "benchmark_performed",
        "cuda_execution_performed",
        "stego_tool_execution_performed",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "llm_vision_token_reading_performed",
        "semantic_image_interpretation_performed",
        "solve_claim",
    ]:
        assert payload[key] is False
