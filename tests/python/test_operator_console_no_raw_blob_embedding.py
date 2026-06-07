from __future__ import annotations

from libreprimus.operator_console.source_browser.manual_entries import build_manual_entry, validate_no_huge_raw_blob


def test_manual_entry_builder_does_not_allow_solve_or_execution_flags() -> None:
    payload = build_manual_entry(
        {
            "entry_id": "unsafe",
            "title": "Unsafe",
            "solve_claim": True,
            "execution_allowed": True,
        }
    )

    assert payload["solve_claim"] is False
    assert payload["execution_allowed"] is False


def test_manual_entry_raw_blob_limit_applies_to_nested_values() -> None:
    errors = validate_no_huge_raw_blob({"nested": {"body": "\n".join(str(i) for i in range(1100))}})

    assert errors
