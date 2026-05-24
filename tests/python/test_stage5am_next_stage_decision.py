from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.website_render.stage5am import build_stage5am_next_stage_decision


def test_next_stage_decision_selects_stage5an_when_validation_passes(tmp_path: Path) -> None:
    validation = tmp_path / "validation.yaml"
    audit = tmp_path / "audit.yaml"
    out = tmp_path / "decision.yaml"
    validation.write_text("static_site_validation_passed: true\nsolve_claim: false\n", encoding="utf-8")
    audit.write_text("privacy_audit_passed: true\nsolve_claim: false\n", encoding="utf-8")
    decision = build_stage5am_next_stage_decision(site_validation_path=validation, privacy_audit_path=audit, out=out)
    assert decision["deep_research_next_ready"] is True
    assert decision["selected_next_stage_title"] == "Stage 5AN - Deep Research source inventory and reliability prompt"
    assert decision["records"][0]["website_expansion_recommended_next"] is False
    assert decision["records"][0]["unsolved_page_cuda_recommended_next"] is False


def test_committed_next_stage_decision_is_stage5an() -> None:
    decision = yaml.safe_load(Path("data/website-render/stage5am-next-stage-decision.yaml").read_text(encoding="utf-8"))
    assert decision["selected_option_id"] == "stage5an_deep_research_source_inventory_and_reliability_prompt"
    assert decision["deep_research_next_ready"] is True
