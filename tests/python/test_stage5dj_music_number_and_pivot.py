from __future__ import annotations

from libreprimus.token_block.stage5dj import (
    validate_stage5dj_music_candidate_family,
    validate_stage5dj_music_number_analysis,
    validate_stage5dj_pivot_integration,
)

from test_stage5dj_common import ensure_stage5dj_built, load_yaml, write_temp_yaml


def test_stage5dj_number_analysis_is_metadata_arithmetic_only() -> None:
    ensure_stage5dj_built()

    counts, errors = validate_stage5dj_music_number_analysis()
    assert errors == []
    payload = load_yaml("data/historical-route/stage5dj-music-number-analysis-metadata.yaml")
    if payload["source_number"] is not None:
        assert payload["prime_factorization"] == [1031, 1229, 1259]
        assert payload["base60_digits"] == [2, 3, 5, 32, 40, 41]
        assert payload["mod29_remainder"] == 24
    assert counts["analysis_status"] in {
        "metadata_arithmetic_only",
        "source_number_not_observed",
    }


def test_stage5dj_music_candidate_family_is_not_seed_ready() -> None:
    ensure_stage5dj_built()

    counts, errors = validate_stage5dj_music_candidate_family()
    assert errors == []
    payload = load_yaml("data/project-state/stage5dj-music-candidate-family-index.yaml")
    assert counts["candidate_family_count"] == 1
    family = payload["candidate_families"][0]
    assert family["candidate_family_id"] == "music_3301_instar_crab_canon_v0"
    assert family["usable_as_experiment_seed_now"] is False
    assert family["selected_now"] is False


def test_stage5dj_pivot_integration_adds_seventh_unselected_option() -> None:
    ensure_stage5dj_built()

    counts, errors = validate_stage5dj_pivot_integration()
    assert errors == []
    payload = load_yaml("data/project-state/stage5dj-pivot-readiness-integration.yaml")
    assert counts["pivot_option_count"] == 7
    assert payload["music_option_id"] == "music_3301_instar_crab_canon_first"
    assert payload["selected_next_solve_target_id"] is None
    assert all(candidate["selected_now"] is False for candidate in payload["pivot_candidates"])


def test_stage5dj_pivot_validator_rejects_selected_music_option(tmp_path) -> None:
    ensure_stage5dj_built()
    payload = load_yaml("data/project-state/stage5dj-pivot-readiness-integration.yaml")
    payload["pivot_candidates"][4]["selected_now"] = True
    temp = write_temp_yaml(tmp_path / "bad.yaml", payload)

    _, errors = validate_stage5dj_pivot_integration(package=temp)
    assert any("pivot_candidates_must_remain_unselected" in error for error in errors)
