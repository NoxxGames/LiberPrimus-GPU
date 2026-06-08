from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, load_yaml


def test_stage5ds_source_browser_loadability_record() -> None:
    ensure_stage5ds_built()
    record = load_yaml("data/project-state/stage5ds-source-browser-loadability-summary.yaml")
    assert record["source_browser_loadability_validated"] is True
    assert record["source_browser_index_valid"] is True
    assert record["stage5ds_entries_loaded"] >= 62
    assert "Music" in record["stage5ds_categories"]
