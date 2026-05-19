from __future__ import annotations

from libreprimus.source_lock_snapshots.copyright_policy import committed_snapshot_allowed
from libreprimus.source_lock_snapshots.snapshot_policy import (
    artifact_kind,
    choose_snapshot_policy,
    classify_source_class,
)


def test_stage4k_font_policy_is_metadata_only() -> None:
    url = "https://github.com/cicada-solvers/iddqd/blob/master/ttf/runes.ttf"
    assert artifact_kind(url, "font_metadata_only") == "font"
    assert choose_snapshot_policy(url, "github_blob", "font_metadata_only") == "metadata_only"


def test_stage4k_binary_image_audio_archive_not_committed_by_default() -> None:
    cases = [
        ("https://example.invalid/file.jpg", "image_fixture_candidate"),
        ("https://example.invalid/file.mp3", "audio_fixture_candidate"),
        ("https://example.invalid/file.zip", "archive"),
    ]
    for url, artifact in cases:
        policy = choose_snapshot_policy(url, "artifact_metadata", artifact)
        assert policy == "metadata_only"
        allowed, _reason = committed_snapshot_allowed(url, policy, artifact)
        assert allowed is False


def test_stage4k_small_text_snapshot_allowed_only_by_explicit_policy() -> None:
    allowed, _reason = committed_snapshot_allowed(
        "https://github.com/example/repo/blob/main/notes.txt",
        "committed_small_text_snapshot",
        "reference_source",
    )
    assert allowed is True
    disallowed, _reason = committed_snapshot_allowed(
        "https://github.com/example/repo/blob/main/notes.txt",
        "ignored_local_snapshot",
        "reference_source",
    )
    assert disallowed is False


def test_stage4k_classifies_uncovering_page() -> None:
    assert classify_source_class("https://uncovering-cicada.fandom.com/wiki/OutGuess") == "uncovering_cicada_page"
