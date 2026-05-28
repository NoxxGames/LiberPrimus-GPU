from test_stage5bn_common import load_yaml


def test_stage5bn_codex_handoff_uses_hyphenated_root_only() -> None:
    payload = load_yaml("data/source-harvester/stage5bn-codex-handoff-policy.yaml")

    assert payload["canonical_handoff_root"] == "codex-output"
    assert payload["codex_completion_summary_path"] == "codex-output/stage5bn-codex-completion.md"
    assert payload["deprecated_handoff_root"] == "codex_output"
    assert payload["codex_output_used"] is False
    assert payload["codex_output_directory_created"] is False
    assert payload["codex_completion_summary_committed"] is False
