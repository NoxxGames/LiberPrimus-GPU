from __future__ import annotations

from pathlib import Path

import pytest

from libreprimus.token_block import stage6c
from test_stage6_common import load_yaml


def ensure_stage6c_built() -> None:
    if not stage6c.PROJECT_STATE_PATHS["summary"].exists():
        stage6c.build_stage6c()


def test_stage6c_summary_routes_to_stage6d_and_preserves_stage6b() -> None:
    ensure_stage6c_built()
    summary = load_yaml(stage6c.PROJECT_STATE_PATHS["summary"])
    assert summary["stage_id"] == "stage-6c"
    assert summary["previous_stage_id"] == "stage-6b"
    assert summary["recommended_next_stage_id"] == "stage-6d"
    assert summary["stage6b_preserved"] is True
    assert summary["stage6b_probe_mapping_repairs_preserved"] is True
    assert summary["stage6b_hook_report_only_default_preserved"] is True
    assert summary["stage6b_default_hook_exit_zero_preserved"] is True
    assert summary["stage6b_strict_hook_mode_preserved"] is True
    assert summary["stage7_execution_allowed_next"] is False
    assert summary["stage7_zip_archive_creation_allowed_next"] is False


def test_stage6c_text_layer_policy_and_source_crosslinks() -> None:
    ensure_stage6c_built()
    record = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["i31_vowel_voice_circumference"])
    policy = record["text_layer_policy"]
    assert record["exact_quote"] == "THE I IS THE VOICE OF THE CIRCUMFERENCE"
    assert record["quote_source_status"] == "solved_translation_precedent"
    assert policy["gp_profile_preferred_latin_labels"] == "required_for_arithmetic"
    assert policy["exact_rune_tokens"] == "required_where_available"
    assert "U/V" in policy["alias_groups"]
    assert "O and U are distinct GP runes" in policy["important_negative_alias_note"]
    assert "data/profiles/gematria/gematria-primus-v0.json" in record["source_paths"]
    for paths in stage6c.SOURCE_CROSSLINKS.values():
        for path in paths:
            assert Path(path).exists(), path


def test_stage6c_exact_arithmetic_and_tolerant_geometry() -> None:
    ensure_stage6c_built()
    assert stage6c.validate_stage6c_ouroboros_arithmetic().validation_error_count == 0
    i31 = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["i31_vowel_voice_circumference"])
    shell = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["t16_consonant_shell_pdd153"])
    page32 = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["o_ring_3222_page32"])
    internal = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["palindromic_core"])
    checksum = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["index_checksum"])
    geometry = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["i31_geometry"])
    assert i31["gp_values"] == [7, 3, 11, 7, 61, 7, 11, 7, 53]
    assert i31["ouroboros_total"] == 167
    assert i31["vowel_positions_one_based"] == [1, 2, 4, 6, 8]
    assert i31["vowel_sum"] == 31
    assert shell["consonant_sum"] == 136
    assert shell["t16"] == 136
    assert shell["pdd153"] == 153
    assert shell["delta_ouroboros_minus_pdd153"] == 14
    assert page32["o_cyclic_distances"] == [3, 2, 2, 2]
    assert page32["o_cyclic_distance_compact"] == "3222"
    assert internal["inter_o_segment_gp_values"] == [14, 61, 11, 53]
    assert internal["robor_gp_sum"] == 97
    assert internal["oro_gp_sum"] == 25
    assert checksum["zero_based_index_sum"] == 53
    assert checksum["one_based_index_sum"] == 62
    assert abs(geometry["radius_if_circumference_31"] - 4.93) < 0.01
    assert abs(geometry["diameter_if_circumference_31"] - 9.87) < 0.01


def test_stage6c_variant_controls_are_finite_and_no_alias_search() -> None:
    ensure_stage6c_built()
    variants = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["variant_spelling_controls"])
    by_spelling = {item["spelling"]: item for item in variants["variant_controls"]}
    assert set(by_spelling) == {"OUROBOROS", "UROBOROS", "OROBOROS"}
    assert by_spelling["OUROBOROS"]["gp_total"] == 167
    assert by_spelling["OUROBOROS"]["vowel_sum"] == 31
    assert by_spelling["OUROBOROS"]["consonant_sum"] == 136
    assert by_spelling["UROBOROS"]["gp_total"] == 160
    assert by_spelling["UROBOROS"]["vowel_sum"] == 24
    assert by_spelling["UROBOROS"]["consonant_sum"] == 136
    assert by_spelling["UROBOROS"]["excess_over_pdd153"] == 7
    assert by_spelling["UROBOROS"]["excess_label"] == "O"
    assert by_spelling["OROBOROS"]["gp_total"] == 164
    assert by_spelling["OROBOROS"]["vowel_sum"] == 28
    assert by_spelling["OROBOROS"]["consonant_sum"] == 136
    assert by_spelling["OROBOROS"]["excess_over_pdd153"] == 11
    assert by_spelling["OROBOROS"]["excess_label"] == "R"
    assert variants["arbitrary_dictionary_or_spelling_search_performed"] is False


def test_stage6c_page32_3222_policy_keeps_highlight_unconfirmed() -> None:
    ensure_stage6c_built()
    assert stage6c.validate_stage6c_page32_3222_policy().validation_error_count == 0
    record = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["o_ring_3222_page32"])
    status = record["page32_3222_status"]
    assert status["source_backed_as_grid_value"] is True
    assert status["source_backed_as_spiral_sequence_value"] is True
    assert status["source_backed_as_red_or_highlighted"] is False
    assert status["image_inspection_performed_now"] is False
    assert status["image_interpretation_performed_now"] is False
    assert record["operator_observed_highlight_claim_pending_source_confirmation"] is True


