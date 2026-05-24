from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.deep_research_export.stage5an import build_next_stage_decision


def test_next_stage_selects_deep_research_only_when_outputs_validate(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    hosted = tmp_path / "hosted.yaml"
    combined = tmp_path / "combined.yaml"
    audit = tmp_path / "audit.yaml"
    out = tmp_path / "decision.yaml"
    manifest.write_text(yaml.safe_dump({"content_pack_generated": True}), encoding="utf-8")
    hosted.write_text(yaml.safe_dump({"hosted_content_export_generated": True}), encoding="utf-8")
    combined.write_text(yaml.safe_dump({"combined_webroot_generated": True}), encoding="utf-8")
    audit.write_text(yaml.safe_dump({"publication_gate_audit_passed": True}), encoding="utf-8")
    decision = build_next_stage_decision(
        manifest_summary=manifest,
        hosted_summary=hosted,
        combined_summary=combined,
        publication_gate_audit=audit,
        out=out,
    )
    assert decision["selected_option_id"] == "stage5ao_deep_research_source_inventory_and_reliability_prompt_with_private_content"
    assert decision["deep_research_next_ready"] is True


def test_committed_next_stage_does_not_select_scored_cuda_or_public_expansion() -> None:
    decision = yaml.safe_load(Path("data/deep-research-export/stage5an-next-stage-decision.yaml").read_text(encoding="utf-8"))
    selected = [record for record in decision["records"] if record["selected"]]
    assert selected[0]["deep_research_recommended_next"] is True
    assert all(record["scored_experiment_recommended_next"] is False for record in decision["records"])
    assert all(record["unsolved_page_cuda_recommended_next"] is False for record in decision["records"])
    assert all(record["public_website_expansion_recommended_next"] is False for record in decision["records"])
