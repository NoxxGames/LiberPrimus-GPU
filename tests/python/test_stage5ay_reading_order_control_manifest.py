from pathlib import Path

import yaml


def test_stage5ay_reading_order_controls_defined_not_executed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-reading-order-control-manifest.yaml").read_text(encoding="utf-8"))

    assert payload["controls_executed"] is False
    assert {record["family_id"] for record in payload["families"]} >= {"global_32_row_order", "token_shuffle_fixed_seed"}
