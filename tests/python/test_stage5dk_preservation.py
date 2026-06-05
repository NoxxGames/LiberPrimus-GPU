from __future__ import annotations

from libreprimus.token_block import stage5dk
from test_stage5dk_common import ensure_stage5dk_built, load_yaml, write_temp_yaml


def test_stage5dk_preserves_stage5dj_stage5dg_stage5bd_and_lineage() -> None:
    ensure_stage5dk_built()
    stage5dj = load_yaml("data/token-block/stage5dk-stage5dj-preservation.yaml")
    stage5dg = load_yaml("data/token-block/stage5dk-stage5dg-operator-approval-preservation.yaml")
    stage5bd = load_yaml("data/token-block/stage5dk-stage5bd-plan-preservation.yaml")
    lineage = load_yaml("data/token-block/stage5dk-active-lineage-preservation.yaml")

    assert stage5dj["stage5dj_preserved"] is True
    assert stage5dj["stage5dj_activation_authorized"] is False
    assert stage5dg["stage5dg_operator_approval_preserved"] is True
    assert stage5dg["operator_approval_component_satisfied_now"] is True
    assert stage5dg["real_operator_approval_record_created_now"] is False
    assert stage5dg["deep_research_approval_component_satisfied"] is False
    assert stage5dg["combined_gate_satisfied"] is False
    assert stage5bd["stage5bd_run_plan_id_count"] == 10
    assert stage5bd["stage5bd_validation_error_count"] == 0
    assert lineage["active_lineage_record_count"] == 8
    assert lineage["active_lineage_preserved"] is True


def test_stage5dk_preservation_validators_reject_count_and_gate_drift(
    monkeypatch: object,
    tmp_path,
) -> None:
    ensure_stage5dk_built()

    stage5bd = load_yaml("data/token-block/stage5dk-stage5bd-plan-preservation.yaml")
    stage5bd["stage5bd_run_plan_id_count"] = 9
    stage5bd_path = write_temp_yaml(tmp_path / "stage5bd.yaml", stage5bd)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "stage5bd_plan_preservation", stage5bd_path)
    assert stage5dk.validate_stage5dk_stage5bd_preservation().validation_error_count > 0

    lineage = load_yaml("data/token-block/stage5dk-active-lineage-preservation.yaml")
    lineage["active_lineage_record_count"] = 7
    lineage_path = write_temp_yaml(tmp_path / "lineage.yaml", lineage)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "active_lineage_preservation", lineage_path)
    assert stage5dk.validate_stage5dk_active_lineage_preservation().validation_error_count > 0


def test_stage5dk_rejects_16_worker_reintroduction(monkeypatch: object, tmp_path) -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/project-state/stage5dk-summary.yaml")
    record["parallel_worker_cap"] = 16
    record["worker_cap_16_allowed"] = True
    path = write_temp_yaml(tmp_path / "summary.yaml", record)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "summary", path)

    result = stage5dk.validate_stage5dk_governance_scope()
    assert result.validation_error_count > 0
    assert any("parallel_worker_cap_must_be_8" in error for error in result.errors)
    assert any("worker_cap_16_allowed_must_be_false" in error for error in result.errors)
