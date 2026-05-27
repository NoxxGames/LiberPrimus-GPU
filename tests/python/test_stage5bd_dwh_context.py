from pathlib import Path

import yaml


def test_stage5bd_dwh_context_remains_non_operational() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-dwh-dry-run-context.yaml").read_text())

    assert payload["dwh_operational_status"] == "not_operational"
    assert payload["hash_search_performed"] is False
    assert payload["hash_preimage_claim"] is False
