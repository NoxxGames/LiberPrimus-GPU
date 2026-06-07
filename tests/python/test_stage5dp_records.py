from __future__ import annotations

from test_stage5dp_common import ROOT, ensure_stage5dp_built, load_yaml


def test_stage5dp_summary_and_gate_status() -> None:
    ensure_stage5dp_built()
    summary = load_yaml("data/project-state/stage5dp-summary.yaml")

    assert summary["stage_id"] == "stage-5dp"
    assert summary["status"] == "complete"
    assert summary["new_reddit_source_lock_created"] is True
    assert summary["required_reddit_source_folders_represented"] == 6
    assert summary["candidate_records_created"] == 23
    assert summary["source_browser_gui_implemented_now"] is False
    assert summary["source_browser_gui_deferred_to_next_stage"] is True
    assert summary["pivot_target_selected_now"] is False
    assert summary["route_extraction_performed_now"] is False
    assert summary["ocr_performed"] is False
    assert summary["image_forensics_performed"] is False
    assert summary["execution_performed"] is False
    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["active_lineage_record_count"] == 8
    assert summary["parallel_worker_cap"] == 8
    assert summary["recommended_next_stage_id"] == "stage-5dq"


def test_stage5dp_source_folders_and_raw_policy() -> None:
    ensure_stage5dp_built()
    source_lock = load_yaml("data/source-harvester/stage5dp-new-reddit-source-lock-register.yaml")
    raw_proof = load_yaml("data/source-harvester/stage5dp-raw-source-noncommit-proof.yaml")
    represented = {item["source_folder"] for item in source_lock["source_folders"]}

    for folder in source_lock["required_source_folders"]:
        assert folder in represented
    assert source_lock["source_gap_count"] == 0
    for folder in source_lock["source_folders"]:
        for file_record in folder["files"]:
            assert file_record["raw_file_committed_now"] is False
            assert file_record["source_lock_only"] is True
    assert raw_proof["raw_source_files_committed_now"] is False
    assert raw_proof["raw_source_files_staged_now"] == 0


def test_stage5dp_mayfly_workbook_and_docx_metadata() -> None:
    ensure_stage5dp_built()
    mayfly = load_yaml("data/source-harvester/stage5dp-mayfly-docx-xlsx-source-lock.yaml")

    assert mayfly["mayfly_docx_present"] is True
    assert mayfly["mayfly_xlsx_present"] is True
    assert mayfly["mayfly_docx_embedded_media_count"] == 37
    assert mayfly["mayfly_docx_paragraph_count"] >= 600
    assert mayfly["mayfly_workbook_sheet_names"] == [
        "READ ME",
        "958x1092 (binary)",
        "958x1092 (4x4 4x5 5x5)",
        "230x262 (binary)",
        "230x262 (weighted)",
    ]
    assert mayfly["original_binary_grid_dimensions"] == [958, 1092]
    assert mayfly["original_binary_ones_sum"] == 35210
    assert mayfly["reduced_binary_grid_dimensions"] == [230, 262]
    assert mayfly["reduced_binary_ones_sum"] == 2033
    assert mayfly["weighted_grid_sum"] == 35210
    assert mayfly["weighted_block_counts"] == {"value_16": 1420, "value_20": 567, "value_25": 46}
    assert mayfly["block_total_from_weighted_counts"] == 2033
    assert mayfly["raw_text_committed_now"] is False
    assert mayfly["raw_workbook_committed_now"] is False


def test_stage5dp_candidate_records_are_source_locked_only() -> None:
    ensure_stage5dp_built()
    key = load_yaml("data/historical-route/stage5dp-mayfly-four-block-key-genome-candidate-v0.yaml")
    axis = load_yaml(
        "data/historical-route/stage5dp-mayfly-horizontal-axis-167-229-229-229-104-candidate-v0.yaml"
    )
    five_dot = load_yaml("data/historical-route/stage5dp-five-dot-shift-skipped-f-page56-candidate-v0.yaml")
    page33 = load_yaml("data/historical-route/stage5dp-page33-three-dot-emirp-area-block-candidate-v0.yaml")
    front = load_yaml("data/historical-route/stage5dp-front-cover-3301-concat-prime-not-emirp-correction-v0.yaml")
    iso = load_yaml(
        "data/historical-route/stage5dp-iso-560-13-560-17-palindromic-prime-size-candidate-v0.yaml"
    )
    problems = load_yaml(
        "data/historical-route/stage5dp-problems-2012-autostereogram-source-tool-candidate-v0.yaml"
    )

    assert key["source_claims"]["gematria_primus_mapping_candidate"] == ["G", "N", "E", "M", "OE"]
    assert key["accepted_as_key"] is False
    assert axis["horizontal_axis_grouped"] == [167, 229, 229, 229, 104]
    assert five_dot["page56_claims"]["skipped_rune"] == "F"
    assert five_dot["pixel_measurements_require_canonical_image_verification"] is True
    assert page33["area_pattern"]["decrement"] == 9
    assert page33["pixel_geometry_source_claimed_pending_canonical_verification"] is True
    assert front["verified_or_source_claimed_arithmetic"]["132714273301_emirp"] is False
    assert iso["arithmetic_claims"]["118818811_palindrome"] is True
    assert problems["lp_relevance"] == "historical_low_priority"
    for record in [key, axis, five_dot, page33, front, iso, problems]:
        assert record["accepted_as_route"] is False
        assert record["route_extraction_performed_now"] is False
        assert record["execution_performed"] is False


def test_stage5dp_chatgpt_context_file_contains_compact_facts() -> None:
    ensure_stage5dp_built()
    text = (ROOT / "ChatGPT-ContextFile.md").read_text(encoding="utf-8")

    assert "Stage 5DP source-locked new Reddit Mayfly/dot/cover/ISO material" in text
    assert "MayFlyInvestigation is high value" in text
    assert "2033 active reduced cells" in text
    assert "candidate-only, not active solve routes" in text
