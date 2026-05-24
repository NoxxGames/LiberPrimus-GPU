from __future__ import annotations

from pathlib import Path

from libreprimus.deep_research_export.combined_webroot import build_combined_webroot
from libreprimus.deep_research_export.hosted_export import build_hosted_export
from test_stage5an_content_pack_builder import build_fixture_pack


def test_combined_webroot_contains_metadata_index_and_private_content(tmp_path: Path) -> None:
    fixture = build_fixture_pack(tmp_path)
    hosted = tmp_path / "hosted"
    data = tmp_path / "data"
    build_hosted_export(
        content_pack_root=fixture["pack"],
        metadata_site_root=fixture["metadata"],
        out_root=hosted,
        summary_out=data / "hosted.yaml",
        upload_instructions_out=data / "upload.yaml",
        consumption_guide_out=data / "guide.yaml",
    )
    combined = tmp_path / "webroot"
    summary = build_combined_webroot(
        metadata_site_root=fixture["metadata"],
        private_content_root=hosted,
        out_root=combined,
        summary_out=data / "combined.yaml",
    )
    assert summary["metadata_index_present"] is True
    assert summary["private_content_present"] is True
    assert (combined / "index.html").exists()
    assert (combined / "private-content/index.html").exists()
    assert "/private-content/" in (combined / "index.html").read_text(encoding="utf-8")
