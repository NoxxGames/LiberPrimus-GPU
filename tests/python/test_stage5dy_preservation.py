from __future__ import annotations

from test_stage5dy_common import ensure_stage5dy_built, load_yaml


def test_stage5dx_stage5bd_and_active_lineage_preserved() -> None:
    ensure_stage5dy_built()
    stage5dx = load_yaml("data/project-state/stage5dy-stage5dx-preservation.yaml")
    stage5bd = load_yaml("data/token-block/stage5dy-stage5bd-preservation.yaml")
    active_lineage = load_yaml("data/token-block/stage5dy-active-lineage-preservation.yaml")

    assert stage5dx["stage5dx_reviewed_entry_count"] == 20
    assert stage5dx["stage5dx_overlay_count"] == 23
    assert stage5bd["stage5bd_run_plan_id_count"] == 10
    assert active_lineage["active_lineage_record_count"] == 8
