"""Stage 4E source-variant comparison backlog records."""

from __future__ import annotations

from typing import Any


def build_variant_comparison_records(path_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return future comparison records without performing image/audio comparisons."""

    records: list[dict[str, Any]] = []
    for candidate in path_candidates:
        category = str(candidate.get("artifact_type"))
        if category not in {"lp_full_image", "lp_unsolved_image", "lp_outguessed", "audio_fixture_candidate", "image_fixture_candidate"}:
            continue
        records.append(
            {
                "record_type": "source_variant_comparison_record",
                "comparison_id": f"stage4e-variant-{category}",
                "source_id": candidate["source_id"],
                "artifact_type": category,
                "local_reference": "third_party/LiberPrimusPages" if category.startswith("lp_") else None,
                "remote_path_sample": candidate["path"],
                "comparison_status": "future_source_lock_required",
                "recommended_action": candidate["recommended_action"],
                "raw_file_committed": False,
                "binary_committed": False,
                "trusted_as_canonical": False,
                "solve_claim": False,
                "notes": "Comparison is queued only; Stage 4E does not fetch or process the raw artefact.",
            }
        )
    return records
