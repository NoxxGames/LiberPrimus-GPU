from __future__ import annotations

from libreprimus.doc_staleness.stage_ids import find_stage_ids, parse_stage_id


def test_stage5ah_parser_orders_multi_letter_stage_suffixes() -> None:
    stages = [
        parse_stage_id(label)
        for label in ("Stage 5N", "Stage 5Z", "Stage 5AA", "Stage 5AG", "Stage 5AH", "Stage 5AI")
    ]

    assert stages == sorted(stages)


def test_stage5ah_parser_accepts_compact_and_dash_forms() -> None:
    assert parse_stage_id("stage5ag").label == "Stage 5AG"
    assert parse_stage_id("stage-5ah").label == "Stage 5AH"
    assert [stage.label for stage in find_stage_ids("Stage 5AG then stage-5ah then stage5ai")] == [
        "Stage 5AG",
        "Stage 5AH",
        "Stage 5AI",
    ]
