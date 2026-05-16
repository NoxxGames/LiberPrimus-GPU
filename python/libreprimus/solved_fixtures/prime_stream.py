"""CPU-only prime-minus-one / phi-prime fixture decoder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import GematriaProfile, load_gematria_profile
from libreprimus.solved_fixtures.direct_translation import normalize_plaintext, sha256_text

DEFAULT_GEMATRIA_PROFILE = Path("data/profiles/gematria/gematria-primus-v0.json")


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def first_n_primes(count: int) -> list[int]:
    if count < 0:
        raise ValueError("Prime count must be non-negative.")
    primes: list[int] = []
    candidate = 2
    while len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes


def phi_prime_value(prime: int) -> int:
    if not is_prime(prime):
        raise ValueError(f"phi_prime_value requires a prime input: {prime}")
    return prime - 1


def prime_minus_one_stream(count: int, *, prime_start_index: int = 0) -> list[int]:
    if prime_start_index < 0:
        raise ValueError("prime_start_index must be non-negative.")
    return [prime - 1 for prime in first_n_primes(count + prime_start_index)[prime_start_index:]]


def phi_prime_stream(count: int, *, prime_start_index: int = 0) -> list[int]:
    return [phi_prime_value(prime) for prime in first_n_primes(count + prime_start_index)[prime_start_index:]]


def transform_chain_parameters(transform_chain: list[Any]) -> dict[str, Any]:
    for item in transform_chain:
        if isinstance(item, dict) and item.get("name") in {"prime_minus_one_stream", "phi_prime_stream"}:
            params = item.get("params", {})
            return dict(params) if isinstance(params, dict) else {}
    return {}


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


def _payload_line_ranges(payload_checks: list[dict[str, Any]]) -> set[int]:
    lines: set[int] = set()
    for check in payload_checks:
        selector = check.get("payload_selector", {})
        if not isinstance(selector, dict):
            continue
        start = selector.get("start_logical_line_index")
        end = selector.get("end_logical_line_index")
        if isinstance(start, int) and isinstance(end, int):
            lines.update(range(start, end + 1))
    return lines


def _extract_payload_text(tokens: list[dict[str, Any]], line_numbers: set[int]) -> str:
    grouped: dict[int, list[str]] = {}
    for token in tokens:
        line = token.get("logical_line_index")
        if not isinstance(line, int) or line not in line_numbers:
            continue
        kind = str(token.get("token_kind"))
        if kind in {"numeric_literal", "unknown_symbol", "hex_literal_candidate"}:
            grouped.setdefault(line, []).append(str(token.get("raw_text", "")))
    lines = ["".join(parts) for _, parts in sorted(grouped.items()) if "".join(parts)]
    return "\n".join(lines)


def evaluate_payload_checks(tokens: list[dict[str, Any]], payload_checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for check in payload_checks:
        line_numbers = _payload_line_ranges([check])
        actual = _extract_payload_text(tokens, line_numbers)
        expected = check.get("expected_payload_text")
        expected_sha = check.get("expected_payload_sha256")
        actual_sha = sha256_text(actual) if actual else None
        if not line_numbers:
            status = "pending"
            warnings = ["Payload selector has no logical-line range."]
        elif not actual:
            status = "pending"
            warnings = ["Payload text could not be extracted from selected tokens."]
        elif isinstance(expected_sha, str) and actual_sha == expected_sha:
            status = "pass"
            warnings = []
        else:
            status = "fail"
            warnings = ["Payload SHA-256 did not match fixture expectation."]
        results.append(
            {
                "payload_id": str(check.get("payload_id", "")),
                "payload_kind": str(check.get("payload_kind", "")),
                "expected_sha256": expected_sha,
                "actual_sha256": actual_sha,
                "match_status": status,
                "payload_length": len(actual),
                "preservation_policy": str(check.get("preservation_policy", "")),
                "warnings": warnings,
                "expected_payload_present": isinstance(expected, str) and bool(expected),
            }
        )
    return results


def decode_prime_minus_one_stream(
    tokens: list[dict[str, Any]],
    *,
    transform_chain: list[Any],
    payload_checks: list[dict[str, Any]] | None = None,
    gematria_profile: GematriaProfile | None = None,
) -> dict[str, Any]:
    """Decode selected tokens with the declared prime-minus-one stream over Z_29."""
    profile = gematria_profile or load_gematria_profile(repo_root() / DEFAULT_GEMATRIA_PROFILE)
    index_to_entry = profile.index_to_entry
    params = transform_chain_parameters(transform_chain)
    if "prime_start_index" not in params:
        raise ValueError("prime_minus_one_stream requires params.prime_start_index.")
    prime_start_index = params["prime_start_index"]
    if not isinstance(prime_start_index, int) or prime_start_index < 0:
        raise ValueError("prime_minus_one_stream requires non-negative integer params.prime_start_index.")
    if params.get("direction") != "forward":
        raise ValueError("prime_minus_one_stream supports direction='forward' only.")
    if params.get("stream_value") != "prime_minus_one_mod29":
        raise ValueError("prime_minus_one_stream requires stream_value='prime_minus_one_mod29'.")

    checks = payload_checks or []
    payload_lines = _payload_line_ranges(checks)
    payload_check_results = evaluate_payload_checks(tokens, checks)
    rule = _skip_rule(params)

    parts: list[str] = []
    warnings: list[str] = []
    rune_count = 0
    numeric_literal_count = 0
    separator_count = 0
    stream_position = 0
    skip_rule_applied_count = 0
    prime_values: list[int] = []
    stream_values: list[int] = []
    max_stream_tokens = sum(
        1
        for token in tokens
        if token.get("token_kind") == "rune"
        and not (isinstance(token.get("logical_line_index"), int) and token["logical_line_index"] in payload_lines)
    )
    prime_cache = first_n_primes(prime_start_index + max_stream_tokens)

    for token in tokens:
        line = token.get("logical_line_index")
        if isinstance(line, int) and line in payload_lines:
            continue
        kind = str(token.get("token_kind"))
        if kind == "rune":
            raw_index = token.get("index29")
            if not isinstance(raw_index, int) or raw_index < 0 or raw_index > 28:
                raise ValueError(f"Rune token missing valid index29 at token {token.get('token_index_global')}.")
            if _should_skip(token, rule):
                decoded_index = raw_index
                skip_rule_applied_count += 1
            else:
                prime = prime_cache[prime_start_index + stream_position]
                stream_value = (prime - 1) % 29
                prime_values.append(prime)
                stream_values.append(stream_value)
                decoded_index = (raw_index - stream_value) % 29
                stream_position += 1
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
            warnings.append(f"Unknown symbol preserved in prime-stream decode: {raw!r}.")
            continue

    for result in payload_check_results:
        warnings.extend(str(warning) for warning in result.get("warnings", []))
    plaintext = normalize_plaintext(parts)
    return {
        "decoded_normalized_plaintext": plaintext,
        "decoded_normalized_plaintext_sha256": sha256_text(plaintext),
        "decoded_index_formula": "decoded_index = (cipher_index - ((prime_i - 1) mod 29)) mod 29",
        "transform_parameters": params,
        "skip_rule_applied_count": skip_rule_applied_count,
        "prime_values_used_count": len(prime_values),
        "stream_values_used_count": len(stream_values),
        "first_prime_values": prime_values[:20],
        "first_stream_values_mod29": stream_values[:20],
        "payload_check_results": payload_check_results,
        "rune_count": rune_count,
        "numeric_literal_count": numeric_literal_count,
        "separator_count": separator_count,
        "warnings": warnings,
    }
