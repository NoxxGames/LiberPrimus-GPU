from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_implementation_gate_only_allows_future_synthetic_scope(
    tmp_path: Path,
) -> None:
    record = _records(_build_all(tmp_path)["gate"])[0]
    assert record["readiness_status"] == "ready_for_synthetic_cuda_kernel_implementation_contract_only"
    assert record["future_synthetic_kernel_implementation_ready"] is True
    assert record["current_stage_allows_kernel_implementation"] is False
    assert record["current_stage_allows_cuda_execution"] is False
    assert record["current_stage_allows_native_execution"] is False
    assert record["full_p56_status"] == "blocked_full_p56_token_buffer_missing"
    assert "no_p56_fixture_execution" in record["allowed_future_scope"]
