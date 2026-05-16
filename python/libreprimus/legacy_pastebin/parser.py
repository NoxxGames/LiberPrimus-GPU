"""Parser for the local legacy Pastebin LP2 rune/prime-value serialization."""

from __future__ import annotations

import re
from dataclasses import dataclass

from libreprimus.legacy_pastebin.gematria_validation import (
    decimal_index_for_prime,
    validate_glyph_prime,
)
from libreprimus.legacy_pastebin.models import (
    SOURCE_ID,
    SOURCE_LOCAL_FILENAME,
    LegacyPastebinLinePair,
    LegacyPastebinWarning,
)

RUNE_RE = re.compile(r"[\u16A0-\u16FF]")
PRIME_ROW_RE = re.compile(r"^[\s{},0-9]+$")


@dataclass(frozen=True)
class ParsedPhysicalRow:
    line_number: int
    raw_line: str
    trimmed: str
    row_class: str


def classify_row(trimmed: str) -> str:
    """Classify one nonblank row."""
    if trimmed == "{}":
        return "empty_row"
    if RUNE_RE.search(trimmed) and trimmed.startswith("{") and trimmed.endswith("}"):
        return "rune_row"
    if trimmed.startswith("{") and trimmed.endswith("}") and PRIME_ROW_RE.fullmatch(trimmed):
        return "prime_value_row"
    return "unknown"


def parse_physical_rows(text: str) -> list[ParsedPhysicalRow]:
    """Parse nonblank physical rows while preserving line numbers and raw text."""
    rows: list[ParsedPhysicalRow] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        trimmed = raw_line.strip()
        if not trimmed:
            continue
        rows.append(
            ParsedPhysicalRow(
                line_number=line_number,
                raw_line=raw_line,
                trimmed=trimmed,
                row_class=classify_row(trimmed),
            )
        )
    return rows


def parse_rune_row(trimmed: str) -> list[str]:
    """Parse a rune row into word-like rune tokens."""
    if trimmed == "{}":
        return []
    if not (trimmed.startswith("{") and trimmed.endswith("}")):
        raise ValueError(f"Rune row does not use outer braces: {trimmed!r}")
    inner = trimmed[1:-1].strip()
    if not inner:
        return []
    return [part.strip() for part in inner.split(",") if part.strip()]


def parse_prime_row(trimmed: str) -> list[list[int]]:
    """Parse a nested prime-value row into integer word arrays."""
    if trimmed == "{}":
        return []
    if not (trimmed.startswith("{") and trimmed.endswith("}")):
        raise ValueError(f"Prime row does not use outer braces: {trimmed!r}")

    inner = trimmed[1:-1].strip()
    if not inner:
        return []

    words: list[list[int]] = []
    index = 0
    while index < len(inner):
        while index < len(inner) and inner[index] in {" ", "\t", ","}:
            index += 1
        if index >= len(inner):
            break
        if inner[index] != "{":
            raise ValueError(f"Expected nested word brace in prime row near: {inner[index:index+20]!r}")
        end = inner.find("}", index + 1)
        if end == -1:
            raise ValueError("Unclosed nested word brace in prime row.")
        word_inner = inner[index + 1 : end].strip()
        if word_inner:
            words.append([int(part.strip()) for part in word_inner.split(",") if part.strip()])
        else:
            words.append([])
        index = end + 1

    return words


def _warning(
    *,
    source_sha256: str,
    message: str,
    pair_index: int | None = None,
    source_line_number: int | None = None,
    word_index: int | None = None,
    glyph_index: int | None = None,
) -> LegacyPastebinWarning:
    return LegacyPastebinWarning(
        record_type="legacy_pastebin_warning",
        source_id=SOURCE_ID,
        source_sha256=source_sha256,
        source_local_filename=SOURCE_LOCAL_FILENAME,
        message=message,
        pair_index=pair_index,
        source_line_number=source_line_number,
        word_index=word_index,
        glyph_index=glyph_index,
    )


def _pair_rows(rows: list[ParsedPhysicalRow], source_sha256: str) -> tuple[list[tuple[ParsedPhysicalRow, ParsedPhysicalRow | None]], list[LegacyPastebinWarning]]:
    pairs: list[tuple[ParsedPhysicalRow, ParsedPhysicalRow | None]] = []
    warnings: list[LegacyPastebinWarning] = []
    index = 0

    while index < len(rows):
        rune_row = rows[index]
        if rune_row.row_class == "prime_value_row":
            warnings.append(
                _warning(
                    source_sha256=source_sha256,
                    message="Expected rune row but found prime-value row; skipping row for recovery.",
                    source_line_number=rune_row.line_number,
                )
            )
            index += 1
            continue
        if rune_row.row_class == "unknown":
            warnings.append(
                _warning(
                    source_sha256=source_sha256,
                    message="Expected rune row but found unknown row; attempting to pair anyway.",
                    source_line_number=rune_row.line_number,
                )
            )

        prime_row = rows[index + 1] if index + 1 < len(rows) else None
        if prime_row is None:
            warnings.append(
                _warning(
                    source_sha256=source_sha256,
                    message="Rune row has no following prime-value row.",
                    source_line_number=rune_row.line_number,
                )
            )
            pairs.append((rune_row, None))
            break

        if prime_row.row_class not in {"prime_value_row", "empty_row"}:
            warnings.append(
                _warning(
                    source_sha256=source_sha256,
                    message="Expected prime-value row after rune row; attempting local recovery.",
                    source_line_number=prime_row.line_number,
                )
            )
            pairs.append((rune_row, None))
            index += 1
            continue

        pairs.append((rune_row, prime_row))
        index += 2

    return pairs, warnings


