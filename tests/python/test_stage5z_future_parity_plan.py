from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_future_parity_plan_selects_synthetic_first_and_blocks_wider_scope(
    tmp_path: Path,
) -> None:
    records = _records(_build_all(tmp_path)["future"])
    by_id = {record["future_parity_plan_record_id"]: record for record in records}
    assert by_id["stage5z-future-parity-synthetic-kernel-v0"]["readiness_status"] == (
        "ready_for_contract_scoped_future_stage"
    )
    assert by_id["stage5z-future-parity-full-p56-v0"]["readiness_status"] == (
        "blocked_full_p56_token_buffer_missing"
    )
    assert by_id["stage5z-future-parity-scored-experiment-v0"]["readiness_status"] == (
        "blocked_manifest_gate_required"
    )
    assert all(record["execution_enabled"] is False for record in records)
    assert all(record["cuda_execution_allowed"] is False for record in records)
    assert all(record["benchmark_allowed"] is False for record in records)
