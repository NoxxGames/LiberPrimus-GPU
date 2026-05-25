from __future__ import annotations

from pathlib import Path

import yaml


def _yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_stage5ar_page_split_records_community_10_13_9() -> None:
    policy = _yaml("data/token-block/stage5ar-page-split-policy.yaml")
    records = _yaml("data/token-block/stage5ar-page-split-records.yaml")
    assert policy["candidate_page_split_id"] == "community_10_13_9"
    assert records["page_49_row_count"] == 10
    assert records["page_50_row_count"] == 13
    assert records["page_51_row_count"] == 9
    assert records["row_count_sum"] == 32
