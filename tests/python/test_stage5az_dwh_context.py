from pathlib import Path

import yaml


def test_stage5az_dwh_context_blocks_hash_search() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5az-dwh-manifest-integrity-context.yaml").read_text(encoding="utf-8")
    )

    assert payload["dwh_expansion"] == "Deep Web Hash"
    assert payload["dwh_operational_status"] == "not_operational"
    assert payload["hash_search_allowed_now"] is False
    assert payload["hash_search_performed"] is False
    assert payload["decode_claim"] is False
