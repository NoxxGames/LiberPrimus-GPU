from __future__ import annotations

from libreprimus.scoring.null_controls import generate_negative_control_texts, generate_null_control_texts
from libreprimus.scoring.minimal_triage import score_text


def test_null_controls_are_deterministic_with_seed() -> None:
    policy = {"random_seed": 42, "length": 17, "random_control_count": 3, "shuffled_control_count": 2}

    first = generate_null_control_texts(policy=policy, seed_text="ABCDEFGHIJKLMNOPQ")
    second = generate_null_control_texts(policy=policy, seed_text="ABCDEFGHIJKLMNOPQ")

    assert first == second


def test_null_controls_match_requested_length() -> None:
    policy = {"random_seed": 42, "length": 23, "random_control_count": 2, "shuffled_control_count": 1}

    controls = generate_null_control_texts(policy=policy, seed_text="A" * 23)

    assert all(len(control["text"]) == 23 for control in controls)


def test_negative_controls_score_low_or_noisy() -> None:
    controls = generate_negative_control_texts(length=30)
    labels = {score_text(control["text"]).confidence_label for control in controls}

    assert labels <= {"noisy", "garbage"}
    assert "garbage" in labels
