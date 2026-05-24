from __future__ import annotations

import yaml

from libreprimus.paths import repo_root
from libreprimus.website_render.privacy import sanitize_record


def test_publication_gates_are_displayed_and_not_overridden() -> None:
    gates = yaml.safe_load((repo_root() / "data/website-ingest/stage5al/publication-gates.yaml").read_text(encoding="utf-8"))
    statuses = {record["status"] for record in gates["records"]}
    assert "private_deep_research_only" in statuses
    assert "raw_source_never_publish" in statuses
    for record in gates["records"]:
        assert record["website_publication_allowed"] is False
        assert record["raw_content_publication_allowed"] is False
        assert record["private_ids_allowed"] is False


def test_sanitizer_removes_body_fields_and_preserves_blocked_labels() -> None:
    record = {
        "claim_id": "claim-1",
        "title": "Claim",
        "claim_text": "raw body should not publish",
        "publication_status": "blocked_private_or_sensitive",
        "raw_content_publication_allowed": False,
    }
    sanitized = sanitize_record(record)
    assert "claim_text" not in sanitized
    assert sanitized["publication_status"] == "blocked_private_or_sensitive"
    assert sanitized["raw_bodies_included"] is False
    assert sanitized["private_ids_published"] is False
