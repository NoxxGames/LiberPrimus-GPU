from __future__ import annotations

from libreprimus.consistency.models import (
    ConsistencyCheckSuiteResult,
    fail_result,
    pass_result,
    warning_result,
)


def test_pass_result_serializes() -> None:
    result = pass_result("group", "check", "ok")
    payload = result.to_dict()

    assert payload["status"] == "pass"
    assert payload["severity"] == "info"


def test_fail_result_serializes() -> None:
    result = fail_result("group", "check", "bad")
    payload = result.to_dict()

    assert payload["status"] == "fail"
    assert payload["severity"] == "error"
    assert result.is_failure


def test_suite_counts_statuses() -> None:
    suite = ConsistencyCheckSuiteResult(
        "suite",
        [
            pass_result("group", "pass", "ok"),
            fail_result("group", "fail", "bad"),
            warning_result("group", "warning", "warn"),
        ],
    )

    assert suite.pass_count == 1
    assert suite.fail_count == 1
    assert suite.warning_count == 1
    assert suite.skipped_count == 0
    assert suite.has_failures
    assert suite.has_warnings
