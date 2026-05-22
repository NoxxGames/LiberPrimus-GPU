from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.topk_conformance import build_topk_conformance


def test_stage5v_topk_tie_policy_is_deterministic(tmp_path: Path) -> None:
    records = build_topk_conformance(topk_conformance_out=tmp_path / "topk.yaml", out_dir=tmp_path / "out")
    assert len(records) == 1
    record = records[0]
    assert record["tie_policy"] == "score_desc_candidate_id_asc"
    assert record["sorted_candidate_ids"] == ["cand-a", "cand-b", "cand-c"]
    assert record["gpu_benchmark_performed"] is False
