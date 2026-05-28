from test_stage5bn_common import load_yaml


def test_stage5bn_guardrails_block_execution_and_media_processing() -> None:
    payload = load_yaml("data/historical-route/stage5bn-guardrail.yaml")

    assert payload["source_gap_closure_only"] is True
    assert payload["human_review_pack_preparation_only"] is True
    for key in [
        "active_token_block_manifest_changed",
        "canonical_transcription_changed",
        "spreadsheet_committed",
        "spreadsheet_cell_dump_committed",
        "generated_crops_committed",
        "human_review_pack_committed",
        "token_experiment_executed",
        "real_byte_stream_generated",
        "variant_materialisation_performed",
        "dwh_hash_search_performed",
        "decode_attempt_performed",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "method_status_upgraded",
    ]:
        assert payload[key] is False
    assert payload["new_cuda_kernels_added"] == 0
    assert payload["future_token_block_execution_remains_blocked"] is True
