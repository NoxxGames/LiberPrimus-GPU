from __future__ import annotations

from pathlib import Path

from libreprimus.token_block.original_images import classify_variant


def test_stage5ar_variant_classifier_distinguishes_original_from_screenshot() -> None:
    variant, source_class, allowed = classify_variant(Path("third_party/LiberPrimusPages/49.jpg"), {})
    assert variant == "original_candidate"
    assert source_class == "original_liber_primus_page_image"
    assert allowed is True

    variant, _, allowed = classify_variant(Path("research-inputs/page49_screenshot.png"), {})
    assert variant == "derived_screenshot"
    assert allowed is False
