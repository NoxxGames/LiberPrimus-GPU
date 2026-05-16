"""CPU-only explicit-key Vigenere fixture decoder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import GematriaProfile, load_gematria_profile
from libreprimus.solved_fixtures.direct_translation import normalize_plaintext, sha256_text

DEFAULT_GEMATRIA_PROFILE = Path("data/profiles/gematria/gematria-primus-v0.json")


def transform_chain_parameters(transform_chain: list[Any]) -> dict[str, Any]:
    """Return explicitly declared parameters for the Vigenere transform."""
    for item in transform_chain:
        if isinstance(item, dict) and item.get("name") == "vigenere_explicit_key":
            params = item.get("params", {})
            return dict(params) if isinstance(params, dict) else {}
    return {}


def label_to_index_map(profile: GematriaProfile) -> dict[str, int]:
    labels: dict[str, int] = {}
    for entry in profile.entries:
        labels[entry.preferred_latin_label.upper()] = entry.index
        for label in entry.latin_labels:
            labels[label.upper()] = entry.index
    return labels


def key_text_to_indices(key_text: str, profile: GematriaProfile) -> list[int]:
    """Convert explicit fixture key text through Gematria profile Latin labels."""
    labels = label_to_index_map(profile)
    ordered_labels = sorted(labels, key=len, reverse=True)
    key = key_text.upper()
    indices: list[int] = []
    position = 0
    while position < len(key):
        char = key[position]
        if char.isspace() or char in {"-", "_"}:
            position += 1
            continue
        matched_label = None
        for label in ordered_labels:
            if key.startswith(label, position):
                matched_label = label
                break
        if matched_label is None:
            raise ValueError(f"Vigenere key contains text outside Gematria profile labels at offset {position}.")
        indices.append(labels[matched_label])
        position += len(matched_label)
    if not indices:
        raise ValueError("Vigenere explicit key must contain at least one Gematria label.")
    return indices


def _skip_rule(params: dict[str, Any]) -> dict[str, Any]:
    rule = params.get("skip_rule", {})
    return dict(rule) if isinstance(rule, dict) else {}


def _skip_indices(rule: dict[str, Any]) -> set[int]:
    values = rule.get("cleartext_pass_through_rune_indices", [])
    return {int(value) for value in values if isinstance(value, int)}


def _skip_token_indices(rule: dict[str, Any]) -> set[int] | None:
    if "cleartext_pass_through_token_indices" not in rule:
        return None
    values = rule.get("cleartext_pass_through_token_indices", [])
    return {int(value) for value in values if isinstance(value, int)}


def _should_skip(token: dict[str, Any], rule: dict[str, Any]) -> bool:
    raw_index = token.get("index29")
    token_index = token.get("token_index_global")
    if not isinstance(raw_index, int) or raw_index not in _skip_indices(rule):
        return False
    explicit_tokens = _skip_token_indices(rule)
    if explicit_tokens is not None:
        return isinstance(token_index, int) and token_index in explicit_tokens
    return True


def decode_vigenere_explicit_key(
    tokens: list[dict[str, Any]],
    *,
    transform_chain: list[Any],
    gematria_profile: GematriaProfile | None = None,
) -> dict[str, Any]:
    """Decode selected tokens with declared-key Vigenere over Z_29."""
    profile = gematria_profile or load_gematria_profile(repo_root() / DEFAULT_GEMATRIA_PROFILE)
    params = transform_chain_parameters(transform_chain)
    key_text = params.get("key_text")
    if not isinstance(key_text, str) or not key_text:
        raise ValueError("vigenere_explicit_key requires params.key_text.")
    direction = params.get("direction")
    if direction != "decrypt_subtract":
        raise ValueError("vigenere_explicit_key supports direction='decrypt_subtract' only.")
    key_indices = key_text_to_indices(key_text, profile)
    index_to_entry = profile.index_to_entry
    rule = _skip_rule(params)

    parts: list[str] = []
    warnings: list[str] = []
    rune_count = 0
    numeric_literal_count = 0
    separator_count = 0
    key_position = 0
    skip_rule_applied_count = 0

    for token in tokens:
        kind = str(token.get("token_kind"))
        if kind == "rune":
            raw_index = token.get("index29")
            if not isinstance(raw_index, int) or raw_index < 0 or raw_index > 28:
                raise ValueError(f"Rune token missing valid index29 at token {token.get('token_index_global')}.")
            if _should_skip(token, rule):
                decoded_index = raw_index
                skip_rule_applied_count += 1
            else:
                key_index = key_indices[key_position % len(key_indices)]
                decoded_index = (raw_index - key_index) % 29
                key_position += 1
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
            warnings.append(f"Unknown symbol preserved in Vigenere decode: {raw!r}.")
            continue

    plaintext = normalize_plaintext(parts)
    return {
        "decoded_normalized_plaintext": plaintext,
        "decoded_normalized_plaintext_sha256": sha256_text(plaintext),
        "decoded_index_formula": "decoded_index = (cipher_index - key_index[key_position]) mod 29",
        "transform_parameters": params,
        "key_text": key_text,
        "key_indices": key_indices,
        "skip_rule_applied_count": skip_rule_applied_count,
        "rune_count": rune_count,
        "numeric_literal_count": numeric_literal_count,
        "separator_count": separator_count,
        "warnings": warnings,
    }
