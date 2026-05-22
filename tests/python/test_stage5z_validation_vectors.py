from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.models import (
    P56_BOUNDED_FORMULA_HASH,
    P56_BOUNDED_OUTPUT_HASH,
    SYNTHETIC_OUTPUT_HASH,
)
from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_validation_vectors_include_expected_hashes_and_blockers(
    tmp_path: Path,
) -> None:
    records = _records(_build_all(tmp_path)["vectors"])
    by_kind = {record["validation_vector_kind"]: record for record in records}
    assert by_kind["synthetic_positive"]["expected_output_token_hash"] == SYNTHETIC_OUTPUT_HASH
    assert by_kind["synthetic_positive"]["executable_in_stage5aa"] is True
    assert by_kind["bounded_p56_fixture_safe"]["expected_output_token_hash"] == P56_BOUNDED_OUTPUT_HASH
    assert by_kind["bounded_p56_fixture_safe"]["expected_formula_hash"] == P56_BOUNDED_FORMULA_HASH
    assert by_kind["bounded_p56_fixture_safe"]["executable_in_stage5aa"] is False
    assert by_kind["full_p56_blocker"]["validation_status"] == "blocked_full_p56_token_buffer_missing"
    assert by_kind["full_p56_blocker"]["expected_output_token_hash"] is None
    assert by_kind["full_p56_blocker"]["full_p56_allowed"] is False
    assert "invalid_token_value_control" in by_kind
    assert "separator_preservation_control" in by_kind
