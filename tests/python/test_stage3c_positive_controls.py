from __future__ import annotations

from libreprimus.scoring.positive_controls import load_positive_control_texts


def test_positive_controls_load_from_solved_fixtures() -> None:
    controls = load_positive_control_texts()

    fixture_controls = [control for control in controls if control["control_id"].startswith("positive-")]
    assert len(fixture_controls) >= 10
    assert any("expected" not in control["text"].lower() for control in fixture_controls)
    assert all(control["text"] for control in fixture_controls)
