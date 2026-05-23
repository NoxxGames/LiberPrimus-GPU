from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_harvester.manifest_linkage import link_local_sources


def test_stage5ag_linkage_maps_known_names_and_unclassified(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "records": [
                    {"source_id": "complete_cicada3301_archive", "priority": "A1", "source_type": "github_repo"},
                    {"source_id": "user_uploaded_2012_archive", "priority": "A1", "source_type": "local_user_upload"},
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    root = tmp_path / "third_party"
    (root / "The-Complete-Cicada3301-Archive-main" / "2012").mkdir(parents=True)
    (root / "mystery.png").write_bytes(b"image")

    linkage = link_local_sources(
        manifest_path=manifest,
        source_root=root,
        results_dir=tmp_path / "out",
        out=tmp_path / "linkage.yaml",
        out_extension=tmp_path / "extension.yaml",
    )

    records = {record["source_id"]: record for record in linkage["records"]}
    assert records["complete_cicada3301_archive"]["local_match_status"] == "matched_exact"
    assert records["user_uploaded_2012_archive"]["local_match_status"] == "matched_exact"
    assert records["local_unclassified_mystery_png"]["local_match_status"] == "not_expected_local"
    assert linkage["unclassified_local_count"] == 1
