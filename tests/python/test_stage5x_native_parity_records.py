from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_parity.native_execution import build_native_run_records
from libreprimus.prime_minus_one_native_parity.parity_records import build_parity_records


def test_stage5x_parity_records_match_stage5w_expected_hashes(tmp_path: Path) -> None:
    run = tmp_path / "run.yaml"
    parity = tmp_path / "parity.yaml"
    build_native_run_records(native_run_out=run, out_dir=tmp_path)
    records = build_parity_records(native_run=run, native_parity_out=parity, out_dir=tmp_path)
    passed = [record for record in records if record["parity_status"] == "passed"]
    blocked = [record for record in records if record["parity_status"] == "blocked_not_executed"]
    assert len(passed) == 2
    assert len(blocked) == 1
    assert all(record["computed_output_token_hash"] == record["expected_output_token_hash"] for record in passed)
    assert blocked[0]["mapping_id"] == "stage5w-mapping-p56-full-fixture-blocked-v0"
