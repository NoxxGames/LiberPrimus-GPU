from pathlib import Path

from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import FIRST_29_PRIMES, compute_sha256, load_gematria_profile, validate_gematria_profile


def _profile_path() -> Path:
    return repo_root() / "data/profiles/gematria/gematria-primus-v0.json"


def test_gematria_profile_v0_validates() -> None:
    profile = load_gematria_profile(_profile_path())
    result = validate_gematria_profile(profile)

    assert result.valid, result.errors
    assert len(profile.entries) == 29
    assert [entry.index for entry in profile.entries] == list(range(29))
    assert [entry.prime for entry in profile.entries] == FIRST_29_PRIMES
    assert len(profile.rune_to_entry) == 29
    assert len(profile.prime_to_entry) == 29
    assert profile.modulus == 29
    assert "\u16c2" not in profile.rune_to_entry


def test_gematria_profile_sha256_lock_matches() -> None:
    path = _profile_path()
    expected = (path.with_suffix(".sha256").read_text(encoding="utf-8").split()[0])

    assert compute_sha256(path) == expected
