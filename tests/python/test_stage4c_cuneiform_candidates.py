from __future__ import annotations

import yaml
from pathlib import Path


def test_stage4c_cuneiform_candidate_is_review_only() -> None:
    records = yaml.safe_load(
        Path(
            "data/observations/visual/stage4c-cuneiform-reading-candidates.yaml",
        ).read_text(encoding="utf-8")
    )["records"]

    candidate = records[0]
    assert candidate["proposed_reading"] == [17, 13, 55, 1]
    assert candidate["annotation_status"] == "needs_human_coordinates"
    assert candidate["coordinate_system"] == "unknown_pending_annotation"
    assert candidate["usable_as_experiment_seed"] is False
    assert candidate["solve_claim"] is False
