from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.implementation_status import build_implementation_status


def test_stage5v_implementation_status_converts_stage5u_gaps(tmp_path: Path) -> None:
    records = build_implementation_status(implementation_status_out=tmp_path / "status.yaml", out_dir=tmp_path / "out")
    assert len(records) == 8
    by_gap = {record["stage5u_gap_id"]: record for record in records}
    assert by_gap["token_buffer_header"]["implementation_status"] == "passed"
    assert by_gap["key_schedule_buffer"]["implementation_status"] == "shape_only"
    assert by_gap["stream_schedule_buffer"]["implementation_status"] == "shape_only"
    assert by_gap["cuda_backend"]["implementation_status"] == "blocked"
    assert all(record["cuda_execution_performed"] is False for record in records)
