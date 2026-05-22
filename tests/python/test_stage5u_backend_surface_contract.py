from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.backend_surface_contract import build_backend_surface_contract


def test_stage5u_backend_surfaces_keep_python_orchestration_and_no_cuda_execution(tmp_path: Path) -> None:
    records = build_backend_surface_contract(backend_surface_contract_out=tmp_path / "backends.yaml", out_dir=tmp_path / "reports")
    surfaces = {record["backend_surface_id"]: record for record in records}
    assert {"python_orchestration_surface", "native_cpp_reference_surface", "cuda_device_kernel_surface"}.issubset(surfaces)
    assert surfaces["python_orchestration_surface"]["owner_layer"] == "python"
    assert surfaces["native_cpp_reference_surface"]["future_status"] == "may own deterministic CPU conformance in Stage 5V"
    assert surfaces["cuda_device_kernel_surface"]["requires_cuda_c_subset"] is True
    assert all(record["allowed_to_execute_cuda"] is False for record in records)
    assert all(record["cxx_launches_python_workers"] is False for record in records)
