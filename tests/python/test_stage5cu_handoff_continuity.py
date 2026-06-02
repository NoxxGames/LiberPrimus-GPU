from libreprimus.token_block.stage5cu import CODEX_COMPLETION_PATH, validate_stage5cu_handoff_continuity

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_handoff_uses_hyphenated_codex_output_root_and_no_placeholders() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/source-harvester/stage5cu-codex-handoff-policy.yaml")
    assert payload["canonical_codex_handoff_root"] == "codex-output"
    assert payload["codex_output_used"] is False
    text = CODEX_COMPLETION_PATH.read_text(encoding="utf-8").lower()
    assert "pending" not in text
    assert "todo" not in text
    assert "tbd" not in text
    counts, errors = validate_stage5cu_handoff_continuity()
    assert not errors
    assert counts["stage5cu_handoff_continuity_valid"] is True
