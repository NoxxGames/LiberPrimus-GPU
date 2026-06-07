from __future__ import annotations

import yaml

from libreprimus.operator_console.source_browser import overrides


def test_manual_override_writer_is_nonexecuting(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(overrides, "MANUAL_OVERRIDES_DIR", tmp_path)

    path = overrides.save_override(
        target_entry_id="target-entry",
        target_source_record_path="data/example.yaml",
        fields={"title": "Adjusted title"},
    )
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert payload["record_type"] == "source_browser_manual_override"
    assert payload["target_entry_id"] == "target-entry"
    assert payload["solve_claim"] is False
    assert payload["execution_allowed"] is False
