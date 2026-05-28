from subprocess import run

from test_stage5bm_common import ROOT, run_git_check_ignore


def test_stage5bm_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert run_git_check_ignore("experiments/results/token-block/stage5bm/string4-stage5aw-branch-membership.json")
    assert run_git_check_ignore("experiments/results/historical-route/stage5bm/summary.json")
    assert run_git_check_ignore("codex-output/stage5bm-codex-completion.md")


def test_stage5bm_raw_sources_are_not_tracked_or_staged() -> None:
    assert run_git_check_ignore("third_party/CiadaSolversIddqd_v2/byte-strings/byte-strings")

    status = run(
        ["git", "status", "--short", "--", "third_party/CiadaSolversIddqd_v2", "codex-output"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert not status.strip()
