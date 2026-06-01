from libreprimus.token_block.stage5cs import CODEX_COMPLETION_PATH, validate_stage5cs_handoff_continuity

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_handoff_uses_hyphenated_codex_output_root() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/source-harvester/stage5cs-codex-handoff-policy.yaml")
    assert payload["canonical_codex_handoff_root"] == "codex-output"
    assert payload["codex_output_used"] is False
    assert payload["codex_completion_summary_committed"] is False
    assert payload["stage5cs_codex_completion_summary_required"] is True
    assert CODEX_COMPLETION_PATH.is_file()
    counts, errors = validate_stage5cs_handoff_continuity()
    assert not errors
    assert counts["stage5cs_handoff_continuity_valid"] is True
