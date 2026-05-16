from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import load_gematria_profile
from libreprimus.profiles.glyph_variant_profile import load_glyph_variant_profile, validate_glyph_variant_profile


def test_glyph_variant_profile_v0_validates_against_gematria() -> None:
    root = repo_root()
    gematria = load_gematria_profile(root / "data/profiles/gematria/gematria-primus-v0.json")
    variants = load_glyph_variant_profile(root / "data/profiles/glyph-variants/glyph-variants-v0.json")

    result = validate_glyph_variant_profile(variants, gematria)

    assert result.valid, result.errors
    variant = variants.variants[0]
    assert variant.observed_glyph == "\u16c2"
    assert variant.normalized_rune_candidate == "\u16c4"
    assert variant.normalized_index_candidate == 11
    assert variant.normalized_prime_candidate == 37
    assert variant.canonical_mapping_change is False
    assert "preserve_raw" in variant.policy
