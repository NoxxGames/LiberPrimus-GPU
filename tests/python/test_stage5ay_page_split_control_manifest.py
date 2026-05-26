from pathlib import Path

import yaml


def test_stage5ay_page_split_controls_defined_without_finalising_boundaries() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-page-split-control-manifest.yaml").read_text(encoding="utf-8"))

    assert payload["controls_executed"] is False
    assert payload["page_boundaries_final"] is False
    assert {record["family_id"] for record in payload["families"]} >= {"accepted_10_13_9_split", "no_page_boundary_control"}
