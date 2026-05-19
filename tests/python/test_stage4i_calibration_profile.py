from __future__ import annotations

from libreprimus.scoring_consolidation.calibration_profiles import build_calibration_profile
from libreprimus.scoring_consolidation.report_builder import build_calibration_report


def test_stage4i_calibration_profile_can_use_research_log_source() -> None:
    profile = build_calibration_profile(prefer_generated=False)
    assert profile["calibration_source"] == "research_log_summary"
    assert profile["positive_control_count"] == 12
    assert profile["null_control_count"] == 250
    assert profile["negative_control_count"] == 4


def test_stage4i_calibration_report_records_controls_and_noisy_families() -> None:
    report = build_calibration_report(build_calibration_profile(prefer_generated=False))
    assert report["positive_controls_available"] is True
    assert report["null_controls_available"] is True
    assert report["negative_controls_available"] is True
    assert "caesar_affine" in report["known_noisy_families"]
    assert report["solve_claim"] is False
