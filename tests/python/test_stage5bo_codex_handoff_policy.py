from test_stage5bo_common import load_yaml, run_git_check_ignore


def test_stage5bo_handoff_uses_hyphenated_codex_output_only() -> None:
    payload = load_yaml("data/source-harvester/stage5bo-codex-handoff-policy.yaml")

    assert payload["canonical_codex_handoff_root"] == "codex-output"
    assert payload["codex_completion_summary_path"] == "codex-output/stage5bo-codex-completion.md"
    assert payload["deprecated_codex_output_root"] == "codex_output"
    assert payload["codex_output_used"] is False
    assert run_git_check_ignore("codex-output/stage5bo-codex-completion.md")
    assert run_git_check_ignore("codex_output/stage5bo-codex-completion.md")
