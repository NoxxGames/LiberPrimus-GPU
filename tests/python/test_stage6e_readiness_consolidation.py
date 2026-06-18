from __future__ import annotations

from pathlib import Path
import subprocess

from libreprimus.token_block import stage6, stage6c, stage6d, stage6e
from test_stage6_common import load_yaml


def ensure_stage6e_built() -> None:
    if not stage6e.PROJECT_STATE_PATHS["summary"].exists():
        stage6e.build_stage6e()


def test_stage6e_summary_routes_to_stage6f_without_manifest_archive_or_execution() -> None:
    ensure_stage6e_built()
    summary = load_yaml(stage6e.PROJECT_STATE_PATHS["summary"])
    current = load_yaml("data/project-state/current-stage-state.yaml")
    assert summary["stage_id"] == "stage-6e"
    assert summary["previous_stage_id"] == "stage-6d"
    assert summary["recommended_next_stage_id"] == "stage-6f"
    assert summary["stage6f_manifest_finalization_blocker_count"] == 0
    assert summary["stage6f_can_attempt_final_manifest_without_prior_repair"] is True
    allowed_current_routes = {
        "stage-6e": ("stage-6d", "stage-6f"),
        "stage-6f": ("stage-6e", "stage-6g"),
        "stage-6g": ("stage-6f", "stage-6h"),
    }
    previous, next_stage = allowed_current_routes[current["latest_completed_stage_id"]]
    assert current["previous_completed_stage_id"] == previous
    assert current["recommended_next_stage_id"] == next_stage
    for key in [
        "stage7_execution_allowed_next",
        "stage7_zip_archive_creation_allowed_next",
        "stage6e_final_finite_stage7_manifest_created_now",
        "stage6e_archive_run_contract_finalized_now",
        "stage6e_creates_stage7_result_archive_now",
        "stage6e_generates_stage7_outputs_now",
        "stage6e_routes_to_stage7_now",
        "stage6e_runs_any_probe_now",
        "probe_execution_performed_now",
        "route_stream_generated_now",
        "real_byte_stream_generated",
        "solve_claim",
    ]:
        assert summary[key] is False
        assert current[key] is False


def test_stage6e_bridge_arithmetic_and_source_surface_are_exact_or_gap_recorded() -> None:
    ensure_stage6e_built()
    circumference = load_yaml(stage6e.HISTORICAL_ROUTE_PATHS["circumference_398_two_i_am"])
    masks = load_yaml(stage6e.HISTORICAL_ROUTE_PATHS["c_to_f_gp376"])
    page56 = load_yaml(stage6e.HISTORICAL_ROUTE_PATHS["page56_prime64"])
    big_gap = load_yaml(stage6e.HISTORICAL_ROUTE_PATHS["big_gap_prime104"])
    page32 = load_yaml(stage6e.HISTORICAL_ROUTE_PATHS["page32_3222_factor179"])
    music = load_yaml(stage6e.HISTORICAL_ROUTE_PATHS["music_circumference"])
    dju = load_yaml(stage6e.HISTORICAL_ROUTE_PATHS["dju_bei_source_gap"])
    assert circumference["CIRCUMFERENCE_gp_sum"] == 398
    assert circumference["I_AM_gp_sum"] == 199
    assert circumference["relation"] == "398 = 2 * 199"
    mask_table = {row["mask_bits"]: row for row in masks["mask_table"]}
    assert mask_table["000"]["gp_sum"] == 398
    assert {row["gp_sum"] for row in mask_table.values() if row["mask_count"] == 1} == {387}
    assert {row["gp_sum"] for row in mask_table.values() if row["mask_count"] == 2} == {376}
    assert mask_table["111"]["spelling"] == "FIRFUMFERENFE"
    assert mask_table["111"]["gp_sum"] == 365
    assert masks["normalized_gp_surface"] == "DIUINITY"
    assert masks["divinity_or_diuinity_sum"] == 376
    assert page56["AN_END_gp_sum"] == 311
    assert page56["FIVE_DOTS_gp_sum"] == 311
    assert page56["prime_index_policy"]["convention"] == "one_indexed"
    assert big_gap["big_gap_one_based_page_sum"] == 569
    assert big_gap["one_indexed_prime_104"] == 569
    assert page32["page32_value"] == 3222
    assert page32["page15_phrase_gp_sum"] == 971
    assert page32["reverse_971"] == 179
    assert music["music_line_gp_sum"] == 1031
    assert dju["exact_span_found"] is False
    assert dju["source_gap_or_precondition"]
    assert dju["stage6f_manifest_eligible"] is False


