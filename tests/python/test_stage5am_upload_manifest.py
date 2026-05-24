from __future__ import annotations

import yaml

from libreprimus.paths import repo_root


def test_upload_manifest_identifies_static_export_directory() -> None:
    manifest = yaml.safe_load((repo_root() / "data/website-render/stage5am-render-output-manifest.yaml").read_text(encoding="utf-8"))
    upload = yaml.safe_load((repo_root() / "data/website-render/stage5am-upload-instructions.yaml").read_text(encoding="utf-8"))
    assert manifest["upload_directory"] == "website-export/stage5am/research-index"
    assert upload["upload_directory"] == "website-export/stage5am/research-index"
    assert manifest["zip_package_generated"] is True
    assert manifest["raw_bodies_included"] is False
    assert upload["public_website_publication_performed"] is False


def test_generated_export_manifest_has_file_hashes() -> None:
    manifest = yaml.safe_load((repo_root() / "data/website-render/stage5am-render-output-manifest.yaml").read_text(encoding="utf-8"))
    hashes = manifest["file_hashes"]
    assert hashes
    assert any(record["path"] == "index.html" for record in hashes)
