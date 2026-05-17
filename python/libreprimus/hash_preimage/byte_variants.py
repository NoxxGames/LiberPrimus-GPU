"""Byte-variant expansion for bounded hash-preimage packs."""

from __future__ import annotations

BYTE_VARIANTS = {
    "raw",
    "lower",
    "upper",
    "trailing_lf",
    "trailing_crlf",
    "leading_space",
    "trailing_space",
    "wrapped_space",
}


def apply_byte_variant(literal: str, variant: str) -> str:
    """Apply an explicit byte-string variant before UTF-8 encoding."""
    if variant == "raw":
        return literal
    if variant == "lower":
        return literal.lower()
    if variant == "upper":
        return literal.upper()
    if variant == "trailing_lf":
        return f"{literal}\n"
    if variant == "trailing_crlf":
        return f"{literal}\r\n"
    if variant == "leading_space":
        return f" {literal}"
    if variant == "trailing_space":
        return f"{literal} "
    if variant == "wrapped_space":
        return f" {literal} "
    raise ValueError(f"Unsupported byte variant: {variant}")


def encode_utf8(literal: str) -> bytes:
    return literal.encode("utf-8")
