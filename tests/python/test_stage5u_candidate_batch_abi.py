from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.candidate_batch_abi import build_candidate_batch_abi


def test_candidate_batch_abi_defines_required_no_execution_surfaces(tmp_path: Path) -> None:
    records = build_candidate_batch_abi(candidate_batch_abi_out=tmp_path / "abi.yaml", out_dir=tmp_path / "reports")
    assert len(records) == 1
    record = records[0]
    assert record["abi_id"] == "candidate_batch_abi_v0"
    assert record["abi_scope"] == "contract_only_no_execution"
    assert record["cuda_execution_performed"] is False
    assert record["new_cuda_kernel_added"] is False
    assert record["no_gpu_ci_safe"] is True
    assert {"variable_length_token_buffers", "score_vector_outputs", "topk_candidate_outputs"}.issubset(
        record["supported_surfaces"]
    )
