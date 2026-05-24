from __future__ import annotations

import json
from pathlib import Path

from libreprimus.deep_research_export.hosted_export import build_hosted_export
from test_stage5an_content_pack_builder import build_fixture_pack


def test_hosted_content_export_references_existing_files(tmp_path: Path) -> None:
    fixture = build_fixture_pack(tmp_path)
    hosted = tmp_path / "hosted"
    data = tmp_path / "hosted-data"
    build_hosted_export(
        content_pack_root=fixture["pack"],
        metadata_site_root=fixture["metadata"],
        out_root=hosted,
        summary_out=data / "hosted.yaml",
        upload_instructions_out=data / "upload.yaml",
        consumption_guide_out=data / "guide.yaml",
    )
    manifest = json.loads((hosted / "data/content-pack-manifest.json").read_text(encoding="utf-8"))
    assert (hosted / "index.html").exists()
    assert (hosted / "robots.txt").read_text(encoding="utf-8").strip() == "User-agent: *\nDisallow: /"
    for record in manifest["included_files"]:
        assert (hosted / record["relative_path"]).exists()
