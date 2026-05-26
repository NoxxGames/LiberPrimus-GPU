from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_dwh_context_blocks_hash_or_decode_work() -> None:
    payload = yaml.safe_load(
        (ROOT / "data/token-block/stage5aw-dwh-decision-context.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert payload["dwh_defined"] is True
    assert payload["dwh_expansion"] == "Deep Web Hash"
    assert payload["dwh_operational_status"] == "not_operational"
    assert payload["hash_search_performed"] is False
    assert payload["hash_preimage_claim"] is False
    assert payload["decode_claim"] is False
