from __future__ import annotations

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import source_browser_summary, validate_source_index


def test_source_index_loads_committed_metadata() -> None:
    index = build_source_index()

    assert len(index.scanned_paths) >= 1200
    assert len(index.entries) >= len(index.scanned_paths)
    assert any(entry.entry_id == "chatgpt-context-file" for entry in index.entries)
    assert not index.parse_errors


def test_source_index_validation_and_summary_are_consistent() -> None:
    result = validate_source_index()
    summary = source_browser_summary()

    assert result.ok
    assert result.counts["entries_loaded"] == summary["entries_loaded"]
    assert summary["entries_loaded"] >= 1200
    assert summary["chatgpt_context"]["exists"] is True
