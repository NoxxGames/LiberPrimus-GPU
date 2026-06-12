from __future__ import annotations

from pathlib import Path

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_skills_are_deferred() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_skill_readiness()
    policy = load_yaml("data/project-state/stage5ef-skill-readiness-policy.yaml")

    assert result.validation_error_count == 0
    assert policy["repo_local_skills_installed_now"] is False
    assert policy["skills_deferred_because_agents_skills_not_repo_convention"] is True
    assert not Path(".agents/skills").exists()
