from __future__ import annotations

from libreprimus.observation_promotion.blockers import build_blocker_records
from libreprimus.observation_promotion.gates import evaluate_decision


def test_stage4l_cookie_zero_match_creates_negative_blocker() -> None:
    decision = {
        "review_decision_id": "decision-cookie",
        "observation_id": "cookie-1",
        "observation_type": "cookie_hash_candidate",
        "review_state": "deferred",
        "source_locked": True,
        "solve_claim": False,
    }
    result = evaluate_decision(decision)
    records = build_blocker_records(decision, result["blockers"])
    assert result["promotion_category"] == "blocked_negative_result"
    assert records[0]["blocker_kind"] == "negative_result"


def test_stage4l_stego_audio_missing_expected_output_creates_blocker() -> None:
    decision = {
        "review_decision_id": "decision-stego",
        "observation_id": "stego-1",
        "observation_type": "stego_audio_fixture_candidate",
        "review_state": "deferred",
        "source_locked": True,
        "solve_claim": False,
    }
    result = evaluate_decision(decision)
    records = build_blocker_records(decision, result["blockers"])
    kinds = {record["blocker_kind"] for record in records}
    assert result["promotion_category"] == "blocked_toolchain_unavailable"
    assert "missing_expected_output" in kinds
    assert "toolchain_unavailable" in kinds
