"""Models for Stage 3S post-Discord Onion 7 seed-pack execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from libreprimus.bounded_execution.models import InputSlice

MODULUS = 29
EXPERIMENT_ID = "EXP-3R-003"
TRANSFORM_FAMILY = "onion7_numeric_seed_pack"
TRANSFORM_ID = "onion7_mod29_stream_subtract"
DEFAULT_MANIFEST = "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml"
DEFAULT_OUTPUT_DIR = "experiments/results/post-discord/stage3s"

RAW_TABLE = [
    [3258, 3222, 3152, 3038],
    [3278, 3299, 3298, 2838],
    [3288, 3294, 3296, 2472],
    [4516, 1206, 708, 1820],
]

# The prime-delta derivation is documented as |3301 - x|. The prime-order table is
# preserved separately because it is a documented derived observation, not source truth.
PRIME_ORDER_TABLE = [
    [13, 21, 34, 55],
    [8, 0, 1, 89],
    [5, 3, 2, 144],
    [987, 610, 377, 233],
]

SUPPORTED_VALUE_SPACES = ("raw_table", "prime_delta_table", "prime_order_table")
SUPPORTED_ROUTES = (
    "row_major",
    "column_major",
    "reverse_row_major",
    "reverse_column_major",
    "clockwise_spiral",
    "counterclockwise_spiral",
)
SUPPORTED_DIRECTIONS = ("forward", "reverse")
SUPPORTED_RESET_MODES = ("none", "line")


@dataclass(frozen=True)
class Onion7Manifest:
    experiment_id: str
    description: str
    candidate_count_cap: int
    payload: dict[str, Any]
    value_spaces: list[str]
    routes: list[str]
    directions: list[str]
    reset_modes: list[str]
    expected_candidate_count: int
    tables: dict[str, list[list[int]]]
    table_sources: dict[str, str]


@dataclass(frozen=True)
class Onion7Input:
    input_slice: InputSlice
    token_records: list[dict[str, Any]]
    transformable_count: int
    has_token_break_metadata: bool
    has_line_metadata: bool
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DeferredOnion7Candidate:
    candidate_index: int
    value_space: str
    route: str
    direction: str
    reset_mode: str
    reason: str
