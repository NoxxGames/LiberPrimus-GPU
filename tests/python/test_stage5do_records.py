from __future__ import annotations

from test_stage5do_common import ensure_stage5do_built, load_yaml


def test_stage5do_summary_and_gates_are_closed() -> None:
    ensure_stage5do_built()
    summary = load_yaml("data/project-state/stage5do-summary.yaml")

    assert summary["stage_id"] == "stage-5do"
    assert summary["status"] == "complete"
    assert summary["number_facts_collection_locked"] is True
    assert summary["potential_hint_locked"] is True
    assert summary["number_facts_file_count"] == 11
    assert summary["potential_hint_file_count"] == 10
    assert summary["messages_txt_source_locks"] == 2
    assert summary["candidate_records_created"] == 15
    assert summary["pixel_rgb185_3301_status"] == "source_locked_canonical_image_verification_required"
    assert summary["source_browser_gui_future_requirement_recorded"] is True
    assert summary["source_browser_gui_implemented_now"] is False
    assert summary["pivot_target_selected_now"] is False
    assert summary["execution_authorized_now"] is False
    assert summary["parallel_worker_cap_for_stage5do_and_later"] == 8
    assert summary["recommended_next_stage_id"] == "stage-5dp"


def test_stage5do_source_locks_are_metadata_only() -> None:
    ensure_stage5do_built()
    number_facts = load_yaml("data/source-harvester/stage5do-number-facts-source-lock-register.yaml")
    potential_hint = load_yaml("data/source-harvester/stage5do-potential-hint-source-lock-register.yaml")
    raw_proof = load_yaml("data/source-harvester/stage5do-raw-source-noncommit-proof.yaml")

    assert number_facts["source_root_exists"] is True
    assert number_facts["file_count_observed"] == 11
    assert potential_hint["source_root_exists"] is True
    assert potential_hint["file_count_observed"] == 10
    assert all(item["raw_file_committed_now"] is False for item in number_facts["files"])
    assert all(item["raw_file_committed_now"] is False for item in potential_hint["files"])
    assert raw_proof["raw_source_files_committed_now"] is False
    assert raw_proof["raw_source_files_staged_now"] == 0


def test_stage5do_arithmetic_candidates_are_review_only() -> None:
    ensure_stage5do_built()
    page32_sum = load_yaml("data/historical-route/stage5do-page32-red-header-progressive-gp-sum-2472.yaml")
    page32_index = load_yaml("data/historical-route/stage5do-page32-red-header-cumulative-index-463-3299.yaml")
    no_f = load_yaml("data/historical-route/stage5do-no-f-rune-count-section-flow-candidate.yaml")
    lp1 = load_yaml("data/historical-route/stage5do-lp1-encrypted-word-count-464-prime-3301.yaml")

    assert page32_sum["progressive_sum"] == 2472
    assert page32_sum["arithmetic_verified_now"] is True
    assert page32_sum["accepted_as_route"] is False
    assert page32_index["gp_total"] == 463
    assert page32_index["prime_463_one_indexed"] == 3299
    assert page32_index["accepted_as_route"] is False
    assert no_f["claims"][0]["value"] == 1433
    assert no_f["claims"][0]["component_sum_verified_now"] is True
    assert no_f["canonical_transcript_verification_required"] is True
    assert lp1["word_count_claims"]["total"] == 464
    assert lp1["prime_464"] == 3301


def test_stage5do_pixel_and_frequency_records_stay_blocked() -> None:
    ensure_stage5do_built()
    pixel = load_yaml("data/historical-route/stage5do-page32-dead-tree-rgb185-count-3301-candidate.yaml")
    tables = load_yaml("data/historical-route/stage5do-pixel-colour-frequency-source-tables.yaml")

    assert pixel["claimed_rgb"] == [185, 185, 185]
    assert pixel["claimed_frequency"] == 3301
    assert pixel["canonical_original_image_verification_required"] is True
    assert pixel["pixel_count_verified_against_canonical_now"] is False
    assert pixel["probability_claim_quarantined"] is True
    assert tables["prime_index_correction"]["prime_174"] == 1033
    assert tables["prime_index_correction"]["prime_185"] == 1103
    assert tables["prime_index_correction"]["statement"] == "1033 is not the 185th prime"


def test_stage5do_future_gui_is_requirement_only() -> None:
    ensure_stage5do_built()
    gui = load_yaml("data/project-state/stage5do-source-lock-browser-gui-future-requirement.yaml")

    assert gui["operator_requested_browser"] is True
    assert gui["implementation_now"] is False
    assert gui["recommended_future_stage_id"] == "stage-5dp"
    assert gui["no_puzzle_execution_from_gui"] is True
    assert gui["no_target_validation_from_gui"] is True
