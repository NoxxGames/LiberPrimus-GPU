from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ar_null_control_update_adds_coordinate_controls() -> None:
    record = yaml.safe_load(Path("data/token-block/stage5ar-token-block-null-control-update.yaml").read_text(encoding="utf-8"))
    assert record["coordinate_specific_controls_created"] is True
    assert "I/l swap control" in record["case_confusion_controls"]
    assert "accepted 10/13/9 split" in record["page_split_controls"]
    assert "global 32-row reading order" in record["coordinate_controls"]
    assert record["execution_enabled"] is False
