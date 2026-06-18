from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.token_block import stage6d
from test_stage6_common import load_yaml


def ensure_stage6d_built() -> None:
    if not stage6d.PROJECT_STATE_PATHS["summary"].exists():
        stage6d.build_stage6d()


def assert_exact_profile_values_from_reproduction(reproduction: dict) -> None:
    p15 = reproduction["profiles"]["pages15_70"]
    raw = reproduction["raw_vs_collapsed"]
    p14 = reproduction["profiles"]["pages14_70"]
    p72 = reproduction["profiles"]["pages15_72"]
    assert p15["rune_count"] == 12956
    assert p15["lag1_adjacent_doublets"] == 86
    assert p15["lag_counts"][5] == 479
    assert p15["compact_vector"] == "42442156242421632042324217223"
    assert p15["vector"] == stage6d.EXPECTED_PAGES15_70_VECTOR
    assert raw["raw_adjacent_doublets"] == 60
    assert raw["delimiter_bridged_doublets"] == 26
    assert raw["collapsed_total"] == 86
    assert raw["delimiter_bridge_breakdown"] == {
        "word_delimiter_minus": 21,
        "line_delimiter_slash": 3,
        "slash_minus_mixed_boundary": 1,
        "clause_delimiter_period": 1,
    }
    assert p14["rune_count"] == 13045
    assert p14["lag1_adjacent_doublets"] == 89
    assert p14["delta_from_pages15_70"] == {"F": 1, "L": 2}
    assert p72["rune_count"] == 13136
    assert p72["lag_counts"][1] == 89
    assert p72["lag_counts"][11] == 395
    assert p72["lag_counts"][99] == 520
    assert p72["average_lag2_to_lag110_approx"] == 451


def assert_exact_profile_values_from_committed_records() -> None:
    p15 = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["canonical_doublet_profile_pages15_70"])
    raw = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["raw_vs_collapsed_doublet_boundary_contribution"])
    p14 = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["instruction_page14_doublet_delta"])
    p72 = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["lag_distance_profile_pages15_72"])
    assert p15["rune_count"] == 12956
    assert p15["doublet_lag1_total"] == 86
    assert p15["lag5_equal_count"] == 479
    assert p15["adjacent_doublet_compact_vector"] == "42442156242421632042324217223"
    assert p15["adjacent_doublet_vector"] == stage6d.EXPECTED_PAGES15_70_VECTOR
    assert raw["raw_adjacent_doublets"] == 60
    assert raw["delimiter_bridged_doublets"] == 26
    assert raw["collapsed_total"] == 86
    assert raw["delimiter_bridge_breakdown"] == {
        "word_delimiter_minus": 21,
        "line_delimiter_slash": 3,
        "slash_minus_mixed_boundary": 1,
        "clause_delimiter_period": 1,
    }
    assert p14["rune_count"] == 13045
    assert p14["lag1_adjacent_doublets"] == 89
    assert p14["delta_from_pages15_70"] == {"F": 1, "L": 2}
    assert p72["rune_count"] == 13136
    assert p72["lag1"] == 89
    assert p72["lag11"] == 395
    assert p72["lag99"] == 520
    assert p72["average_lag2_to_lag110_approx"] == 451


