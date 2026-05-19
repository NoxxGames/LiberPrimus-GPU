from __future__ import annotations

import yaml
from pathlib import Path


def test_stage4c_dot_task_records_ambiguity() -> None:
    records = yaml.safe_load(
        Path("data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml").read_text(
            encoding="utf-8"
        )
    )["records"]

    dot = records[0]
    assert {"13", "31"} <= set(dot["claimed_readings"])
    assert "13/31 remains ambiguous" in dot["notes"]
    assert dot["review_status"] != "verified"
    assert dot["usable_as_experiment_seed"] is False
