from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.result_store_compatibility import build_result_store_compatibility


def test_stage5u_result_store_compatibility_is_compact_hash_only(tmp_path: Path) -> None:
    records = build_result_store_compatibility(
        result_store_compatibility_out=tmp_path / "compat.yaml",
        out_dir=tmp_path / "reports",
    )
    assert len(records) == 3
    assert all(record["result_store_contract"] == "stage4p" for record in records)
    assert all(record["score_summary_contract"] == "stage4i" for record in records)
    assert all(record["output_token_hash_required"] is True for record in records)
    assert all(record["generated_body_publication_allowed"] is False for record in records)
    assert all(record["method_status_upgrade_allowed"] is False for record in records)
