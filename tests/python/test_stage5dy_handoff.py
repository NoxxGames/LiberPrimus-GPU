from __future__ import annotations

from test_stage5dy_common import ensure_stage5dy_built, load_yaml


def test_handoff_uses_codex_output_and_not_deprecated_root() -> None:
    ensure_stage5dy_built()
    handoff = load_yaml("data/source-harvester/stage5dy-codex-handoff-policy.yaml")

    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["codex_output_used"] is False
    assert handoff["completion_summary_committed"] is False
