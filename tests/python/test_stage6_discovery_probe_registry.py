from __future__ import annotations

from libreprimus.token_block import stage6
from test_stage6_common import stage6_data


def test_stage6_registry_preserves_stage5eh_probe_ids() -> None:
    payload = stage6_data("discovery_probe_manifest_registry")
    ids = {entry["diagnostic_id"] for entry in payload["diagnostics"]}
    assert set(stage6.STAGE5EH_PROBE_IDS).issubset(ids)
    assert payload["stage5eh_probe_count_preserved"] == 23


def test_stage6_registry_includes_exact_observation_future_probe_ids() -> None:
    payload = stage6_data("discovery_probe_manifest_registry")
    ids = {entry["diagnostic_id"] for entry in payload["diagnostics"]}
    assert set(stage6.OBSERVATION_PROBE_IDS).issubset(ids)
    assert payload["observation_on_rune_frequency_probe_count"] == 11


def test_stage6_all_probe_registry_entries_are_future_only() -> None:
    payload = stage6_data("discovery_probe_manifest_registry")
    for entry in payload["diagnostics"]:
        assert entry["stage6_run_now"] is False
        assert entry["execution_enabled_now"] is False
        assert entry["finite_input_set_required"] is True
        assert entry["full_output_archive_required_when_run"] is True
        assert entry["not_solve_evidence"] is True


def test_stage6_builder_uses_explicit_probe_family_mapping() -> None:
    records = {
        entry["diagnostic_id"]: entry
        for entry in stage6.stage6_discovery_probe_records_for_validation()
    }
    expected = stage6.expected_probe_classification_for_validation()
    assert set(records) == set(expected)
    for probe_id, expected_record in expected.items():
        assert records[probe_id]["family_id"] == expected_record["family_id"]
        assert records[probe_id]["readiness_class"] == expected_record["readiness_class"]
        assert records[probe_id]["run_allowed_stage"] == expected_record["run_allowed_stage"]


def test_stage6_original_mapping_bug_does_not_recur() -> None:
    records = {
        entry["diagnostic_id"]: entry
        for entry in stage6.stage6_discovery_probe_records_for_validation()
    }
    non_lag5 = {
        "outguess_pgp_signature_verification_probe_candidate_v0",
        "outguess_00_01_02_xor_reconstruction_probe_candidate_v0",
        "byte_strings_token_block_matrix_comparison_probe_candidate_v0",
        "page54_55_red_numbered_line_block_transcript_alignment_probe_candidate_v0",
        "lp_pages_stegdetect_baseline_probe_manifest_v0",
        "page13_canonical_image_hash_and_detector_reproduction_probe_manifest_v0",
    }
    for probe_id in non_lag5:
        assert records[probe_id]["family_id"] != "lag5_copy_null_doublet_diagnostics"
    assert (
        records["page54_55_red_numbered_line_block_transcript_alignment_probe_candidate_v0"]["family_id"]
        == "page54_55_red_number_alignment_readiness"
    )
    assert (
        records["lp_pages_stegdetect_baseline_probe_manifest_v0"]["family_id"]
        == "stego_positive_control_toolchain_readiness"
    )


def test_stage6_probe_source_traceability_or_stage6c_gap_exists() -> None:
    for entry in stage6.stage6_discovery_probe_records_for_validation():
        assert (
            entry["source_records"]
            or entry["source_roots"]
            or entry["source_gap_or_stage6c_precondition"]
        )
