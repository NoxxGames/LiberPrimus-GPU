from __future__ import annotations

from test_stage5dc_common import ensure_stage5dc_built, load_yaml


def test_stage5dc_preserves_stage5cy_stage5da_stage5bd_and_lineage() -> None:
    ensure_stage5dc_built()
    summary = load_yaml("data/project-state/stage5dc-summary.yaml")

    assert summary["stage5cy_option_selection_preflight_preserved"] is True
    assert summary["stage5cy_validation_count_reconciliation_preserved"] is True
    assert summary["stage5cy_governance_scope_control_preserved"] is True
    assert summary["stage5da_operator_choice_pause_scaffold_preserved"] is True
    assert summary["stage5bd_dry_run_records_remain_valid"] is True
    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["stage5bd_run_plan_ids_changed"] is False
    assert summary["active_lineage_record_count"] == 8
    assert summary["correct_stage5aw_path_included"] is True
    assert summary["deprecated_stage5aw_path_absent"] is True


def test_stage5dc_does_not_mutate_canonical_or_active_manifests() -> None:
    ensure_stage5dc_built()
    lineage = load_yaml("data/token-block/stage5dc-active-lineage-preservation.yaml")

    assert lineage["canonical_transcription_changed"] is False
    assert lineage["active_token_block_manifest_changed"] is False
    assert lineage["all_lineage_paths_resolve"] is True
