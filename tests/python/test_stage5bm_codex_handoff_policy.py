from pathlib import Path

from test_stage5bm_common import load_yaml


def test_stage5bm_codex_handoff_policy_uses_hyphenated_root() -> None:
    record = load_yaml("data/source-harvester/stage5bm-codex-handoff-policy.yaml")

    assert record["canonical_handoff_root"] == "codex-output"
    assert record["deprecated_handoff_root"] == "codex_output"
    assert record["codex_completion_summary_path"] == "codex-output/stage5bm-codex-completion.md"
    assert record["codex_output_used"] is False
    assert not Path("codex_output").exists()
