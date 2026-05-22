from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.score_vector_contract import build_score_vector_contract


def test_stage5u_score_vector_contract_uses_stage4i_triage_labels_only(tmp_path: Path) -> None:
    records = build_score_vector_contract(score_vector_contract_out=tmp_path / "scores.yaml", out_dir=tmp_path / "reports")
    components = {record["score_component_id"] for record in records}
    assert {"output_token_hash", "score_status", "confidence_label", "triage_label"}.issubset(components)
    assert len(records) == 7
    assert all(record["score_summary_contract"] == "stage4i" for record in records)
    assert all(record["triage_only"] is True for record in records)
    assert all(record["method_status_upgrade_allowed"] is False for record in records)
