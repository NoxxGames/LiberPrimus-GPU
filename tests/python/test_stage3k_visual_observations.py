from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.visual_observations.validation import validate_visual_records

REPO = Path(__file__).resolve().parents[2]
VISUAL = REPO / "data/observations/visual/visual-numeric-observations-v0.yaml"


def _records() -> dict:
    payload = yaml.safe_load(VISUAL.read_text(encoding="utf-8"))
    return {record["observation_id"]: record for record in payload["records"]}


def test_visual_observations_validate() -> None:
    count, errors = validate_visual_records(VISUAL)

    assert count == 5
    assert errors == []


def test_cuneiform_record_contains_declared_values() -> None:
    record = _records()["lp-cuneiform-sexagesimal-candidate-v0"]
    values = record["derived_values"]

    assert values["pairwise_17_13_base60"] == 1033
    assert values["pairwise_55_1_base60"] == 3301
    assert values["full_base60"] == 3722101
    assert values["full_base60_mod29"] == 9


def test_binary_dot_record_preserves_ambiguity() -> None:
    record = _records()["lp-binary-dot-tree-candidate-v0"]
    values = record["derived_values"]["three_filled_two_empty_candidate_values"]

    assert values == [7, 11, 13, 14, 19, 21, 22, 25, 26, 28]
    assert 13 in values
    assert "not unique" in record["candidate_readings"][0]["notes"]


def test_visual_observations_not_experiment_seeds() -> None:
    for record in _records().values():
        assert record["usable_as_experiment_seed"] is False
        assert record["trusted_as_canonical"] is False
