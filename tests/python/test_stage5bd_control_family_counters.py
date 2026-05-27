from pathlib import Path

import yaml


def test_stage5bd_control_family_counts_match_expected_surface() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-control-family-plan-counters.yaml").read_text())

    assert payload["alphabet_control_family_count"] == 6
    assert payload["reading_order_control_family_count"] == 8
    assert payload["page_split_control_family_count"] == 4
    assert payload["source_control_family_count"] == 3
    assert payload["dry_run_plan_family_count"] == 11520
