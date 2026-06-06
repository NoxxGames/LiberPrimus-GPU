from __future__ import annotations

from test_stage5dn_common import ensure_stage5dn_built, load_yaml


def test_stage5dn_summary_and_gates_are_closed() -> None:
    ensure_stage5dn_built()
    summary = load_yaml("data/project-state/stage5dn-summary.yaml")

    assert summary["stage_id"] == "stage-5dn"
    assert summary["status"] == "complete"
    assert summary["disk_cipher_v1_source_lock_created"] is True
    assert summary["candidate_records_created"] == 11
    assert summary["pivot_target_selected_now"] is False
    assert summary["execution_authorized_now"] is False
    assert summary["alberti_cipher_execution_performed_now"] is False
    assert summary["html_tool_executed_now"] is False
    assert summary["ocr_performed"] is False
    assert summary["parallel_worker_cap_for_stage5dn_and_later"] == 8
    assert summary["recommended_next_stage_id"] == "stage-5do"


def test_stage5dn_disk_source_lock_inventory_is_metadata_only() -> None:
    ensure_stage5dn_built()
    record = load_yaml("data/source-harvester/stage5dn-disk-cipher-v1-source-lock-register.yaml")

    assert record["source_root_exists"] is True
    assert record["results_png_present"] is True
    assert record["message_bodies_present"] is True
    assert record["html_tool_present"] is True
    assert record["raw_files_committed_now"] is False
    assert record["file_count_observed"] >= 3
    assert all(item["raw_file_committed_now"] is False for item in record["files"])


def test_stage5dn_results_png_and_message_bodies_are_locked_not_processed() -> None:
    ensure_stage5dn_built()
    results = load_yaml("data/source-harvester/stage5dn-disk-results-png-source-lock.yaml")
    bodies = load_yaml("data/source-harvester/stage5dn-disk-message-bodies-source-lock.yaml")

    assert results["source_present"] is True
    assert results["raw_file_committed_now"] is False
    assert results["image_forensics_performed"] is False
    assert results["ocr_performed"] is False
    assert bodies["present"] is True
    assert bodies["full_raw_body_committed"] is False
    assert len(bodies["claim_groups"]) >= 6


def test_stage5dn_disk_56311_wynn_way_bridge_is_review_only() -> None:
    ensure_stage5dn_built()
    record = load_yaml("data/historical-route/stage5dn-disk-56311-wynn-way-bridge-v1.yaml")

    assert record["candidate_family_id"] == "disk_56311_wynn_way_bridge_v1"
    assert record["source_sequence"] == [5, 6, 3, 11]
    assert record["wynn_bridge_present"] is True
    assert record["word52_way_derivation_candidate"] is True
    assert record["accepted_as_route"] is False
    assert record["execution_allowed"] is False


def test_stage5dn_p39_doublet_probability_and_circumference_records() -> None:
    ensure_stage5dn_built()
    p39 = load_yaml("data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml")
    doublet = load_yaml("data/historical-route/stage5dn-disk-doublet-suppression-candidate-v1.yaml")
    probability = load_yaml("data/historical-route/stage5dn-disk-probability-claim-quarantine-v1.yaml")
    precedent = load_yaml(
        "data/historical-route/stage5dn-solved-i-voice-of-circumference-precedent-v0.yaml"
    )

    assert p39["candidate_family_id"] == "disk_p39_row1_math_semantic_cluster_v1"
    assert p39["accepted_as_route"] is False
    assert p39["disk_cipher_execution_performed_now"] is False
    assert doublet["claimed_expected_doublets"] == 448
    assert doublet["claimed_observed_doublets"] == 89
    assert doublet["accepted_as_validated"] is False
    assert doublet["accepted_as_route"] is False
    assert probability["probability_claims_present"] is True
    assert probability["probability_claim_accepted_as_validated"] is False
    assert "negative_controls" in probability["future_requirements"]
    assert precedent["accepted_as_solved_precedent"] is True
    assert precedent["used_for_decryption_now"] is False


def test_stage5dn_preserves_prior_stage_and_handoff_policy() -> None:
    ensure_stage5dn_built()
    stage5dm = load_yaml("data/project-state/stage5dn-stage5dm-preservation.yaml")
    handoff = load_yaml("data/source-harvester/stage5dn-codex-handoff-policy.yaml")
    drive = load_yaml("data/project-state/stage5dn-drive-folder-policy-update.yaml")

    assert stage5dm["stage5dm_preserved"] is True
    assert stage5dm["stage5dm_rerun_performed"] is False
    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["deprecated_codex_output_used"] is False
    assert drive["preferred_google_drive_folder_now"] == "LiberPrimusSolver"
    assert drive["google_drive_storage_used"] is False
