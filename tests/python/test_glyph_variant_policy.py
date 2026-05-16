from pathlib import Path

from libreprimus.alignment.pastebin_to_transcript import align_pastebin_to_transcript
from libreprimus.legacy_pastebin.gematria_validation import RUNE_TO_ENTRY


def test_glyph_variant_observation_preserves_raw_and_does_not_change_mapping(tmp_path: Path) -> None:
    pastebin = tmp_path / "pastebin.txt"
    pastebin.write_text("{ᛂ}\n{{37}}\n", encoding="utf-8")
    transcript = tmp_path / "rtkd.txt"
    transcript.write_text("ᛄ/\n", encoding="utf-8")

    result = align_pastebin_to_transcript(pastebin, transcript)
    observation = result["glyph_variant_observations"][0]
    alignment = result["alignments"][0]

    assert "ᛂ" not in RUNE_TO_ENTRY
    assert observation.observed_glyph == "ᛂ"
    assert observation.observed_prime_value == 37
    assert observation.inferred_decimal_index == 11
    assert observation.inferred_canonical_glyph_candidate == "ᛄ"
    assert observation.variant_policy == "preserve_raw_apply_documented_normalized_view_only"
    assert alignment.best_match is not None
    assert alignment.best_match.variant_mapping_applied is True
    assert result["pastebin_extraction"].line_pairs[0].rune_words == ["ᛂ"]
