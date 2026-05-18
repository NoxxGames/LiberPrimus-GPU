from __future__ import annotations

from libreprimus.post_discord.gp_rune_claim_verifier import compute_derived_value, compute_rune_span


def test_synthetic_rune_span_counts_and_gp_sum() -> None:
    computed = compute_rune_span({"rune_indices": [0, 1, 2], "separator_count": 2})
    assert computed["rune_count"] == 3
    assert computed["transformable_rune_count"] == 3
    assert computed["separator_count"] == 2
    assert computed["gp_sum"] == 10
    assert computed["gp_sum_mod29"] == 10


def test_cuneiform_derived_arithmetic() -> None:
    assert (
        compute_derived_value(
            {
                "kind": "cuneiform_digits",
                "digits": [17, 13, 55, 1],
                "derived_name": "full_base60",
            }
        )["value"]
        == 3722101
    )
    assert (
        compute_derived_value(
            {
                "kind": "cuneiform_digits",
                "digits": [17, 13, 55, 1],
                "derived_name": "full_base60_mod29",
            }
        )["value"]
        == 9
    )
