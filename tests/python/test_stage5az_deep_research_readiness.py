from pathlib import Path

import yaml


def test_stage5az_readiness_points_to_repaired_records() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5az-deep-research-readiness.yaml").read_text(encoding="utf-8")
    )

    assert payload["deep_research_readiness"] is True
    assert payload["execution_enabled"] is False
    assert "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml" in payload[
        "records_deep_research_should_inspect"
    ]
    assert "data/token-block/stage5ay-bounded-variant-family-manifest.yaml" in payload[
        "records_deep_research_should_not_treat_as_active"
    ]
