from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_harvester.important_links import parse_important_links


def test_stage5aj_important_links_parse_and_dedupe(tmp_path: Path) -> None:
    source_root = tmp_path / "UsefulFilesAndIdeas"
    source_root.mkdir()
    (source_root / "important_links.txt").write_text(
        "\n".join(
            [
                "Existing: https://example.test/existing",
                "PAGE 56: https://uncovering-cicada.fandom.com/wiki/PAGE_56",
                "Post: https://www.reddit.com/r/cicada/comments/abc/example/",
            ]
        ),
        encoding="utf-8",
    )
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump({"records": [{"source_id": "existing", "url": "https://example.test/existing"}]}),
        encoding="utf-8",
    )

    result = parse_important_links(
        source_root=source_root,
        existing_manifest_path=manifest,
        results_dir=tmp_path / "results",
        out=tmp_path / "links.yaml",
        out_manifest_extension=tmp_path / "extension.yaml",
    )

    extension = yaml.safe_load((tmp_path / "extension.yaml").read_text(encoding="utf-8"))
    ids = {record["source_id"] for record in extension["records"]}
    assert result["important_links_urls_found"] == 3
    assert result["important_links_new_urls"] == 2
    assert "fandom_page_56" in ids
    assert any(record["source_type"] == "reddit_post" for record in extension["records"])
    assert extension["network_fetch_performed"] is False
