from libreprimus.alignment.signatures import (
    build_signature_index,
    decimal_indices_for_glyphs,
    normalize_glyph_sequence,
    pastebin_signature,
)
from libreprimus.legacy_pastebin.parser import build_line_pairs


def test_pastebin_signature_uses_prime_values_as_decimal_indices() -> None:
    line_pairs, _, _, _ = build_line_pairs("{ᛋᚻᛖ}\n{{53,23,67}}\n", "abc123")

    signature = pastebin_signature(line_pairs[0])

    assert signature.raw_rune_sequence == "ᛋᚻᛖ"
    assert signature.decimal_index_sequence == [15, 8, 18]
    assert signature.decimal_index_sequence != [53, 23, 67]
    assert signature.signature_sha256


def test_variant_normalized_view_does_not_mutate_raw_sequence() -> None:
    assert normalize_glyph_sequence("ᛂ") == "ᛄ"
    assert decimal_indices_for_glyphs("ᛂ") == [11]


def test_signature_index_is_hash_map_based() -> None:
    line_pairs, _, _, _ = build_line_pairs("{ᛋ}\n{{53}}\n{ᚻ}\n{{23}}\n", "abc123")
    signatures = [pastebin_signature(line_pair) for line_pair in line_pairs]

    index = build_signature_index(signatures, "raw_rune_sequence")

    assert set(index) == {"ᛋ", "ᚻ"}
    assert index["ᛋ"][0].source_index == 0
