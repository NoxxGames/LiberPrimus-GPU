"""Non-authoritative anchor detection for legacy Pastebin records."""

from __future__ import annotations

from libreprimus.legacy_pastebin.models import SOURCE_ID, LegacyPastebinAnchor, LegacyPastebinLinePair

PARABLE_WORD = "ᛈᚪᚱᚪᛒᛚᛖ"


def infer_anchors(line_pairs: list[LegacyPastebinLinePair]) -> list[LegacyPastebinAnchor]:
    """Detect non-authoritative alignment anchors without finalizing page boundaries."""
    anchors: list[LegacyPastebinAnchor] = []
    for line_pair in line_pairs:
        if PARABLE_WORD in line_pair.rune_words:
            anchors.append(
                LegacyPastebinAnchor(
                    record_type="legacy_pastebin_anchor",
                    source_id=SOURCE_ID,
                    anchor_type="known_solved_direct_text",
                    page_label_candidate="57.jpg",
                    confidence="high",
                    canonical_page_boundary=False,
                    pair_index=line_pair.pair_index,
                    evidence=f"matched rune word {PARABLE_WORD}",
                )
            )
    return anchors
