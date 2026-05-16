from libreprimus.corpus_candidate.tokenizer import CorpusTokenizer
from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import load_gematria_profile
from libreprimus.profiles.glyph_variant_profile import load_glyph_variant_profile
from libreprimus.profiles.separator_grammar import load_separator_grammar


def _tokenizer() -> CorpusTokenizer:
    root = repo_root()
    return CorpusTokenizer(
        gematria=load_gematria_profile(root / "data/profiles/gematria/gematria-primus-v0.json"),
        variants=load_glyph_variant_profile(root / "data/profiles/glyph-variants/glyph-variants-v0.json"),
        separators=load_separator_grammar(root / "data/profiles/separators/rtkd-separator-grammar-v0.json"),
        source_sha256="source-sha",
    )


def test_tokenizer_preserves_runes_variants_separators_numbers_and_unknowns() -> None:
    tokens, lines, warnings = _tokenizer().tokenize("\u16a0-\u16c2.% 123 @/")

    rune = next(token for token in tokens if token.raw_text == "\u16a0")
    variant = next(token for token in tokens if token.raw_text == "\u16c2")
    page = next(token for token in tokens if token.raw_text == "%")
    number = next(token for token in tokens if token.raw_text == "123")
    unknown = next(token for token in tokens if token.raw_text == "@")

    assert rune.index29 == 0
    assert rune.prime_value == 2
    assert variant.raw_glyph == "\u16c2"
    assert variant.normalized_glyph == "\u16c4"
    assert variant.variant_mapping_applied is True
    assert page.token_kind == "page_separator_or_marker"
    assert page.separator_class == "page_separator_or_marker"
    assert number.token_kind == "numeric_literal"
    assert unknown.token_kind == "unknown_symbol"
    assert unknown.source_column_start == 11
    assert warnings
    assert lines
