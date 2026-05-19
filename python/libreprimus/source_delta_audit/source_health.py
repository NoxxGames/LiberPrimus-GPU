"""Build source-health records for Stage 4E selected source paths."""

from __future__ import annotations

from typing import Any


def build_source_health_records(candidates: list[dict[str, Any]], *, reachable: bool, remote_head: str | None, repo_url: str) -> list[dict[str, Any]]:
    """Create metadata-only health records for selected categories."""

    records: list[dict[str, Any]] = []
    for candidate in candidates:
        category = str(candidate["artifact_type"])
        base_url = repo_url[:-4] if repo_url.endswith(".git") else repo_url
        records.append(
            {
                "record_type": "source_health_record",
                "source_id": f"stage4e-iddqd-{category}",
                "url": f"{base_url}/tree/master/{candidate['path']}",
                "source_class": candidate["source_class"],
                "health_status": "reachable_metadata_only" if reachable else "deferred_remote_unavailable",
                "fragility": "high" if category in {"lp_outguessed", "audio_fixture_candidate", "font_metadata_only"} else "medium",
                "checked_at_stage": "stage4e",
                "retrieval_status": "tree_metadata_recorded_no_blobs",
                "recommended_action": candidate["recommended_action"],
                "remote_head": remote_head,
                "trusted_as_canonical": False,
                "solve_claim": False,
                "notes": "Stage 4E records source-health metadata only; no raw files or binaries are committed.",
            }
        )
    return records
