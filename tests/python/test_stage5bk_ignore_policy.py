import subprocess

from test_stage5bk_common import ROOT


def test_stage5bk_raw_generated_and_codex_outputs_are_ignored() -> None:
    for path in [
        "codex-output/stage5bk-codex-completion.md",
        "experiments/results/historical-route/stage5bk/summary.json",
        "experiments/results/token-block/stage5bk/token_block_impact.json",
        "third_party/CiadaSolversIddqd_v2/byte-strings/byte-strings",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
        assert result.returncode == 0, path


def test_stage5bk_deprecated_codex_output_root_absent() -> None:
    assert not (ROOT / "codex_output").exists()
