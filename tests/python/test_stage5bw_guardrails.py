from test_stage5bw_common import git_check_ignore, load_yaml


def test_stage5bw_guardrails_block_forbidden_work() -> None:
    guardrail = load_yaml("data/historical-route/stage5bw-guardrail.yaml")

    for key in (
        "real_byte_stream_generated",
        "variant_materialisation_performed",
        "dwh_hash_search_performed",
        "decode_attempt_performed",
        "scoring_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "stego_tool_execution_performed",
        "image_forensics_performed",
        "ocr_performed",
        "method_status_upgraded",
        "solve_claim",
    ):
        assert guardrail[key] is False
    assert guardrail["future_token_block_execution_remains_blocked"] is True


def test_stage5bw_codex_output_policy() -> None:
    handoff = load_yaml("data/source-harvester/stage5bw-codex-handoff-policy.yaml")
    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["codex_output_used"] is False
    assert git_check_ignore("codex-output/stage5bw-codex-completion.md")
    assert git_check_ignore("experiments/results/token-block/stage5bw/summary.json")
