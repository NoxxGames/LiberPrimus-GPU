from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ai_website_ingest_is_metadata_ready_without_publication() -> None:
    payload = yaml.safe_load(Path("data/source-harvester/stage5ai-website-ingest-format.yaml").read_text(encoding="utf-8"))
    assert payload["website_ingest_metadata_ready"] is True
    assert payload["website_ingest_source_card_records"] == 26
    assert payload["website_ingest_content_records"] == 19
    assert payload["public_website_ready_count"] == 0
    assert payload["website_expansion_performed"] is False
