from pathlib import Path


def test_stage5bj_source_of_truth_names_latest_and_next_stage() -> None:
    text = Path("data/project-state/stage5ah-doc-staleness-source-of-truth.yaml").read_text()

    assert "latest_completed_stage_prefix: Stage 5BJ" in text
    assert "expected_next_stage_prefix: Stage 5BK" in text
