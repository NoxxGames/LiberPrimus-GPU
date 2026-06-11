from __future__ import annotations

from test_stage5eb_common import ROOT, ensure_stage5eb_built, load_yaml


def test_stage5eb_keeps_active_byte_and_execution_gates_closed() -> None:
    ensure_stage5eb_built()

    active = load_yaml("data/token-block/stage5eb-no-active-ingestion-proof.yaml")
    byte_stream = load_yaml("data/token-block/stage5eb-no-byte-stream-transition-gate.yaml")
    execution = load_yaml("data/token-block/stage5eb-no-execution-transition-gate.yaml")

    assert active["active_ingestion_gate_closed"] is True
    assert active["authorized_now"] is False
    assert byte_stream["byte_stream_transition_gate_closed"] is True
    assert byte_stream["authorized_now"] is False
    assert execution["execution_transition_gate_closed"] is True
    assert execution["authorized_now"] is False


def test_stage5eb_preserves_codex_output_handoff_and_credential_policy() -> None:
    ensure_stage5eb_built()

    handoff = load_yaml("data/source-harvester/stage5eb-codex-handoff-policy.yaml")
    redaction = load_yaml("data/source-harvester/stage5eb-credential-redaction-policy-preservation.yaml")

    assert handoff["canonical_handoff_root"] == "codex-output"
    assert handoff["codex_output_used"] is False
    assert handoff["codex_underscore_output_root_forbidden"] is True
    assert not (ROOT / "codex_output").exists()
    assert redaction["credential_redaction_policy_preserved"] is True
    assert redaction["secrets_or_tokens_committed"] is False
