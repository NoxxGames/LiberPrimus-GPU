from __future__ import annotations

from test_stage5ee_common import ensure_stage5ee_built, load_yaml


def test_stage5ee_overlay_collection_has_expected_source_register_music_fandom_cards() -> None:
    ensure_stage5ee_built()
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5ee-review-batch-005-source-register-music-fandom-overlays.yaml"
    )
    labels = {overlay["display_label"] for overlay in collection["overlays"]}
    ids = {overlay["overlay_id"] for overlay in collection["overlays"]}

    assert collection["overlay_count"] == 25
    assert "stage5ee_pixel_colour_frequency_table_counts_overlay" in ids
    assert "stage5ee_music_source_inventory_7_4_3_overlay" in ids
    assert "stage5ee_761_mp3_id3_parable_metadata_overlay" in ids
    assert "stage5ee_fandom_source_lock_14_sources_overlay" in ids
    assert "stage5ee_local_archive_source_gap_summary_overlay" in ids
    assert any("12,543 prime-colour" in label for label in labels)
    assert any("7 files: 4 MP3 and 3 PDF" in label for label in labels)
    assert any("14 Fandom sources" in label for label in labels)


def test_stage5ee_overlays_are_not_decision_or_execution_seeds() -> None:
    ensure_stage5ee_built()
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5ee-review-batch-005-source-register-music-fandom-overlays.yaml"
    )

    for overlay in collection["overlays"]:
        assert overlay["review_state"] == "overlay_enriched_fact"
        assert overlay["usable_for_decision_now"] is False
        assert {"proof", "route_seed", "execution_seed", "solve_claim"} <= set(overlay["not_allowed_as"])
        assert overlay["risk_notes"]
