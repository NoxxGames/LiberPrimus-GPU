"""No-fudge raw number-square route verification for Stage 4D."""

from __future__ import annotations

from typing import Any

from libreprimus.bounded_numeric.manifest_loader import cap_for
from libreprimus.bounded_numeric.models import FIXED_ROUTES
from libreprimus.bounded_numeric.no_fudge_policy import enforce_cap


def extract_raw_number_square_tables(visual_records: list[dict[str, Any]]) -> list[list[list[int]]]:
    """Extract locked raw number-square tables from Stage 4B observations if present."""

    tables: list[list[list[int]]] = []
    for record in visual_records:
        if record.get("observation_family") != "number_square_raw":
            continue
        for reading in record.get("candidate_readings", []) or []:
            if not isinstance(reading, dict):
                continue
            value = reading.get("value")
            if _is_table(value):
                tables.append([[int(cell) for cell in row] for row in value])
    return tables


def build_number_square_route_records(manifest: dict[str, Any], tables: list[list[list[int]]]) -> list[dict[str, Any]]:
    """Build fixed route records, or a missing-raw skip record."""

    manifest_id = str(manifest.get("manifest_id"))
    cap = cap_for(manifest)
    if not tables:
        return [
            _result(
                result_id=f"{manifest_id}-skipped-missing-raw-values",
                manifest_id=manifest_id,
                status="skipped_missing_raw_values",
                cap=cap,
                raw_values=None,
                derived_values=[],
                notes="Raw number-square values remain pending source-lock; no route candidates executed.",
            )
        ]

    records: list[dict[str, Any]] = []
    for table_index, table in enumerate(tables, start=1):
        for route in FIXED_ROUTES:
            sequence = route_sequence(table, route)
            records.append(
                _result(
                    result_id=f"{manifest_id}-table{table_index}-{route}",
                    manifest_id=manifest_id,
                    status="executed_no_fudge_route",
                    cap=cap,
                    raw_values={"table_index": table_index, "table": table, "route": route},
                    derived_values=[
                        {
                            "name": "route_sequence",
                            "formula": f"fixed_route:{route}",
                            "source": "raw_number_square_table",
                            "value": sequence,
                        },
                        {
                            "name": "route_sequence_mod29",
                            "formula": "value % 29",
                            "source": "route_sequence",
                            "value": [value % 29 for value in sequence],
                        },
                    ],
                    candidate_count=1,
                    notes="Fixed no-fudge route only; no nearest-prime, +/-n, or post-hoc adjustment.",
                )
            )
    enforce_cap(records, cap, manifest_id)
    return records


def route_sequence(table: list[list[int]], route: str) -> list[int]:
    """Return a deterministic route sequence over a rectangular table."""

    _validate_table(table)
    rows = len(table)
    columns = len(table[0])
    if route == "row_major":
        return [value for row in table for value in row]
    if route == "column_major":
        return [table[row][column] for column in range(columns) for row in range(rows)]
    if route == "reverse_row_major":
        return list(reversed(route_sequence(table, "row_major")))
    if route == "reverse_column_major":
        return list(reversed(route_sequence(table, "column_major")))
    if route == "clockwise_spiral":
        return _spiral(table, clockwise=True)
    if route == "counterclockwise_spiral":
        return _spiral(table, clockwise=False)
    raise ValueError(f"unsupported_route:{route}")


def _spiral(table: list[list[int]], *, clockwise: bool) -> list[int]:
    top = 0
    left = 0
    bottom = len(table) - 1
    right = len(table[0]) - 1
    values: list[int] = []
    while top <= bottom and left <= right:
        if clockwise:
            values.extend(table[top][column] for column in range(left, right + 1))
            values.extend(table[row][right] for row in range(top + 1, bottom + 1))
            if top < bottom:
                values.extend(table[bottom][column] for column in range(right - 1, left - 1, -1))
            if left < right:
                values.extend(table[row][left] for row in range(bottom - 1, top, -1))
        else:
            values.extend(table[row][left] for row in range(top, bottom + 1))
            values.extend(table[bottom][column] for column in range(left + 1, right + 1))
            if left < right:
                values.extend(table[row][right] for row in range(bottom - 1, top - 1, -1))
            if top < bottom:
                values.extend(table[top][column] for column in range(right - 1, left, -1))
        top += 1
        left += 1
        bottom -= 1
        right -= 1
    return values


def _is_table(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(row, list) and row for row in value)
        and all(isinstance(cell, int) for row in value for cell in row)
    )


def _validate_table(table: list[list[int]]) -> None:
    if not table or not table[0]:
        raise ValueError("number_square_table_empty")
    width = len(table[0])
    if any(len(row) != width for row in table):
        raise ValueError("number_square_table_not_rectangular")


def _result(
    *,
    result_id: str,
    manifest_id: str,
    status: str,
    cap: int,
    raw_values: Any,
    derived_values: list[dict[str, Any]],
    candidate_count: int = 0,
    notes: str,
) -> dict[str, Any]:
    return {
        "record_type": "bounded_numeric_result_record",
        "result_id": result_id,
        "execution_manifest_id": manifest_id,
        "audit_type": "number_square_raw_routes",
        "status": status,
        "candidate_count": candidate_count,
        "cap": cap,
        "raw_values": raw_values,
        "derived_values": derived_values,
        "no_fudge_policy": True,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
        "generated_outputs_committed": False,
        "notes": notes,
    }
