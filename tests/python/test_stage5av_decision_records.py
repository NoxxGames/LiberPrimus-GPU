from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_decision_records_preserve_unresolved_selected_null() -> None:
    decisions = yaml.safe_load(
        (ROOT / "data/token-block/stage5av-human-review-decision-records.yaml").read_text(
            encoding="utf-8"
        )
    )
    unresolved = [record for record in decisions["records"] if record["decision"] == "unresolved"]
    assert decisions["decision_record_count"] == 203
    assert len(unresolved) == 77
    assert all(record["selected_token"] is None for record in unresolved)
    assert all(record["canonical_transcription_changed"] is False for record in decisions["records"])
