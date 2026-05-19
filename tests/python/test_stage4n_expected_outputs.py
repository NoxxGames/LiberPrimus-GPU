from __future__ import annotations

from libreprimus.stego_positive_controls.expected_outputs import build_expected_output_record


def test_stage4n_missing_expected_output_blocks_historical_positive() -> None:
    record = {"fixture_id": "historical", "expected_role": "known_positive_candidate"}
    expected = build_expected_output_record(record, category="outguess_known_positive_candidate")
    assert expected["expected_output_status"] == "unknown"
    assert expected["expected_output_required"] is True


def test_stage4n_synthetic_expected_output_is_known() -> None:
    record = {"fixture_id": "synthetic-positive"}
    expected = build_expected_output_record(record, category="synthetic_positive_control", synthetic=True)
    assert expected["expected_output_status"] == "synthetic_known"
    assert expected["expected_payload_sha256"]
