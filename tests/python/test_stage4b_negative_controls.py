from __future__ import annotations

from libreprimus.source_lock_triage.negative_controls import build_negative_controls


def test_stage4b_braille_and_constellation_negative_controls_created() -> None:
    controls = {record["false_positive_class"]: record for record in build_negative_controls()}

    assert controls["braille_dot_readings"]["false_positive_risk"] == "extreme"
    assert controls["constellation_dot_readings"]["false_positive_risk"] == "extreme"
    assert controls["braille_dot_readings"]["solve_claim"] is False


def test_stage4b_broad_outguess_negative_control_created() -> None:
    controls = {record["false_positive_class"]: record for record in build_negative_controls()}

    assert "broad_outguess_bruteforce_garbage" in controls
    assert "expected hash" in controls["broad_outguess_bruteforce_garbage"]["recommended_use"].lower()
