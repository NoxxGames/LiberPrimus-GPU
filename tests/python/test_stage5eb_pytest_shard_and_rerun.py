from __future__ import annotations

from libreprimus.parallel_validation.pytest_runner import DEFAULT_WORKERS, shard_plan_record
from test_stage5eb_common import ROOT, ensure_stage5eb_built, load_yaml


def test_stage5eb_pytest_shard_records_duration_and_rerun_metadata() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-pytest-shard-duration-policy.yaml")
    plan = shard_plan_record(ROOT / "tests/python", worker_count=2)

    assert record["pytest_sharding_duration_aware"] is True
    assert record["pytest_shard_plan_records_estimated_weight"] is True
    assert record["pytest_shard_plan_records_rerun_commands"] is True
    assert DEFAULT_WORKERS == 10
    assert plan["duration_aware_balancing"] is True
    assert all("estimated_weight" in shard for shard in plan["shards"])
    assert all("rerun_command" in shard for shard in plan["shards"])


def test_stage5eb_failing_shard_rerun_helpers_are_documented() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-failing-shard-rerun-policy.yaml")

    assert record["failing_shard_rerun_helper_available"] is True
    assert record["do_not_rerun_full_parallel_until_failing_slice_passes"] is True
    assert (ROOT / "scripts/ci/run-pytest-shard.ps1").exists()
    assert (ROOT / "scripts/ci/run-pytest-shard.sh").exists()
    assert (ROOT / "scripts/ci/run-failing-pytest-slice.ps1").exists()
    assert (ROOT / "scripts/ci/run-failing-pytest-slice.sh").exists()