def build_line_pairs(text: str, source_sha256: str) -> tuple[list[LegacyPastebinLinePair], list[LegacyPastebinWarning], int, int]:
    """Parse, pair, and validate all local legacy Pastebin rows."""
    rows = parse_physical_rows(text)
    row_pairs, warnings = _pair_rows(rows, source_sha256)
    line_pairs: list[LegacyPastebinLinePair] = []
    rune_row_count = 0
    prime_row_count = 0

    for pair_index, (rune_row, prime_row) in enumerate(row_pairs):
        if rune_row.row_class in {"rune_row", "empty_row"}:
            rune_row_count += 1
        if prime_row is not None and prime_row.row_class in {"prime_value_row", "empty_row"}:
            prime_row_count += 1

        try:
            rune_words = parse_rune_row(rune_row.trimmed)
        except ValueError as error:
            rune_words = []
            warnings.append(
                _warning(
                    source_sha256=source_sha256,
                    message=str(error),
                    pair_index=pair_index,
                    source_line_number=rune_row.line_number,
                )
            )

        prime_words: list[list[int]] = []
        if prime_row is not None:
            try:
                prime_words = parse_prime_row(prime_row.trimmed)
            except ValueError as error:
                warnings.append(
                    _warning(
                        source_sha256=source_sha256,
                        message=str(error),
                        pair_index=pair_index,
                        source_line_number=prime_row.line_number,
                    )
                )

        pair_warnings: list[str] = []
        word_count_match = len(rune_words) == len(prime_words)
        per_word_length_match = True
        validated_prime_mapping = True
        glyph_alias_inferred = False
        decimal_index_words: list[list[int | None]] = []

        if not word_count_match:
            message = f"Word count mismatch: rune_words={len(rune_words)}, prime_words={len(prime_words)}."
            pair_warnings.append(message)
            warnings.append(
                _warning(
                    source_sha256=source_sha256,
                    message=message,
                    pair_index=pair_index,
                    source_line_number=rune_row.line_number,
                )
            )
            validated_prime_mapping = False

        for word_index, prime_word in enumerate(prime_words):
            rune_word = rune_words[word_index] if word_index < len(rune_words) else ""
            glyphs = list(rune_word)
            decimal_indices: list[int | None] = []

            if len(glyphs) != len(prime_word):
                per_word_length_match = False
                validated_prime_mapping = False
                message = (
                    f"Rune/prime length mismatch for word {word_index}: "
                    f"runes={len(glyphs)}, primes={len(prime_word)}."
                )
                pair_warnings.append(message)
                warnings.append(
                    _warning(
                        source_sha256=source_sha256,
                        message=message,
                        pair_index=pair_index,
                        source_line_number=rune_row.line_number,
                        word_index=word_index,
                    )
                )

            for glyph_index, prime_value in enumerate(prime_word):
                decimal_indices.append(decimal_index_for_prime(prime_value))
                if glyph_index >= len(glyphs):
                    continue

                validation = validate_glyph_prime(glyphs[glyph_index], prime_value)
                if not validation.valid and not validation.alias_inferred:
                    validated_prime_mapping = False
                if validation.alias_inferred:
                    glyph_alias_inferred = True
                if validation.warning is not None:
                    pair_warnings.append(validation.warning)
                    warnings.append(
                        _warning(
                            source_sha256=source_sha256,
                            message=validation.warning,
                            pair_index=pair_index,
                            source_line_number=rune_row.line_number,
                            word_index=word_index,
                            glyph_index=glyph_index,
                        )
                    )

            decimal_index_words.append(decimal_indices)

        line_pairs.append(
            LegacyPastebinLinePair(
                record_type="legacy_pastebin_line_pair",
                source_id=SOURCE_ID,
                source_sha256=source_sha256,
                source_local_filename=SOURCE_LOCAL_FILENAME,
                pair_index=pair_index,
                source_rune_line_number=rune_row.line_number,
                source_prime_line_number=prime_row.line_number if prime_row is not None else None,
                raw_rune_line=rune_row.raw_line,
                raw_prime_line=prime_row.raw_line if prime_row is not None else None,
                rune_words=rune_words,
                prime_words=prime_words,
                decimal_index_words=decimal_index_words,
                word_count_match=word_count_match,
                per_word_length_match=per_word_length_match,
                validated_prime_mapping=validated_prime_mapping,
                validation_status="valid" if not pair_warnings else "warnings",
                page_index_inferred=None,
                page_boundary_confidence="not_inferred",
                trusted_as_canonical=False,
                warnings=pair_warnings,
                empty_pair=not rune_words and not prime_words,
                glyph_alias_inferred=glyph_alias_inferred,
            )
        )

    return line_pairs, warnings, rune_row_count, prime_row_count
