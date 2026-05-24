from __future__ import annotations

import yaml

from libreprimus.paths import repo_root


def _load(name: str) -> dict:
    return yaml.safe_load((repo_root() / "data/website-ingest/stage5al" / name).read_text(encoding="utf-8"))


def test_stage5al_consumes_stage5ai_stage5aj_stage5ak_metadata() -> None:
    summary = _load("summary.yaml")
    assert summary["stage5ai_consumed"] is True
    assert summary["stage5aj_consumed"] is True
    assert summary["stage5ak_consumed"] is True
    assert summary["source_card_count"] >= 61
    assert summary["content_index_count"] >= 58
    assert summary["claim_record_count"] == 12


def test_stage5al_website_package_validates_counts() -> None:
    summary = _load("summary.yaml")
    assert _load("research-bundles.yaml")["record_count"] == summary["bundle_count"]
    assert _load("source-cards.yaml")["record_count"] == summary["source_card_count"]
    assert _load("content-index.yaml")["record_count"] == summary["content_index_count"]
    assert _load("community-claims.yaml")["record_count"] == summary["claim_record_count"]
    assert summary["website_shell_present"] is False
    assert summary["website_expansion_performed"] is False
