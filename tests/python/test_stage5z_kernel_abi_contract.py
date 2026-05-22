from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_kernel_abi_is_contract_only_cuda_c_subset(tmp_path: Path) -> None:
    record = _records(_build_all(tmp_path)["kernel"])[0]
    forbidden = set(record["forbidden_cuda_features"])
    assert record["abi_status"] == "contract_only_not_implemented"
    assert record["cuda_c_style_subset"] is True
    assert record["cuda_kernel_implemented"] is False
    assert record["cuda_source_modified"] is False
    assert record["implementation_allowed"] is False
    assert {"std::vector", "std::string", "exceptions", "dynamic_allocation"} <= forbidden
    assert "token_values" in record["input_buffers"]
    assert "status_codes" in record["output_buffers"]
