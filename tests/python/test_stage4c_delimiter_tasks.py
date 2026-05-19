from __future__ import annotations

import yaml
from pathlib import Path


def test_stage4c_delimiter_tasks_do_not_enable_reset_boundary() -> None:
    records = yaml.safe_load(
        Path("data/observations/visual/stage4c-delimiter-annotation-tasks.yaml").read_text(
            encoding="utf-8"
        )
    )["records"]

    assert len(records) == 2
    assert all(record["reset_boundary_hypothesis"] is False for record in records)
    assert all(record["annotation_status"] == "needs_human_coordinates" for record in records)
