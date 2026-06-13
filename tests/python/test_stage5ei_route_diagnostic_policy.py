from __future__ import annotations

from test_stage5ei_common import stage5ei_data


def test_stage5ei_route_policy_is_fingerprint_based_not_plaintext_gated() -> None:
    payload = stage5ei_data("route_diagnostic_policy")

    assert payload["plaintext_likeness_required_for_route_interest"] is False
    assert payload["english_readability_required_for_route_interest"] is False
    assert payload["high_entropy_output_can_be_interesting"] is True
    assert payload["ciphertext_like_output_can_be_interesting"] is True
    assert payload["key_like_output_can_be_interesting"] is True
    assert payload["control_stream_like_output_can_be_interesting"] is True
    assert payload["byte_like_output_can_be_interesting"] is True
    assert payload["null_copy_mask_like_output_can_be_interesting"] is True
    assert payload["intermediate_surface_output_can_be_interesting"] is True
    assert len(payload["future_route_stream_fingerprints"]) == 12
    assert "lag5_d1_d4_fingerprint" in payload["future_route_stream_fingerprints"]


def test_stage5ei_records_pascal_fibonacci_diagonal_context_as_candidate_only() -> None:
    payload = stage5ei_data("pascal_fibonacci_diagonal_context")

    assert payload["pascal_fibonacci_triangle_context_recorded"] is True
    assert payload["operator_observed_direct_above_vs_diagonal_sum_difference"] is True
    assert payload["pdd153_diagonal_sum_or_diagonal_relation_candidate"] is True
    assert payload["pdd153_diagonal_relation_accepted_as_method_now"] is False
    assert payload["pdd153_diagonal_route_probe_run_now"] is False
    assert "page32_moebius_fibonacci_prime_index_spiral_v1" in payload["crosslinks"]

