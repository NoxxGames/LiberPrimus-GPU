from __future__ import annotations

from libreprimus.operator_console.source_browser.manual_entries import build_manual_entry, validate_no_huge_raw_blob


def test_manual_entry_defaults_are_nonexecuting() -> None:
    entry = build_manual_entry({"entry_id": "example", "title": "Example", "summary": "Review note"})

    assert entry["record_type"] == "source_browser_manual_entry"
    assert entry["solve_claim"] is False
    assert entry["execution_allowed"] is False
    assert entry["entry_type"] == "manual_note"


def test_manual_entry_rejects_huge_raw_blob() -> None:
    errors = validate_no_huge_raw_blob({"notes": "x" * 20001})

    assert errors
    assert "exceeds" in errors[0]
