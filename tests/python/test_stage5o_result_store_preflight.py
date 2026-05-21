from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_solved_fixture_cuda_repeat.result_store_preflight import build_result_store_preflight


def test_stage5o_result_store_preflight_references_stage4p_and_compact_policy(tmp_path: Path) -> None:
    records = build_result_store_preflight(
        result_store_preflight_out=tmp_path / "result-store.yaml",
        out_dir=tmp_path,
    )

    ready = [record for record in records if record["stage5p_ready"] is True]
    assert len(records) == 3
    assert len(ready) == 1
    assert ready[0]["result_store_contract"] == "stage4p"
    assert ready[0]["score_summary_contract"] == "stage4i"
    assert ready[0]["generated_result_body_publication_allowed"] is False
    assert ready[0]["compact_summary_only"] is True
    assert ready[0]["method_status_upgrade_allowed"] is False


def test_stage5o_result_store_preflight_blocks_missing_stage4p_summary(tmp_path: Path) -> None:
    records = build_result_store_preflight(
        stage4p_summary=tmp_path / "missing-stage4p-summary.yaml",
        result_store_preflight_out=tmp_path / "result-store.yaml",
        out_dir=tmp_path,
    )

    assert records[0]["stage4p_summary_present"] is False
    assert records[0]["preflight_status"] == "blocked_repeat_parity_or_stage4p_missing"
    assert all(record["stage5p_ready"] is False for record in records)
