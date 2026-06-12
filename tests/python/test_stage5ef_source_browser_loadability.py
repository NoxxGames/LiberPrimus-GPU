from __future__ import annotations

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_preserves_source_browser_loadability() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_source_browser_loadability()
    summary = load_yaml("data/project-state/stage5ef-source-browser-loadability-summary.yaml")

    assert result.validation_error_count == 0
    assert summary["source_browser_entries_loaded"] > 0
    assert summary["source_browser_validation_error_count"] == 0
    assert summary["source_browser_records_modified_now"] is False
