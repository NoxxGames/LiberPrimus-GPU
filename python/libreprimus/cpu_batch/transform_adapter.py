"""Transform adapters for the CPU batch API."""

from __future__ import annotations

import hashlib
from typing import Any

from libreprimus.bounded_execution.caesar_affine import affine_inverse, labels_by_index
from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.cpu_batch.models import AdapterResult, SUPPORTED_LOCAL_TRANSFORMS, SUPPORTED_REGISTRY_TRANSFORMS
from libreprimus.solved_fixtures.direct_translation import normalize_plaintext
from libreprimus.transforms.dispatch import dispatch_transform
from libreprimus.transforms.models import TransformRegistry


def adapter_status(transform_id: str) -> str:
    """Return the explicit adapter status for one transform ID."""

    if transform_id in SUPPORTED_REGISTRY_TRANSFORMS or transform_id in SUPPORTED_LOCAL_TRANSFORMS:
        return "supported"
    return "adapter_missing"


def apply_transform(
    *,
    registry: TransformRegistry,
    stream: dict[str, Any],
    candidate: dict[str, Any],
) -> AdapterResult:
    """Apply one supported CPU transform or return an adapter-missing record."""

    transform_id = str(candidate["transform_id"])
    parameters = dict(candidate.get("transform_parameters", {}))
    tokens = [dict(item) for item in stream.get("tokens", [])]
    if transform_id in SUPPORTED_REGISTRY_TRANSFORMS:
        result = dispatch_transform(
            registry=registry,
            transform_id=transform_id,
            tokens=tokens,
            parameters=parameters,
            payload_checks=[dict(item) for item in candidate.get("payload_checks", [])],
        )
        output_text = result.decoded_normalized_plaintext
        output_text_hash = result.decoded_normalized_plaintext_sha256
        output_token_hash = stable_json_sha256(
            {
                "canonical_transform_id": result.canonical_transform_id,
                "parameters": result.parameters,
                "output_text_hash": output_text_hash,
            }
        )
        return AdapterResult(
            status="executed",
            canonical_transform_id=result.canonical_transform_id,
            output_text=output_text,
            output_text_hash=output_text_hash,
            output_token_hash=output_token_hash,
            transform_parameters=result.parameters,
            warnings=list(result.warnings),
        )
    if transform_id in SUPPORTED_LOCAL_TRANSFORMS:
        return _apply_local_transform(transform_id, tokens, parameters)
    output_token_hash = hashlib.sha256(f"adapter_missing:{transform_id}".encode("utf-8")).hexdigest()
    return AdapterResult(
        status="adapter_missing",
        canonical_transform_id=None,
        output_text=None,
        output_text_hash=None,
        output_token_hash=output_token_hash,
        transform_parameters=parameters,
        warnings=[f"CPU batch adapter missing for transform_id={transform_id}."],
    )


def _apply_local_transform(transform_id: str, tokens: list[dict[str, Any]], parameters: dict[str, Any]) -> AdapterResult:
    labels = labels_by_index()
    parts: list[str] = []
    output_indices: list[int] = []
    warnings: list[str] = []
    for token in tokens:
        kind = str(token.get("token_kind"))
        if kind == "rune":
            raw_index = token.get("index29")
            if not isinstance(raw_index, int) or raw_index < 0 or raw_index > 28:
                raise ValueError(f"Rune token missing valid index29 at token {token.get('token_index_global')}.")
            decoded_index = _decode_local_index(transform_id, raw_index, parameters)
            output_indices.append(decoded_index)
            parts.append(labels[decoded_index].upper())
            continue
        if kind == "word_separator":
            parts.append(" ")
            continue
        if kind == "clause_separator":
            parts.append(". ")
            continue
        if kind in {"paragraph_separator", "segment_separator", "chapter_separator", "page_separator_or_marker", "whitespace"}:
            parts.append(" ")
            continue
        if kind == "numeric_literal":
            parts.append(str(token.get("raw_text", "")))
            continue
        if kind == "unknown_symbol":
            raw = str(token.get("raw_text", ""))
            parts.append(raw)
            warnings.append(f"Unknown symbol preserved in {transform_id}: {raw!r}.")
    output_text = normalize_plaintext(parts)
    output_text_hash = hashlib.sha256(output_text.encode("utf-8")).hexdigest()
    output_token_hash = stable_json_sha256({"output_indices": output_indices, "parameters": parameters, "transform_id": transform_id})
    return AdapterResult(
        status="executed",
        canonical_transform_id=transform_id,
        output_text=output_text,
        output_text_hash=output_text_hash,
        output_token_hash=output_token_hash,
        transform_parameters=dict(parameters),
        warnings=warnings,
    )


def _decode_local_index(transform_id: str, value: int, parameters: dict[str, Any]) -> int:
    if transform_id == "caesar_shift":
        shift = int(parameters.get("shift", 0))
        direction = str(parameters.get("direction", "forward"))
        if direction == "reverse":
            return (value - shift) % 29
        return (value + shift) % 29
    if transform_id == "affine_mod29":
        a_value = int(parameters["a"])
        b_value = int(parameters["b"])
        direction = str(parameters.get("direction", "forward"))
        if direction == "reverse":
            inverse = affine_inverse(a_value)
            return (inverse * (value - b_value)) % 29
        return (a_value * value + b_value) % 29
    raise ValueError(f"Unsupported local transform adapter: {transform_id}")
