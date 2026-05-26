from pathlib import Path

import yaml


def test_stage5ay_alphabet_controls_defined_not_executed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-alphabet-control-manifest.yaml").read_text(encoding="utf-8"))

    assert payload["controls_executed"] is False
    assert {record["family_id"] for record in payload["families"]} >= {"primary60_current_alphabet", "seeded_permutation_3301_control"}
