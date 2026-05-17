"""Small integer prime helpers for image metadata."""

from __future__ import annotations


def is_prime(value: int) -> bool:
    """Return true when value is prime."""
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    factor = 3
    while factor * factor <= value:
        if value % factor == 0:
            return False
        factor += 2
    return True
