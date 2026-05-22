from __future__ import annotations

import pytest

from libreprimus.doc_staleness.stage_ids import parse_stage_id


def test_stage5ab_stage_parser_orders_double_suffixes() -> None:
    assert parse_stage_id("Stage 5Z") < parse_stage_id("Stage 5AA")
    assert parse_stage_id("Stage 5AA") < parse_stage_id("Stage 5AB")
    assert parse_stage_id("Stage 5AB") < parse_stage_id("Stage 5AC")


def test_stage5ab_stage_parser_orders_normal_stages() -> None:
    assert parse_stage_id("Stage 4Q") < parse_stage_id("Stage 5A")
    assert parse_stage_id("Stage 5Y") < parse_stage_id("Stage 5Z")


def test_stage5ab_stage_parser_rejects_missing_stage() -> None:
    with pytest.raises(ValueError):
        parse_stage_id("not a stage label")
