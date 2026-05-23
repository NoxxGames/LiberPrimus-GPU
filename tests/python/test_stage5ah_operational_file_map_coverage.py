from __future__ import annotations

from pathlib import Path

from libreprimus.doc_staleness.coverage import build_operational_file_map_coverage


def test_stage5ah_operational_file_map_has_required_coverage() -> None:
    report = build_operational_file_map_coverage(
        operational_file_map=Path("data/project-state/operational-file-map.yaml")
    )

    assert report["coverage_finding_count"] == 0
    assert report["record_count"] >= 38


def test_stage5ah_operational_file_map_records_local_inventory_guides() -> None:
    text = Path("data/project-state/operational-file-map.yaml").read_text(encoding="utf-8")

    assert "docs/onboarding/source-harvester-workflow.md" in text
    assert "docs/onboarding/local-source-inventory-workflow.md" in text
    assert "data/project-state/stage5ah-doc-staleness-source-of-truth.yaml" in text
