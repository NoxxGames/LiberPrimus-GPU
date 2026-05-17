"""Base29 rendering for bounded hash-preimage candidate packs."""

from __future__ import annotations

BASE29_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRS"


def render_base29_upper(value: int) -> str:
    """Render a non-negative integer with digits 0-9 and A-S for 10..28."""
    if value < 0:
        raise ValueError("base29 renderer only supports non-negative integers")
    if value == 0:
        return "0"
    digits: list[str] = []
    current = value
    while current:
        current, remainder = divmod(current, 29)
        digits.append(BASE29_ALPHABET[remainder])
    return "".join(reversed(digits))
