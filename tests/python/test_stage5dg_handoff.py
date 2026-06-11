from __future__ import annotations

from libreprimus.token_block.stage5dg import (
    CODEX_COMPLETION_PATH,
    validate_stage5dg_credential_redaction_policy,
)

from test_stage5dg_common import ensure_stage5dg_built, git_check_ignore, load_yaml


def test_stage5dg_handoff_uses_hyphenated_ignored_codex_output() -> None:
    ensure_stage5dg_built()
    assert git_check_ignore(CODEX_COMPLETION_PATH.as_posix())
    assert CODEX_COMPLETION_PATH.as_posix() == "codex-output/stage5dg-codex-completion.md"
    if CODEX_COMPLETION_PATH.exists():
        assert "pending" not in CODEX_COMPLETION_PATH.read_text(encoding="utf-8").lower()

    payload = load_yaml("data/source-harvester/stage5dg-codex-handoff-policy.yaml")
    assert payload["codex_output_used"] is False
    assert payload["codex_completion_summary_committed"] is False
    assert payload["stage5dg_codex_completion_summary_required"] is True
    assert payload["stage5dg_codex_completion_summary_path"] == CODEX_COMPLETION_PATH.as_posix()


def test_stage5dg_credential_redaction_policy_preserved() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_credential_redaction_policy()

    assert errors == []
    assert counts["remote_url_values_printed"] is False
