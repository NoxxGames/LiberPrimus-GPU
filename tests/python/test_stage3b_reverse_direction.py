from __future__ import annotations

from libreprimus.bounded_execution.caesar_affine import (
    affine_inverse,
    reverse_affine_outputs,
    reverse_caesar_outputs,
)
from libreprimus.bounded_execution.runner import AFFINE_COUNT, CAESAR_COUNT, TOTAL_COUNT


def test_reverse_caesar_formula_works() -> None:
    outputs = dict((params["shift"], values) for params, values in reverse_caesar_outputs([0, 1, 28]))

    assert len(outputs) == CAESAR_COUNT
    assert outputs[1] == [28, 0, 27]


def test_affine_inverse_mod29_works() -> None:
    assert (26 * affine_inverse(26)) % 29 == 1
    assert affine_inverse(1) == 1


def test_reverse_affine_generates_812_candidates() -> None:
    outputs = reverse_affine_outputs([0, 1, 28])

    assert len(outputs) == AFFINE_COUNT
    assert all(0 <= value <= 28 for _, values in outputs for value in values)


def test_reverse_total_candidates_841() -> None:
    assert len(reverse_caesar_outputs([0])) + len(reverse_affine_outputs([0])) == TOTAL_COUNT
