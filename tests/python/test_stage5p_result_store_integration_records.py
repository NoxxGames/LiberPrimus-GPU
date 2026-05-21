from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_result_store.result_store_integration import build_result_store_integration


def test_stage5p_result_store_integration_is_compact_and_stage4p_compatible(tmp_path: Path) -> None:
    records = build_result_store_integration(
        result_store_integration_out=tmp_path / "result-store.yaml",
        out_dir=tmp_path,
    )

    assert len(records) == 5
    for record in records:
        assert record["stage4p_compatibility"] is True
        assert record["result_store_contract"] == "stage4p"
        assert record["stage5p_integration_status"] == "integrated_compact_summary"
        assert record["generated_body_publication_allowed"] is False
        assert record["generated_outputs_committed"] is False
        assert record["cuda_execution_performed"] is False
        assert record["source_cuda_execution_performed"] is True
        assert "output_token_hash" in record
        assert "output_tokens" not in record
        assert "output_text" not in record


def test_stage5p_result_store_links_stage5o_repeat_parity(tmp_path: Path) -> None:
    records = build_result_store_integration(
        result_store_integration_out=tmp_path / "result-store.yaml",
        out_dir=tmp_path,
    )

    assert {record["source_repeat_parity_record_id"] for record in records} == {
        f"stage5o-repeat-parity-{index:02d}" for index in range(5)
    }
    assert all(record["stage5o_repeat_cuda_output_token_hash"] == record["output_token_hash"] for record in records)
