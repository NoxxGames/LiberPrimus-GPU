"""Resolve safe input slices for bounded Stage 3A execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.bounded_execution.models import InputSlice, MissingReviewableSliceInput
from libreprimus.paths import repo_root


def load_input_slice(item: dict[str, Any]) -> InputSlice:
    corpus_slice = dict(item.get("corpus_slice", {}))
    selector = dict(corpus_slice.get("selector", {}))
    inline_indices = selector.get("index29_values")
    if isinstance(inline_indices, list):
        return _inline_input_slice(corpus_slice, selector, inline_indices)
    return _corpus_candidate_input_slice(corpus_slice, selector)


def _inline_input_slice(
    corpus_slice: dict[str, Any],
    selector: dict[str, Any],
    inline_indices: list[Any],
) -> InputSlice:
    values = [int(value) for value in inline_indices]
    _validate_index_values(values)
    return InputSlice(
        slice_id=str(corpus_slice.get("slice_id", "inline-slice")),
        corpus_candidate_id=str(corpus_slice.get("corpus_candidate_id", "synthetic-inline")),
        page_candidate_id=str(selector.get("page_candidate_id", "inline-index29-values")),
        index29_values=values,
        source_metadata={"selector_kind": selector.get("selector_kind", "inline_index29_values")},
        warnings=["synthetic_inline_index_stream"],
    )


def _corpus_candidate_input_slice(corpus_slice: dict[str, Any], selector: dict[str, Any]) -> InputSlice:
    page_candidate_id = str(selector.get("page_candidate_id", ""))
    if not page_candidate_id or "placeholder" in page_candidate_id:
        raise MissingReviewableSliceInput("missing_reviewable_slice_input: page_candidate_id is missing or placeholder.")
    metadata = _metadata_paths(corpus_slice)
    page_candidates_path = metadata.get("generated_ignored_page_candidate_metadata")
    tokens_path = metadata.get("generated_ignored_token_metadata")
    if page_candidates_path is None or tokens_path is None:
        raise MissingReviewableSliceInput("missing_reviewable_slice_input: queue item lacks generated metadata paths.")
    if not page_candidates_path.is_file() or not tokens_path.is_file():
        raise MissingReviewableSliceInput("missing_reviewable_slice_input: generated corpus candidate outputs are absent.")

    page_candidate = _load_page_candidate(page_candidates_path, page_candidate_id)
    start = int(selector.get("start_token_index", page_candidate["start_token_index"]))
    end = int(selector.get("end_token_index", page_candidate["end_token_index"]))
    values = _load_index_values(tokens_path, start, end)
    _validate_index_values(values)
    expected = selector.get("expected_rune_token_count")
    warnings = ["flat_rune_index_stream_no_separator_context"]
    if expected is not None and int(expected) != len(values):
        warnings.append(f"expected_rune_token_count_mismatch:{expected}!={len(values)}")
    return InputSlice(
        slice_id=str(corpus_slice["slice_id"]),
        corpus_candidate_id=str(corpus_slice.get("corpus_candidate_id", page_candidate.get("corpus_candidate_id", ""))),
        page_candidate_id=page_candidate_id,
        index29_values=values,
        source_metadata={
            "page_candidate_id": page_candidate_id,
            "page_candidate_confidence": page_candidate.get("confidence"),
            "start_token_index": start,
            "end_token_index": end,
            "page_candidates_path": str(page_candidates_path),
            "tokens_path": str(tokens_path),
            "raw_unsolved_text_included": False,
        },
        warnings=warnings,
    )


def _metadata_paths(corpus_slice: dict[str, Any]) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for item in corpus_slice.get("metadata_paths", []):
        if not isinstance(item, dict):
            continue
        role = str(item.get("role", ""))
        raw_path = item.get("path")
        if not role or not raw_path:
            continue
        path = Path(str(raw_path))
        paths[role] = path if path.is_absolute() else repo_root() / path
    return paths


def _load_page_candidate(path: Path, page_candidate_id: str) -> dict[str, Any]:
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if payload.get("candidate_page_id") == page_candidate_id:
            return payload
    raise MissingReviewableSliceInput(f"missing_reviewable_slice_input: {page_candidate_id} not found.")


def _load_index_values(path: Path, start: int, end: int) -> list[int]:
    values: list[int] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        index = int(payload["token_index_global"])
        if index < start:
            continue
        if index > end:
            break
        index29 = payload.get("index29")
        if index29 is not None:
            values.append(int(index29))
    return values


def _validate_index_values(values: list[int]) -> None:
    if not values:
        raise MissingReviewableSliceInput("missing_reviewable_slice_input: input slice has no index29 values.")
    if any(value < 0 or value > 28 for value in values):
        raise ValueError("Index29 values must be in 0..28.")
