from __future__ import annotations

import json
from pathlib import Path

from test_stage5eg_common import ensure_stage5eg_built


def test_codex_agents_are_read_only() -> None:
    ensure_stage5eg_built()

    for path in sorted(Path(".codex/agents").glob("*.toml")):
        text = path.read_text(encoding="utf-8")
        assert 'sandbox_mode = "read-only"' in text


def test_hooks_use_command_handlers_and_do_not_invoke_agents() -> None:
    ensure_stage5eg_built()

    hooks = json.loads(Path(".codex/hooks.json").read_text(encoding="utf-8"))
    rendered = json.dumps(hooks, sort_keys=True)

    assert '"type": "command"' in rendered
    assert "doc-drift-auditor" not in rendered
    assert "current-truth-auditor" not in rendered
    assert "closeout-reviewer" not in rendered
    assert "audit-stale-current-claims" in Path(".codex/hooks/stop_doc_staleness_guard.py").read_text(
        encoding="utf-8"
    )


def test_codex_hooks_are_declared_not_claimed_effective() -> None:
    from test_stage5eg_common import stage5eg_data

    policy = stage5eg_data("stop_hook_policy")

    assert policy["project_hooks_declared_now"] is True
    assert policy["project_hooks_require_operator_trust_before_effective"] is True
    assert policy["active_hooks_effective_now"] is False
    assert policy["blocking_hooks_effective_now"] is False


def test_daily_doc_staleness_automation_prefers_local_venv_and_stays_report_only() -> None:
    prompt = Path("docs/automations/daily-doc-staleness-triage.prompt.md").read_text(encoding="utf-8")
    setup = Path("docs/automations/daily-doc-staleness-triage.setup.md").read_text(encoding="utf-8")
    combined = f"{prompt}\n{setup}"

    expected_command = (
        r".\.venv\Scripts\python.exe -m libreprimus.cli consistency "
        "audit-stale-current-claims --strict --report-only"
    )

    assert expected_command in combined
    assert "Execution environment: local repository checkout." in setup
    assert "Do not edit files." in prompt
    assert "Do not commit." in prompt
    assert "Environment failures must be reported explicitly" in setup
    assert "must not be counted as document drift" in setup
