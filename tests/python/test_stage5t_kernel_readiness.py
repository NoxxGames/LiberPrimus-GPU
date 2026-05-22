from __future__ import annotations

from pathlib import Path

import yaml


def _kernels() -> dict[str, dict[str, object]]:
    records = yaml.safe_load(Path("data/cuda/stage5t-cuda-kernel-readiness.yaml").read_text(encoding="utf-8"))[
        "records"
    ]
    return {record["candidate_family_id"]: record for record in records}


def test_stage5t_kernel_readiness_does_not_authorize_implementation() -> None:
    for record in _kernels().values():
        assert record["implementation_allowed_now"] is False
        assert record["cuda_execution_performed"] is False
        assert record["new_cuda_kernel_added"] is False


def test_stage5t_kernel_readiness_prioritizes_existing_parity_then_abi_work() -> None:
    kernels = _kernels()
    assert kernels["gematria_shift_score_only"]["priority_rank"] == 1
    assert kernels["prime_minus_one_stream"]["requires_batch_abi"] is True
    assert kernels["vigenere_explicit_key"]["requires_batch_abi"] is True
    assert kernels["top_k_reducer"]["requires_batch_abi"] is True
    assert kernels["direct_translation"]["readiness_status"] == "not_cuda_kernel_priority"
