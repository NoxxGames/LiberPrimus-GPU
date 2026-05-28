from test_stage5bn_common import load_yaml


def test_stage5bn_next_stage_decision_selects_non_execution_integration() -> None:
    payload = load_yaml("data/project-state/stage5bn-next-stage-decision.yaml")

    assert payload["selected_next_stage_id"] == "stage-5bo-codex-token-option-addendum-integration-without-execution"
    assert payload["selected_next_prompt_type"] == "codex_metadata_implementation"
    for key in [
        "token_block_execution_selected",
        "byte_stream_generation_selected",
        "variant_materialisation_selected",
        "dwh_hash_search_selected",
        "decode_selected",
        "scored_experiments_selected",
        "benchmark_selected",
        "cuda_selected",
        "stego_execution_selected",
        "ocr_selected",
        "ai_ml_selected",
        "canonical_corpus_activation_selected",
        "page_boundary_finalisation_selected",
        "method_status_upgrade_selected",
        "solve_claim",
    ]:
        assert payload[key] is False