def test_stage6e_gp_text_layer_policy_and_source_paths_are_attached() -> None:
    ensure_stage6e_built()
    for key in ["circumference_398_two_i_am", "c_to_f_gp376", "music_circumference"]:
        record = load_yaml(stage6e.HISTORICAL_ROUTE_PATHS[key])
        policy = record["gp_text_layer_policy"]
        assert policy["preferred_latin_labels_used_for_arithmetic"] is True
        assert policy["source_surface_preserved"] is True
        assert policy["c_to_f_mask_is_not_alias_normalization"] is True
        assert policy["c_to_f_mask_is_finite_source_backed_transform_family"] is True
    for path in stage6e.HISTORICAL_ROUTE_PATHS.values():
        record = load_yaml(path)
        assert record["source_paths_all_resolve_or_gap_recorded"] is True
        assert record.get("source_paths") or record.get("source_gap_or_precondition")


def test_stage6e_warning_classification_is_bucketed_and_scanner_not_weakened() -> None:
    ensure_stage6e_built()
    warnings = load_yaml(stage6e.PROJECT_STATE_PATHS["warning_classification"])
    nonweakening = load_yaml(stage6e.PROJECT_STATE_PATHS["scanner_nonweakening"])
    assert warnings["warnings_fully_classified"] is True
    assert warnings["strict_error_count_after_stage6e_fix"] == 0
    assert warnings["remaining_warnings_all_have_named_bucket"] is True
    assert sum(row["warning_count"] for row in warnings["warning_bucket_rows"]) == warnings["remaining_warning_count"]
    assert all(row["bucket_id"] not in {"misc", "other"} for row in warnings["warning_bucket_rows"])
    assert nonweakening["scanner_weakened"] is False
    assert nonweakening["broad_docs_ignore_added"] is False
    assert nonweakening["broad_current_mirror_ignore_added"] is False
    assert nonweakening["strict_mode_weakened"] is False
    assert nonweakening["real_current_error_downgraded"] is False
    assert nonweakening["broad_path_glob_suppression_added"] is False


def test_stage6e_preflight_hook_is_bounded_report_only_and_preserves_current_truth_order() -> None:
    ensure_stage6e_built()
    preflight = load_yaml(stage6e.PROJECT_STATE_PATHS["preprompt_hook_status"])
    hooks = load_yaml(stage6e.PROJECT_STATE_PATHS["hook_runner_evidence"])
    assert preflight["preprompt_hook_installed"] is True
    assert preflight["scanner_timeout_seconds_default"] == 120
    assert preflight["report_only_default_exit_zero"] is True
    assert preflight["raw_warning_table_printed_to_stdout"] is False
    assert hooks["default_hook_test_environment"]["LIBERPRIMUS_CODEX_HOOK_STRICT"] == "unset"
    assert hooks["strict_hook_test_environment"]["LIBERPRIMUS_CODEX_HOOK_STRICT"] == "1"
    assert hooks["hook_default_exit_zero_verified"] is True
    assert hooks["strict_mode_can_return_nonzero"] is True
    assert hooks["current_truth_context_printed_before_preflight"] is True
    assert hooks["preflight_machine_readable_lines_printed"] is True
    assert hooks["sessionstart_dispatcher_used"] is True


def test_stage6e_traceability_adaptive_counts_and_no_empty_evidence_rows() -> None:
    ensure_stage6e_built()
    matrix = load_yaml(stage6e.TOKEN_BLOCK_PATHS["probe_traceability_matrix"])
    expected = 23 + 11 + 10 + 12 + matrix["stage6e_bridge_probe_count_actual"]
    assert matrix["stage6e_core_bridge_probe_count"] == 9
    assert matrix["stage6e_optional_bridge_probe_count_committed"] == 2
    assert matrix["traceability_expected_row_count"] == expected == 67
    assert matrix["traceability_actual_row_count"] == len(matrix["traceability_rows"]) == expected
    groups = {}
    for row in matrix["traceability_rows"]:
        groups[row["source_group"]] = groups.get(row["source_group"], 0) + 1
        assert row["source_records"] or row["source_gap_or_precondition"]
        assert row["stage7_execution_enabled_now"] is False
        assert row["local_source_presence_required_before_stage7_execution"] is True
        if row["blocking_source_gap"]:
            assert row["stage6f_manifest_eligible"] is False
    assert groups["stage5eh_future_probes"] == len(stage6.STAGE5EH_PROBE_IDS)
    assert groups["stage6_observation_on_rune_frequency_probes"] == len(stage6.OBSERVATION_PROBE_IDS)
    assert groups["stage6c_ouroboros_i31_probes"] == len(stage6c.FUTURE_PROBE_IDS)
    assert groups["stage6d_canonical_doublet_boundary_probes"] == len(stage6d.FUTURE_PROBE_IDS)
    assert groups["stage6e_bridge_probes"] == len(stage6e.STAGE6E_BRIDGE_PROBE_IDS)


