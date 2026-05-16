"""Gematria Primus frozen profile helpers."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

FIRST_29_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
GEMATRIA_PROFILE_ID = "gematria-primus-v0"


@dataclass(frozen=True)
class ProfileValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


@dataclass(frozen=True)
class GematriaEntry:
    index: int
    prime: int
    rune: str
    latin_labels: list[str]
    preferred_latin_label: str
    notes: list[str]


@dataclass(frozen=True)
class GematriaProfile:
    profile_id: str
    status: str
    canonical_profile_active: bool
    canonical_corpus_active: bool
    modulus: int
    entries: list[GematriaEntry]
    sha256: str

    @property
    def rune_to_entry(self) -> dict[str, GematriaEntry]:
        return {entry.rune: entry for entry in self.entries}

    @property
    def prime_to_entry(self) -> dict[int, GematriaEntry]:
        return {entry.prime: entry for entry in self.entries}

    @property
    def index_to_entry(self) -> dict[int, GematriaEntry]:
        return {entry.index: entry for entry in self.entries}


def compute_sha256(path: Path) -> str:
    """Return SHA-256 for file bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON from UTF-8."""
    return json.loads(path.read_text(encoding="utf-8"))


def _entries(payload: dict[str, Any]) -> list[GematriaEntry]:
    return [
        GematriaEntry(
            index=int(item["index"]),
            prime=int(item["prime"]),
            rune=str(item["rune"]),
            latin_labels=[str(label) for label in item["latin_labels"]],
            preferred_latin_label=str(item["preferred_latin_label"]),
            notes=[str(note) for note in item.get("notes", [])],
        )
        for item in payload.get("entries", [])
    ]


def load_gematria_profile(path: Path) -> GematriaProfile:
    """Load a Gematria profile without silently normalizing it."""
    payload = load_json(path)
    return GematriaProfile(
        profile_id=str(payload["profile_id"]),
        status=str(payload["status"]),
        canonical_profile_active=bool(payload["canonical_profile_active"]),
        canonical_corpus_active=bool(payload["canonical_corpus_active"]),
        modulus=int(payload["modulus"]),
        entries=_entries(payload),
        sha256=compute_sha256(path),
    )


def validate_gematria_profile(profile: GematriaProfile) -> ProfileValidationResult:
    """Validate Stage 0E Gematria profile invariants."""
    errors: list[str] = []
    if profile.profile_id != GEMATRIA_PROFILE_ID:
        errors.append("Unexpected Gematria profile id.")
    if profile.status != "frozen_profile":
        errors.append("Gematria profile status must be frozen_profile.")
    if profile.canonical_profile_active is not True:
        errors.append("Gematria profile must have canonical_profile_active=true.")
    if profile.canonical_corpus_active is not False:
        errors.append("Gematria profile must have canonical_corpus_active=false.")
    if profile.modulus != 29:
        errors.append("Gematria modulus must be 29.")
    if len(profile.entries) != 29:
        errors.append("Gematria profile must contain exactly 29 entries.")
    indices = [entry.index for entry in profile.entries]
    primes = [entry.prime for entry in profile.entries]
    runes = [entry.rune for entry in profile.entries]
    if indices != list(range(29)):
        errors.append("Gematria indices must be exactly 0..28 in order.")
    if primes != FIRST_29_PRIMES:
        errors.append("Gematria prime values must equal the first 29 primes in order.")
    if len(set(runes)) != len(runes):
        errors.append("Gematria rune glyphs must be unique.")
    if len(set(primes)) != len(primes):
        errors.append("Gematria prime values must be unique.")
    if any(not entry.preferred_latin_label for entry in profile.entries):
        errors.append("Preferred Latin labels must be non-empty.")
    if any(not entry.latin_labels for entry in profile.entries):
        errors.append("Latin label lists must be non-empty.")
    if "\u16c2" in set(runes):
        errors.append("Glyph variant \u16c2 must not be canonical in Gematria profile.")
    if len(profile.rune_to_entry) != 29 or len(profile.prime_to_entry) != 29:
        errors.append("Gematria inverse lookups must be bijective.")
    return ProfileValidationResult(valid=not errors, errors=errors, warnings=[])


def assert_gematria_profile_valid(path: Path) -> GematriaProfile:
    """Load and validate or raise ValueError."""
    profile = load_gematria_profile(path)
    result = validate_gematria_profile(profile)
    if not result.valid:
        raise ValueError("; ".join(result.errors))
    return profile
