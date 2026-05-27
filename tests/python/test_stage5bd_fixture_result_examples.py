from pathlib import Path

import yaml


def test_stage5bd_fixture_result_examples_are_synthetic() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-fixture-result-example-policy.yaml").read_text())

    assert payload["fixture_result_examples_allowed"] is True
    assert payload["real_token_block_data_used"] is False
    assert payload["fixture_data_not_derived_from_liber_primus"] is True
