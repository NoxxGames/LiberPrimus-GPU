from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_contract.stream_contract import build_stream_contract


def test_stage5w_stream_contract_records_source_backed_formula_and_skip_policy(tmp_path: Path) -> None:
    records = build_stream_contract(stream_contract_out=tmp_path / "contract.yaml", out_dir=tmp_path)
    main = next(record for record in records if record["contract_id"] == "prime_minus_one_stream_native_contract_v0")
    assert main["stream_formula"] == "(prime_i - 1) mod 29"
    assert "ciphertext_token -" in main["ciphertext_to_plaintext_formula"]
    assert main["skip_policy"] == "cleartext_pass_through_tokens_do_not_advance_stream"
    assert main["cuda_execution_allowed"] is False
    assert main["solve_claim"] is False

