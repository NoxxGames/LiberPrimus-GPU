"""No-fudge numeric policy helpers for Stage 4D."""

from __future__ import annotations

from typing import Any

FORBIDDEN_OPERATION_TERMS = (
    "nearest_prime",
    "prime_nearby",
    "plus_minus",
    "plus_n",
    "minus_n",
    "arbitrary_delta",
    "row_addition",
    "column_addition",
    "magic_adjustment",
    "post_hoc",
    "fuzzy",
    "fudge",
)


def validate_no_fudge_operation(operation: str) -> list[str]:
    """Return policy errors for a named numeric operation."""

    normalized = operation.lower().replace("-", "_").replace(" ", "_")
    return [f"forbidden_numeric_operation:{term}" for term in FORBIDDEN_OPERATION_TERMS if term in normalized]


def validate_no_fudge_record(record: dict[str, Any]) -> list[str]:
    """Validate no-fudge fields and derived-value provenance on a generated record."""

    errors: list[str] = []
    if record.get("no_fudge_policy") is not True:
        errors.append(f"{record.get('result_id')}:no_fudge_policy_must_be_true")
    if record.get("solve_claim") is not False:
        errors.append(f"{record.get('result_id')}:solve_claim_must_be_false")
    if record.get("cuda_used") is not False:
        errors.append(f"{record.get('result_id')}:cuda_used_must_be_false")
    if record.get("trusted_as_canonical") is not False:
        errors.append(f"{record.get('result_id')}:trusted_as_canonical_must_be_false")
    for item in record.get("derived_values", []) or []:
        if not isinstance(item, dict):
            errors.append(f"{record.get('result_id')}:derived_value_must_be_mapping")
            continue
        formula = str(item.get("formula") or "")
        source = str(item.get("source") or "")
        if not formula or not source:
            errors.append(f"{record.get('result_id')}:derived_value_missing_formula_or_source")
        errors.extend(validate_no_fudge_operation(formula))
    for operation in record.get("operations", []) or []:
        errors.extend(validate_no_fudge_operation(str(operation)))
    return errors


def enforce_cap(records: list[dict[str, Any]], cap: int, manifest_id: str) -> None:
    """Raise if a generated record list exceeds its manifest cap."""

    if len(records) > cap:
        raise ValueError(f"{manifest_id}:candidate_count_exceeds_cap:{len(records)}>{cap}")
