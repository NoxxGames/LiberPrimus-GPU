from __future__ import annotations

from pathlib import Path

from libreprimus.parallel_validation.pytest_runner import SERIAL_ISOLATED_TEST_FILES

from test_stage5dy_common import ensure_stage5dy_built, load_yaml


def test_parallel_policy_caps_workers_and_records_race_handling() -> None:
    ensure_stage5dy_built()
    policy = load_yaml("data/project-state/stage5dy-parallel-validation-policy.yaml")
    audit = load_yaml("data/project-state/stage5dy-pytest-shard-race-audit.yaml")

    assert policy["parallel_worker_cap"] == 8
    assert policy["default_workers"] == 8
    assert policy["default_pytest_workers"] == 8
    assert policy["old_16_worker_default_reintroduced"] is False
    assert audit["stage5cu_jsondecodeerror_observed_parallel_only"] is True
    assert audit["affected_group_isolated_or_serialized"] is True
    assert audit["treated_as_race_avoidance_not_hidden_pass"] is True


def test_parallel_scripts_default_to_current_ten_worker_policy_and_ignored_state() -> None:
    ps1 = Path("scripts/ci/run-parallel-validation.ps1").read_text(encoding="utf-8")
    sh = Path("scripts/ci/run-parallel-validation.sh").read_text(encoding="utf-8")

    assert "else { 10 }" in ps1
    assert "LIBERPRIMUS_VALIDATION_WORKERS:-10" in sh
    assert "_stage5ax_state" in ps1
    assert "_stage5ax_state" in sh
    assert "--out-safety-audit" in ps1
    assert "--out-safety-audit" in sh


def test_stage5cu_cli_test_is_serial_isolated_from_parallel_shards() -> None:
    assert Path("tests/python/test_stage5cu_cli.py") in SERIAL_ISOLATED_TEST_FILES
