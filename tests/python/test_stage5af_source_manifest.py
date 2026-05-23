from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_harvester.manifest import validate_manifest
from libreprimus.source_harvester.models import REQUIRED_SOURCE_IDS


def test_stage5af_source_manifest_validates() -> None:
    summary, errors = validate_manifest(Path("data/source-harvester/stage5af-cicada-source-manifest.yaml"))
    assert errors == []
    assert summary["required_source_ids_present"] is True
    assert summary["source_manifest_records"] >= len(REQUIRED_SOURCE_IDS)


def test_stage5af_required_sources_and_manual_exports() -> None:
    manifest = yaml.safe_load(Path("data/source-harvester/stage5af-cicada-source-manifest.yaml").read_text())
    records = {record["source_id"]: record for record in manifest["records"]}
    assert REQUIRED_SOURCE_IDS.issubset(records)
    for source_id in (
        "solved_page_google_sheet",
        "solved_pages_colab_notebook",
        "chapterized_rune_map_google_doc",
        "liber_primus_dropbox_files",
    ):
        assert records[source_id]["manual_collection_required"] is True
        assert records[source_id]["google_drive_storage_allowed"] is False
    assert manifest["storage_policy"]["local_storage_only"] is True
    assert manifest["storage_policy"]["google_drive_storage_allowed"] is False
