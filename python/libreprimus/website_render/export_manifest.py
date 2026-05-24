"""Manifest helpers for Stage 5AM static website exports."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .loader import repo_relative, resolve


def file_hashes(site_root: Path) -> list[dict[str, Any]]:
    """Return SHA-256 hashes for generated static export files."""

    root = resolve(site_root)
    records: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        data = path.read_bytes()
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
            }
        )
    return records


def build_render_inputs_record(inputs: dict[str, Any]) -> dict[str, Any]:
    """Build the committed render input inventory record."""

    summary = inputs["stage5al_summary"]
    return {
        "record_type": "stage5am_render_inputs",
        "schema": "schemas/website-render/render-inputs-v0.schema.json",
        "stage_id": "stage-5am",
        "source_stage_id": "stage-5al",
        "website_ingest_dir": inputs["website_ingest_dir"],
        "stage5al_summary_path": inputs["stage5al_summary_path"],
        "stage5al_commit": "66d6ba9f7739861bc5f797d0896f32082af92326",
        "metadata_only": True,
        "source_card_count": summary.get("source_card_count", 0),
        "content_record_count": summary.get("content_index_count", 0),
        "claim_record_count": summary.get("claim_record_count", 0),
        "bundle_count": summary.get("bundle_count", 0),
        "publication_gate_count": summary.get("publication_gate_count", 0),
        "missing_source_count": summary.get("missing_source_count", 0),
        "raw_bodies_included": False,
        "private_ids_published": False,
        "solve_claim": False,
    }


def build_render_policy_record() -> dict[str, Any]:
    """Build the Stage 5AM render policy record."""

    return {
        "record_type": "stage5am_render_policy",
        "schema": "schemas/website-render/render-policy-v0.schema.json",
        "stage_id": "stage-5am",
        "source_stage_id": "stage-5al",
        "metadata_only": True,
        "review_gated": True,
        "raw_bodies_included": False,
        "private_ids_published": False,
        "public_website_publication_performed": False,
        "publication_gates_override": False,
        "noindex_required": True,
        "robots_disallow_all_required": True,
        "external_network_dependencies_allowed": False,
        "deep_research_performed": False,
        "solve_claim": False,
    }


def attach_hashes(manifest: dict[str, Any], site_root: Path) -> dict[str, Any]:
    """Attach generated file hashes to a manifest."""

    enriched = dict(manifest)
    enriched["file_hashes"] = file_hashes(site_root)
    enriched["site_root"] = repo_relative(site_root)
    return enriched
