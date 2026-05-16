from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import compute_sha256
from libreprimus.profiles.separator_grammar import REQUIRED_SEPARATOR_CLASSES, load_separator_grammar, validate_separator_grammar


def test_separator_grammar_v0_validates() -> None:
    path = repo_root() / "data/profiles/separators/rtkd-separator-grammar-v0.json"
    grammar = load_separator_grammar(path)
    result = validate_separator_grammar(grammar)

    assert result.valid, result.errors
    assert REQUIRED_SEPARATOR_CLASSES.issubset(set(grammar.by_class_id))
    assert grammar.by_glyph["%"].canonical_page_boundary is False
    assert grammar.by_glyph["/"].token_kind == "line_separator"
    assert grammar.by_class_id["unknown_symbol"].requires_warning is True
    assert compute_sha256(path) == path.with_suffix(".sha256").read_text(encoding="utf-8").split()[0]
