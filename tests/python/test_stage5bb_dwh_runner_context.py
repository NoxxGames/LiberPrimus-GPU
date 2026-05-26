from pathlib import Path

import yaml


def test_stage5bb_dwh_runner_context_blocks_hash_search() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-dwh-runner-context.yaml").read_text())

    assert payload["dwh_defined"] is True
    assert payload["dwh_expansion"] == "Deep Web Hash"
    assert payload["dwh_operational_status"] == "not_operational"
    assert payload["hash_search_performed"] is False
    assert payload["dwh_hash_search_supported_by_stage5bb"] is False
