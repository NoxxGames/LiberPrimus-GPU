"""Glyph variant profile helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from libreprimus.profiles.gematria_profile import GematriaProfile, ProfileValidationResult, compute_sha256, load_json

GLYPH_VARIANT_PROFILE_ID = "glyph-variants-v0"


@dataclass(frozen=True)
class GlyphVariant:
    observed_glyph: str
    normalized_rune_candidate: str
    normalized_index_candidate: int
    normalized_prime_candidate: int
    normalized_latin_label_candidate: str
    policy: str
    evidence: list[dict[str, Any]]
    canonical_mapping_change: bool
    warnings: list[str]


@dataclass(frozen=True)
class GlyphVariantProfile:
    profile_id: str
    status: str
    canonical_profile_active: bool
    canonical_corpus_active: bool
    variants: list[GlyphVariant]
    sha256: str

    @property
    def observed_to_variant(self) -> dict[str, GlyphVariant]:
        return {variant.observed_glyph: variant for variant in self.variants}


def load_glyph_variant_profile(path: Path) -> GlyphVariantProfile:
    payload = load_json(path)
    variants = [
        GlyphVariant(
            observed_glyph=str(item["observed_glyph"]),
            normalized_rune_candidate=str(item["normalized_rune_candidate"]),
            normalized_index_candidate=int(item["normalized_index_candidate"]),
            normalized_prime_candidate=int(item["normalized_prime_candidate"]),
            normalized_latin_label_candidate=str(item["normalized_latin_label_candidate"]),
            policy=str(item["policy"]),
            evidence=list(item.get("evidence", [])),
            canonical_mapping_change=bool(item["canonical_mapping_change"]),
            warnings=[str(warning) for warning in item.get("warnings", [])],
        )
        for item in payload.get("variants", [])
    ]
    return GlyphVariantProfile(
        profile_id=str(payload["profile_id"]),
        status=str(payload["status"]),
        canonical_profile_active=bool(payload["canonical_profile_active"]),
        canonical_corpus_active=bool(payload["canonical_corpus_active"]),
        variants=variants,
        sha256=compute_sha256(path),
    )


def validate_glyph_variant_profile(profile: GlyphVariantProfile, gematria: GematriaProfile) -> ProfileValidationResult:
    errors: list[str] = []
    if profile.profile_id != GLYPH_VARIANT_PROFILE_ID:
        errors.append("Unexpected glyph variant profile id.")
    if profile.status != "frozen_profile":
        errors.append("Glyph variant profile status must be frozen_profile.")
    if profile.canonical_profile_active is not True:
        errors.append("Glyph variant profile must have canonical_profile_active=true.")
    if profile.canonical_corpus_active is not False:
        errors.append("Glyph variant profile must have canonical_corpus_active=false.")
    canonical_runes = set(gematria.rune_to_entry)
    for variant in profile.variants:
        entry = gematria.rune_to_entry.get(variant.normalized_rune_candidate)
        if entry is None:
            errors.append(f"Variant {variant.observed_glyph!r} maps to a non-Gematria rune.")
            continue
        if variant.observed_glyph in canonical_runes:
            errors.append(f"Variant {variant.observed_glyph!r} duplicates a canonical rune.")
        if entry.index != variant.normalized_index_candidate:
            errors.append(f"Variant {variant.observed_glyph!r} has wrong normalized index.")
        if entry.prime != variant.normalized_prime_candidate:
            errors.append(f"Variant {variant.observed_glyph!r} has wrong normalized prime.")
        if variant.canonical_mapping_change:
            errors.append(f"Variant {variant.observed_glyph!r} must not change canonical mapping.")
        if variant.policy != "preserve_raw_apply_normalized_view_only":
            errors.append(f"Variant {variant.observed_glyph!r} has unsupported policy.")
    return ProfileValidationResult(valid=not errors, errors=errors, warnings=[])
