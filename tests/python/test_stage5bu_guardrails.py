from test_stage5bu_common import load_yaml


def test_stage5bu_guardrails_block_execution_and_handoff_uses_codex_output() -> None:
    guardrail = load_yaml("data/historical-route/stage5bu-guardrail.yaml")
    handoff = load_yaml("data/source-harvester/stage5bu-codex-handoff-policy.yaml")
    next_stage = load_yaml("data/project-state/stage5bu-next-stage-decision.yaml")

    assert guardrail["future_token_block_execution_remains_blocked"] is True
    assert guardrail["real_byte_stream_generated"] is False
    assert guardrail["cuda_execution_performed"] is False
    assert guardrail["solve_claim"] is False
    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["codex_output_used"] is False
    assert next_stage["selected_next_stage_id"] == "stage-5bv"
    assert next_stage["token_block_execution_selected"] is False
