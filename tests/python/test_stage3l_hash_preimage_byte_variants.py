from __future__ import annotations

from libreprimus.hash_preimage.byte_variants import apply_byte_variant, encode_utf8


def test_raw_byte_variant_uses_literal_text() -> None:
    assert apply_byte_variant("Cicada", "raw") == "Cicada"
    assert encode_utf8("Cicada") == b"Cicada"


def test_lower_and_upper_variants() -> None:
    assert apply_byte_variant("Cicada 3301", "lower") == "cicada 3301"
    assert apply_byte_variant("Cicada 3301", "upper") == "CICADA 3301"


def test_line_ending_and_space_variants() -> None:
    assert apply_byte_variant("167", "trailing_lf") == "167\n"
    assert apply_byte_variant("167", "trailing_crlf") == "167\r\n"
    assert apply_byte_variant("167", "leading_space") == " 167"
    assert apply_byte_variant("167", "trailing_space") == "167 "
    assert apply_byte_variant("167", "wrapped_space") == " 167 "
