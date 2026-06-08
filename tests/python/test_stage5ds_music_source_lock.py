from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, load_yaml


def test_stage5ds_music_inventory_metadata_only() -> None:
    ensure_stage5ds_built()
    inventory = load_yaml("data/source-harvester/stage5ds-music-community-theory-file-inventory.yaml")
    assert inventory["file_count"] == 29
    assert inventory["audio_file_count"] == 10
    assert inventory["pdf_file_count"] == 11
    assert inventory["image_file_count"] == 7
    assert all(row["raw_file_committed"] is False for row in inventory["files"])
    assert all(len(row["sha256"]) == 64 for row in inventory["files"])


def test_stage5ds_message_anchors_are_compact() -> None:
    ensure_stage5ds_built()
    anchors = load_yaml(
        "data/source-harvester/stage5ds-music-message-attachment-anchor-index.yaml"
    )
    assert anchors["anchor_count"] == 28
    assert anchors["raw_message_body_committed"] is False
    assert all(len(str(row.get("message_excerpt") or "")) <= 160 for row in anchors["anchors"])
