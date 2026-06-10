from __future__ import annotations

from libreprimus.token_block.stage5dz import TOKEN_PATHS
from test_stage5dz_common import ensure_stage5dz_built, load_yaml


def test_stage5dz_prior_stage_preservation_records() -> None:
    ensure_stage5dz_built()

    assert load_yaml(TOKEN_PATHS["stage5dy_preservation"])["stage5dy_preserved"] is True
    assert load_yaml(TOKEN_PATHS["stage5dx_preservation"])["stage5dx_overlay_count"] == 23
    assert load_yaml(TOKEN_PATHS["stage5dw_preservation"])["stage5dw_overlay_count"] == 37
    assert load_yaml(TOKEN_PATHS["stage5dv_preservation"])["source_browser_path_canonicalization_preserved"] is True
    assert load_yaml(TOKEN_PATHS["stage5du_preservation"])["stage5du_thread_image_paths_under_third_party"] is True
    assert load_yaml(TOKEN_PATHS["stage5dg_preservation"])["combined_approval_gate_satisfied_now"] is False
    assert load_yaml(TOKEN_PATHS["stage5bd_preservation"])["stage5bd_run_plan_id_count"] == 10
    assert load_yaml(TOKEN_PATHS["active_lineage_preservation"])["active_lineage_record_count"] == 8
