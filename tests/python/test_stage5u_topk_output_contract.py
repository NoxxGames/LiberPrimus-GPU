from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.topk_output_contract import build_topk_output_contract


def test_stage5u_topk_output_contract_is_deterministic_without_reducer_implementation(tmp_path: Path) -> None:
    record = build_topk_output_contract(topk_output_contract_out=tmp_path / "topk.yaml", out_dir=tmp_path / "reports")[0]
    assert record["stable_sort_required"] is True
    assert record["deterministic_across_threads"] is True
    assert record["deterministic_across_backends"] is True
    assert record["required_hashes"] == ["output_token_hash"]
    assert record["implementation_allowed_now"] is False
