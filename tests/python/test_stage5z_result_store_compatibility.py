from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_result_store_compatibility_preserves_stage4p_and_stage4i_contracts(
    tmp_path: Path,
) -> None:
    records = _records(_build_all(tmp_path)["result"])
    contracts = {record["compatibility_contract"] for record in records}
    assert contracts == {"stage4p", "stage4i"}
    assert all(record["compact_summary_only"] is True for record in records)
    assert all(record["result_body_publication_allowed"] is False for record in records)
    assert all(record["score_interpretation"] == "triage_only" for record in records)
