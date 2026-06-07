from __future__ import annotations

from libreprimus.operator_console.source_browser.column_profiles import load_column_profile, visible_columns


def test_default_column_profile_loads_expected_columns() -> None:
    profile = load_column_profile()
    columns = visible_columns()
    keys = {column["key"] for column in columns}

    assert profile["record_type"] == "source_browser_column_profile"
    assert "title" in keys
    assert "title" in keys
    assert "category" in keys
