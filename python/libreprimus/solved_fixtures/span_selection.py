"""Span selection for solved-page fixture reproduction."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.solved_fixtures.models import SpanSelector


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def select_tokens(candidate_dir: Path, selector: SpanSelector) -> tuple[list[dict[str, Any]], str | None]:
    if selector.selector_kind == "pending":
        return [], "pending span selector"
    tokens = read_jsonl(candidate_dir / "tokens.jsonl")
    if selector.selector_kind == "explicit_token_range":
        if selector.start_token_index is None or selector.end_token_index is None:
            return [], "explicit token range is incomplete"
        return [
            token
            for token in tokens
            if selector.start_token_index <= int(token["token_index_global"]) <= selector.end_token_index
        ], None
    if selector.selector_kind == "explicit_logical_line_range":
        if selector.start_logical_line_index is None or selector.end_logical_line_index is None:
            return [], "explicit logical line range is incomplete"
        return [
            token
            for token in tokens
            if selector.start_logical_line_index <= int(token["logical_line_index"]) <= selector.end_logical_line_index
        ], None
    if selector.selector_kind == "page_candidate_reference":
        pages = read_jsonl(candidate_dir / "page_candidates.jsonl")
        ranges: list[tuple[int, int]] = []
        for page in pages:
            if page.get("candidate_page_id") in selector.page_candidate_ids:
                start = page.get("start_token_index")
                end = page.get("end_token_index")
                if isinstance(start, int) and isinstance(end, int):
                    ranges.append((start, end))
        if not ranges:
            return [], "page candidate reference has no token range"
        selected: list[dict[str, Any]] = []
        for token in tokens:
            index = int(token["token_index_global"])
            if any(start <= index <= end for start, end in ranges):
                selected.append(token)
        return selected, None
    return [], f"unsupported selector kind: {selector.selector_kind}"
