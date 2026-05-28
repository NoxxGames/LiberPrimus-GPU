from test_stage5bo_common import load_yaml


def test_stage5bo_guardrails_block_execution_and_manifest_mutation() -> None:
    payload = load_yaml("data/historical-route/stage5bo-guardrail.yaml")

    assert payload["metadata_only"] is True
    assert payload["corrected_template_consumed_as_ignored_local_input"] is True
    for key in [
        "canonical_transcription_changed",
        "active_token_block_manifest_changed",
        "stage5aw_branch_manifest_changed",
        "stage5ay_branch_eligibility_changed",
        "stage5az_variant_family_manifest_changed",
        "real_token_block_byte_streams_generated",
        "variant_materialisation_performed",
        "full_cartesian_product_enumerated",
        "dwh_hash_search_performed",
        "decode_attempt_performed",
        "stego_tool_execution_performed",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "cuda_execution_performed",
        "scoring_performed",
        "benchmark_performed",
        "template_bodies_committed",
        "decision_template_committed",
        "corrected_decision_template_committed",
        "generated_outputs_committed",
        "codex_output_used",
    ]:
        assert payload[key] is False
    assert payload["future_token_block_execution_remains_blocked"] is True
