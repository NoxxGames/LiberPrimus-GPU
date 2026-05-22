from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_contract.prime_schedule import build_prime_schedule, stream_values


def test_stage5w_prime_schedule_generation_is_deterministic() -> None:
    assert stream_values(8) == stream_values(8)
    primes, values = stream_values(8)
    assert primes == [2, 3, 5, 7, 11, 13, 17, 19]
    assert values == [1, 2, 4, 6, 10, 12, 16, 18]


def test_stage5w_prime_schedule_records_are_bounded(tmp_path: Path) -> None:
    records = build_prime_schedule(prime_schedule_out=tmp_path / "schedule.yaml", out_dir=tmp_path)
    assert len(records) == 3
    assert all(record["prime_index_base"] == 0 for record in records)
    assert all(record["deterministic"] is True for record in records)
    assert all(record["cuda_execution_allowed"] is False for record in records)
    assert max(record["value_count"] for record in records) == 84

