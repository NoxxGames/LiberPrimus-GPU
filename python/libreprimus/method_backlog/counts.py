"""Deterministic candidate-count calculations for Stage 3E queue items."""

from __future__ import annotations

from typing import Any


def candidate_count_for_item(item: dict[str, Any]) -> int:
    kind = str(item.get("experiment_kind", ""))
    params = _parameters(item)
    if kind == "vigenere_key_pack":
        return len(params.get("keys", [])) * len(params.get("reset_modes", [])) * len(params.get("advance_modes", []))
    if kind == "prime_minus_one_offset_sweep":
        return _count_range(params.get("offsets")) * len(params.get("directions", [])) * len(params.get("reset_modes", []))
    if kind == "family_specific_negative_controls":
        return len(params.get("negative_corpora", [])) * int(params.get("representative_transform_subset_size", 0))
    if kind == "reset_advance_ablation":
        return len(params.get("base_transforms", [])) * len(params.get("reset_modes", [])) * len(params.get("advance_modes", []))
    if kind == "prime_neighbour_streams":
        return (
            len(params.get("families", []))
            * _count_range(params.get("offsets"))
            * len(params.get("directions", []))
            * len(params.get("reset_modes", []))
        )
    if kind == "mersenne_prime_stream_tiny":
        return (
            len(params.get("stream_variants", []))
            * _count_range(params.get("offsets"))
            * len(params.get("directions", []))
            * len(params.get("reset_modes", []))
        )
    families = dict(item.get("transform_plan", {})).get("families", [])
    return sum(int(family.get("candidate_count", 0)) for family in families if isinstance(family, dict))


def validate_candidate_count(item: dict[str, Any]) -> int:
    calculated = candidate_count_for_item(item)
    declared = int(item.get("candidate_count_upper_bound", -1))
    if calculated != declared:
        raise ValueError(f"{item.get('item_id')}: calculated candidate count {calculated} != declared {declared}.")
    return calculated


def _parameters(item: dict[str, Any]) -> dict[str, Any]:
    plan = dict(item.get("transform_plan", {}))
    params = plan.get("parameters", {})
    return dict(params) if isinstance(params, dict) else {}


def _count_range(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        start = int(value.get("start", 0))
        end = int(value.get("end", value.get("stop_inclusive", -1)))
        step = int(value.get("step", 1))
        if step <= 0:
            raise ValueError("Range step must be positive.")
        if end < start:
            return 0
        return ((end - start) // step) + 1
    return 0
