from __future__ import annotations

from libreprimus.cpu_batch.parity_contract import parity_contract_record


def test_stage4h_parity_contract_has_required_fields() -> None:
    record = parity_contract_record()
    assert record["parity_contract_version"] == "cpu-cuda-parity-contract-v0"
    assert record["cuda_used"] is False
    assert record["cuda_required"] is False
    assert record["no_solve_claim"] is True
    assert "output_text_hash" in record["required_result_fields"]
    assert any("Modulo arithmetic" in item for item in record["required_semantics"])
