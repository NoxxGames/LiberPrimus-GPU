from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_kernel.synthetic_parity import EXPECTED_NATIVE_HASH, python_reference_hash


def test_stage5f_implementation_record_is_synthetic_only() -> None:
    payload = yaml.safe_load(Path("data/cuda/stage5f-cuda-synthetic-kernel-implementation.yaml").read_text(encoding="utf-8"))
    record = payload["records"][0]

    assert record["selected_kernel_id"] == "shift_score_kernel"
    assert record["selected_transform_family"] == "caesar_mod29"
    assert record["selected_adapter_family"] == "native_cpu_synthetic_shift_adapter"
    assert record["synthetic_only"] is True
    assert record["real_liber_primus_data_used"] is False
    assert record["gpu_benchmark_performed"] is False
    assert record["performance_claim"] is False
    assert record["speedup_claim"] is False
    assert record["native_reference_hash"] == EXPECTED_NATIVE_HASH


def test_stage5f_python_reference_hash_matches_stage5d_native_hash() -> None:
    assert python_reference_hash() == EXPECTED_NATIVE_HASH


def test_stage5f_cuda_source_does_not_launch_python_workers() -> None:
    source_text = Path("cuda/kernels/shift_score_kernel.cu").read_text(encoding="utf-8").lower()
    test_text = Path("cuda/tests/shift_score_kernel_test.cpp").read_text(encoding="utf-8").lower()
    combined = source_text + "\n" + test_text

    assert "python" not in combined
    assert "py_" not in combined
