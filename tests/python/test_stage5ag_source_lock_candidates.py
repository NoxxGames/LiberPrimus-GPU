from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_harvester.source_lock_candidates import build_source_lock_candidates


def test_stage5ag_source_lock_candidates_classify_ready_missing_and_unclassified(
    tmp_path: Path,
) -> None:
    linkage = tmp_path / "linkage.yaml"
    linkage.write_text(
        yaml.safe_dump(
            {
                "records": [
                    {"source_id": "complete", "local_match_status": "matched_exact", "matched_paths": ["x"]},
                    {"source_id": "manual", "local_match_status": "missing", "manual_collection_required": True},
                    {"source_id": "local_unclassified_image", "local_match_status": "not_expected_local"},
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    result = build_source_lock_candidates(
        local_linkage_path=linkage,
        out=tmp_path / "candidates.yaml",
        gap_report=tmp_path / "gaps.yaml",
    )

    statuses = {record["source_id"]: record["candidate_status"] for record in result["summary"]["records"]}
    assert statuses["complete"] == "ready_for_source_lock_inventory"
    assert statuses["manual"] == "needs_manual_export"
    assert statuses["local_unclassified_image"] == "needs_manual_classification"
    assert result["summary"]["ready_count"] == 1
