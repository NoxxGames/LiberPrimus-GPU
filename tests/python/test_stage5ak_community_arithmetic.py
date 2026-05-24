from __future__ import annotations

from pathlib import Path

from libreprimus.source_harvester.community_arithmetic import (
    build_community_arithmetic_preflight,
    is_prime,
    prime_index,
)
from libreprimus.source_harvester.community_claims import build_community_claim_records


def test_stage5ak_arithmetic_preflight_records_explicit_error_only(tmp_path: Path) -> None:
    build_community_claim_records(
        source_root=tmp_path / "community-facts",
        claim_policy_out=tmp_path / "policy.yaml",
        claim_records_out=tmp_path / "claims.yaml",
        correction_log_out=tmp_path / "corrections.yaml",
        clue_categories_out=tmp_path / "categories.yaml",
        results_dir=tmp_path / "claim-results",
    )

    result = build_community_arithmetic_preflight(
        claim_records_path=tmp_path / "claims.yaml",
        correction_log_path=tmp_path / "corrections.yaml",
        out=tmp_path / "arithmetic.yaml",
        results_dir=tmp_path / "results",
    )

    assert result["arithmetic_preflight_records"] == 16
    assert result["arithmetic_verified_count"] == 15
    assert result["arithmetic_error_count"] == 1
    assert result["scan_or_search_performed"] is False
    error = [record for record in result["records"] if record["verification_status"] == "arithmetic_error"][0]
    assert error["check_id"] == "stage5ak-check-13136-plus-256"
    assert error["computed_value"] == 13392
    assert error["correction_record_present"] is True


def test_stage5ak_prime_helpers_are_deterministic_for_claim_values() -> None:
    assert prime_index(463) == 90
    assert is_prime(23571113172329313753257) is True
