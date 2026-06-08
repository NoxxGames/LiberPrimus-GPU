from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, load_yaml


def test_stage5ds_preserves_prior_stage_boundaries() -> None:
    ensure_stage5ds_built()
    stage5dr = load_yaml("data/project-state/stage5ds-stage5dr-preservation.yaml")
    stage5dg = load_yaml("data/token-block/stage5ds-stage5dg-preservation.yaml")
    stage5bd = load_yaml("data/token-block/stage5ds-stage5bd-preservation.yaml")
    lineage = load_yaml("data/token-block/stage5ds-active-lineage-preservation.yaml")
    assert stage5dr["stage5dr_complete"] is True
    assert stage5dg["stage5dg_operator_approval_record_preserved"] is True
    assert stage5dg["combined_approval_gate_satisfied_now"] is False
    assert stage5bd["stage5bd_run_plan_id_count"] == 10
    assert lineage["active_lineage_record_count"] == 8
