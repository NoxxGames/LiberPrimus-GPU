from pathlib import Path

from test_stage5cw_common import ensure_stage5cw_built, git_check_ignore, load_yaml


def test_stage5cw_handoff_uses_codex_output_hyphenated_root_only() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/source-harvester/stage5cw-codex-handoff-policy.yaml")

    assert payload["canonical_codex_handoff_root"] == "codex-output"
    assert payload["deprecated_handoff_root"] == "codex_output"
    assert payload["codex_output_used"] is False
    assert Path("codex_output").exists() is False
    assert git_check_ignore("codex-output/stage5cw-codex-completion.md")
    assert payload["codex_completion_summary_committed"] is False
