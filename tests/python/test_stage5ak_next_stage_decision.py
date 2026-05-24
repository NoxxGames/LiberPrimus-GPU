from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_harvester.stage5ak_records import build_stage5ak_next_stage_decision


def _write_yaml(path: Path, payload: dict) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def test_stage5ak_next_stage_selects_deep_research_not_execution(tmp_path: Path) -> None:
    readiness = tmp_path / "readiness.yaml"
    claims = tmp_path / "claims.yaml"
    missing = tmp_path / "missing.yaml"
    _write_yaml(readiness, {"bundles_ready_for_private_deep_research": 10})
    _write_yaml(claims, {"claim_record_count": 12})
    _write_yaml(missing, {"missing_source_records": 1})

    result = build_stage5ak_next_stage_decision(
        readiness_path=readiness,
        claim_records_path=claims,
        missing_source_plan_path=missing,
        out=tmp_path / "decision.yaml",
    )

    selected = [record for record in result["records"] if record["selected"] is True][0]
    assert result["selected_option_id"] == "stage5al_deep_research_source_inventory_and_reliability_prompt"
    assert selected["deep_research_recommended_next"] is True
    assert selected["scored_experiment_recommended_next"] is False
    assert selected["benchmark_recommended_next"] is False
    assert selected["unsolved_page_cuda_recommended_next"] is False
    assert selected["website_expansion_recommended_next"] is False
    assert selected["execution_enabled"] is False
