from __future__ import annotations

from libreprimus.post_discord.gp_rune_claim_verifier import GpRuneClaim, verify_claim


def test_verified_and_unverified_claims() -> None:
    verified = verify_claim(
        GpRuneClaim(
            claim_id="verified",
            source_basis="synthetic",
            claim_type="gp_sum_equals",
            target_span={"rune_indices": [0, 1, 2]},
            claimed_value=10,
            value_type="integer",
        )
    )
    wrong = verify_claim(
        GpRuneClaim(
            claim_id="wrong",
            source_basis="synthetic",
            claim_type="gp_sum_mod29_equals",
            target_span={"rune_indices": [0, 1, 2]},
            claimed_value=11,
            value_type="integer",
        )
    )
    assert verified.verification_status == "verified"
    assert wrong.verification_status == "unverified"


def test_missing_unsupported_malformed_and_boundary_sensitive() -> None:
    assert (
        verify_claim(
            GpRuneClaim(
                claim_id="missing",
                source_basis="synthetic",
                claim_type="rune_count_equals",
                target_span={"page_id": "p1"},
                claimed_value=3,
                value_type="integer",
            )
        ).verification_status
        == "missing_source_span"
    )
    assert (
        verify_claim(
            GpRuneClaim(
                claim_id="unsupported",
                source_basis="synthetic",
                claim_type="neighbouring_span_search",
                target_span={},
                claimed_value=3,
                value_type="integer",
            )
        ).verification_status
        == "unsupported_claim_type"
    )
    assert (
        verify_claim(
            GpRuneClaim(
                claim_id="malformed",
                source_basis="synthetic",
                claim_type="rune_count_equals",
                target_span={"rune_indices": [0]},
                claimed_value=None,
                value_type="integer",
            )
        ).verification_status
        == "malformed_claim"
    )
    assert (
        verify_claim(
            GpRuneClaim(
                claim_id="boundary",
                source_basis="synthetic",
                claim_type="rune_count_equals",
                target_span={"rune_indices": [0]},
                claimed_value=1,
                value_type="integer",
                computation_policy={"boundary_sensitive": True},
            )
        ).verification_status
        == "boundary_sensitive"
    )
