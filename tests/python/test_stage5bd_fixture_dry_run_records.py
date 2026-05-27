from pathlib import Path

import yaml


def test_stage5bd_fixture_dry_run_records_use_no_real_token_block_data() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-fixture-dry-run-records.yaml").read_text())

    assert payload["fixture_record_count"] == 1
    assert payload["fixture_records"][0]["real_token_block_data_used"] is False
    assert payload["fixture_records"][0]["fixture_source"] == "synthetic_fixture_only"
