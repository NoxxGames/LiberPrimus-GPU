"""Possible-token parsing helpers for token-case review notes."""

from __future__ import annotations

import re
from dataclasses import dataclass


PLAUSIBLE_FIRST_SYMBOLS = set("01234OoZzIiLl?")
VISIBLE_TOKEN_RE = re.compile(r"^[^\s]{2}")
VISUAL_PLACEHOLDER_RE = re.compile(r"(?<!\S)([0-4?][0-9A-Za-z?]|[0-9A-Za-z?]\?)(?=\s|$|[.,;:])")


@dataclass(frozen=True)
class PossibleTokenParse:
    possible_tokens: list[str]
    include_all_possible_tokens_for_variant_controls: bool
    cleanup_warnings: list[str]
    malformed_fragments: list[dict[str, object]]


def _dedupe_ordered(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def _is_plausible_token_prefix(value: str) -> bool:
    if len(value) != 2:
        return False
    if value[0] not in PLAUSIBLE_FIRST_SYMBOLS:
        return False
    return not any(char.isspace() for char in value)


def _extract_from_fragment(raw_fragment: str) -> tuple[list[str], list[str], dict[str, object] | None]:
    fragment = raw_fragment.strip()
    if not fragment:
        return [], ["empty_possible_token_fragment"], {
            "raw_fragment": raw_fragment,
            "extracted_tokens": [],
            "cleanup_status": "empty_possible_token_fragment",
        }

    tokens: list[str] = []
    warnings: list[str] = []
    malformed: dict[str, object] | None = None
    prefix_match = VISIBLE_TOKEN_RE.match(fragment)
    prefix = prefix_match.group(0) if prefix_match else ""
    remainder = fragment[2:].strip() if prefix else fragment

    if _is_plausible_token_prefix(prefix):
        tokens.append(prefix)
        if remainder:
            warnings.append("extracted_token_prefix_from_prose_segment")
    elif len(fragment) == 2:
        warnings.append("malformed_possible_token_fragment")
    else:
        warnings.append("malformed_possible_token_fragment")

    for match in VISUAL_PLACEHOLDER_RE.finditer(remainder):
        token = match.group(1)
        if "?" in token and token not in tokens:
            tokens.append(token)
            warnings.append("extracted_visual_placeholder_from_prose")

    if remainder or not tokens:
        status = "token_prefix_extracted_from_prose" if tokens else "no_token_extracted"
        if any("?" in token for token in tokens):
            status = "token_prefix_and_visual_placeholder_extracted"
        malformed = {
            "raw_fragment": raw_fragment,
            "extracted_tokens": tokens,
            "cleanup_status": status,
        }
    return tokens, _dedupe_ordered(warnings), malformed


def parse_possible_token_notes(notes: str | None) -> PossibleTokenParse:
    """Parse semicolon-delimited review notes without treating prose as tokens."""

    if not notes:
        return PossibleTokenParse([], False, [], [])

    possible_tokens: list[str] = []
    cleanup_warnings: list[str] = []
    malformed_fragments: list[dict[str, object]] = []
    include_all = False

    for segment in notes.split(";"):
        stripped = segment.strip()
        if not stripped:
            continue
        key, sep, value = stripped.partition("=")
        if not sep:
            continue
        key = key.strip().lower()
        value = value.strip()
        if key == "include_all_possible_tokens_for_variant_controls":
            include_all = value.lower() == "true"
            continue
        if key != "possible_tokens":
            continue
        for raw_fragment in value.split("|"):
            tokens, warnings, malformed = _extract_from_fragment(raw_fragment)
            possible_tokens.extend(tokens)
            cleanup_warnings.extend(warnings)
            if malformed is not None:
                malformed_fragments.append(malformed)

    return PossibleTokenParse(
        possible_tokens=_dedupe_ordered(possible_tokens),
        include_all_possible_tokens_for_variant_controls=include_all,
        cleanup_warnings=_dedupe_ordered(cleanup_warnings),
        malformed_fragments=malformed_fragments,
    )
