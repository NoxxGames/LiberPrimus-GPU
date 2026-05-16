"""Parameter-space helpers for Stage 2E dry-run cardinality estimates."""

from __future__ import annotations

from typing import Any


def list_length(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, list):
        return len(value)
    raise ValueError(f"Expected a list parameter, got {type(value).__name__}.")


def inclusive_range_length(value: Any) -> int:
    if not isinstance(value, dict):
        raise ValueError("Range parameter must be a mapping with start/end/step.")
    start = int(value["start"])
    end = int(value["end"])
    step = int(value.get("step", 1))
    if step <= 0:
        raise ValueError("Range step must be positive.")
    if end < start:
        return 0
    return ((end - start) // step) + 1


def list_or_range_count(parameters: dict[str, Any], list_key: str, range_key: str) -> int | None:
    if list_key in parameters:
        return list_length(parameters[list_key])
    if range_key in parameters:
        return inclusive_range_length(parameters[range_key])
    return None


def product(values: list[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result
