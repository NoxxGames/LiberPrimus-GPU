from __future__ import annotations

from libreprimus.post_discord.models import RAW_TABLE
from libreprimus.post_discord.onion7_seed_pack import reduce_mod29, route_sequence


def test_onion7_row_and_column_routes_are_deterministic() -> None:
    assert route_sequence(RAW_TABLE, "row_major")[:6] == [3258, 3222, 3152, 3038, 3278, 3299]
    assert route_sequence(RAW_TABLE, "column_major")[:6] == [3258, 3278, 3288, 4516, 3222, 3299]


def test_onion7_reverse_routes_are_deterministic() -> None:
    assert route_sequence(RAW_TABLE, "reverse_row_major")[:4] == [1820, 708, 1206, 4516]
    assert route_sequence(RAW_TABLE, "reverse_column_major")[:4] == [1820, 2472, 2838, 3038]


def test_onion7_spiral_routes_are_deterministic() -> None:
    assert route_sequence(RAW_TABLE, "clockwise_spiral") == [
        3258,
        3222,
        3152,
        3038,
        2838,
        2472,
        1820,
        708,
        1206,
        4516,
        3288,
        3278,
        3299,
        3298,
        3296,
        3294,
    ]
    assert route_sequence(RAW_TABLE, "counterclockwise_spiral") == [
        3258,
        3278,
        3288,
        4516,
        1206,
        708,
        1820,
        2472,
        2838,
        3038,
        3152,
        3222,
        3299,
        3294,
        3296,
        3298,
    ]


def test_onion7_mod29_reduction_is_deterministic() -> None:
    assert reduce_mod29([3258, 3222, 29, 30, 0]) == [10, 3, 0, 1, 0]
