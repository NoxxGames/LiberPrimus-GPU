from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_kernel_contract.native_parity_mapping import build_native_parity_adapter_map
from libreprimus.cuda_kernel_contract.readiness import build_implementation_readiness
from libreprimus.cuda_kernel_contract.selection import select_first_kernel_contract


def test_stage5e_readiness_is_synthetic_only(tmp_path: Path) -> None:
    contract_path = tmp_path / "contract.yaml"
    native_path = tmp_path / "native.yaml"
    select_first_kernel_contract(
        out_dir=tmp_path / "out",
        contract_out=contract_path,
        adapter_selection_out=tmp_path / "adapter.yaml",
    )
    build_native_parity_adapter_map(
        contract_path=contract_path,
        out_dir=tmp_path / "out",
        native_parity_out=native_path,
    )

    records = build_implementation_readiness(
        contract_path=contract_path,
        native_parity_path=native_path,
        out_dir=tmp_path / "out",
        readiness_out=tmp_path / "readiness.yaml",
    )
    record = records[0]

    assert record["readiness_status"] == "ready_for_stage5f_synthetic_only_implementation"
    assert "gpu_benchmark" in record["blocked_scopes"]
    assert "raw_data_processing" in record["blocked_scopes"]
    assert record["cuda_kernel_added"] is False
    assert record["gpu_benchmark_performed"] is False
