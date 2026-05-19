from __future__ import annotations

from pathlib import Path


def test_stage4a_followup_wiki_publish_report_records_blocker() -> None:
    report = Path("docs/github/wiki-publish-report.md").read_text(encoding="utf-8")

    assert "Stage 4A Follow-Up Diagnosis" in report
    assert "Wiki remote accessible: false" in report
    assert "Publish attempted: true" in report
    assert "Repository not found" in report
    assert "create an initial Wiki page in the GitHub UI" in report
