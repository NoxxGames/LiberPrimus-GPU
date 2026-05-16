"""Summary helpers for legacy Pastebin extraction."""

from __future__ import annotations

from libreprimus.legacy_pastebin.models import (
    SOURCE_ID,
    SOURCE_LOCAL_FILENAME,
    LegacyPastebinLinePair,
    LegacyPastebinSummary,
    LegacyPastebinWarning,
)


def summarize(
    *,
    source_sha256: str,
    line_pairs: list[LegacyPastebinLinePair],
    warnings: list[LegacyPastebinWarning],
    rune_row_count: int,
    prime_value_row_count: int,
) -> LegacyPastebinSummary:
    """Create a non-canonical extraction summary."""
    unknown_glyph_count = sum(1 for warning in warnings if "Unknown glyph" in warning.message)
    unknown_prime_value_count = sum(
        1 for warning in warnings if "Unknown Gematria prime value" in warning.message
    )

    return LegacyPastebinSummary(
        record_type="legacy_pastebin_summary",
        source_id=SOURCE_ID,
        source_sha256=source_sha256,
        source_local_filename=SOURCE_LOCAL_FILENAME,
        line_pair_count=len(line_pairs),
        rune_row_count=rune_row_count,
        prime_value_row_count=prime_value_row_count,
        empty_pair_count=sum(1 for line_pair in line_pairs if line_pair.empty_pair),
        validation_warning_count=len(warnings),
        unknown_glyph_count=unknown_glyph_count,
        unknown_prime_value_count=unknown_prime_value_count,
        all_records_trusted_as_canonical=all(
            line_pair.trusted_as_canonical for line_pair in line_pairs
        )
        if line_pairs
        else False,
        canonical_corpus_allowed=False,
        page_boundary_status="not_finalized",
    )
