from __future__ import annotations

import subprocess

from test_stage5ea_common import ROOT, ensure_stage5ea_built, load_yaml


def test_stage5ea_handoff_uses_codex_output_not_underscore_root() -> None:
    ensure_stage5ea_built()

    record = load_yaml("data/source-harvester/stage5ea-codex-handoff-policy.yaml")
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", "codex-output/stage5ea-codex-completion.md"],
        cwd=ROOT,
        check=False,
    )

    assert record["canonical_handoff_root"] == "codex-output"
    assert record["codex_output_used"] is False
    assert record["codex_underscore_output_root_forbidden"] is True
    assert ignored.returncode == 0
