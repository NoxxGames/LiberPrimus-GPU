from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.scored_experiment_readiness import build_scored_experiment_readiness


def test_stage5y_scored_experiment_readiness_blocks_unsolved_and_benchmarks(tmp_path: Path) -> None:
    records = build_scored_experiment_readiness(scored_experiment_readiness_out=tmp_path / "scored.yaml", out_dir=tmp_path)
    by_class = {record["experiment_class"]: record for record in records}
    assert by_class["bounded_cpu_native_prime_minus_one_scored_experiment"]["readiness_status"].startswith("ready")
    assert by_class["bounded_unsolved_page_micro_pilot"]["readiness_status"].startswith("blocked")
    assert all(record["benchmark_allowed"] is False for record in records)
    assert all(record["generated_body_publication_allowed"] is False for record in records)
    assert all(record["unsolved_scope_allowed"] is False for record in records)
