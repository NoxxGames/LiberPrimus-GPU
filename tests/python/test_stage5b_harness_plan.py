from __future__ import annotations

from libreprimus.cuda_parity.harness_plan import build_harness_plan


def test_stage5b_harness_plan_status_counts(tmp_path) -> None:
    harness, fixtures = build_harness_plan(
        out_dir=tmp_path,
        harness_plan_out=tmp_path / "harness.yaml",
        parity_fixtures_out=tmp_path / "fixtures.yaml",
    )
    assert len(harness) == len(fixtures) == 14
    assert sum(1 for record in harness if record["harness_status"] == "ready_for_future_kernel") == 9
    assert sum(1 for record in harness if record["harness_status"] == "blocked") == 2
    assert sum(1 for record in harness if record["harness_status"] == "skipped_non_target") == 3


def test_stage5b_harness_plan_never_requires_local_16gb(tmp_path) -> None:
    harness, _ = build_harness_plan(
        out_dir=tmp_path,
        harness_plan_out=tmp_path / "harness.yaml",
        parity_fixtures_out=tmp_path / "fixtures.yaml",
    )
    assert all(record["local_16gb_profile_required"] is False for record in harness)
    assert all(record["gpu_benchmark_performed"] is False for record in harness)
    assert all(record["speedup_claim"] is False for record in harness)
