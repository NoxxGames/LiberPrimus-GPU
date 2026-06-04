from __future__ import annotations

from libreprimus.token_block.stage5dg import (
    CODEX_COMPLETION_PATH,
    validate_stage5dg_credential_redaction_policy,
    validate_stage5dg_handoff_continuity,
)

from test_stage5dg_common import ensure_stage5dg_built, git_check_ignore, load_yaml


def test_stage5dg_handoff_uses_hyphenated_ignored_codex_output() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_handoff_continuity()

    assert errors == []
    assert counts["stage5dg_codex_completion_summary_present"] is True
    assert git_check_ignore(CODEX_COMPLETION_PATH.as_posix())
    assert "pending" not in CODEX_COMPLETION_PATH.read_text(encoding="utf-8").lower()

    payload = load_yaml("data/source-harvester/stage5dg-codex-handoff-policy.yaml")
    assert payload["codex_output_used"] is False
    assert payload["codex_completion_summary_committed"] is False


def test_stage5dg_credential_redaction_policy_preserved() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_credential_redaction_policy()

    assert errors == []
    assert counts["remote_url_values_printed"] is False
