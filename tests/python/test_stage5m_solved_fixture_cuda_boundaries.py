from __future__ import annotations

from pathlib import Path
import re

import yaml


def test_stage5m_boundary_record_declares_exact_allowed_scope() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml").read_text(encoding="utf-8"))[
        "records"
    ][0]
    assert record["approved_scope"] == "exact_five_stage5l_mapped_solved_fixture_safe_token_buffers"
    assert record["mapping_count"] == 5
    assert len(record["allowed_mapping_ids"]) == 5
    assert "unsolved_pages" in record["prohibited_inputs"]
    assert "raw_liber_primus_page_text" in record["prohibited_inputs"]
    assert record["no_new_kernel_boundary"] is True
    assert record["host_runner_only_source_change"] is True
    assert record["gpu_benchmark_performed"] is False
    assert record["speedup_claim"] is False
    assert record["solve_claim"] is False


def test_stage5m_cuda_source_keeps_single_existing_device_kernel() -> None:
    text = Path("cuda/kernels/gematria_shift_score_kernel.cu").read_text(encoding="utf-8")
    kernel_definitions = re.findall(r"__global__\s+void\s+(\w+)", text)
    assert kernel_definitions == ["gematria_mod29_shift_score_kernel"]
    assert "run_gematria_shift_score_raw" in text


def test_stage5m_cpp_runner_does_not_launch_python_workers() -> None:
    text = Path("cuda/tests/gematria_shift_score_stage5m_runner.cpp").read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(r"Py_Initialize|python\.exe|python3|popen\(.*python|system\(.*python")
    assert pattern.search(text) is None
