from __future__ import annotations

import yaml


def test_consumption_guide_urls_and_upload_root() -> None:
    guide = yaml.safe_load(
        open("data/deep-research-export/stage5an-deep-research-consumption-guide.yaml", encoding="utf-8")
    )
    assert guide["metadata_site_url"] == "http://liberprimus-gpu-data.info/index.html"
    assert guide["private_content_url"] == "http://liberprimus-gpu-data.info/private-content/"
    assert guide["private_content_manifest_url"].endswith("/private-content/data/content-pack-manifest.json")
    assert guide["recommended_sftp_upload_root"] == "website-export/stage5an/webserver-root/"
    assert guide["deep_research_performed"] is False
