from __future__ import annotations

from test_stage5dr_common import ensure_stage5dr_built, load_yaml


def test_stage5dr_summary_guardrails() -> None:
    ensure_stage5dr_built()
    summary = load_yaml("data/project-state/stage5dr-summary.yaml")

    assert summary["stage_id"] == "stage-5dr"
    assert summary["status"] == "complete"
    assert summary["stage5dq_preserved"] is True
    assert summary["bottom_details_panel_spans_categories_and_table"] is True
    assert summary["details_panel_hideable"] is True
    assert summary["details_panel_structured_sections"] is True
    assert summary["image_thumbnails_in_details_panel"] is True
    assert summary["image_thumbnail_click_opens_viewer"] is True
    assert summary["url_controls_in_details_panel"] is True
    assert summary["file_location_controls_in_details_panel"] is True
    assert summary["table_context_menu_added"] is True
    assert summary["status_unspecified_display_added"] is True
    assert summary["status_legend_or_tooltip_added"] is True
    assert summary["source_browser_entries_loaded"] >= 1200
    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["active_lineage_record_count"] == 8
    assert summary["parallel_worker_cap"] == 8
    assert summary["route_extraction_performed_now"] is False
    assert summary["ocr_performed"] is False
    assert summary["image_forensics_performed"] is False
    assert summary["execution_performed"] is False
    assert summary["pivot_target_selected_now"] is False
    assert summary["source_lock_record_semantics_rewritten"] is False
    assert summary["recommended_next_stage_id"] == "stage-5ds"


def test_stage5dr_scope_control() -> None:
    ensure_stage5dr_built()
    scope = load_yaml("data/project-state/stage5dr-operator-console-scope-control.yaml")

    assert scope["scope"] == "operator_console_source_browser_detail_panel_and_interaction_refinement_only"
    assert scope["committed_source_lock_records_read_only"] is True
    assert scope["manual_entry_semantics_unchanged"] is True
    assert scope["url_opening_explicit_operator_action_only"] is True
    assert scope["image_thumbnail_generation_interpretation_free"] is True
    assert scope["raw_third_party_files_mutated_by_gui"] is False
    assert scope["committed_source_lock_records_directly_rewritten"] is False
