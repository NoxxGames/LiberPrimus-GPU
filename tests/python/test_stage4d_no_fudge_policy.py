from __future__ import annotations

from libreprimus.bounded_numeric.no_fudge_policy import (
    enforce_cap,
    validate_no_fudge_operation,
    validate_no_fudge_record,
)


def test_stage4d_no_fudge_policy_rejects_nearest_prime() -> None:
    assert validate_no_fudge_operation("nearest-prime adjustment")


def test_stage4d_no_fudge_policy_rejects_arbitrary_delta() -> None:
    assert validate_no_fudge_operation("apply arbitrary +/-n post hoc")


def test_stage4d_no_fudge_record_requires_derived_formula_source() -> None:
    record = {
        "result_id": "bad",
        "no_fudge_policy": True,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
        "derived_values": [{"name": "x", "value": 1}],
    }
    assert validate_no_fudge_record(record)


def test_stage4d_manifest_caps_enforced() -> None:
    try:
        enforce_cap([{"x": 1}, {"x": 2}], 1, "manifest")
    except ValueError as error:
        assert "candidate_count_exceeds_cap" in str(error)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("expected cap failure")
