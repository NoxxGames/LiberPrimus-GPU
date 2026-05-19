from __future__ import annotations

from libreprimus.scoring_consolidation.inventory import scorer_records


def test_stage4i_scorer_records_have_ids_versions() -> None:
    records = scorer_records()
    assert records
    for record in records:
        assert record["scorer_id"]
        assert record["scorer_version"]
        assert record["solve_claim"] is False
        assert record["cuda_used"] is False
