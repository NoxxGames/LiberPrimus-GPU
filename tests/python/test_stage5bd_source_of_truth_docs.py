from pathlib import Path

import yaml


def test_stage5bs_source_of_truth_names_latest_and_next_stage() -> None:
    text = Path("data/project-state/stage5ah-doc-staleness-source-of-truth.yaml").read_text()
    current = yaml.safe_load(Path("data/project-state/current-stage-state.yaml").read_text(encoding="utf-8"))

    latest_prefix = current["latest_completed_stage_title"].split(" - ", 1)[0]
    next_prefix = current["recommended_next_stage_title"].split(" - ", 1)[0]
    assert f"latest_completed_stage_prefix: {latest_prefix}" in text
    assert f"expected_next_stage_prefix: {next_prefix}" in text
