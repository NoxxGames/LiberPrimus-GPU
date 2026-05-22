from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.key_schedule_contract import build_key_schedule_contract


def test_stage5u_key_schedule_is_explicit_and_not_dictionary_scale(tmp_path: Path) -> None:
    records = build_key_schedule_contract(key_schedule_contract_out=tmp_path / "keys.yaml", out_dir=tmp_path / "reports")
    vigenere = records[0]
    assert len(records) == 2
    assert "vigenere_explicit_key" in vigenere["supported_families"]
    assert vigenere["key_token_domain"] == "0..28"
    assert vigenere["supports_dictionary_key_list"] is False
    assert all(record["cuda_execution_allowed"] is False for record in records)
