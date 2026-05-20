from __future__ import annotations

from pathlib import Path

import yaml
from libreprimus.cuda_parity_reporting.solved_fixture_preflight import build_solved_fixture_preflight


def test_stage5g_solved_fixture_preflight_blocks_production_gematria_cuda() -> None:
    payload = yaml.safe_load(Path("data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml").read_text(encoding="utf-8"))
    record = payload["records"][0]
    assert record["production_gematria_mod29_cuda_ready"] is False
    assert record["solved_fixture_cuda_execution_allowed"] is False
    assert record["preflight_blocker_count"] >= 5


def test_stage5g_solved_fixture_preflight_builder_can_write_temp_record(tmp_path: Path) -> None:
    record = build_solved_fixture_preflight(preflight_out=tmp_path / "preflight.yaml", out_dir=tmp_path / "out")[0]
    assert record["current_stage5f_kernel_scope"] == "synthetic_uppercase_latin_only"
    assert "Gematria mod-29 native reference fixture contract" in " ".join(record["preflight_blockers"])
