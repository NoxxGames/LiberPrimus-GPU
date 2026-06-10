from __future__ import annotations

from pathlib import Path

from test_stage5dx_common import ensure_stage5dx_built, load_yaml


def test_stage5dx_handoff_uses_codex_output_and_not_deprecated_root() -> None:
    ensure_stage5dx_built()
    handoff = load_yaml("data/source-harvester/stage5dx-codex-handoff-policy.yaml")

    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["deprecated_codex_output_root_used"] is False
    assert handoff["codex_output_used"] is False
    assert not Path("codex_output").exists()


def test_stage5dx_credential_redaction_and_noncommit_records_are_preserved() -> None:
    ensure_stage5dx_built()
    credential = load_yaml("data/source-harvester/stage5dx-credential-redaction-policy-preservation.yaml")
    noncommit = load_yaml("data/source-harvester/stage5dx-raw-source-noncommit-proof.yaml")

    assert credential["credential_like_remote_count"] == 0
    assert credential["credential_redaction_policy_preserved"] is True
    assert noncommit["raw_source_body_included"] is False
    assert noncommit["raw_source_files_committed"] is False
