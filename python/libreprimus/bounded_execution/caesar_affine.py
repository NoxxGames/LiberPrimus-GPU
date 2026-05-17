"""Caesar and affine mod-29 candidate enumeration for Stage 3A."""

from __future__ import annotations

from pathlib import Path

from libreprimus.profiles.gematria_profile import load_gematria_profile

MODULUS = 29
DEFAULT_GEMATRIA_PROFILE = Path("data/profiles/gematria/gematria-primus-v0.json")


def caesar_outputs(indices: list[int]) -> list[tuple[dict[str, int], list[int]]]:
    return [({"shift": shift}, [(value + shift) % MODULUS for value in indices]) for shift in range(MODULUS)]


def reverse_caesar_outputs(indices: list[int]) -> list[tuple[dict[str, int], list[int]]]:
    return [({"shift": shift, "direction": "reverse"}, [(value - shift) % MODULUS for value in indices]) for shift in range(MODULUS)]


def affine_outputs(indices: list[int]) -> list[tuple[dict[str, int], list[int]]]:
    return [
        ({"a": a_value, "b": b_value}, [(a_value * value + b_value) % MODULUS for value in indices])
        for a_value in range(1, MODULUS)
        for b_value in range(MODULUS)
    ]


def affine_inverse(a_value: int) -> int:
    for candidate in range(1, MODULUS):
        if (a_value * candidate) % MODULUS == 1:
            return candidate
    raise ValueError(f"No inverse modulo {MODULUS}: {a_value}")


def reverse_affine_outputs(indices: list[int]) -> list[tuple[dict[str, int], list[int]]]:
    outputs: list[tuple[dict[str, int], list[int]]] = []
    for a_value in range(1, MODULUS):
        inverse = affine_inverse(a_value)
        for b_value in range(MODULUS):
            outputs.append(
                (
                    {"a": a_value, "b": b_value, "a_inverse": inverse, "direction": "reverse"},
                    [(inverse * (value - b_value)) % MODULUS for value in indices],
                )
            )
    return outputs


def labels_by_index(profile_path: Path | None = None) -> dict[int, str]:
    path = profile_path or DEFAULT_GEMATRIA_PROFILE
    profile = load_gematria_profile(path)
    return {entry.index: entry.preferred_latin_label for entry in profile.entries}


def normalize_indices(indices: list[int], labels: dict[int, str]) -> str:
    return "".join(labels[value] for value in indices)