def test_stage6d_summary_routes_to_stage6e_with_explicit_archive_false_fields() -> None:
    ensure_stage6d_built()
    summary = load_yaml(stage6d.PROJECT_STATE_PATHS["summary"])
    current = load_yaml("data/project-state/current-stage-state.yaml")
    assert summary["stage_id"] == "stage-6d"
    assert summary["previous_stage_id"] == "stage-6c"
    assert summary["recommended_next_stage_id"] == "stage-6e"
    assert summary["stage7_manifest_created_now"] is False
    assert summary["stage7_execution_allowed_next"] is False
    assert summary["stage7_zip_archive_creation_allowed_next"] is False
    assert current["latest_completed_stage_id"] in {"stage-6d", "stage-6e", "stage-6f", "stage-6g"}
    if current["latest_completed_stage_id"] == "stage-6d":
        assert current["previous_completed_stage_id"] == "stage-6c"
        assert current["recommended_next_stage_id"] == "stage-6e"
    elif current["latest_completed_stage_id"] == "stage-6e":
        assert current["previous_completed_stage_id"] == "stage-6d"
        assert current["recommended_next_stage_id"] == "stage-6f"
    elif current["latest_completed_stage_id"] == "stage-6f":
        assert current["previous_completed_stage_id"] == "stage-6e"
        assert current["recommended_next_stage_id"] == "stage-6g"
    else:
        assert current["previous_completed_stage_id"] == "stage-6f"
        assert current["recommended_next_stage_id"] == "stage-6h"
    assert current["stage7_zip_archive_creation_allowed_next"] is False
    assert current["stage6d_archive_run_contract_finalized_now"] is False
    assert current["stage6d_creates_stage7_result_archive_now"] is False


def test_stage6d_bounded_reproduction_matches_exact_profiles() -> None:
    ensure_stage6d_built()
    if stage6d.MASTER_TRANSCRIPTION_PATH.exists():
        assert_exact_profile_values_from_reproduction(stage6d.compute_doublet_reproduction())
    else:
        assert_exact_profile_values_from_committed_records()


def test_stage6d_policy_records_include_delimiters_vector_order_and_lists() -> None:
    ensure_stage6d_built()
    profile = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["canonical_doublet_profile_pages15_70"])
    occurrences = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["doublet_421_occurrence_index_canonical_rebuild"])
    zero_pages = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["zero_doublet_page_count14"])
    groups = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["doublet_count_group_size_sequence"])
    policy = profile["boundary_policy"]
    assert policy["doublet_counting_policy_id"] == "lp_master_page_local_delimiter_collapsed_v0"
    assert policy["delimiter_table"] == stage6d.DELIMITER_TABLE
    assert policy["collapsed_page_local_policy_steps"] == stage6d._collapsed_policy_steps()
    assert policy["raw_adjacent_policy_steps"] == stage6d._raw_policy_steps()
    assert profile["adjacent_doublet_vector_policy"]["vector_order_labels"] == stage6d.EXPECTED_VECTOR_ORDER
    assert zero_pages["zero_doublet_pages"] == stage6d.EXPECTED_ZERO_DOUBLET_PAGES
    assert occurrences["doublet_421_occurrence_indices_global_1_based"] == stage6d.EXPECTED_421_OCCURRENCES
    assert groups["doublet_count_groups_by_count"] == stage6d.EXPECTED_GROUPS_BY_COUNT
    assert groups["group_size_sequence"] == [1, 3, 11, 3, 7, 1, 2, 1]


def test_stage6d_community_sections_are_noncanonical_and_no_community_code_executed() -> None:
    ensure_stage6d_built()
    record = load_yaml(stage6d.HISTORICAL_ROUTE_PATHS["early_section_doublet_suppression_plateau"])
    assert record["community_section_profile"]["section_starts"] == [0, 15, 18, 23, 30, 38, 42, 55, 69, 71, 72, 75]
    assert record["community_section_profile"]["trusted_as_canonical_boundaries"] is False
    assert record["community_section_profile"]["section_boundary_warning"] is True
    assert record["bigrams_py_executed_now"] is False
    assert record["community_code_executed_now"] is False
    assert record["canonical_bigram_matrix_recomputed_now"] is False


