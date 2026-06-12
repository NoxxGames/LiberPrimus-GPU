from __future__ import annotations

from pathlib import Path

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_automation_templates_are_report_only() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_automation_templates()
    registry = load_yaml("data/project-state/stage5ef-automation-audit-template-registry.yaml")

    assert result.validation_error_count == 0
    assert registry["codex_automations_scheduled_now"] is False
    assert registry["automation_auto_commit_enabled"] is False
    for template in registry["automation_templates"]:
        assert template["report_only"] is True
        assert template["auto_commit_allowed"] is False
        assert "report-only" in Path(template["path"]).read_text(encoding="utf-8").lower()
