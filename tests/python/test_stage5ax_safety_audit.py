from __future__ import annotations

from libreprimus.parallel_validation.plan import build_plan_records


def test_safety_audit_proves_mutating_commands_are_not_parallelised() -> None:
    safety = build_plan_records(max_workers=16)["safety"]
    assert safety["git_mutating_commands_parallelised"] is False
    assert safety["github_issue_commands_parallelised"] is False
    assert safety["commit_push_commands_parallelised"] is False
    assert safety["network_commands_parallelised"] is False
    assert safety["raw_data_paths_written"] is False
    assert safety["experiments_results_outputs_ignored"] is True
