from test_stage5by_common import load_yaml


def test_stage5by_guardrail_blocks_execution_surfaces() -> None:
    guardrail = load_yaml("data/historical-route/stage5by-guardrail.yaml")
    for key in [
        "execution_allowed",
        "solve_claim",
        "real_byte_stream_generated",
        "variant_materialisation_performed",
        "dwh_hash_search_performed",
        "decode_attempt_performed",
        "scoring_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "stego_tool_execution_performed",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "website_expansion_performed",
        "method_status_upgraded",
    ]:
        assert guardrail[key] is False
    assert guardrail["future_token_block_execution_remains_blocked"] is True
