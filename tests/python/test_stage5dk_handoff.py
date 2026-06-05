from __future__ import annotations

from libreprimus.token_block import stage5dk
from test_stage5dk_common import ensure_stage5dk_built, load_yaml, write_temp_yaml


def test_stage5dk_handoff_uses_codex_output_and_not_codex_output_underscore() -> None:
    ensure_stage5dk_built()
    handoff = load_yaml("data/source-harvester/stage5dk-codex-handoff-policy.yaml")

    assert handoff["codex_completion_path"] == "codex-output/stage5dk-codex-completion.md"
    assert handoff["deprecated_codex_output_path"] == "codex_output"
    assert handoff["codex_output_canonical"] is True
    assert handoff["codex_output_used"] is False
    assert not (stage5dk.REPO_ROOT / "codex_output").exists()


def test_stage5dk_handoff_validator_rejects_bad_completion_path(
    monkeypatch: object,
    tmp_path,
) -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/source-harvester/stage5dk-codex-handoff-policy.yaml")
    record["codex_completion_path"] = "codex_output/stage5dk.md"
    path = write_temp_yaml(tmp_path / "handoff.yaml", record)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "codex_handoff_policy", path)

    result = stage5dk.validate_stage5dk_handoff_continuity()
    assert result.validation_error_count > 0
    assert any("codex_completion_path_changed" in error for error in result.errors)


def test_stage5dk_credential_redaction_policy_is_preserved() -> None:
    ensure_stage5dk_built()
    record = load_yaml(
        "data/source-harvester/stage5dk-credential-redaction-policy-preservation.yaml"
    )

    assert record["credential_redaction_policy_preserved"] is True
    assert record["secret_values_committed"] is False
    assert record["raw_private_content_committed"] is False
    assert record["network_credentials_required_now"] is False
    assert stage5dk.validate_stage5dk_credential_redaction_policy().validation_error_count == 0
