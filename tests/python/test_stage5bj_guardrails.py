from test_stage5bj_crosswalk_closure import load_yaml


FALSE_KEYS = [
    "live_web_scrape_performed",
    "network_fetch_performed",
    "fandom_page_bodies_committed",
    "fandom_images_committed",
    "raw_archive_files_committed",
    "spreadsheet_committed",
    "generated_outputs_committed",
    "full_surface_bodies_committed",
    "canonical_transcription_changed",
    "active_token_block_manifest_changed",
    "token_experiments_executed",
    "real_token_block_byte_streams_generated",
    "variant_byte_streams_generated",
    "variant_branches_enumerated",
    "real_variant_branches_materialised",
    "full_cartesian_product_enumerated",
    "sampled_real_variants_generated",
    "fandom_surface_combination_performed",
    "xor_attempt_performed",
    "transposition_attempt_performed",
    "outguess_execution_performed",
    "openpuff_execution_performed",
    "mp3stego_execution_performed",
    "stego_tool_execution_performed",
    "pgp_network_key_fetch_performed",
    "pgp_verification_performed_as_project_truth",
    "hash_search_performed",
    "hash_preimage_claim",
    "hash_comparison_performed_as_experiment",
    "decode_attempt_performed",
    "scored_experiments_executed",
    "benchmark_performed",
    "cryptanalytic_benchmark_performed",
    "cuda_execution_performed",
    "cuda_source_modified",
    "ocr_performed",
    "ai_ml_interpretation_performed",
    "llm_vision_token_reading_performed",
    "semantic_image_interpretation_performed",
    "hidden_content_image_forensics_performed",
    "audio_analysis_performed",
    "canonical_corpus_active",
    "page_boundaries_final",
    "method_status_upgraded",
    "public_website_publication_performed",
    "website_expansion_performed",
    "solve_claim",
]


def test_stage5bj_guardrails_preserve_no_execution_boundary() -> None:
    payload = load_yaml("data/historical-route/stage5bj-guardrail.yaml")

    assert payload["metadata_only"] is True
    assert payload["original_archive_crosswalk_closure_only"] is True
    assert payload["source_lock_hashing_performed"] is True
    assert payload["new_cuda_kernels_added"] == 0
    for key in FALSE_KEYS:
        assert payload[key] is False, key
