from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_harvester.bundle_readiness import build_bundle_readiness


def test_stage5ag_research_bundle_readiness_is_deterministic(tmp_path: Path) -> None:
    bundle_plan = tmp_path / "bundle.yaml"
    bundle_plan.write_text(
        yaml.safe_dump(
            {
                "records": [
                    {"bundle_id": "ready", "included_source_ids": ["a"]},
                    {"bundle_id": "partial", "included_source_ids": ["a", "b"]},
                    {"bundle_id": "missing", "included_source_ids": ["c"]},
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    linkage = tmp_path / "linkage.yaml"
    linkage.write_text(
        yaml.safe_dump(
            {"records": [{"source_id": "a", "local_match_status": "matched_exact"}]},
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    summary = build_bundle_readiness(
        bundle_plan_path=bundle_plan,
        local_linkage_path=linkage,
        out=tmp_path / "readiness.yaml",
        results_dir=tmp_path / "out",
    )
    statuses = {record["bundle_id"]: record["readiness_status"] for record in summary["records"]}
    assert statuses == {
        "ready": "ready_for_extraction_prep",
        "partial": "partially_ready",
        "missing": "not_ready",
    }
