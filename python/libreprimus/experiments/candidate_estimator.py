"""Candidate-count estimators for Stage 2E dry-run planning.

These estimators only count declared search spaces. They never enumerate candidate
plaintexts, apply transforms, score outputs, or use CUDA.
"""

from __future__ import annotations

from typing import Any

from libreprimus.experiments.models import CandidateEstimate
from libreprimus.experiments.parameter_space import list_or_range_count, product


def estimate_candidate_count(manifest_payload: dict[str, Any]) -> CandidateEstimate:
    transform_plan = manifest_payload["transform_plan"]
    parameter_space = manifest_payload.get("parameter_space", {})
    family = str(transform_plan["transform_family"])

    if family in {"direct_translation", "reverse_gematria"}:
        return CandidateEstimate(family, 1, "1", {})
    if family == "rotated_reverse_gematria":
        count = list_or_range_count(parameter_space, "rotations", "rotation_range")
        if count is None:
            raise ValueError("rotated_reverse_gematria requires rotations or rotation_range.")
        return CandidateEstimate(family, count, "len(rotations)", {"rotation_count": count})
    if family == "caesar_shift_preview":
        count = list_or_range_count(parameter_space, "shifts", "shift_range") or 29
        return CandidateEstimate(family, count, "len(shifts) or 29", {"shift_count": count})
    if family == "affine_mod29_preview":
        a_count = list_or_range_count(parameter_space, "a_values", "a_range") or 28
        b_count = list_or_range_count(parameter_space, "b_values", "b_range") or 29
        count = a_count * b_count
        return CandidateEstimate(
            family,
            count,
            "valid_a_count * b_count over Z_29",
            {"a_count": a_count, "b_count": b_count},
        )
    if family == "vigenere_key_list_preview":
        keys = parameter_space.get("keys")
        if not isinstance(keys, list):
            raise ValueError("vigenere_key_list_preview requires an explicit keys list.")
        return CandidateEstimate(family, len(keys), "len(keys)", {"key_count": len(keys)})
    if family == "prime_stream_parameter_preview":
        list_lengths = [
            len(value)
            for value in parameter_space.values()
            if isinstance(value, list)
        ]
        if not list_lengths:
            raise ValueError("prime_stream_parameter_preview requires explicit parameter lists.")
        return CandidateEstimate(
            family,
            product(list_lengths),
            "product(explicit parameter list lengths)",
            {"parameter_list_lengths": list_lengths},
        )
    if family in {"vigenere_explicit_key", "prime_minus_one_stream"}:
        list_lengths = [len(value) for value in parameter_space.values() if isinstance(value, list)]
        count = product(list_lengths) if list_lengths else 1
        return CandidateEstimate(
            family,
            count,
            "product(declared parameter sets) or 1",
            {"parameter_list_lengths": list_lengths},
        )
    raise ValueError(f"Unsupported dry-run transform family: {family}")
