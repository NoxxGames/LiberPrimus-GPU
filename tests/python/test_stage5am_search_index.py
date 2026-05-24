from __future__ import annotations

from libreprimus.paths import repo_root
from libreprimus.website_render.loader import load_stage5al_inputs
from libreprimus.website_render.privacy import sanitize_payload
from libreprimus.website_render.search_index import build_search_index


def test_search_index_contains_only_safe_metadata() -> None:
    inputs = load_stage5al_inputs(
        repo_root() / "data/website-ingest/stage5al",
        repo_root() / "data/source-harvester/stage5al-summary.yaml",
    )
    datasets = {name: sanitize_payload(payload) for name, payload in inputs["datasets"].items()}
    index = build_search_index(datasets)
    assert index
    assert {row["kind"] for row in index} >= {"bundle", "source", "content", "claim", "missing_source"}
    forbidden = {"claim_text", "raw_body", "source_message_locator"}
    for row in index:
        assert not (forbidden & set(row))
        assert "id" in row
        assert "title" in row
