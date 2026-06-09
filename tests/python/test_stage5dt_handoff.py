from __future__ import annotations

from test_stage5dt_common import ensure_stage5dt_built, load_yaml


def test_stage5dt_handoff_uses_codex_output_and_recommends_review_stage() -> None:
    ensure_stage5dt_built()
    handoff = load_yaml("data/source-harvester/stage5dt-codex-handoff-policy.yaml")
    decision = load_yaml("data/project-state/stage5dt-next-stage-decision.yaml")

    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["codex_output_used"] is False
    assert decision["selected_next_stage_id"] == "stage-5du"
    assert decision["selected_next_prompt_type"] == "assistant_or_operator_review"
    assert decision["selected_next_stage_authorizes_execution"] is False
