from pathlib import Path

import yaml


def test_stage5bb_result_schema_fixture_policy_is_synthetic_only() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-result-schema-fixture-policy.yaml").read_text())

    assert payload["fixture_result_schema_writer_allowed"] is True
    assert payload["fixture_data_not_derived_from_liber_primus"] is True
    assert payload["real_token_block_data_allowed"] is False
    assert payload["real_variant_byte_streams_allowed"] is False
    assert payload["allowed_fixture"]["fixture_values"] == [0, 1, 2, 255]
