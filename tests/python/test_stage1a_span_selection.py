import json
from pathlib import Path

from libreprimus.solved_fixtures.models import SpanSelector
from libreprimus.solved_fixtures.span_selection import select_tokens


def _write_tokens(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    records = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune"},
        {"token_index_global": 1, "logical_line_index": 1, "token_kind": "rune"},
        {"token_index_global": 2, "logical_line_index": 1, "token_kind": "rune"},
    ]
    (path / "tokens.jsonl").write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
    (path / "page_candidates.jsonl").write_text(
        json.dumps({"candidate_page_id": "p1", "start_token_index": 1, "end_token_index": 2}) + "\n",
        encoding="utf-8",
    )


def test_explicit_token_range_selects_tokens(tmp_path: Path) -> None:
    _write_tokens(tmp_path)
    tokens, error = select_tokens(
        tmp_path,
        SpanSelector("explicit_token_range", "rtkd-master-v0-candidate", start_token_index=1, end_token_index=2),
    )

    assert error is None
    assert [token["token_index_global"] for token in tokens] == [1, 2]


def test_explicit_logical_line_range_selects_tokens(tmp_path: Path) -> None:
    _write_tokens(tmp_path)
    tokens, error = select_tokens(
        tmp_path,
        SpanSelector(
            "explicit_logical_line_range",
            "rtkd-master-v0-candidate",
            start_logical_line_index=1,
            end_logical_line_index=1,
        ),
    )

    assert error is None
    assert len(tokens) == 2


def test_page_candidate_reference_is_reviewable_span(tmp_path: Path) -> None:
    _write_tokens(tmp_path)
    tokens, error = select_tokens(
        tmp_path,
        SpanSelector("page_candidate_reference", "rtkd-master-v0-candidate", page_candidate_ids=["p1"]),
    )

    assert error is None
    assert [token["token_index_global"] for token in tokens] == [1, 2]


def test_pending_selector_returns_pending_error(tmp_path: Path) -> None:
    _write_tokens(tmp_path)
    tokens, error = select_tokens(tmp_path, SpanSelector("pending", "rtkd-master-v0-candidate"))

    assert tokens == []
    assert "pending" in str(error)
