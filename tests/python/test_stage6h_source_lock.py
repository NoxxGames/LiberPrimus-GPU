from __future__ import annotations

from pathlib import Path

from libreprimus.token_block import stage6h
from libreprimus.token_block.models import read_yaml

_BUILT = False


def ensure_stage6h_built() -> None:
    global _BUILT
    if _BUILT:
        return
    if stage6h.PROJECT_STATE_PATHS["summary"].exists() and stage6h.TOKEN_BLOCK_PATHS["stage6i_manifest_input_addendum"].exists():
        _BUILT = True
        return
    stage6h.build_stage6h()
    _BUILT = True


def test_stage6h_aggregate_validator_passes() -> None:
    ensure_stage6h_built()
    result = stage6h.validate_stage6h()
    assert result.errors == []
    assert result.counts["number_fact_overlay_count"] == 15
    assert result.counts["future_diagnostic_count"] == 33


def test_stage6h_source_harvester_provenance_records_are_mandatory() -> None:
    ensure_stage6h_built()
    for key, path in stage6h.SOURCE_HARVESTER_PATHS.items():
        payload = read_yaml(path)
        assert payload["stage_id"] == "stage-6h", key
        assert Path(payload["schema"]).exists(), key
        assert payload["stage7_execution_allowed_next"] is False

    recent = read_yaml(stage6h.SOURCE_HARVESTER_PATHS["recent_chat_provenance"])
    assert recent["recent_chat_transcript_local_file_present"] is False
    assert recent["recent_chat_transcript_prompt_attached_context_present"] is True
    assert recent["recent_chat_transcript_raw_committed_now"] is False
    assert recent["used_as_operator_assistant_analysis_context"] is True
    assert recent["used_as_canonical_image_proof"] is False
    assert recent["used_as_canonical_transcription_proof"] is False
    assert recent["requires_canonical_source_crosscheck"] is True


def test_stage6h_exact_constants_and_center_gp41_guardrail() -> None:
    ensure_stage6h_built()
    constants = read_yaml(stage6h.PROJECT_STATE_PATHS["exact_constants"])
    assert constants["stage6h_exact_constants_must_be_validated"] == stage6h.EXACT_CONSTANTS
    assert constants["stage6h_exact_constants_must_be_validated"]["three_dot_angle"]["atan_degrees"] == 41.1859
    assert constants["stage6h_exact_constants_must_be_validated"]["branch_binary"]["concat_y_x_value"] == 479
    assert constants["stage6h_exact_constants_must_be_validated"]["branch_binary"]["geometric_concat_value"] == 447
    assert constants["stage6h_exact_constants_must_be_validated"]["branch_binary"]["prime_count_pi_447"] == 86

    summary = read_yaml(stage6h.PROJECT_STATE_PATHS["source_lock_summary"])
    center_policy = summary["center_anchor_gp41_claim_policy"]
    assert center_policy["center_position_41_source_locked"] is True
    assert center_policy["center_word_index_41_source_locked"] is True
    assert center_policy["center_rune_gp_value_41_source_locked_now"] is False
    assert center_policy["operator_claim_pending_source_confirmation"] is True
    assert center_policy["do_not_assert_as_source_locked_fact"] is True


