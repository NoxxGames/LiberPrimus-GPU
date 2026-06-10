from __future__ import annotations

from libreprimus.token_block.stage5dz import PROJECT_STATE_PATHS
from test_stage5dz_common import ensure_stage5dz_built, run_token_block_cli, load_yaml


def test_stage5dz_source_browser_loadability_validates() -> None:
    ensure_stage5dz_built()

    output = run_token_block_cli("validate-stage5dz-source-browser-loadability")
    summary = load_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])

    assert "token_block_stage5dz_source_browser_loadability_valid=true" in output
    assert summary["source_browser_loadability_validated"] is True
    assert summary["source_browser_validation_error_count"] == 0
    assert summary["stage5dz_overlay_count"] == 12
    assert summary["overlay_only_fact_cards_supported"] is True
