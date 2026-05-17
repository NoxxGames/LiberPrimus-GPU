from __future__ import annotations

from pathlib import Path

from libreprimus.method_backlog.loader import load_method_backlog
from libreprimus.method_backlog.validation import validate_method_backlog_item

REPO = Path(__file__).resolve().parents[2]
BACKLOG = REPO / "experiments/queues/stage3e-method-backlog.yaml"


def test_method_backlog_schema_validates() -> None:
    backlog = load_method_backlog(BACKLOG)

    assert backlog.payload["record_type"] == "method_backlog"
    assert backlog.payload["no_solve_claim"] is True
    assert backlog.payload["cuda_enabled"] is False
    assert len(backlog.items) == 6


def test_all_stage3e_backlog_items_validate() -> None:
    backlog = load_method_backlog(BACKLOG)

    for item in backlog.items:
        validated = validate_method_backlog_item(item)
        assert validated["no_solve_claim"] is True
        assert validated["cuda_enabled"] is False
        assert validated["canonical_corpus_active"] is False
        assert validated["page_boundaries_final"] is False