def test_stage6h_branch_binary_order_table_and_prime_count_policy() -> None:
    ensure_stage6h_built()
    table = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-branch-dot-five-slot-binary-order-policy-table-v0"])
    policies = table["branch_dot_ordering_policies"]
    assert policies["y_x_black_1"] == {"bits": "01110", "value": 14}
    assert policies["y_x_white_1"] == {"bits": "10001", "value": 17}
    assert policies["geometric_black_1"] == {"bits": "01101", "value": 13}
    assert policies["geometric_white_1"] == {"bits": "10010", "value": 18}
    assert policies["centroid_angle_black_1"] == {"bits": "10101", "value": 21}
    assert policies["centroid_angle_white_1"] == {"bits": "01010", "value": 10}
    assert policies["left_to_right_black_1"] == {"bits": "10011", "value": 19}
    assert policies["left_to_right_white_1"] == {"bits": "01100", "value": 12}
    assert policies["branch_anchor_black_1"] == {"bits": "10110", "value": 22}
    assert policies["branch_anchor_white_1"] == {"bits": "01001", "value": 9}
    assert table["selected_order_policy_now"] is None
    assert table["selection_status"] == "no_order_selected"
    assert table["branch_bridges_required"]["direct_concat_479"]["concat_value"] == 479
    assert table["branch_bridges_required"]["weaker_primepi86_control"]["concat_value"] == 447
    assert table["branch_bridges_required"]["weaker_primepi86_control"]["prime_count_pi_447"] == 86

    prime_control = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-branch-dot-geometric-concat-primepi86-control-v0"])
    policy = prime_control["prime_count_policy"]
    assert policy["pi_447_means_number_of_primes_less_than_or_equal_to_447"] is True
    assert policy["pi_447_expected_value"] == 86
    assert policy["not_prime_86"] is True
    assert policy["not_one_indexed_prime_lookup"] is True


def test_stage6h_way_read_records_preserve_candidate_caveats() -> None:
    ensure_stage6h_built()
    word52 = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-pdd153-pdd-minus-reversed-word52-way-verified-v0"])
    assert word52["word52_way"]["result_latin"] == "WAY"
    assert word52["word52_way"]["operation"] == "heading_minus_reversed_word_mod29"

    word55 = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-pdd153-pdd-minus-reversed-word55-read-prefix-candidate-v0"])
    assert word55["word55_read_prefix"]["result_prefix"] == "READ"
    assert word55["word55_read_prefix"]["full_plaintext_claimed"] is False
    assert "READ_prefix_does_not_continue_as_full_plaintext_under_first_pass" in word55["risk_notes"]
    assert "transform_does_not_solve_PDD153" in word55["risk_notes"]


def test_stage6h_residue_and_pdd_geometry_records_are_exact() -> None:
    ensure_stage6h_built()
    pdd = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-pdd153-right-angle-coordinate-transform-v0"])
    assert pdd["right_angle_transform"]["position_formula"] == "n = T(r - 1) + c"

    ray = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-pdd153-dot-angle41-center-to-d4-position133-bridge-v0"])
    assert ray["visual_7_8_ray"]["endpoint_position"] == 133
    assert ray["visual_7_8_ray"]["endpoint_diagonal"] == "d4"

    complement = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-pdd153-dot-angle-complement-8-7-route-candidate-v0"])
    assert complement["visual_8_7_complement"]["endpoint_position"] == 148

    folded = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-pdd153-folded-7-8-8-7-seam-50-51-candidate-v0"])
    assert folded["folded_7_8_8_7"]["seven_eight_endpoint_position"] == 50
    assert folded["folded_7_8_8_7"]["eight_seven_endpoint_position"] == 51

    split = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-pdd153-folded-triangle-72-9-72-spine-split-candidate-v0"])
    assert split["vertical_split"]["left_nonspine_cells"] == 72
    assert split["vertical_split"]["spine_cells"] == 9
    assert split["vertical_split"]["right_nonspine_cells"] == 72
    assert split["vertical_split"]["shared_spine_left_surface_cells"] == 81
    assert split["vertical_split"]["shared_spine_right_surface_cells"] == 81
    assert split["vertical_split"]["spine_positions"] == [1, 5, 13, 25, 41, 61, 85, 113, 145]

    iam = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-pdd153-i-am-circumference-mod153-left-edge-bridge-v0"])
    assert iam["i_am_circumference_mod153"]["I_AM_gp"] == 199
    assert iam["i_am_circumference_mod153"]["I_AM_mod153"] == 46
    assert iam["i_am_circumference_mod153"]["CIRCUMFERENCE_gp"] == 398
    assert iam["i_am_circumference_mod153"]["CIRCUMFERENCE_mod153"] == 92

    variants = read_yaml(stage6h.HISTORICAL_ROUTE_PATHS["stage6h-ouroboros-variant-mod153-offset-bridge-v0"])
    assert variants["ouroboros_variants"]["UROBOROS"]["pdd153_excess"] == 7
    assert variants["ouroboros_variants"]["OROBOROS"]["pdd153_excess"] == 11
    assert variants["ouroboros_variants"]["OUROBOROS"]["pdd153_excess"] == 14


