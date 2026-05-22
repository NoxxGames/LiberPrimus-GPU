from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_contract.native_parity_preparation import build_native_parity_preparation


def test_stage5w_native_parity_preparation_does_not_claim_execution(tmp_path: Path) -> None:
    records = build_native_parity_preparation(native_parity_preparation_out=tmp_path / "prep.yaml", out_dir=tmp_path)
    assert len(records) == 3
    assert all(record["native_execution_performed"] is False for record in records)
    assert all(record["python_reference_execution_performed"] is False for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
    blocked = next(record for record in records if record["preparation_status"] == "blocked_missing_full_p56_token_values")
    assert blocked["expected_output_token_hash"] is None
    ready = next(record for record in records if record["preparation_status"] == "p56_stage4o_bounded_reference_hash_linked")
    assert ready["expected_output_token_hash"]

