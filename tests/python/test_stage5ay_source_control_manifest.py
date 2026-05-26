from pathlib import Path

import yaml


def test_stage5ay_source_controls_defined_not_executed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-source-control-manifest.yaml").read_text(encoding="utf-8"))

    assert payload["controls_executed"] is False
    assert payload["future_source_lock_required_for_wrong_page_block_control"] is True
    assert {record["family_id"] for record in payload["families"]} >= {"random_lp_like_token_stream_from_uniform_primary60"}
