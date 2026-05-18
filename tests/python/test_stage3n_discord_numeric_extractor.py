from __future__ import annotations

from libreprimus.discord_ingestion.numeric_extractor import extract_numeric_candidates


def test_numeric_extractor_finds_known_numbers_near_keywords() -> None:
    records = extract_numeric_candidates(
        "Gematria GP sum near 3301, 1033, 761, and 167.",
        source_file_sha256="c" * 64,
        ordinal=1,
    )

    assert records
    assert {3301, 1033, 761, 167}.issubset(set(records[0]["numbers"]))
    assert records[0]["raw_message_committed"] is False
