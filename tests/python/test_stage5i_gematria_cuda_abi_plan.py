from __future__ import annotations

from libreprimus.gematria_cuda_prep.abi_plan import build_abi_plan_records
from libreprimus.gematria_cuda_prep.validation import validate_stage5i_results


def test_stage5i_abi_plan_requires_pod_raw_buffer_interface(tmp_path) -> None:
    records = build_abi_plan_records(abi_plan_out=tmp_path / "abi.yaml", out_dir=tmp_path)
    record = records[0]
    assert record["c_compatible_kernel_boundary"] is True
    assert set(record["buffer_layout"]) >= {
        "token_values",
        "transformable_mask",
        "shifts",
        "output_token_values",
        "token_count",
        "candidate_count",
    }
    assert "uint8_t*" in record["future_kernel_signature_plan"]


def test_stage5i_abi_plan_rejects_stl_exceptions_and_allocation(tmp_path) -> None:
    abi = build_abi_plan_records(abi_plan_out=tmp_path / "abi.yaml", out_dir=tmp_path)[0]
    abi["stl_in_device_path_allowed"] = True
    abi["exceptions_in_device_path_allowed"] = True
    abi["dynamic_allocation_in_device_path_allowed"] = True
    errors = validate_stage5i_results.__globals__["_abi_errors"](abi, "abi")
    assert errors
