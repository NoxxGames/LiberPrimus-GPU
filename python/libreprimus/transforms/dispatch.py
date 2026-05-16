"""Dispatch CPU reference transforms by registry transform ID."""

from __future__ import annotations

from typing import Any

from libreprimus.solved_fixtures.atbash_family import decode_atbash_family
from libreprimus.solved_fixtures.direct_translation import decode_direct_translation
from libreprimus.solved_fixtures.prime_stream import decode_prime_minus_one_stream
from libreprimus.solved_fixtures.vigenere import decode_vigenere_explicit_key
from libreprimus.transforms.models import TransformRegistry, TransformResult
from libreprimus.transforms.registry import resolve_transform
from libreprimus.transforms.validation import validate_parameters


FORBIDDEN_TRUE_FLAGS = {"search_enabled", "cuda_enabled", "scoring_enabled"}


def _reject_execution_flags(parameters: dict[str, Any]) -> None:
    for flag in FORBIDDEN_TRUE_FLAGS:
        if parameters.get(flag) is True:
            raise ValueError(f"{flag}=true is not supported by the CPU reference registry.")


def _chain(transform_id: str, parameters: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"name": transform_id, "params": parameters}]


def dispatch_transform(
    *,
    registry: TransformRegistry,
    transform_id: str,
    tokens: list[dict[str, Any]],
    parameters: dict[str, Any] | None = None,
    payload_checks: list[dict[str, Any]] | None = None,
) -> TransformResult:
    if registry.search_enabled or registry.cuda_enabled or registry.scoring_enabled:
        raise ValueError("Unsafe registry flags are enabled.")
    requested = transform_id
    definition = resolve_transform(registry, transform_id)
    canonical_id = definition.transform_id
    params = dict(parameters or {})
    _reject_execution_flags(params)
    validate_parameters(definition.parameter_schema, params)
    if definition.supports_gpu or definition.search_enabled or definition.scoring_enabled:
        raise ValueError(f"Unsafe transform definition flags for {definition.transform_id}.")

    if canonical_id == "direct_translation":
        raw_result = decode_direct_translation(tokens)
        decoded_index_formula = "decoded_index = cipher_index"
        transform_parameters: dict[str, Any] = {}
    elif canonical_id in {"reverse_gematria", "rotated_reverse_gematria"}:
        raw_result = decode_atbash_family(
            tokens,
            method_family=canonical_id,
            transform_chain=_chain(canonical_id, params),
        )
        decoded_index_formula = str(raw_result["decoded_index_formula"])
        transform_parameters = dict(raw_result["transform_parameters"])
    elif canonical_id == "vigenere_explicit_key":
        raw_result = decode_vigenere_explicit_key(
            tokens,
            transform_chain=_chain("vigenere_explicit_key", params),
        )
        decoded_index_formula = str(raw_result["decoded_index_formula"])
        transform_parameters = dict(raw_result["transform_parameters"])
    elif canonical_id == "prime_minus_one_stream":
        raw_result = decode_prime_minus_one_stream(
            tokens,
            transform_chain=_chain("prime_minus_one_stream", params),
            payload_checks=payload_checks or [],
        )
        decoded_index_formula = str(raw_result["decoded_index_formula"])
        transform_parameters = dict(raw_result["transform_parameters"])
    else:
        raise ValueError(f"Unsupported registry transform: {canonical_id}")

    return TransformResult(
        transform_id=requested,
        canonical_transform_id=canonical_id,
        transform_version=definition.transform_version,
        parameters=transform_parameters,
        decoded_index_formula=decoded_index_formula,
        decoded_normalized_plaintext=raw_result["decoded_normalized_plaintext"],
        decoded_normalized_plaintext_sha256=raw_result["decoded_normalized_plaintext_sha256"],
        rune_count=int(raw_result["rune_count"]),
        numeric_literal_count=int(raw_result["numeric_literal_count"]),
        separator_count=int(raw_result["separator_count"]),
        warnings=[str(item) for item in raw_result["warnings"]],
        search_performed=False,
        cuda_used=False,
        scoring_used=False,
        key_text=raw_result.get("key_text") if isinstance(raw_result.get("key_text"), str) else None,
        key_indices=[int(item) for item in raw_result.get("key_indices", [])],
        skip_rule_applied_count=int(raw_result.get("skip_rule_applied_count", 0)),
        prime_values_used_count=int(raw_result.get("prime_values_used_count", 0)),
        stream_values_used_count=int(raw_result.get("stream_values_used_count", 0)),
        first_prime_values=[int(item) for item in raw_result.get("first_prime_values", [])],
        first_stream_values_mod29=[int(item) for item in raw_result.get("first_stream_values_mod29", [])],
        payload_check_results=[
            dict(item) for item in raw_result.get("payload_check_results", []) if isinstance(item, dict)
        ],
    )
