from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ai_unclassified_sources_are_provisional_only() -> None:
    payload = yaml.safe_load(Path("data/source-harvester/stage5ai-unclassified-source-classification.yaml").read_text(encoding="utf-8"))
    assert payload["classification_records"] == 14
    assert payload["evidence_status_upgraded"] is False
    records = {record["source_path"]: record for record in payload["records"]}
    assert records["third_party/depictions_original.png"]["provisional_bundle_ids"] == ["05-red-markers-and-visual-numerics"]
    discord = records["third_party/LiberPrimusDiscordChats"]
    assert discord["publication_status"] == "blocked_private_or_sensitive"
    assert discord["website_publication_allowed"] is False
