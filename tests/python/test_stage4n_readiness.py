from __future__ import annotations

from libreprimus.stego_positive_controls.readiness import build_readiness_record


def test_stage4n_historical_missing_expected_output_is_blocked() -> None:
    readiness = build_readiness_record(
        {"fixture_id": "historical", "toolchain": ["outguess"]},
        category="outguess_known_positive_candidate",
        cache_record={"cache_record_id": "cache", "local_availability": "source_only"},
        expected_record={"expected_output_id": "expected", "expected_output_required": True, "expected_output_status": "unknown"},
        toolchain_records=[{"toolchain": "outguess", "toolchain_state": "outguess_missing"}],
        record_type="stego_positive_control_readiness",
    )
    assert readiness["ready_state"] == "blocked_expected_output_unknown"
    assert "expected_output_unknown" in readiness["blockers"]


def test_stage4n_validate_rejects_forbidden_execution_flags(tmp_path) -> None:
    from libreprimus.stego_positive_controls.validation import _validate_false_fields

    errors: list[str] = []
    _validate_false_fields({"tool_executed": True, "raw_file_committed": True, "solve_claim": True}, label="test", errors=errors)
    assert "test:tool_executed_must_be_false" in errors
    assert "test:raw_file_committed_must_be_false" in errors
    assert "test:solve_claim_must_be_false" in errors
