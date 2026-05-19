from __future__ import annotations

from libreprimus.source_delta_audit.tree_classifier import classify_path, selected_path_candidates


def test_tree_classifier_identifies_high_value_paths() -> None:
    assert classify_path("liber-primus__images--full/00.jpg") == "lp_full_image"
    assert classify_path("lp_outguessed/00.txt") == "lp_outguessed"
    assert classify_path("2014/05/3301 - Interconnectedness.mp3") == "audio_fixture_candidate"
    assert classify_path("ttf/some-font.ttf") == "font_metadata_only"


def test_selected_path_candidates_marks_lp_outguessed_duplicate() -> None:
    candidates = selected_path_candidates(
        [
            "liber-primus__images--full/00.jpg",
            "lp_outguessed/00.txt",
            "2016/01/4gq25.jpg",
        ]
    )
    by_type = {candidate["artifact_type"]: candidate for candidate in candidates}
    assert by_type["lp_outguessed"]["duplicate_of"] == "stage4b-cicada-solvers-iddqd-lp-outguessed"
    assert by_type["image_fixture_candidate"]["recommended_action"] == "queue fixture source-lock"
