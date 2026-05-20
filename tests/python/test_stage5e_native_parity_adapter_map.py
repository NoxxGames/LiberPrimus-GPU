from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_kernel_contract.native_parity_mapping import build_native_parity_adapter_map
from libreprimus.cuda_kernel_contract.selection import select_first_kernel_contract


EXPECTED_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"


def test_stage5e_native_parity_map_uses_stage5d_hashes(tmp_path: Path) -> None:
    contract_path = tmp_path / "contract.yaml"
    select_first_kernel_contract(
        out_dir=tmp_path / "out",
        contract_out=contract_path,
        adapter_selection_out=tmp_path / "adapter.yaml",
    )

    records = build_native_parity_adapter_map(
        contract_path=contract_path,
        out_dir=tmp_path / "out",
        native_parity_out=tmp_path / "native.yaml",
    )
    record = records[0]

    assert record["native_parity_mapped"] is True
    assert record["stage5d_one_thread_hash"] == EXPECTED_HASH
    assert record["stage5d_multi_thread_hash"] == EXPECTED_HASH
    assert record["stage5d_thread_counts"] == [1, 2, 4, 8, 16]
    assert record["stage5d_python_native_parity"] is True
