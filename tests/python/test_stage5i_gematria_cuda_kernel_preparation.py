from __future__ import annotations

from libreprimus.gematria_cuda_prep.kernel_preparation import build_kernel_preparation_records
from libreprimus.gematria_cuda_prep.models import SOURCE_CONTRACT_ID


def test_stage5i_preparation_requires_stage5h_contract_id(tmp_path) -> None:
    records = build_kernel_preparation_records(preparation_out=tmp_path / "prep.yaml", out_dir=tmp_path)
    record = records[0]
    assert record["source_contract_id"] == SOURCE_CONTRACT_ID
    assert record["target_future_kernel_name"] == "gematria_mod29_shift_score_kernel"
    assert record["cuda_execution_performed"] is False
    assert record["new_cuda_kernels_added"] == 0
