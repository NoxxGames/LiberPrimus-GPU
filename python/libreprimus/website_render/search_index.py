"""Build safe browser-side search metadata for Stage 5AM."""

from __future__ import annotations

from typing import Any


def build_search_index(datasets: dict[str, Any]) -> list[dict[str, Any]]:
    """Build a compact metadata-only search index."""

    rows: list[dict[str, Any]] = []
    specs = [
        ("bundle", "research-bundles", "bundle_id"),
        ("source", "source-cards", "source_id"),
        ("content", "content-index", "content_id"),
        ("claim", "community-claims", "claim_id"),
        ("missing_source", "missing-sources", "source_id"),
    ]
    for kind, dataset_name, id_key in specs:
        payload = datasets.get(dataset_name, {})
        records = payload.get("records", []) if isinstance(payload, dict) else []
        for record in records:
            if not isinstance(record, dict):
                continue
            rows.append(
                {
                    "kind": kind,
                    "id": str(record.get(id_key, "")),
                    "title": str(record.get("title", record.get(id_key, ""))),
                    "publication_status": str(record.get("publication_status", "unknown")),
                    "review_status": str(record.get("review_status", "unknown")),
                    "risk_level": str(record.get("risk_level", "unknown")),
                    "bundle_ids": record.get("bundle_ids", record.get("bundle_id", [])),
                }
            )
    return sorted(rows, key=lambda row: (row["kind"], row["id"], row["title"]))
