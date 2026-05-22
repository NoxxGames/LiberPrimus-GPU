from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.fixtures import build_conformance_fixtures


def test_stage5v_conformance_fixtures_are_raw_data_free_and_abi_backed(tmp_path: Path) -> None:
    records = build_conformance_fixtures(conformance_fixtures_out=tmp_path / "fixtures.yaml", out_dir=tmp_path / "out")
    assert len(records) == 7
    assert all(record["candidate_batch_abi_id"] == "candidate_batch_abi_v0" for record in records)
    assert all(record["raw_data_free"] is True for record in records)
    assert all(record["no_gpu_safe"] is True for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
    assert sum(1 for record in records if record["execution_status"] == "executed_python_reference") == 3
