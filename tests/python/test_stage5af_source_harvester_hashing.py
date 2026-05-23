from __future__ import annotations

import zipfile
from pathlib import Path

from libreprimus.source_harvester.hashing import inventory_archive, write_hash_path


def test_stage5af_hash_path_hashes_local_files(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture.txt"
    fixture.write_bytes(b"cicada\n")
    out = tmp_path / "hashes.jsonl"
    records = write_hash_path(fixture, out=out, source_id="fixture")
    assert len(records) == 1
    assert records[0]["size_bytes"] == len(b"cicada\n")
    assert len(records[0]["sha256"]) == 64
    assert out.exists()


def test_stage5af_inventory_archive_hashes_zip_members(tmp_path: Path) -> None:
    archive = tmp_path / "fixture.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("a.txt", "alpha")
        handle.writestr("nested/b.txt", "beta")
    out = tmp_path / "inventory.jsonl"
    records = inventory_archive(path=archive, source_id="user_uploaded_2012_archive", out=out)
    assert [record["archive_member_path"] for record in records] == ["a.txt", "nested/b.txt"]
    assert all(len(record["sha256"]) == 64 for record in records)
    assert out.exists()
