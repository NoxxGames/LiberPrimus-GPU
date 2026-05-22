from __future__ import annotations

from libreprimus.consistency.runner import run_consistency_suite
from libreprimus.consistency.state_drift import check_state_drift_consistency


def test_stage5ab_state_drift_includes_doc_staleness_pass() -> None:
    results = check_state_drift_consistency()

    assert not [result for result in results if result.is_failure]
    assert any(result.check_name == "doc_staleness_dynamic_stage_check" for result in results)


def test_stage5ab_check_all_includes_state_drift_doc_staleness() -> None:
    suite = run_consistency_suite(["state_drift"])

    assert not suite.has_failures
    assert any(
        result.check_name == "doc_staleness_dynamic_stage_check"
        for result in suite.results
    )
