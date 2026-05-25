from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ar_dwh_context_defines_deep_web_hash_and_blocks_search() -> None:
    record = yaml.safe_load(Path("data/token-block/stage5ar-dwh-coordinate-context.yaml").read_text(encoding="utf-8"))
    assert record["dwh_defined"] is True
    assert record["dwh_expansion"] == "Deep Web Hash"
    assert record["hash_search_performed"] is False
    assert record["hash_preimage_claim"] is False
    assert record["decode_claim"] is False
