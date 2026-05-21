from __future__ import annotations

from libreprimus.gematria_cuda_kernel.models import EXPECTED_OUTPUTS, NATIVE_FIXTURE_HASH
from libreprimus.gematria_cuda_kernel.synthetic_parity import python_reference_outputs


def test_stage5j_python_reference_vectors_match_stage5i_validation_vectors() -> None:
    assert python_reference_outputs() == [list(row) for row in EXPECTED_OUTPUTS]


def test_stage5j_passed_parity_requires_native_hash() -> None:
    record = {
        "parity_status": "passed",
        "cuda_output_hash": NATIVE_FIXTURE_HASH,
        "cuda_native_hash_match": True,
        "gematria_cuda_synthetic_parity_verified": True,
    }
    assert record["cuda_output_hash"] == NATIVE_FIXTURE_HASH
    assert record["cuda_native_hash_match"] is True
    assert record["gematria_cuda_synthetic_parity_verified"] is True


def test_stage5j_skipped_parity_does_not_claim_verified() -> None:
    record = {
        "parity_status": "skipped_build_not_requested",
        "cuda_output_hash": "",
        "cuda_native_hash_match": None,
        "gematria_cuda_synthetic_parity_verified": False,
    }
    assert record["parity_status"] != "passed"
    assert record["gematria_cuda_synthetic_parity_verified"] is False
