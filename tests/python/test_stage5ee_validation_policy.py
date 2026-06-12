from __future__ import annotations

from test_stage5ee_common import ensure_stage5ee_built, load_yaml


def test_stage5ee_records_full_parallel_as_normal_final_profile() -> None:
    ensure_stage5ee_built()
    evidence = load_yaml("data/project-state/stage5ee-reviewable-validation-evidence.yaml")
    summary = load_yaml("data/project-state/stage5ee-summary.yaml")

    assert evidence["parallel_worker_cap"] == 10
    assert evidence["full_parallel_is_normal_final_local_profile"] is True
    assert evidence["full_serial_pytest_required_for_normal_stage_completion"] is False
    assert summary["full_serial_pytest_default_for_future_stages"] is False
    assert summary["full_serial_pytest_allowed_only_when_explicitly_requested"] is True
