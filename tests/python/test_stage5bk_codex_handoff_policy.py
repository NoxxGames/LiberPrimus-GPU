import subprocess
from pathlib import Path

from test_stage5bk_common import ROOT, load_yaml


def test_stage5bk_codex_handoff_uses_hyphenated_root_only() -> None:
    payload = load_yaml("data/source-harvester/stage5bk-codex-handoff-policy-correction.yaml")
    assert payload["canonical_handoff_root"] == "codex-output"
    assert payload["deprecated_handoff_root"] == "codex_output"
    assert payload["future_stages_must_use_deprecated_root"] is False
    assert payload["codex_output_used"] is False
    completion_path = "codex-output/stage5bk-codex-completion.md"
    result = subprocess.run(
        ["git", "check-ignore", "-q", completion_path],
        cwd=ROOT,
        check=False,
    )
    assert result.returncode == 0
    assert not Path(ROOT / "codex_output").exists()
