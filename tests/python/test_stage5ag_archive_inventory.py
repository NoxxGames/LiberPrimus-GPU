from __future__ import annotations

from pathlib import Path
import zipfile

from libreprimus.source_harvester.local_inventory import inventory_local_sources


def test_stage5ag_zip_archives_are_listed_without_extraction(tmp_path: Path) -> None:
    root = tmp_path / "third_party"
    root.mkdir()
    archive_path = root / "DiskCipherStuff.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("DiskCipherStuff/a.txt", "alpha")
        archive.writestr("DiskCipherStuff/b.png", b"not-image")

    result = inventory_local_sources(
        source_root=root,
        results_dir=tmp_path / "out",
        out_root_inventory=tmp_path / "root.yaml",
        out_file_summary=tmp_path / "files.yaml",
        out_archive_summary=tmp_path / "archives.yaml",
        out_hash_summary=tmp_path / "hashes.yaml",
    )
    archive = result["archive_records"][0]
    assert archive["supported_for_listing"] is True
    assert archive["raw_extraction_performed"] is False
    assert archive["member_count"] == 2
    assert not (root / "DiskCipherStuff").exists()


def test_stage5ag_unsupported_archive_types_are_not_fatal(tmp_path: Path) -> None:
    root = tmp_path / "third_party"
    root.mkdir()
    (root / "archive.7z").write_bytes(b"not a real archive")

    result = inventory_local_sources(
        source_root=root,
        results_dir=tmp_path / "out",
        out_root_inventory=tmp_path / "root.yaml",
        out_file_summary=tmp_path / "files.yaml",
        out_archive_summary=tmp_path / "archives.yaml",
        out_hash_summary=tmp_path / "hashes.yaml",
    )
    archive = result["archive_records"][0]
    assert archive["supported_for_listing"] is False
    assert archive["inventory_status"] == "unsupported_archive_type"
    assert result["archive_summary"]["unsupported_archive_count"] == 1
