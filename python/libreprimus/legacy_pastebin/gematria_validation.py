"""Non-canonical Gematria prime-value validation profile for Stage 0C."""

from __future__ import annotations

from dataclasses import dataclass

PROFILE_NAME = "legacy_validation_gematria_primus_v0"


@dataclass(frozen=True)
class GematriaEntry:
    rune: str
    label: str
    decimal_index: int
    prime_value: int


ENTRIES: tuple[GematriaEntry, ...] = (
    GematriaEntry("ᚠ", "F", 0, 2),
    GematriaEntry("ᚢ", "V/U", 1, 3),
    GematriaEntry("ᚦ", "TH", 2, 5),
    GematriaEntry("ᚩ", "O", 3, 7),
    GematriaEntry("ᚱ", "R", 4, 11),
    GematriaEntry("ᚳ", "C/K", 5, 13),
    GematriaEntry("ᚷ", "G", 6, 17),
    GematriaEntry("ᚹ", "W", 7, 19),
    GematriaEntry("ᚻ", "H", 8, 23),
    GematriaEntry("ᚾ", "N", 9, 29),
    GematriaEntry("ᛁ", "I", 10, 31),
    GematriaEntry("ᛄ", "J", 11, 37),
    GematriaEntry("ᛇ", "EO", 12, 41),
    GematriaEntry("ᛈ", "P", 13, 43),
    GematriaEntry("ᛉ", "X", 14, 47),
    GematriaEntry("ᛋ", "S/Z", 15, 53),
    GematriaEntry("ᛏ", "T", 16, 59),
    GematriaEntry("ᛒ", "B", 17, 61),
    GematriaEntry("ᛖ", "E", 18, 67),
    GematriaEntry("ᛗ", "M", 19, 71),
    GematriaEntry("ᛚ", "L", 20, 73),
    GematriaEntry("ᛝ", "NG/ING", 21, 79),
    GematriaEntry("ᛟ", "OE", 22, 83),
    GematriaEntry("ᛞ", "D", 23, 89),
    GematriaEntry("ᚪ", "A", 24, 97),
    GematriaEntry("ᚫ", "AE", 25, 101),
    GematriaEntry("ᚣ", "Y", 26, 103),
    GematriaEntry("ᛡ", "IA/IO", 27, 107),
    GematriaEntry("ᛠ", "EA", 28, 109),
)

RUNE_TO_ENTRY = {entry.rune: entry for entry in ENTRIES}
PRIME_TO_ENTRY = {entry.prime_value: entry for entry in ENTRIES}
VALID_PRIME_VALUES = frozenset(PRIME_TO_ENTRY)


@dataclass(frozen=True)
class GlyphValidation:
    decimal_index: int | None
    valid: bool
    unknown_glyph: bool
    unknown_prime_value: bool
    alias_inferred: bool
    warning: str | None


def decimal_index_for_prime(prime_value: int) -> int | None:
    """Return decimal index for a Gematria prime value."""
    entry = PRIME_TO_ENTRY.get(prime_value)
    if entry is None:
        return None
    return entry.decimal_index


def validate_glyph_prime(glyph: str, observed_prime_value: int) -> GlyphValidation:
    """Validate one rune glyph against one observed Gematria prime value."""
    decimal_index = decimal_index_for_prime(observed_prime_value)
    entry = RUNE_TO_ENTRY.get(glyph)

    if decimal_index is None:
        return GlyphValidation(
            decimal_index=None,
            valid=False,
            unknown_glyph=entry is None,
            unknown_prime_value=True,
            alias_inferred=False,
            warning=f"Unknown Gematria prime value {observed_prime_value} for glyph {glyph!r}.",
        )

    if entry is None:
        inferred = PRIME_TO_ENTRY[observed_prime_value]
        return GlyphValidation(
            decimal_index=decimal_index,
            valid=False,
            unknown_glyph=True,
            unknown_prime_value=False,
            alias_inferred=True,
            warning=(
                f"Unknown glyph {glyph!r}; observed prime value {observed_prime_value} "
                f"matches {inferred.rune!r} ({inferred.label})."
            ),
        )

    if entry.prime_value != observed_prime_value:
        return GlyphValidation(
            decimal_index=decimal_index,
            valid=False,
            unknown_glyph=False,
            unknown_prime_value=False,
            alias_inferred=False,
            warning=(
                f"Prime mismatch for glyph {glyph!r}: expected {entry.prime_value}, "
                f"observed {observed_prime_value}."
            ),
        )

    return GlyphValidation(
        decimal_index=entry.decimal_index,
        valid=True,
        unknown_glyph=False,
        unknown_prime_value=False,
        alias_inferred=False,
        warning=None,
    )
