from pathlib import Path

import yaml


def test_stage5bb_fixture_result_schema_records_use_no_real_outputs() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-fixture-result-schema-records.yaml").read_text())
    record = payload["fixture_records"][0]

    assert payload["fixture_record_count"] == 1
    assert record["fixture_source"] == "synthetic_fixture_only"
    assert record["not_derived_from_liber_primus"] is True
    assert record["variant_output_generated"] is False
    assert record["score_generated"] is False
