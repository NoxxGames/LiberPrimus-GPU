from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, git_check_ignore, load_yaml


def test_stage5ds_handoff_root_and_raw_ignores() -> None:
    ensure_stage5ds_built()
    policy = load_yaml("data/source-harvester/stage5ds-codex-handoff-policy.yaml")
    assert policy["canonical_codex_handoff_root"] == "codex-output"
    assert policy["codex_output_used"] is False
    assert git_check_ignore("codex-output/stage5ds-codex-completion.md")
    assert git_check_ignore("third_party/CicadaMusic/community-theory/messages.txt")
    assert git_check_ignore("experiments/results/token-block/stage5ds/example.json")
