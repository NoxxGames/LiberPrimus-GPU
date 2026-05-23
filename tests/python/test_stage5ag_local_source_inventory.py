from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.source_harvester.local_inventory import inventory_local_sources


def test_stage5ag_inventory_handles_missing_source_root(tmp_path: Path) -> None:
    result = inventory_local_sources(
        source_root=tmp_path / "missing",
        results_dir=tmp_path / "out",
        out_root_inventory=tmp_path / "root.yaml",
        out_file_summary=tmp_path / "files.yaml",
        out_archive_summary=tmp_path / "archives.yaml",
        out_hash_summary=tmp_path / "hashes.yaml",
    )
    assert result["root_inventory"]["root_exists"] is False
    assert result["root_inventory"]["status"] == "blocked_missing_source_root"
    assert result["file_summary"]["inventory_record_count"] == 0


def test_stage5ag_inventory_records_files_dirs_and_image_metadata(tmp_path: Path) -> None:
    root = tmp_path / "third_party"
    nested = root / "VisualClues"
    nested.mkdir(parents=True)
    (root / "note.txt").write_text("same", encoding="utf-8")
    (nested / "copy.txt").write_text("same", encoding="utf-8")
    Image.new("RGB", (7, 5), "white").save(root / "image.png")

    result = inventory_local_sources(
        source_root=root,
        results_dir=tmp_path / "out",
        out_root_inventory=tmp_path / "root.yaml",
        out_file_summary=tmp_path / "files.yaml",
        out_archive_summary=tmp_path / "archives.yaml",
        out_hash_summary=tmp_path / "hashes.yaml",
    )

    assert result["root_inventory"]["total_files"] == 3
    assert result["root_inventory"]["total_dirs"] == 1
    assert result["root_inventory"]["image_counts"] == 1
    image_record = next(record for record in result["file_records"] if record["category"] == "image")
    assert image_record["image_width"] == 7
    assert image_record["image_height"] == 5
    assert result["hash_summary"]["duplicate_hash_groups"] == 1
