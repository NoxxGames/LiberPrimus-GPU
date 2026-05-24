"""Stage 5AK arithmetic-preflight helpers for explicit community facts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_yaml, write_json, write_records
from .models import (
    STAGE5AK_ARITHMETIC_PREFLIGHT_PATH,
    STAGE5AK_ID,
    STAGE5AK_OUTPUT_DIR,
    STAGE5AK_REPORTS,
    STAGE5AK_SOURCE_STAGE_ID,
)


def build_community_arithmetic_preflight(
    *,
    claim_records_path: Path,
    correction_log_path: Path,
    out: Path = STAGE5AK_ARITHMETIC_PREFLIGHT_PATH,
    results_dir: Path = STAGE5AK_OUTPUT_DIR,
) -> dict[str, Any]:
    """Verify only explicit arithmetic claims; do not scan or search."""

    claims = read_yaml(claim_records_path)
    corrections = read_yaml(correction_log_path)
    records = _preflight_records()
    claim_ids = {record["claim_family"]: record["claim_id"] for record in claims.get("records", [])}
    for record in records:
        record["related_claim_id"] = claim_ids.get(record["claim_family"])
    correction_ids = {record["correction_id"] for record in corrections.get("records", [])}
    for record in records:
        if record["check_id"] == "stage5ak-check-13136-plus-256":
            record["related_correction_id"] = "stage5ak-correction-13136-plus-256"
            record["correction_record_present"] = record["related_correction_id"] in correction_ids
    summary = {
        "record_type": "stage5ak_community_facts_arithmetic_preflight",
        "schema": "schemas/source-harvester/community-facts-arithmetic-preflight-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "arithmetic_preflight_records": len(records),
        "arithmetic_verified_count": sum(1 for record in records if record["verification_status"] == "arithmetic_verified_only"),
        "arithmetic_error_count": sum(1 for record in records if record["verification_status"] == "arithmetic_error"),
        "source_material_unverified_count": sum(1 for record in records if record["source_material_status"] != "not_required"),
        "scan_or_search_performed": False,
        "hypothesis_execution_performed": False,
        "execution_ready": False,
        "solve_claim": False,
    }
    write_records(out, records, **summary)
    write_json(results_dir / STAGE5AK_REPORTS["arithmetic_preflight"], {**summary, "records": records})
    return {**summary, "records": records}


def is_prime(value: int) -> bool:
    """Return a deterministic Miller-Rabin result for positive integers used here."""

    if value < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if value in small_primes:
        return True
    if any(value % prime == 0 for prime in small_primes):
        return False
    d = value - 1
    shifts = 0
    while d % 2 == 0:
        shifts += 1
        d //= 2
    # Fixed bases are deterministic for this code path and cover the explicit
    # small/medium claims used by the Stage 5AK records.
    for base in small_primes:
        witness = pow(base, d, value)
        if witness in {1, value - 1}:
            continue
        for _ in range(shifts - 1):
            witness = pow(witness, 2, value)
            if witness == value - 1:
                break
        else:
            return False
    return True


def nth_prime(index: int) -> int:
    """Return the one-based nth prime for the explicit small indexes used here."""

    if index < 1:
        raise ValueError("prime index must be one-based")
    count = 0
    candidate = 1
    while count < index:
        candidate += 1
        if is_prime(candidate):
            count += 1
    return candidate


def prime_index(value: int) -> int | None:
    """Return the one-based prime index of value if value is prime."""

    if not is_prime(value):
        return None
    count = 0
    candidate = 1
    while candidate < value:
        candidate += 1
        if is_prime(candidate):
            count += 1
    return count


def euler_phi(value: int) -> int:
    """Return Euler phi for explicit small values."""

    result = value
    n = value
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            while n % factor == 0:
                n //= factor
            result -= result // factor
        factor += 1
    if n > 1:
        result -= result // n
    return result


def base_digits(value: int, base: int) -> list[int]:
    """Return most-significant-first digits for an integer base."""

    if value == 0:
        return [0]
    digits = []
    current = value
    while current:
        digits.append(current % base)
        current //= base
    return list(reversed(digits))


def _preflight_records() -> list[dict[str, Any]]:
    checks = [
        _check("stage5ak-check-prime-463", "red_3299_fehu_count_prime_index", "prime_index(463)", 90, prime_index(463)),
        _check("stage5ak-check-463rd-prime", "red_3299_fehu_count_prime_index", "nth_prime(463)", 3299, nth_prime(463)),
        _check("stage5ak-check-269-prime-index", "p56_p57_fehu_boundary_prime_observations", "prime_index(269)", 57, prime_index(269)),
        _check("stage5ak-check-277-prime-index", "p56_p57_fehu_boundary_prime_observations", "prime_index(277)", 59, prime_index(277)),
        _check("stage5ak-check-1033-prime-index", "cicada_prime_index_number_network", "prime_index(1033)", 174, prime_index(1033)),
        _check("stage5ak-check-761-prime-index", "cicada_prime_index_number_network", "prime_index(761)", 135, prime_index(761)),
        _check("stage5ak-check-167-prime-index", "cicada_prime_index_number_network", "prime_index(167)", 39, prime_index(167)),
        _check("stage5ak-check-761-plus-167", "cicada_prime_index_number_network", "761 + 167", 928, 761 + 167),
        _check("stage5ak-check-928-half", "cicada_prime_index_number_network", "928 / 2", 464, 928 // 2),
        _check("stage5ak-check-133-plus-331", "cicada_prime_index_number_network", "133 + 331", 464, 133 + 331),
        _check("stage5ak-check-13136-plus-256", "count_policy_correction_log", "13136 + 256", 13397, 13136 + 256),
        _check(
            "stage5ak-check-whitespace-prime",
            "whitespace_prime_sequence_claim",
            "is_prime(23571113172329313753257)",
            True,
            is_prime(23571113172329313753257),
            source_material_status="source_lock_required",
        ),
        _check("stage5ak-check-3301-base60", "base60_emirp_index_observations", "base_digits(3301, 60)", [55, 1], base_digits(3301, 60)),
        _check("stage5ak-check-reversed-base60", "base60_emirp_index_observations", "1 * 60 + 55", 115, 1 * 60 + 55),
        _check("stage5ak-check-449-plus-311", "artwork_red_header_gp_match", "449 + 311", 760, 449 + 311, source_material_status="label_policy_unverified"),
        _check("stage5ak-check-phi-761", "artwork_red_header_gp_match", "euler_phi(761)", 760, euler_phi(761), source_material_status="label_policy_unverified"),
    ]
    return checks


def _check(
    check_id: str,
    claim_family: str,
    expression: str,
    expected: Any,
    computed: Any,
    *,
    source_material_status: str = "not_required",
) -> dict[str, Any]:
    status = "arithmetic_verified_only" if expected == computed else "arithmetic_error"
    return {
        "record_type": "stage5ak_community_facts_arithmetic_preflight_record",
        "schema": "schemas/source-harvester/community-facts-arithmetic-preflight-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "check_id": check_id,
        "claim_family": claim_family,
        "expression": expression,
        "expected_value": expected,
        "computed_value": computed,
        "verification_status": status,
        "verification_method": "deterministic_explicit_arithmetic_only",
        "source_material_status": source_material_status,
        "scan_or_search_performed": False,
        "hypothesis_execution_performed": False,
        "execution_ready": False,
        "solve_claim": False,
    }
