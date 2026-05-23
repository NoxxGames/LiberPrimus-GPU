from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_harvester.stage5ag_records import build_stage5ag_next_stage_decision


def test_stage5ag_next_stage_decision_selects_curated_extraction(tmp_path: Path) -> None:
    root = tmp_path / "root.yaml"
    root.write_text(yaml.safe_dump({"root_exists": True}, sort_keys=False), encoding="utf-8")
    linkage = tmp_path / "linkage.yaml"
    linkage.write_text(yaml.safe_dump({"matched_count": 3, "missing_count": 1}, sort_keys=False), encoding="utf-8")
    readiness = tmp_path / "readiness.yaml"
    readiness.write_text(
        yaml.safe_dump({"ready_for_extraction_prep_count": 0, "partial_count": 1}, sort_keys=False),
        encoding="utf-8",
    )

    result = build_stage5ag_next_stage_decision(
        root_inventory_path=root,
        local_linkage_path=linkage,
        bundle_readiness_path=readiness,
        out=tmp_path / "decision.yaml",
    )
    selected = [record for record in result["records"] if record["selected"]][0]
    assert selected["option_id"] == "stage5ah_curated_research_bundle_extraction_from_local_inventory"
    assert selected["deep_research_recommended_next"] is False
    assert selected["execution_enabled"] is False
