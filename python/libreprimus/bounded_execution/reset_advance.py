"""Shared reset and advance state machine for bounded CPU experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from libreprimus.solved_fixtures.direct_translation import normalize_plaintext

RESET_MODES = {"none", "word", "clause", "line"}
ADVANCE_MODES = {"runes_only", "token_break_preserving"}
TRANSFORMABLE_KIND = "rune"


@dataclass(frozen=True)
class TransformToken:
    kind: str
    index29: int | None
    token_index_global: int | None
    line_id: Any | None
    separator_kind: str
    separator_text: str
    raw: dict[str, Any]

    @property
    def is_transformable(self) -> bool:
        return self.kind == TRANSFORMABLE_KIND and self.index29 is not None


@dataclass(frozen=True)
class MetadataSupport:
    token_breaks: bool
    word: bool
    clause: bool
    line: bool

    def as_dict(self) -> dict[str, bool]:
        return {
            "token_breaks": self.token_breaks,
            "word": self.word,
            "clause": self.clause,
            "line": self.line,
        }


@dataclass(frozen=True)
class RenderedCandidate:
    output_text: str
    output_indices: list[int]
    transformable_token_count: int
    metadata_support_status: dict[str, bool]
    warnings: list[str]


TransformStep = Callable[[int, int], tuple[int, dict[str, Any]]]


def build_tokens(token_records: list[dict[str, Any]]) -> list[TransformToken]:
    tokens: list[TransformToken] = []
    for record in token_records:
        kind = str(record.get("token_kind", "unknown"))
        index29 = record.get("index29")
        line_id = _line_id(record)
        tokens.append(
            TransformToken(
                kind=kind,
                index29=int(index29) if isinstance(index29, int) else None,
                token_index_global=_optional_int(record.get("token_index_global")),
                line_id=line_id,
                separator_kind=_separator_kind(record),
                separator_text=_separator_text(record),
                raw=dict(record),
            )
        )
    return tokens


def metadata_support(tokens: list[TransformToken]) -> MetadataSupport:
    rune_tokens = [token for token in tokens if token.is_transformable]
    return MetadataSupport(
        token_breaks=any(not token.is_transformable for token in tokens),
        word=any(token.separator_kind == "word" for token in tokens),
        clause=any(token.separator_kind == "clause" for token in tokens),
        line=bool(rune_tokens) and all(token.line_id is not None for token in rune_tokens),
    )


def unsupported_reset_reason(tokens: list[TransformToken], reset_mode: str) -> str | None:
    if reset_mode not in RESET_MODES:
        raise ValueError(f"Unsupported reset mode: {reset_mode}")
    support = metadata_support(tokens)
    if reset_mode == "word" and not support.word:
        return "word_reset_metadata_missing"
    if reset_mode == "clause" and not support.clause:
        return "clause_reset_metadata_missing"
    if reset_mode == "line" and not support.line:
        return "line_reset_metadata_missing"
    return None


def apply_stateful_transform(
    tokens: list[TransformToken],
    labels: dict[int, str],
    *,
    reset_mode: str,
    advance_mode: str,
    transform_step: TransformStep,
) -> RenderedCandidate:
    if reset_mode not in RESET_MODES:
        raise ValueError(f"Unsupported reset mode: {reset_mode}")
    if advance_mode not in ADVANCE_MODES:
        raise ValueError(f"Unsupported advance mode: {advance_mode}")
    reason = unsupported_reset_reason(tokens, reset_mode)
    if reason:
        raise ValueError(reason)

    support = metadata_support(tokens)
    warnings: list[str] = []
    if advance_mode == "token_break_preserving" and not support.token_breaks:
        warnings.append("token_break_metadata_missing_flat_mode_used")

    parts: list[str] = []
    output_indices: list[int] = []
    state_position = 0
    previous_line_id: Any = object()
    for token in tokens:
        if token.is_transformable:
            if reset_mode == "line" and token.line_id != previous_line_id:
                state_position = 0
                previous_line_id = token.line_id
            output_index, _details = transform_step(int(token.index29), state_position)
            if output_index < 0 or output_index > 28:
                raise ValueError(f"Transform produced out-of-range index: {output_index}")
            output_indices.append(output_index)
            parts.append(labels[output_index])
            state_position += 1
            continue

        if advance_mode == "token_break_preserving" and token.separator_text:
            parts.append(token.separator_text)
        if reset_mode == token.separator_kind:
            state_position = 0

    return RenderedCandidate(
        output_text=normalize_plaintext(parts),
        output_indices=output_indices,
        transformable_token_count=len(output_indices),
        metadata_support_status=support.as_dict(),
        warnings=warnings,
    )


def _optional_int(value: Any) -> int | None:
    return int(value) if isinstance(value, int) else None


def _line_id(token: dict[str, Any]) -> Any | None:
    for field in ("logical_line_index", "physical_line_number", "line_index"):
        value = token.get(field)
        if value is not None:
            return value
    return None


def _separator_kind(token: dict[str, Any]) -> str:
    kind = str(token.get("token_kind", "unknown"))
    if kind == "word_separator":
        return "word"
    if kind == "clause_separator":
        return "clause"
    if kind in {"line_separator", "physical_newline"}:
        return "line"
    return "unknown"


def _separator_text(token: dict[str, Any]) -> str:
    kind = str(token.get("token_kind", "unknown"))
    if kind == "word_separator":
        return " "
    if kind == "clause_separator":
        return ". "
    if kind in {"line_separator", "physical_newline"}:
        return "\n"
    if kind in {"paragraph_separator", "segment_separator", "chapter_separator", "page_separator_or_marker", "whitespace"}:
        return " "
    if kind in {"numeric_literal", "unknown_symbol"}:
        return str(token.get("raw_text", ""))
    return ""
