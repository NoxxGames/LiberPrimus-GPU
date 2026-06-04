from __future__ import annotations

from test_stage5de_common import ensure_stage5de_built, git_check_ignore, load_yaml


def test_stage5de_handoff_uses_hyphenated_codex_output() -> None:
    ensure_stage5de_built()
    handoff = load_yaml("data/source-harvester/stage5de-codex-handoff-policy.yaml")

    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["codex_output_used"] is False
    assert handoff["stage5de_codex_completion_summary_written_locally_before_final_response"] is True
    assert git_check_ignore("codex-output/stage5de-codex-completion.md")


def test_stage5de_credential_redaction_policy_preserved() -> None:
    ensure_stage5de_built()
    credential = load_yaml(
        "data/source-harvester/stage5de-credential-redaction-policy-preservation.yaml"
    )

    assert credential["remote_url_values_printed"] is False
    assert credential["secret_values_printed_or_committed"] is False
    assert credential["credential_redaction_policy_preserved"] is True
