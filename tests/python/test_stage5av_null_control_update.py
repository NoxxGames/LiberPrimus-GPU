from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_null_control_update_is_decision_aware_without_execution() -> None:
    payload = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5av-null-control-decision-update.yaml"
        ).read_text(encoding="utf-8")
    )
    assert payload["baseline_current_control_preserved"] is True
    assert payload["confirmed_token_control_count"] == 126
    assert payload["unresolved_variant_control_count"] == 77
    assert payload["execution_performed"] is False
