from __future__ import annotations

from pathlib import Path

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_handoff_files_are_ignored_and_uncommitted() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_handoff_continuity()
    policy = load_yaml("data/source-harvester/stage5ef-codex-handoff-policy.yaml")

    assert result.validation_error_count == 0
    assert policy["codex_output_committed"] is False
    assert Path("codex-output/stage5ef-codex-plan.md").exists()
    assert Path("codex-output/stage5ef-codex-completion.md").exists()
