from pathlib import Path

import yaml


def test_stage5at_dwh_case_context_blocks_hash_and_decode() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5at-dwh-case-context.yaml").read_text())
    assert payload["dwh_defined"] is True
    assert payload["dwh_expansion"] == "Deep Web Hash"
    assert payload["hash_search_performed"] is False
    assert payload["hash_preimage_claim"] is False
    assert payload["decode_claim"] is False
