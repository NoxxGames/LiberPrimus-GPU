from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.gap_closure import build_gap_closure


def test_stage5u_gap_closure_closes_stage5t_gaps_by_contract_only(tmp_path: Path) -> None:
    records = build_gap_closure(
        stage5t_gaps=Path("data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml"),
        gap_closure_out=tmp_path / "gaps.yaml",
        out_dir=tmp_path / "reports",
    )
    surfaces = {record["surface_id"] for record in records}
    assert surfaces == {"token_buffer_header", "key_schedule_buffer", "stream_schedule_buffer", "score_vector_shape", "top_k_output_shape"}
    assert len(records) == 5
    assert all(record["stage5u_closure_status"] == "closed_by_contract" for record in records)
    assert all(record["implementation_pending"] is True for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