def test_stage6c_overlays_are_review_only_and_complete() -> None:
    ensure_stage6c_built()
    assert stage6c.validate_stage6c_number_fact_overlays().validation_error_count == 0
    payload = load_yaml(stage6c.OPERATOR_CONSOLE_PATHS["number_fact_overlays"])
    overlays = {item["overlay_id"]: item for item in payload["overlays"]}
    assert set(overlays) == set(stage6c.OVERLAY_IDS)
    for overlay in overlays.values():
        assert overlay["usable_for_decision_now"] is False
        assert overlay["not_allowed_as"] == stage6c.NOT_ALLOWED_AS
        assert overlay["source_record_path"]
        assert overlay["source_fact_id"]
        assert overlay["expression"]
        assert overlay["relation"]
        assert overlay["source_paths"]
    assert "inter-O segment sums" in overlays["stage6c_ouroboros_inter_o_segments_offset14_overlay"]["expression"]
    assert "zero-based GP profile indices sum" in overlays["stage6c_ouroboros_index_checksum_overlay"]["expression"]


def test_stage6c_future_probes_and_stage6d_addendum_are_non_executable() -> None:
    ensure_stage6c_built()
    assert stage6c.validate_stage6c_future_probe_registry().validation_error_count == 0
    registry = load_yaml(stage6c.TOKEN_BLOCK_PATHS["future_probe_registry"])
    addendum = load_yaml(stage6c.TOKEN_BLOCK_PATHS["stage6d_manifest_input_addendum"])
    assert registry["future_probe_ids"] == stage6c.FUTURE_PROBE_IDS
    for probe in registry["future_probes"]:
        assert probe["stage6c_run_now"] is False
        assert probe["execution_enabled_now"] is False
        assert probe["stage7_execution_enabled_now"] is False
        assert probe["full_output_archive_required_when_run"] is True
        assert probe["control_bundle_id"] == stage6c.CONTROL_BUNDLE_ID
        assert probe["controls_required"] == stage6c.CONTROL_BUNDLE
        assert probe["usable_for_decision_now"] is False
        assert probe["not_solve_evidence"] is True
    assert addendum["source_locked_review_facts"] == stage6c.SOURCE_LOCKED_REVIEW_FACTS
    assert addendum["future_probe_ids"] == stage6c.FUTURE_PROBE_IDS
    assert addendum["not_final_stage7_manifest"] is True
    assert addendum["stage6d_final_manifest_required"] is True


def test_stage6c_stage8_stage9_watchlist_is_not_execution() -> None:
    ensure_stage6c_built()
    assert stage6c.validate_stage6c_stage8_watchlist().validation_error_count == 0
    watchlist = load_yaml(stage6c.HISTORICAL_ROUTE_PATHS["stage8_stage9_watchlist"])
    assert "I31_voice_layer" in watchlist["stage8_stage9_watchlist_terms"]
    assert "OUROBOROS_167" in watchlist["stage8_stage9_watchlist_terms"]
    assert watchlist["stage8_triangle_readiness_started_now"] is False
    assert watchlist["stage9_experiments_started_now"] is False
    assert watchlist["triangular_transposition_readouts_generated_now"] is False
    assert watchlist["spiral_route_readouts_generated_now"] is False


def test_stage6c_current_state_and_guardrails() -> None:
    ensure_stage6c_built()
    assert stage6c.validate_stage6c_current_stage_transition().validation_error_count == 0
    assert stage6c.validate_stage6c_gate_closure().validation_error_count == 0
    current = load_yaml("data/project-state/current-stage-state.yaml")
    assert current["latest_completed_stage_id"] == "stage-6c"
    assert current["previous_completed_stage_id"] == "stage-6b"
    assert current["recommended_next_stage_id"] == "stage-6d"
    assert current["stage7_execution_allowed_next"] is False
    assert current["stage7_zip_archive_creation_allowed_next"] is False
    summary = load_yaml(stage6c.PROJECT_STATE_PATHS["summary"])
    for key, expected in stage6c.FORBIDDEN_FALSE.items():
        if key in summary:
            assert summary[key] is expected


def test_stage6c_cli_summary_contains_core_counts() -> None:
    ensure_stage6c_built()
    text = stage6c.stage6c_summary_text()
    assert "stage_id=stage-6c" in text
    assert "recommended_next_stage_id=stage-6d" in text
    assert "ouroboros_total=167" in text
    assert "future_probe_count=10" in text


@pytest.mark.parametrize(
    "validator",
    [
        stage6c.validate_stage6c_stage6b_preservation,
        stage6c.validate_stage6c_source_lock_records,
        stage6c.validate_stage6c_ouroboros_arithmetic,
        stage6c.validate_stage6c_page32_3222_policy,
        stage6c.validate_stage6c_number_fact_overlays,
        stage6c.validate_stage6c_future_probe_registry,
        stage6c.validate_stage6c_stage8_watchlist,
        stage6c.validate_stage6c_source_browser_loadability,
        stage6c.validate_stage6c_current_stage_transition,
        stage6c.validate_stage6c_gate_closure,
        stage6c.validate_stage6c_handoff,
    ],
)
def test_stage6c_focused_validators_pass(validator) -> None:
    ensure_stage6c_built()
    assert validator().validation_error_count == 0
