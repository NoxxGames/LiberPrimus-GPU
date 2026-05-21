from __future__ import annotations

from pathlib import Path

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_cuda_kernel.models import IMPLEMENTED_KERNEL_NAME, NATIVE_FIXTURE_HASH, SOURCE_CONTRACT_ID


def test_stage5j_implementation_record_has_required_kernel_and_fixture() -> None:
    record = read_yaml(Path("data/cuda/stage5j-gematria-cuda-kernel-implementation.yaml"))["records"][0]
    assert record["implemented_kernel_name"] == IMPLEMENTED_KERNEL_NAME
    assert record["source_contract_id"] == SOURCE_CONTRACT_ID
    assert record["native_fixture_hash"] == NATIVE_FIXTURE_HASH
    assert record["new_cuda_kernels_added"] == 1
    assert record["real_liber_primus_data_used"] is False
    assert record["solved_fixture_cuda_used"] is False
    assert record["unsolved_page_cuda_used"] is False


def test_stage5j_summary_keeps_performance_and_production_flags_false() -> None:
    summary = read_yaml(Path("data/cuda/stage5j-gematria-cuda-kernel-summary.yaml"))
    assert summary["implemented_kernel_name"] == IMPLEMENTED_KERNEL_NAME
    assert summary["gpu_benchmark_performed"] is False
    assert summary["performance_claim"] is False
    assert summary["speedup_claim"] is False
    assert summary["production_gematria_mod29_cuda_ready"] is False
    assert summary["solved_fixture_cuda_execution_allowed"] is False
    assert summary["real_liber_primus_data_used"] is False
    assert summary["solve_claim"] is False
