from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_kernel.synthetic_parity import EXPECTED_NATIVE_HASH


def test_stage5f_parity_record_matches_native_hash_when_passed() -> None:
    payload = yaml.safe_load(Path("data/cuda/stage5f-cuda-synthetic-parity-records.yaml").read_text(encoding="utf-8"))
    record = payload["records"][0]

    assert record["candidate_count"] == 6
    assert record["native_reference_hash"] == EXPECTED_NATIVE_HASH
    if record["parity_status"] == "passed":
        assert record["cuda_output_hash"] == EXPECTED_NATIVE_HASH
        assert record["cuda_native_hash_match"] is True


def test_stage5f_parity_record_never_claims_real_data_or_benchmark() -> None:
    payload = yaml.safe_load(Path("data/cuda/stage5f-cuda-synthetic-parity-records.yaml").read_text(encoding="utf-8"))
    record = payload["records"][0]

    assert record["real_liber_primus_data_used"] is False
    assert record["solved_fixture_cuda_used"] is False
    assert record["unsolved_page_cuda_used"] is False
    assert record["gpu_benchmark_performed"] is False
    assert record["performance_claim"] is False
    assert record["speedup_claim"] is False
    assert record["solve_claim"] is False
