from __future__ import annotations

from libreprimus.bounded_numeric.number_square_routes import (
    build_number_square_route_records,
    route_sequence,
)


def test_stage4d_route_builders_are_deterministic() -> None:
    table = [[1, 2], [3, 4]]

    assert route_sequence(table, "row_major") == [1, 2, 3, 4]
    assert route_sequence(table, "column_major") == [1, 3, 2, 4]
    assert route_sequence(table, "reverse_row_major") == [4, 3, 2, 1]
    assert route_sequence(table, "clockwise_spiral") == [1, 2, 4, 3]


def test_stage4d_number_square_skips_when_raw_values_absent() -> None:
    records = build_number_square_route_records(
        {"manifest_id": "exp_stage4b_onion7_raw_routes_v1", "candidate_count_upper_bound": 96},
        [],
    )

    assert records[0]["status"] == "skipped_missing_raw_values"
    assert records[0]["candidate_count"] == 0
