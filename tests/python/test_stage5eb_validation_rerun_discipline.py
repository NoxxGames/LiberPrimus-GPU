from __future__ import annotations

from test_stage5eb_common import ensure_stage5eb_built, load_yaml


def test_stage5eb_validation_rerun_discipline_records_failing_slice_policy() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-validation-rerun-discipline.yaml")

    assert record["focused_baseline_validators_before_editing"] is True
    assert record["stage_fast_after_code_change"] is True
    assert record["local_fast_before_commit"] is True
    assert record["full_parallel_once_before_commit"] is True
    assert record["inspect_failure_before_rerun"] is True
    assert record["rerun_only_failing_slice_before_full_parallel"] is True
    assert record["after_push_wait_for_ci"] is True
