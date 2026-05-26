from pathlib import Path

import yaml


def test_stage5ay_dwh_context_blocks_hash_search_and_decode() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-dwh-preflight-context.yaml").read_text(encoding="utf-8"))

    assert payload["dwh_defined"] is True
    assert payload["dwh_expansion"] == "Deep Web Hash"
    assert payload["dwh_operational_status"] == "not_operational"
    assert payload["hash_preimage_search_performed"] is False
    assert payload["decode_attempt_performed"] is False
