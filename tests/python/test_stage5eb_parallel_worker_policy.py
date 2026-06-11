from __future__ import annotations

from test_stage5eb_common import ROOT, ensure_stage5eb_built, load_yaml


def test_stage5eb_parallel_worker_policy_sets_10_worker_local_cap() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-parallel-worker-policy.yaml")

    assert record["local_parallel_default_workers"] == 10
    assert record["local_parallel_default_pytest_workers"] == 10
    assert record["maximum_supported_workers"] == 10
    assert record["maximum_supported_pytest_workers"] == 10
    assert record["old_8_worker_cap_removed"] is True
    assert record["old_16_worker_default_reintroduced"] is False


def test_stage5eb_validation_wrappers_default_to_10_workers() -> None:
    ensure_stage5eb_built()

    ps1 = (ROOT / "scripts/ci/run-stage-validation.ps1").read_text(encoding="utf-8")

    assert 'Stage = "stage5eb"' in ps1
    assert "else { 10 }" in ps1
    assert "caps local workers at $MaxWorkers" in ps1