def test_stage6d_overlays_and_future_probes_are_review_only() -> None:
    ensure_stage6d_built()
    overlays = load_yaml(stage6d.OPERATOR_PATHS["number_fact_overlays"])["overlays"]
    registry = load_yaml(stage6d.TOKEN_BLOCK_PATHS["doublet_future_probe_registry"])
    assert {item["overlay_id"] for item in overlays} == set(stage6d.OVERLAY_IDS)
    for overlay in overlays:
        assert overlay["usable_for_decision_now"] is False
        assert overlay["not_allowed_as"] == stage6d.NOT_ALLOWED_AS
        assert overlay["source_record_path"]
        assert overlay["expression"]
    assert registry["future_probe_ids"] == stage6d.FUTURE_PROBE_IDS
    for probe in registry["future_probes"]:
        assert probe["stage6d_run_now"] is False
        assert probe["stage7_execution_enabled_now"] is False
        assert probe["execution_enabled_now"] is False
        assert probe["control_bundle_id"] == stage6d.CONTROL_BUNDLE_ID
        assert probe["not_solve_evidence"] is True


def test_stage6d_stage6e_addendum_is_additive_and_not_final_manifest() -> None:
    ensure_stage6d_built()
    addendum = load_yaml(stage6d.TOKEN_BLOCK_PATHS["stage6e_manifest_input_addendum"])
    assert addendum["includes_stage6c_ouroboros_i31_input_addendum"] is True
    assert addendum["includes_stage6d_doublet_boundary_input_addendum"] is True
    assert addendum["supersedes_stage6c_addendum"] is False
    assert addendum["supersedes_stage6d_addendum"] is False
    assert addendum["not_final_stage7_manifest"] is True
    assert addendum["stage6e_final_manifest_required"] is True
    assert addendum["stage7_execution_allowed_next"] is False


def test_stage6d_hook_and_automation_evidence_are_report_only() -> None:
    ensure_stage6d_built()
    hooks = load_yaml(stage6d.PROJECT_STATE_PATHS["hook_verification_summary"])
    automation = load_yaml(stage6d.PROJECT_STATE_PATHS["doc_staleness_automation_triage_summary"])
    assert hooks["default_hook_test_environment"]["LIBERPRIMUS_CODEX_HOOK_STRICT"] == "unset"
    assert hooks["strict_hook_test_environment"]["LIBERPRIMUS_CODEX_HOOK_STRICT"] == "1"
    assert hooks["hook_default_exit_zero_from_repo_root"] is True
    assert hooks["hook_default_exit_zero_from_subdirectory"] is True
    assert hooks["strict_mode_can_return_nonzero"] is True
    assert hooks["report_path"].startswith("experiments/results/doc-drift/")
    assert automation["local_reproduction_run"] is True
    assert automation["error_count_after_fix"] == 0
    assert automation["warnings_classified"] is True
    assert automation["warnings_fixed"] is False


def test_stage6d_no_scanner_weakening_and_no_forbidden_guardrails() -> None:
    ensure_stage6d_built()
    assert stage6d.validate_stage6d_no_scanner_weakening().validation_error_count == 0
    summary = load_yaml(stage6d.PROJECT_STATE_PATHS["summary"])
    for key, expected in stage6d.FORBIDDEN_FALSE.items():
        if key in summary:
            assert summary[key] is expected


def test_stage6d_protected_paths_are_not_outputs_and_handoff_is_ignored() -> None:
    ensure_stage6d_built()
    outputs = {path.as_posix() for path in stage6d.DATA_PATHS.values()}
    outputs.update(path.as_posix() for path in stage6d.SCHEMA_PATHS.values())
    assert not outputs.intersection(stage6d.stage6.PROTECTED_LOCAL_PATHS)
    handoff_path = Path("codex-output/stage6d-codex-completion.md")
    check_ignore = subprocess.run(
        ["git", "check-ignore", "-q", handoff_path.as_posix()],
        check=False,
        cwd=Path.cwd(),
    )
    assert check_ignore.returncode == 0
    proof = load_yaml(stage6d.SOURCE_HARVESTER_PATHS["raw_source_noncommit_proof"])
    assert proof["protected_local_paths_staged"] is False
    assert proof["generated_outputs_staged"] is False
    assert proof["codex_output_staged"] is False


def test_stage6d_focused_validators_pass() -> None:
    ensure_stage6d_built()
    assert stage6d.validate_stage6d().validation_error_count == 0
