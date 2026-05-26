from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_dwh_context_is_context_only() -> None:
    payload = yaml.safe_load(
        (ROOT / "data/token-block/stage5av-dwh-decision-context.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert payload["dwh_defined"] is True
    assert payload["dwh_expansion"] == "Deep Web Hash"
    assert payload["hash_search_performed"] is False
    assert payload["dwh_decode_attempt_performed"] is False
