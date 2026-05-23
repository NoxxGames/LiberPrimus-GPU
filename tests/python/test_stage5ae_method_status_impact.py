from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_method_status_is_not_upgraded() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-method-status-impact.yaml").read_text())["records"][0]
    assert record["method_status_impact_status"] == "no_method_status_upgrade"
    assert record["method_status_upgrade_allowed"] is False
    assert record["method_status_upgraded"] is False
    assert record["solve_claim"] is False
