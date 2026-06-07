from __future__ import annotations

import yaml

from libreprimus.operator_console.source_browser import tombstones


def test_tombstone_writer_is_nonexecuting(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(tombstones, "TOMBSTONES_DIR", tmp_path)

    path = tombstones.save_tombstone(
        target_entry_id="target-entry",
        target_source_record_path="data/example.yaml",
        reason="duplicate_review_row",
    )
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert payload["record_type"] == "source_browser_tombstone"
    assert payload["reason"] == "duplicate_review_row"
    assert payload["solve_claim"] is False
    assert payload["execution_allowed"] is False
