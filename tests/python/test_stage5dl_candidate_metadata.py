from __future__ import annotations

from test_stage5dl_common import ensure_stage5dl_built, load_yaml


def test_stage5dl_number_triangle_v1_metadata_and_subfamilies() -> None:
    ensure_stage5dl_built()
    record = load_yaml("data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml")

    assert record["candidate_family_id"] == "pdd_153_triangle_word_prime_route_v1"
    assert record["triangle_body_word_count"] == 153
    assert record["triangle_row_count"] == 17
    assert record["triangle_center_word_index"] == 41
    assert record["selected_now"] is False
    assert record["execution_authorized_now"] is False
    assert record["solve_claim"] is False
    assert record["subfamilies"] == [
        "pdd_153_triangle_shell_route_v1",
        "pdd_153_triangle_way_anchor_route_v1",
        "pdd_153_triangle_prime_mask_route_v1",
        "pdd_153_triangle_2016_prime_layer_route_v1",
        "pdd_153_triangle_fibonacci_prime_index_route_v1",
        "pdd_153_triangle_56311_wynn_way_route_v1",
    ]


def test_stage5dl_triangle_arithmetic_candidate_metadata() -> None:
    ensure_stage5dl_built()
    way = load_yaml("data/historical-route/stage5dl-triangle-way-anchor-source-lock.yaml")
    prime_mask = load_yaml("data/historical-route/stage5dl-triangle-prime-mask-source-lock.yaml")
    layer = load_yaml("data/historical-route/stage5dl-triangle-2016-prime-layer-source-lock.yaml")
    fib = load_yaml(
        "data/historical-route/stage5dl-triangle-fibonacci-prime-index-source-lock.yaml"
    )
    bridge = load_yaml("data/historical-route/stage5dl-triangle-56311-wynn-way-source-lock.yaml")

    assert way["derived_latin"] == "WAY"
    assert way["heading_minus_reversed_word52_mod29"] == [7, 24, 26]
    assert way["route_extraction_performed_now"] is False
    assert prime_mask["present_prime_count_under_153"] == 20
    assert prime_mask["missing_prime_count_under_153"] == 16
    assert prime_mask["prime_41_hits_triangle_center"] is True
    assert prime_mask["prime_53_hits_single_rune_anchor"] is True
    assert layer["layered_prime_values"] == [2819, 2039, 1277]
    assert layer["layered_prime_index_differences"] == [101, 103]
    assert fib["base_prime"] == 3301
    assert fib["base_prime_index"] == 464
    assert fib["plus_f_minus_f_manipulation_is_weakest_link"] is True
    assert bridge["disk_sequence"] == [5, 6, 3, 11]
    assert bridge["cumulative_from_center_41"] == [46, 52, 55, 66]
    assert bridge["center_plus_sequence_hits_word52"] is True


def test_stage5dl_quote_dialogue_cribs_are_candidates_only() -> None:
    ensure_stage5dl_built()
    record = load_yaml("data/historical-route/stage5dl-section-0-12-quote-dialogue-cribs.yaml")

    assert record["candidate_family_id"] == "section_0_12_quote_dialogue_cribs_v0"
    assert record["candidate_a_proposed_plaintext"] == "HE SAID"
    assert record["candidate_b_proposed_plaintext"] == "HE ANSWERED"
    assert record["i_am_a_quote_template_relevant"] is True
    assert record["i_am_a_applied_now"] is False
    assert record["cribs_applied_now"] is False
    assert record["decryption_performed_now"] is False
    assert record["solve_claim"] is False


def test_stage5dl_koan_candidate_records_visual_source_lock_only() -> None:
    ensure_stage5dl_built()
    record = load_yaml("data/historical-route/stage5dl-koan-depiction-visual-parallel.yaml")

    assert record["source_path"] == "third_party/koan_page.png"
    assert record["operator_observed_similarity_to_lp_body_depictions"] is True
    assert record["visual_similarity_claim_status"] == "human_observation_unverified"
    assert record["lp_page_14_15_16_candidate_paths_checked"] is True
    assert record["image_forensics_performed"] is False
    assert record["ocr_performed"] is False
    assert record["ai_ml_interpretation_performed"] is False
    assert record["solve_claim"] is False
