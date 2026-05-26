from pathlib import Path

import yaml


def test_stage5ay_variant_families_are_not_executed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-bounded-variant-family-manifest.yaml").read_text(encoding="utf-8"))

    assert payload["family_count"] == 11
    assert payload["variant_byte_streams_generated"] is False
    assert payload["token_experiments_executed"] is False
    assert all(record["execution_enabled"] is False for record in payload["families"])
