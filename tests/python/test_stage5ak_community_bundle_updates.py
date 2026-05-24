from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.source_harvester.community_attachments import build_community_attachment_index
from libreprimus.source_harvester.community_claims import build_community_claim_records
from libreprimus.source_harvester.community_facts import (
    build_community_facts_source_cards,
    inventory_community_facts,
    update_community_deep_research_packs,
)


def _source_root(tmp_path: Path) -> Path:
    source_root = tmp_path / "community-facts"
    source_root.mkdir()
    (source_root / "community-facts-collection.txt").write_text("community claim\n", encoding="utf-8")
    for index in range(1, 11):
        Image.new("RGB", (2, 2), "white").save(source_root / f"{index}.webp", format="PNG")
    return source_root


def test_stage5ak_deep_research_pack_update_is_private_and_not_public(tmp_path: Path) -> None:
    source_root = _source_root(tmp_path)
    inventory_community_facts(source_root=source_root, results_dir=tmp_path / "results", out=tmp_path / "inventory.yaml")
    build_community_attachment_index(source_root=source_root, results_dir=tmp_path / "results", out=tmp_path / "attachments.yaml")
    build_community_facts_source_cards(
        inventory_path=tmp_path / "inventory.yaml",
        attachment_index_path=tmp_path / "attachments.yaml",
        out_source_card_summary=tmp_path / "cards.yaml",
        out_content_index_summary=tmp_path / "content.yaml",
        results_dir=tmp_path / "results",
    )
    build_community_claim_records(
        source_root=source_root,
        claim_policy_out=tmp_path / "policy.yaml",
        claim_records_out=tmp_path / "claims.yaml",
        correction_log_out=tmp_path / "corrections.yaml",
        clue_categories_out=tmp_path / "categories.yaml",
        results_dir=tmp_path / "results",
    )

    result = update_community_deep_research_packs(
        stage5aj_bundle_root=tmp_path / "stage5aj",
        source_card_summary_path=tmp_path / "cards.yaml",
        content_index_summary_path=tmp_path / "content.yaml",
        claim_records_path=tmp_path / "claims.yaml",
        correction_log_path=tmp_path / "corrections.yaml",
        bundle_root=tmp_path / "research-inputs" / "stage5ak",
        results_dir=tmp_path / "results",
        out_website_update=tmp_path / "website.yaml",
        out_deep_research_update=tmp_path / "deep.yaml",
        out_readiness=tmp_path / "readiness.yaml",
        out_missing_source_plan=tmp_path / "missing.yaml",
    )

    assert result["readiness"]["bundles_ready_for_private_deep_research"] == 10
    assert result["readiness"]["bundles_public_website_ready"] == 0
    assert result["website"]["website_expansion_performed"] is False
    assert (tmp_path / "research-inputs" / "stage5ak" / "community_claim_records.jsonl").exists()
    assert (tmp_path / "research-inputs" / "stage5ak" / "09-community-hypotheses" / "manifest.yaml").exists()
