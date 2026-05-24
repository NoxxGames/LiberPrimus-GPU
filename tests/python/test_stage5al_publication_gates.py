from __future__ import annotations

import yaml

from libreprimus.paths import repo_root


def test_publication_gates_block_publication_by_default() -> None:
    gates = yaml.safe_load((repo_root() / "data/website-ingest/stage5al/publication-gates.yaml").read_text(encoding="utf-8"))
    statuses = {record["status"] for record in gates["records"]}
    assert "raw_source_never_publish" in statuses
    assert "blocked_private_or_sensitive" in statuses
    assert "private_deep_research_only" in statuses
    for record in gates["records"]:
        assert record["website_publication_allowed"] is False
        assert record["raw_content_publication_allowed"] is False
        assert record["generated_extract_publication_allowed"] is False
        assert record["private_ids_allowed"] is False
        assert record["raw_bodies_allowed"] is False


def test_public_website_ready_count_remains_zero() -> None:
    summary = yaml.safe_load((repo_root() / "data/source-harvester/stage5al-summary.yaml").read_text(encoding="utf-8"))
    assert summary["public_website_ready_count"] == 0
    assert summary["website_publication_performed"] is False
