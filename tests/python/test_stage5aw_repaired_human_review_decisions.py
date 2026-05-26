from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_repaired_decisions_do_not_reinterpret_user_decisions() -> None:
    payload = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5aw-repaired-human-review-decision-records.yaml"
        ).read_text(encoding="utf-8")
    )
    assert payload["decision_record_count"] == 203
    assert payload["user_decisions_reinterpreted"] is False
    records = {record["challenge_id"]: record for record in payload["records"]}
    assert records["stage5at-token-case-013"]["possible_tokens"] == ["04", "O4", "?4"]
    assert records["stage5at-token-case-025"]["possible_tokens"] == ["3I", "3l", "3?"]
