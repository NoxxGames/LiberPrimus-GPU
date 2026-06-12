from __future__ import annotations

from pathlib import Path

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_advisory_hooks_remain_inactive() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_advisory_hooks()
    policy = load_yaml("data/project-state/stage5ef-advisory-hook-policy.yaml")

    assert result.validation_error_count == 0
    assert policy["active_hooks_created_now"] is False
    assert policy["blocking_hooks_enabled_now"] is False
    assert not Path(".codex/hooks.json").exists()
    assert not Path(".codex/hooks.yaml").exists()
