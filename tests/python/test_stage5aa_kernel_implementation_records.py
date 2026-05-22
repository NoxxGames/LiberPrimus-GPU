from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.kernel_implementation import build_kernel_implementation_records


def test_stage5aa_kernel_implementation_is_synthetic_only(tmp_path: Path) -> None:
    record = build_kernel_implementation_records(kernel_implementation_out=tmp_path / "kernel.yaml", out_dir=tmp_path)[0]
    assert record["implementation_status"] == "implemented_synthetic_only"
    assert record["implementation_scope"] == "stage5z_validation_synthetic_prime_control_only"
    assert record["cuda_source_modified"] is True
    assert record["new_cuda_kernels_added"] == 1
    assert record["p56_cuda_allowed"] is False
    assert record["full_p56_cuda_allowed"] is False
    assert record["unsolved_page_cuda_allowed"] is False
    assert record["solve_claim"] is False
