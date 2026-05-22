from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.token_buffer_contract import build_token_buffer_contract


def test_stage5u_token_buffer_contract_preserves_separator_and_mask_rules(tmp_path: Path) -> None:
    records = build_token_buffer_contract(token_buffer_contract_out=tmp_path / "tokens.yaml", out_dir=tmp_path / "reports")
    by_id = {record["buffer_id"]: record for record in records}
    assert len(records) == 8
    assert by_id["token_values_buffer"]["allowed_value_range"] == "rune:0..28; separator:-1"
    assert by_id["transformable_mask_buffer"]["length_field"] == "token_count"
    assert by_id["transformable_mask_buffer"]["null_or_separator_encoding"] == "separator_mask=0"
    assert all(record["token_kind_metadata_preserved_in_output_hash"] is True for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