def test_stage6e_crosswalk_is_ci_safe_and_not_execution_ready() -> None:
    ensure_stage6e_built()
    crosswalk = load_yaml(stage6e.TOKEN_BLOCK_PATHS["source_root_crosswalk"])
    rows = {row["root_path"]: row for row in crosswalk["source_roots"]}
    assert set(stage6e.REQUIRED_SOURCE_ROOTS).issubset(rows)
    assert crosswalk["ci_test_policy"]["require_ignored_third_party_roots_exist"] is False
    for row in rows.values():
        assert row["sufficient_for_stage7_execution"] is False
        assert row["stage7_execution_requires_local_presence_recheck"] is True
        assert row["raw_recursive_hashing_performed_now"] is False


def test_stage6e_stage6b_precondition_superseded_and_stage6f_addendum_merges_inputs() -> None:
    ensure_stage6e_built()
    supersession = load_yaml(stage6e.PROJECT_STATE_PATHS["stage6b_precondition_supersession"])
    addendum = load_yaml(stage6e.TOKEN_BLOCK_PATHS["stage6f_manifest_input_addendum"])
    assert supersession["old_precondition_text"] == "requires Stage 6C to bind finite token-block projection input set"
    assert supersession["old_precondition_status"] == "stale_after_operator_inserted_stage6c_ouroboros_addendum"
    assert supersession["stage6b_precondition_repaired_or_superseded"] is True
    assert supersession["stage7_execution_enabled_now"] is False
    assert addendum["includes_stage6c_ouroboros_i31_input_addendum"] is True
    assert addendum["includes_stage6d_doublet_boundary_input_addendum"] is True
    assert addendum["includes_stage6e_bridge_source_lock_addendum"] is True
    assert addendum["includes_stage6e_probe_source_traceability_matrix"] is True
    assert addendum["includes_stage6e_source_root_crosswalk"] is True
    assert addendum["not_final_stage7_manifest"] is True
    assert addendum["stage7_execution_allowed_from_this_addendum"] is False
    assert addendum["stage7_zip_archive_creation_allowed_from_this_addendum"] is False


def test_stage6e_overlays_and_future_probes_are_review_only() -> None:
    ensure_stage6e_built()
    overlays = load_yaml(stage6e.OPERATOR_CONSOLE_PATHS["number_fact_overlays"])["overlays"]
    registry = load_yaml(stage6e.TOKEN_BLOCK_PATHS["bridge_future_probe_registry"])
    assert len(overlays) == 10
    for overlay in overlays:
        assert overlay["source_record_path"]
        assert overlay["source_fact_id"]
        assert overlay["source_paths"] or "dju_bei" in overlay["overlay_id"]
        assert overlay["usable_for_decision_now"] is False
        assert overlay["not_allowed_as"] == [
            "proof",
            "route_seed",
            "target_selection",
            "activation_decision",
            "execution_seed",
            "solve_claim",
        ]
    assert registry["future_probe_ids"] == stage6e.STAGE6E_BRIDGE_PROBE_IDS
    for probe in registry["future_probes"]:
        assert probe["stage6e_run_now"] is False
        assert probe["execution_enabled_now"] is False
        assert probe["stage7_execution_enabled_now"] is False
        assert probe["control_bundle_id"] == stage6e.BRIDGE_CONTROL_BUNDLE_ID


def test_stage6e_ignored_local_outputs_are_policy_checked_not_required() -> None:
    ensure_stage6e_built()
    for path in [
        "codex-output/stage6e-codex-completion.md",
        "experiments/results/doc-drift/stage6e-local-stale-current-triage.json",
        "experiments/results/doc-drift/codex-preprompt-doc-staleness-preflight.json",
        "experiments/results/doc-drift/codex-stop-hook-stale-current-audit.json",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", path], cwd=Path.cwd(), check=False)
        assert result.returncode == 0
    handoff = load_yaml(stage6e.SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    assert handoff["require_local_file_exists_in_ci"] is False
    assert handoff["require_path_is_git_ignored"] is True


def test_stage6e_focused_validators_pass_and_guardrails_false() -> None:
    ensure_stage6e_built()
    assert stage6e.validate_stage6e().validation_error_count == 0
    summary = load_yaml(stage6e.PROJECT_STATE_PATHS["summary"])
    for key, expected in stage6e.FORBIDDEN_FALSE.items():
        if key in summary:
            assert summary[key] is expected
