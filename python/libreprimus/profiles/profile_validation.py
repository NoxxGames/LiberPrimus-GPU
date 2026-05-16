"""Aggregate profile validation helpers."""

from __future__ import annotations

from pathlib import Path

from libreprimus.profiles.gematria_profile import assert_gematria_profile_valid, validate_gematria_profile
from libreprimus.profiles.glyph_variant_profile import load_glyph_variant_profile, validate_glyph_variant_profile
from libreprimus.profiles.separator_grammar import load_separator_grammar, validate_separator_grammar


def validate_all_profiles(gematria_path: Path, variants_path: Path, separators_path: Path) -> list[str]:
    """Return all profile validation errors."""
    errors: list[str] = []
    gematria = assert_gematria_profile_valid(gematria_path)
    gematria_result = validate_gematria_profile(gematria)
    errors.extend(gematria_result.errors)
    variants = load_glyph_variant_profile(variants_path)
    errors.extend(validate_glyph_variant_profile(variants, gematria).errors)
    separators = load_separator_grammar(separators_path)
    errors.extend(validate_separator_grammar(separators).errors)
    return errors
