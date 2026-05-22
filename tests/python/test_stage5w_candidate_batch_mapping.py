from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_contract.candidate_batch_mapping import build_candidate_batch_mapping


def test_stage5w_candidate_batch_mapping_uses_stream_schedule_refs(tmp_path: Path) -> None:
    records = build_candidate_batch_mapping(candidate_batch_mapping_out=tmp_path / "mapping.yaml", out_dir=tmp_path)
    assert len(records) == 3
    assert all(record["candidate_batch_abi_id"] == "candidate_batch_abi_v0" for record in records)
    assert all(record["stream_start_index"] == 0 for record in records)
    assert all("stream_schedule_ref:uint32" in record["transform_parameter_layout"] for record in records)
    statuses = {record["mapping_status"] for record in records}
    assert "synthetic_control_ready" in statuses
    assert "p56_solved_fixture_ready" in statuses
    assert "p56_blocked_missing_token_values" in statuses

