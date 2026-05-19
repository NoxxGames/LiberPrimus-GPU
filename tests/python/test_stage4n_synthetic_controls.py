from __future__ import annotations

from libreprimus.stego_positive_controls.synthetic_controls import synthetic_outguess_controls


def test_stage4n_synthetic_controls_are_fixture_free() -> None:
    controls = synthetic_outguess_controls()
    assert len(controls) == 2
    assert all(control["source_id"] == "stage4n-synthetic" for control in controls)
    assert any(control["expected_role"] == "synthetic_positive" for control in controls)
