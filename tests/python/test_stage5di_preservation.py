from __future__ import annotations

from libreprimus.token_block.stage5di import (
    validate_stage5di_active_lineage_preservation,
    validate_stage5di_stage5bd_preservation,
    validate_stage5di_stage5dg_preservation,
)

from test_stage5di_common import ensure_stage5di_built, load_yaml, write_temp_yaml


def test_stage5di_preserves_stage5dg_operator_approval_without_gate_opening() -> None:
    ensure_stage5di_built()
    counts, errors = validate_stage5di_stage5dg_preservation()

    assert errors == []
    assert counts["stage5dg_operator_approval_record_preserved"] is True
    assert counts["operator_approval_component_satisfied_now"] is True
    assert counts["combined_approval_gate_satisfied_now"] is False


def test_stage5di_preserves_stage5bd_and_active_lineage_counts() -> None:
    ensure_stage5di_built()
    stage5bd_counts, stage5bd_errors = validate_stage5di_stage5bd_preservation()
    lineage_counts, lineage_errors = validate_stage5di_active_lineage_preservation()

    assert stage5bd_errors == []
    assert lineage_errors == []
    assert stage5bd_counts["stage5bd_run_plan_id_count"] == 10
    assert stage5bd_counts["stage5bd_run_plan_ids_changed"] is False
    assert lineage_counts["active_lineage_record_count"] == 8
    assert lineage_counts["correct_stage5aw_path_included"] is True
    assert lineage_counts["deprecated_stage5aw_path_absent"] is True


def test_stage5di_preservation_rejects_stage5bd_mutation(tmp_path) -> None:
    ensure_stage5di_built()
    payload = load_yaml("data/token-block/stage5di-stage5bd-plan-preservation.yaml")
    payload["stage5bd_run_plan_ids_changed"] = True
    temp = write_temp_yaml(tmp_path / "stage5bd.yaml", payload)

    _, errors = validate_stage5di_stage5bd_preservation(preservation=temp)

    assert errors
    assert "stage5bd_run_plan_ids_changed_must_be_false" in errors
