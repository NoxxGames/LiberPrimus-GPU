"""CPU-only reverse Gematria and rotated reverse Gematria fixture decoders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import GematriaProfile, load_gematria_profile
from libreprimus.solved_fixtures.direct_translation import normalize_plaintext, sha256_text

DEFAULT_GEMATRIA_PROFILE = Path("data/profiles/gematria/gematria-primus-v0.json")


def reverse_gematria_index(cipher_index: int) -> int:
    """Decode one Gematria index with p = 28 - c."""
    if cipher_index < 0 or cipher_index > 28:
        raise ValueError(f"Gematria index out of Z_29 range: {cipher_index}")
    return 28 - cipher_index


def rotated_reverse_gematria_index(cipher_index: int, *, rotation: int) -> int:
    """Decode one Gematria index with p = (28 - c + rotation) mod 29."""
    if cipher_index < 0 or cipher_index > 28:
        raise ValueError(f"Gematria index out of Z_29 range: {cipher_index}")
    if not isinstance(rotation, int):
        raise ValueError("rotated_reverse_gematria requires an integer rotation.")
    return (28 - cipher_index + rotation) % 29


def transform_chain_parameters(transform_chain: list[Any], method_family: str) -> dict[str, Any]:
    """Return explicitly declared transform parameters for a fixture method."""
    for item in transform_chain:
        if isinstance(item, dict) and item.get("name") == method_family:
            params = item.get("params", {})
            return dict(params) if isinstance(params, dict) else {}
        if isinstance(item, str) and item == method_family:
            return {}
    return {}


def decoded_index_formula(method_family: str, params: dict[str, Any]) -> str:
    if method_family == "reverse_gematria":
        return "decoded_index = 28 - cipher_index"
    if method_family == "rotated_reverse_gematria":
        return f"decoded_index = (28 - cipher_index + {params.get('rotation')}) mod 29"
    return "unsupported"


def decode_atbash_family(
    tokens: list[dict[str, Any]],
    *,
    method_family: str,
    transform_chain: list[Any],
    gematria_profile: GematriaProfile | None = None,
) -> dict[str, Any]:
    """Decode selected tokens using an explicit Atbash-family fixture method."""
    profile = gematria_profile or load_gematria_profile(repo_root() / DEFAULT_GEMATRIA_PROFILE)
    index_to_entry = profile.index_to_entry
    params = transform_chain_parameters(transform_chain, method_family)
    if method_family == "rotated_reverse_gematria" and "rotation" not in params:
        raise ValueError("rotated_reverse_gematria fixture must declare params.rotation.")

    parts: list[str] = []
    warnings: list[str] = []
    rune_count = 0
    numeric_literal_count = 0
    separator_count = 0

    for token in tokens:
        kind = str(token.get("token_kind"))
        if kind == "rune":
            raw_index = token.get("index29")
            if not isinstance(raw_index, int):
                raise ValueError(f"Rune token missing integer index29 at token {token.get('token_index_global')}.")
            if method_family == "reverse_gematria":
                decoded_index = reverse_gematria_index(raw_index)
            elif method_family == "rotated_reverse_gematria":
                decoded_index = rotated_reverse_gematria_index(raw_index, rotation=int(params["rotation"]))
            else:
                raise ValueError(f"Unsupported Atbash-family method: {method_family}")
            entry = index_to_entry.get(decoded_index)
            if entry is None:
                raise ValueError(f"Decoded Gematria index missing from profile: {decoded_index}")
            parts.append(entry.preferred_latin_label.upper())
            rune_count += 1
            continue
        if kind == "word_separator":
            parts.append(" ")
            separator_count += 1
            continue
        if kind == "clause_separator":
            parts.append(". ")
            separator_count += 1
            continue
        if kind in {"line_separator", "physical_newline"}:
            separator_count += 1
            continue
        if kind in {"paragraph_separator", "segment_separator", "chapter_separator", "page_separator_or_marker", "whitespace"}:
            parts.append(" ")
            separator_count += 1
            continue
        if kind == "numeric_literal":
            parts.append(str(token.get("raw_text", "")))
            numeric_literal_count += 1
            continue
        if kind == "unknown_symbol":
            raw = str(token.get("raw_text", ""))
            parts.append(raw)
            warnings.append(f"Unknown symbol preserved in Atbash-family decode: {raw!r}.")
            continue

    plaintext = normalize_plaintext(parts)
    return {
        "decoded_normalized_plaintext": plaintext,
        "decoded_normalized_plaintext_sha256": sha256_text(plaintext),
        "decoded_index_formula": decoded_index_formula(method_family, params),
        "transform_parameters": params,
        "rune_count": rune_count,
        "numeric_literal_count": numeric_literal_count,
        "separator_count": separator_count,
        "warnings": warnings,
    }
