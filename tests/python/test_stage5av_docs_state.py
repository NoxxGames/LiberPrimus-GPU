from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_next_stage_is_stage5aw() -> None:
    summary = yaml.safe_load((ROOT / "data/project-state/stage5av-summary.yaml").read_text(encoding="utf-8"))
    next_stage = yaml.safe_load(
        (ROOT / "data/project-state/stage5av-next-stage-decision.yaml").read_text(encoding="utf-8")
    )
    assert summary["next_stage"].startswith("Stage 5AW")
    assert next_stage["next_stage_id"] == "stage-5aw"
    assert next_stage["bounded_preflight_manifest_design_ready"] is True
