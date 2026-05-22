from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_scored_experiments_are_deferred_or_blocked(tmp_path: Path) -> None:
    records = _records(_build_all(tmp_path)["scored"])
    by_class = {record["experiment_class"]: record for record in records}
    assert by_class["bounded_cpu_native_prime_minus_one_scored_experiment"]["readiness_status"] == (
        "deferred_manifest_gate_required"
    )
    assert by_class["bounded_unsolved_page_micro_pilot"]["readiness_status"] == (
        "blocked_unsolved_page_cuda_disallowed"
    )
    assert by_class["benchmark_scored_experiment"]["readiness_status"] == (
        "blocked_benchmark_disallowed"
    )
    assert all(record["execution_enabled"] is False for record in records)
    assert all(record["cuda_execution_allowed"] is False for record in records)
    assert all(record["score_interpretation"] == "triage_only" for record in records)
