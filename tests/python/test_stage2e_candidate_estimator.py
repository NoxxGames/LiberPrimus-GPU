from __future__ import annotations

from libreprimus.experiments.candidate_estimator import estimate_candidate_count


def _manifest(family: str, parameter_space: dict) -> dict:
    return {
        "transform_plan": {"transform_family": family},
        "parameter_space": parameter_space,
    }


def test_direct_count_is_one() -> None:
    assert estimate_candidate_count(_manifest("direct_translation", {})).candidate_count == 1


def test_reverse_count_is_one() -> None:
    assert estimate_candidate_count(_manifest("reverse_gematria", {})).candidate_count == 1


def test_rotation_list_count_works() -> None:
    manifest = _manifest("rotated_reverse_gematria", {"rotations": [0, 1, 2]})

    assert estimate_candidate_count(manifest).candidate_count == 3


def test_caesar_count_is_29() -> None:
    assert estimate_candidate_count(_manifest("caesar_shift_preview", {})).candidate_count == 29


def test_affine_mod29_count_is_812() -> None:
    assert estimate_candidate_count(_manifest("affine_mod29_preview", {})).candidate_count == 812


def test_vigenere_explicit_key_list_count_works() -> None:
    manifest = _manifest("vigenere_key_list_preview", {"keys": ["DIVINITY", "FIRFUMFERENFE"]})

    assert estimate_candidate_count(manifest).candidate_count == 2


def test_prime_parameter_product_works() -> None:
    manifest = _manifest(
        "prime_stream_parameter_preview",
        {
            "prime_start_index": [0, 1],
            "direction": ["forward", "reverse"],
            "stream_value": ["prime_minus_one_mod29"],
        },
    )

    assert estimate_candidate_count(manifest).candidate_count == 4


def test_estimator_does_not_enumerate_plaintexts() -> None:
    estimate = estimate_candidate_count(_manifest("caesar_shift_preview", {}))

    assert not hasattr(estimate, "candidate_plaintexts")
    assert "plaintext" not in estimate.parameter_summary
