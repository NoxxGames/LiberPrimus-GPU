from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_advisory_hooks_remain_inactive() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_advisory_hooks()
    policy = load_yaml("data/project-state/stage5ef-advisory-hook-policy.yaml")

    assert result.validation_error_count == 0
    assert policy["active_hooks_created_now"] is False
    assert policy["blocking_hooks_enabled_now"] is False
    stage5eg_policy_path = Path("data/project-state/stage5eg-stop-hook-policy.yaml")
    if Path(".codex/hooks.json").exists():
        stage5eg_policy = yaml.safe_load(stage5eg_policy_path.read_text(encoding="utf-8"))
        assert stage5eg_policy["project_hooks_declared_now"] is True
        assert stage5eg_policy["active_hooks_effective_now"] is False
        assert stage5eg_policy["hooks_use_deterministic_scanner_now"] is True
        assert stage5eg_policy["hooks_invoke_custom_agents_now"] is False
    else:
        assert not stage5eg_policy_path.exists()
    assert not Path(".codex/hooks.yaml").exists()
