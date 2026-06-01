from libreprimus.token_block.stage5cq import CODEX_COMPLETION_PATH, validate_stage5cq_handoff_restoration

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_handoff_uses_hyphenated_codex_output_root() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/source-harvester/stage5cq-codex-handoff-policy.yaml")
    assert payload["canonical_codex_handoff_root"] == "codex-output"
    assert payload["codex_output_used"] is False
    assert payload["codex_completion_summary_committed"] is False
    assert payload["stage5cq_codex_completion_summary_required"] is True
    assert CODEX_COMPLETION_PATH.is_file()
    counts, errors = validate_stage5cq_handoff_restoration()
    assert not errors
    assert counts["stage5cq_handoff_restoration_valid"] is True


def test_stage5cq_records_stage5co_completion_warning() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/source-harvester/stage5cq-completion-summary-restoration.yaml")
    assert payload["stage5co_missing_completion_summary_warning_integrated"] is True
    assert payload["stage5co_completion_summary_fabricated"] is False
