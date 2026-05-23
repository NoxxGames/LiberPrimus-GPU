from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_harvester.planning import build_plan


def test_stage5af_plan_is_dry_run_and_network_disabled(tmp_path: Path) -> None:
    plan, summary = build_plan(
        manifest_path=Path("data/source-harvester/stage5af-cicada-source-manifest.yaml"),
        out_path=tmp_path / "harvest_plan.json",
        dry_run_summary_out=tmp_path / "dry_run.yaml",
        out_dir=tmp_path,
    )
    assert len(plan) == summary["dry_run_plan_records"]
    assert summary["network_fetch_performed"] is False
    assert summary["download_default_allowed"] is False
    assert all(record["dry_run_only"] is True for record in plan)
    assert all(record["fetch_performed"] is False for record in plan)


def test_stage5af_plan_summary_round_trips(tmp_path: Path) -> None:
    _, summary = build_plan(
        manifest_path=Path("data/source-harvester/stage5af-cicada-source-manifest.yaml"),
        out_path=tmp_path / "plan.json",
        dry_run_summary_out=tmp_path / "dry.yaml",
        out_dir=tmp_path,
    )
    written = yaml.safe_load((tmp_path / "dry.yaml").read_text(encoding="utf-8"))
    assert written == summary
    assert written["plan_status_counts"]["network_fetch_deferred"] > 0
