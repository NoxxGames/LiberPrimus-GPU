from __future__ import annotations

from libreprimus.hash_preimage.base29 import BASE29_ALPHABET, render_base29_upper


def test_base29_renderer_deterministic() -> None:
    assert BASE29_ALPHABET == "0123456789ABCDEFGHIJKLMNOPQRS"
    assert render_base29_upper(0) == "0"
    assert render_base29_upper(28) == "S"
    assert render_base29_upper(29) == "10"
    assert render_base29_upper(3301) == "3QO"
