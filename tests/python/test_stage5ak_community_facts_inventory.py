from __future__ import annotations

from pathlib import Path

from libreprimus.source_harvester.community_facts import inventory_community_facts


def test_stage5ak_inventory_handles_missing_folder_without_raw_commit(tmp_path: Path) -> None:
    result = inventory_community_facts(
        source_root=tmp_path / "missing-community-facts",
        results_dir=tmp_path / "results",
        out=tmp_path / "inventory.yaml",
    )

    assert result["local_folder_exists"] is False
    assert result["community_facts_file_count"] == 0
    assert result["message_log_detected"] is False
    assert result["raw_text_committed"] is False
    assert result["raw_images_committed"] is False
    assert result["solve_claim"] is False


def test_stage5ak_inventory_records_message_log_metadata_only(tmp_path: Path) -> None:
    source_root = tmp_path / "community-facts"
    source_root.mkdir()
    (source_root / "community-facts-collection.txt").write_text("line one\nline two\n", encoding="utf-8")

    result = inventory_community_facts(
        source_root=source_root,
        results_dir=tmp_path / "results",
        out=tmp_path / "inventory.yaml",
    )

    assert result["local_folder_exists"] is True
    assert result["community_facts_file_count"] == 1
    assert result["message_log_detected"] is True
    assert result["message_log_line_count"] == 2
    assert result["raw_data_committed"] is False
    assert (tmp_path / "results" / "community_message_index.json").exists()
