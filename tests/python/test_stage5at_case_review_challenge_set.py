from pathlib import Path

import yaml


ACTIVE = ["I/l", "O/0", "1/I/l", "S/5", "Z/2", "B/8", "G/6", "o/0", "q/g/p"]


def _load(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_stage5at_active_classes_and_challenges_match_stage5ar() -> None:
    stage5ar = _load("data/token-block/stage5ar-token-case-ambiguity-records.yaml")
    stage5at = _load("data/token-block/stage5at-case-review-challenge-set.yaml")
    expected_indexes = {idx for record in stage5ar["records"] for idx in record["affected_token_indexes_0_based"]}

    assert [record["canonical_symbol"] for record in stage5ar["records"]] == ACTIVE
    assert stage5at["active_ambiguity_classes"] == ACTIVE
    assert stage5at["challenge_count"] == len(expected_indexes)
    assert len({record["token_review_group_id"] for record in stage5at["records"]}) == stage5at["challenge_count"]
    assert {"f/F", "A/4", "C/G"}.isdisjoint(stage5at["active_ambiguity_classes"])


def test_stage5at_challenges_link_coordinates_and_values() -> None:
    payload = _load("data/token-block/stage5at-case-review-challenge-set.yaml")
    first = payload["records"][0]
    assert first["original_image_id"].startswith("stage5ar-original-page-")
    assert first["coordinate_ref"].startswith("r")
    assert first["candidate_tokens"]
    assert first["canonical_token"]
    assert first["primary_60_current_value"] is not None
    assert first["primary_60_candidate_values"]
    assert "value_sensitive" in first["value_delta_summary"]
    assert all(record["review_status"] == "human_review_required" for record in payload["records"])
    assert all(record["decision_status"] == "unresolved" for record in payload["records"])
