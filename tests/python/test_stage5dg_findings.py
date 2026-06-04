from __future__ import annotations

from libreprimus.token_block.stage5dg import validate_stage5dg_stage5df_findings

from test_stage5dg_common import ensure_stage5dg_built, load_yaml


def test_stage5dg_findings_integrate_stage5df_accept_with_warnings() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_stage5df_findings()

    assert errors == []
    assert counts["stage5df_verdict"] == "accept_with_warnings"

    payload = load_yaml("data/project-state/stage5dg-stage5df-findings-integration.yaml")
    assert payload["source_review_type"] == "assistant_or_operator_review"
    assert payload["source_review_deep_research_required"] is False
    assert payload["stage5de_accepted_for_next_codex_stage"] is True
    assert payload["stage5de_review_label_anomaly_gate_opening"] is False
