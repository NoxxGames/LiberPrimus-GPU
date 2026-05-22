from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.stream_schedule_contract import build_stream_schedule_contract


def test_stage5u_stream_schedule_blocks_arbitrary_streams(tmp_path: Path) -> None:
    records = build_stream_schedule_contract(stream_schedule_contract_out=tmp_path / "streams.yaml", out_dir=tmp_path / "reports")
    by_id = {record["stream_schedule_contract_id"]: record for record in records}
    prime = by_id["stage5u-prime-minus-one-stream-schedule-v0"]
    blocked = by_id["stage5u-arbitrary-stream-blocking-policy-v0"]
    assert prime["supports_prime_minus_one"] is True
    assert prime["stream_value_formula"] == "(prime_i - 1) mod 29"
    assert blocked["contract_status"] == "blocked_out_of_scope"
    assert blocked["supports_arbitrary_integer_streams"] is False
