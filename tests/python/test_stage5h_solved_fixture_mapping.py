from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5h_solved_fixture_mapping_remains_blocked() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5h-gematria-solved-fixture-safe-mapping.yaml").read_text(encoding="utf-8"))["records"]
    assert records
    for record in records:
        assert record["readiness_state"] == "blocked"
        assert record["solved_fixture_cuda_execution_allowed"] is False
        assert record["unsolved_page_cuda_used"] is False
        assert record["preflight_blocker_count"] >= 7
