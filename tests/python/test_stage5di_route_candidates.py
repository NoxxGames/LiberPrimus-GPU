from __future__ import annotations

from libreprimus.token_block.stage5di import (
    ROUTE_CANDIDATE_FAMILY_IDS,
    SOURCE_FAMILY_IDS,
    validate_stage5di_dinkus_visual_delimiter,
    validate_stage5di_route_candidate_families,
)

from test_stage5di_common import ensure_stage5di_built, load_yaml, write_temp_yaml


def test_stage5di_candidate_family_index_includes_required_families() -> None:
    ensure_stage5di_built()
    counts, errors = validate_stage5di_route_candidate_families()

    assert errors == []
    assert counts["candidate_family_count"] == len(SOURCE_FAMILY_IDS)
    assert counts["route_candidate_family_count"] == len(ROUTE_CANDIDATE_FAMILY_IDS)
    assert counts["visual_marker_candidate_count"] == 1


def test_stage5di_required_historical_route_records_exist() -> None:
    ensure_stage5di_built()

    expected_records = [
        "data/historical-route/stage5di-2016-message-route-meta-clue.yaml",
        "data/historical-route/stage5di-page32-tree-polar-route-candidate.yaml",
        "data/historical-route/stage5di-pdd-153-triangle-word-route-candidate.yaml",
        "data/historical-route/stage5di-page56-dwh-hash-target-contract.yaml",
        "data/historical-route/stage5di-dinkus-visual-delimiter-candidate.yaml",
        "data/historical-route/stage5di-magic-square-matrix-route-context.yaml",
    ]
    for path in expected_records:
        payload = load_yaml(path)
        assert payload["stage_id"] == "stage-5di"
        assert payload["experiment_authorized_now"] is False
        assert payload["solve_claim"] is False


def test_stage5di_dinkus_visual_marker_is_not_interpreted() -> None:
    ensure_stage5di_built()
    counts, errors = validate_stage5di_dinkus_visual_delimiter()

    assert errors == []
    assert counts["candidate_status"] == "source_locked_visual_marker_only"
    assert counts["measurement_performed_now"] is False
    assert counts["meaning_claimed_now"] is False


def test_stage5di_dinkus_validator_rejects_meaning_claim(tmp_path) -> None:
    ensure_stage5di_built()
    payload = load_yaml("data/historical-route/stage5di-dinkus-visual-delimiter-candidate.yaml")
    payload["meaning_claimed_now"] = True
    temp = write_temp_yaml(tmp_path / "dinkus.yaml", payload)

    _, errors = validate_stage5di_dinkus_visual_delimiter(record=temp)

    assert errors
    assert "meaning_claimed_now_must_be_false" in errors
