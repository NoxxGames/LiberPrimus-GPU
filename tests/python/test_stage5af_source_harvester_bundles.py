from __future__ import annotations

from pathlib import Path

from libreprimus.source_harvester.bundles import build_bundle_scaffolds
from libreprimus.source_harvester.models import REQUIRED_BUNDLE_IDS


def test_stage5af_bundle_scaffolds_generate_guardrail_files(tmp_path: Path) -> None:
    records = build_bundle_scaffolds(
        bundle_plan_path=Path("data/source-harvester/stage5af-research-bundle-plan.yaml"),
        out_root=tmp_path / "bundles",
    )
    assert {record["bundle_id"] for record in records} == REQUIRED_BUNDLE_IDS
    for record in records:
        bundle_dir = tmp_path / "bundles" / record["bundle_id"]
        assert (bundle_dir / "do_not_assume.md").exists()
        assert (bundle_dir / "known_questions.md").exists()
        assert record["do_not_assume_generated"] is True
        assert record["known_questions_generated"] is True
