from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from libreprimus.source_harvester.local_inventory import inventory_local_sources


def test_stage5ag_file_hashing_uses_sha256_and_detects_duplicates(tmp_path: Path) -> None:
    root = tmp_path / "third_party"
    root.mkdir()
    (root / "a.txt").write_text("duplicate", encoding="utf-8")
    (root / "b.txt").write_text("duplicate", encoding="utf-8")
    (root / "c.txt").write_text("unique", encoding="utf-8")

    result = inventory_local_sources(
        source_root=root,
        results_dir=tmp_path / "out",
        out_root_inventory=tmp_path / "root.yaml",
        out_file_summary=tmp_path / "files.yaml",
        out_archive_summary=tmp_path / "archives.yaml",
        out_hash_summary=tmp_path / "hashes.yaml",
    )

    digests = {record["file_name"]: record["sha256"] for record in result["file_records"]}
    assert digests["a.txt"] == sha256(b"duplicate").hexdigest()
    assert result["hash_summary"]["duplicate_hash_groups"] == 1
    assert result["hash_summary"]["unique_hash_count"] == 2
