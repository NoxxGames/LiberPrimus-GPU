from __future__ import annotations

from pathlib import Path

from libreprimus.source_harvester.extraction_fidelity import build_extraction_fidelity_policy
from libreprimus.source_harvester.redaction_policy import build_redaction_policy
from libreprimus.source_harvester.scraper_profiles import build_scraper_capture_policy


def test_stage5aj_policies_preserve_private_technical_content(tmp_path: Path) -> None:
    fidelity = build_extraction_fidelity_policy(out=tmp_path / "fidelity.yaml", results_dir=tmp_path / "results")
    redaction = build_redaction_policy(out=tmp_path / "redaction.yaml", results_dir=tmp_path / "results")
    scraper = build_scraper_capture_policy(out=tmp_path / "scraper.yaml", results_dir=tmp_path / "results")

    private = fidelity["private_deep_research_extract_view"]
    assert private["preserve_runes"] is True
    assert private["preserve_numbers"] is True
    assert private["preserve_tables"] is True
    assert private["preserve_cell_coordinates"] is True
    assert redaction["redaction_log_required"] is True
    assert "private Discord identities" in redaction["redaction_targets"]
    assert any(profile["source_type"] == "reddit_post" for profile in scraper["capture_profiles"])
    assert scraper["network_fetch_performed"] is False
