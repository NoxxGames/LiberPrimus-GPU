from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_full_p56_blocker_is_preserved(tmp_path: Path) -> None:
    record = _records(_build_all(tmp_path)["blocker"])[0]
    assert record["blocker_status"] == "enforced"
    assert record["full_p56_status"] == "blocked_full_p56_token_buffer_missing"
    assert record["full_token_buffer_committed"] is False
    assert record["full_p56_cuda_allowed"] is False
    assert record["cuda_execution_allowed"] is False
    assert "committed_full_p56_cipher_token_buffer" in record["required_before_unblock"]
