"""Summary helpers for consistency checks."""

from __future__ import annotations

from libreprimus.consistency.models import ConsistencyCheckSuiteResult


def concise_summary(suite: ConsistencyCheckSuiteResult) -> dict[str, int | str]:
    return {
        "suite_id": suite.suite_id,
        "check_count": suite.check_count,
        "pass_count": suite.pass_count,
        "fail_count": suite.fail_count,
        "warning_count": suite.warning_count,
        "skipped_count": suite.skipped_count,
    }
