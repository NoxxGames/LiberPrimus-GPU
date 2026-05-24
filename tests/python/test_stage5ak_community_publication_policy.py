from __future__ import annotations

from pathlib import Path

import yaml


def _yaml(path: str) -> dict:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_stage5ak_committed_publication_policy_blocks_public_website() -> None:
    summary = _yaml("data/source-harvester/stage5ak-summary.yaml")
    readiness = _yaml("data/source-harvester/stage5ak-research-bundle-readiness.yaml")
    claims = _yaml("data/source-harvester/stage5ak-community-facts-claim-records.yaml")

    assert summary["bundles_public_website_ready"] == 0
    assert summary["community_facts_private_publication_blocked"] is True
    assert readiness["private_deep_research_ready"] is True
    assert readiness["bundles_public_website_ready"] == 0
    assert all(record["website_publication_allowed"] is False for record in claims["records"])
    assert all(record["solve_claim"] is False for record in claims["records"])