def test_stage6h_required_overlays_are_present_review_only_and_blocked_as_evidence() -> None:
    ensure_stage6h_built()
    payload = read_yaml(stage6h.DATA_PATHS["number_fact_overlays"])
    assert payload["stage6h_number_fact_overlays_required"] is True
    assert payload["overlay_count"] == len(stage6h.OVERLAY_IDS) == 15
    overlays = {item["overlay_id"]: item for item in payload["overlays"]}
    assert set(overlays) == set(stage6h.OVERLAY_IDS)

    for overlay_id in stage6h.OVERLAY_IDS:
        overlay = overlays[overlay_id]
        assert overlay["usable_for_decision_now"] is False
        assert overlay["not_allowed_as"] == stage6h.NOT_ALLOWED_AS
        assert overlay["source_record_path"]
        assert overlay["source_paths"]
        assert overlay["risk_notes"]
        assert overlay["controls_required"]

    prime_overlay = overlays["stage6h_branch_concat_447_primepi86_overlay"]
    assert prime_overlay["prime_count_policy"]["pi_447_expected_value"] == 86
    assert prime_overlay["prime_count_policy"]["not_prime_86"] is True


def test_stage6h_future_diagnostics_have_exact_counts_and_remain_disabled() -> None:
    ensure_stage6h_built()
    payload = read_yaml(stage6h.TOKEN_BLOCK_PATHS["future_diagnostic_registry"])
    counts = payload["future_diagnostic_counts"]
    assert counts["dot_diagnostic_count_expected"] == 12
    assert counts["pdd153_diagnostic_count_expected"] == 12
    assert counts["route_cipher_diagnostic_count_expected"] == 9
    assert counts["total_stage6h_future_diagnostic_count_expected"] == 33
    diagnostics = payload["future_diagnostics"]
    assert len(diagnostics) == 33
    assert sum(1 for item in diagnostics if item["diagnostic_group"] == "dot") == 12
    assert sum(1 for item in diagnostics if item["diagnostic_group"] == "pdd153") == 12
    assert sum(1 for item in diagnostics if item["diagnostic_group"] == "route_cipher") == 9

    for item in diagnostics:
        for flag in [
            "stage6h_run_now",
            "execution_enabled_now",
            "stage7_execution_enabled_now",
            "route_stream_generated_now",
            "byte_stream_generated_now",
            "cipher_execution_performed_now",
            "scoring_performed_now",
            "result_archive_created_now",
        ]:
            assert item[flag] is False, (item["diagnostic_id"], flag)
        assert item["full_output_archive_required_when_run_later"] is True
        assert item["no_lossy_filtering_required_when_run_later"] is True


def test_stage6h_stage6i_addendum_merges_explicit_paths_and_is_not_manifest() -> None:
    ensure_stage6h_built()
    payload = read_yaml(stage6h.TOKEN_BLOCK_PATHS["stage6i_manifest_input_addendum"])
    assert payload["stage6i_addendum_required"] is True
    assert payload["stage6i_addendum_path"] == "data/token-block/stage6h-stage6i-manifest-input-addendum.yaml"
    assert payload["not_final_stage7_manifest"] is True
    assert payload["stage7_execution_allowed_from_this_addendum"] is False
    assert payload["stage7_zip_archive_creation_allowed_from_this_addendum"] is False
    assert payload["path_substitution_ledger"] == []

    input_ids = {row["input_id"] for row in payload["stage6i_addendum_inputs"]}
    assert input_ids == {
        "stage6c_ouroboros_i31_inputs",
        "stage6d_doublet_boundary_inputs",
        "stage6e_bridge_traceability_inputs",
        "stage6f_acceptance_traceability_alias_dju_bei_repairs",
        "stage6g_current_doc_handoff_backlog_repair",
        "stage6h_source_lock_records",
        "stage6h_disabled_future_diagnostics",
    }
    for row in payload["stage6i_addendum_inputs"]:
        assert Path(row["path"]).exists(), row
        assert row["path_exists_at_build_time"] is True
