from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_archive_source_lock_is_deferred_not_processed() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ae-archive-source-lock-deferral.yaml").read_text())["records"]
    assert any(record["future_option_id"] == "stage5af_archive_visual_numeric_source_lock" for record in records)
    assert any(record["archive_source_lock_ready_next"] is True for record in records)
    assert all(record["raw_archive_processed"] is False for record in records)
    assert all(record["source_lock_execution_performed"] is False for record in records)
