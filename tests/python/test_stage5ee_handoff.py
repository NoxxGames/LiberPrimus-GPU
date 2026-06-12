from __future__ import annotations

from libreprimus.token_block.stage5ee import (
    validate_stage5ee_credential_redaction_policy,
    validate_stage5ee_handoff_continuity,
)
from test_stage5ee_common import ensure_stage5ee_built, load_yaml


def test_stage5ee_handoff_uses_codex_output_root_only() -> None:
    ensure_stage5ee_built()
    handoff = load_yaml("data/source-harvester/stage5ee-codex-handoff-policy.yaml")

    assert validate_stage5ee_handoff_continuity().validation_error_count == 0
    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["codex_output_used"] is False
    assert handoff["completion_summary_committed"] is False


def test_stage5ee_credential_redaction_policy_is_preserved() -> None:
    ensure_stage5ee_built()
    policy = load_yaml("data/source-harvester/stage5ee-credential-redaction-policy-preservation.yaml")

    assert validate_stage5ee_credential_redaction_policy().validation_error_count == 0
    assert policy["credential_like_remote_count"] == 0
    assert policy["raw_source_body_included"] is False
