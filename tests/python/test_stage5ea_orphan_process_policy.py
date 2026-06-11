from __future__ import annotations

from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_orphan_process_timeout_policy_keeps_finite_timeout() -> None:
    ensure_stage5ea_built()

    record = load_yaml("data/project-state/stage5ea-orphan-process-timeout-policy.yaml")

    assert record["timeout_seconds"] == 3600
    assert record["timeout_cleanup_policy_recorded"] is True
    assert record["validation_subprocesses_must_not_run_indefinitely"] is True
