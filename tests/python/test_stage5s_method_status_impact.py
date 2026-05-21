from __future__ import annotations

from pathlib import Path

import yaml


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5s_method_status_records_never_upgrade_to_solved() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-method-status-impact.yaml")
    assert len(records) == 7
    for record in records:
        assert record["method_status_upgrade_allowed"] is False
        assert record["method_status_upgraded"] is False
        assert record["upgraded_to_solved"] is False
        assert record["unsolved_page_family_activated"] is False
        assert record["broad_solved_fixture_expansion_approved"] is False
        assert record["solve_claim"] is False


def test_stage5s_method_status_records_cover_original_family_boundaries() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-method-status-impact.yaml")
    subjects = {record["method_subject"]: record for record in records}
    assert subjects["gematria_mod29_shift_score_kernel"]["impact_status"] == (
        "expanded_parity_verified_infrastructure_only"
    )
    assert subjects["direct_translation"]["impact_status"] == "not_upgraded_mapped_fixture_source_only"
    assert subjects["stage5q_blocked_original_family_fixtures"]["impact_status"] == (
        "remain_blocked_pending_separate_contracts"
    )
    for subject in ("reverse_gematria", "rotated_reverse_gematria", "vigenere_explicit_key", "prime_minus_one_stream"):
        assert subjects[subject]["impact_status"] == "unaffected"
