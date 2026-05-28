from test_stage5bq_common import load_yaml, run_git_check_ignore


def test_stage5bq_handoff_uses_hyphenated_codex_output_only() -> None:
    payload = load_yaml("data/source-harvester/stage5bq-codex-handoff-policy.yaml")

    assert payload["canonical_codex_handoff_root"] == "codex-output"
    assert payload["deprecated_codex_output_root"] == "codex_output"
    assert payload["codex_completion_summary_path"] == "codex-output/stage5bq-codex-completion.md"
    assert payload["codex_output_used"] is False
    assert run_git_check_ignore("codex-output/stage5bq-codex-completion.md")


def test_stage5bq_next_stage_selects_deep_research_not_execution() -> None:
    payload = load_yaml("data/project-state/stage5bq-next-stage-decision.yaml")

    assert payload["selected_next_stage_id"] == "stage-5br"
    assert payload["selected_next_prompt_type"] == "deep_research_review"
    assert payload["token_block_execution_selected"] is False
    assert payload["byte_stream_generation_selected"] is False
    assert payload["cuda_selected"] is False
