from pathlib import Path

from test_stage5cm_common import ROOT, git_check_ignore


def test_stage5cm_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5cm/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5cm/readiness_boundary_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5cm/credential_scan.json")
    assert git_check_ignore("experiments/results/token-block/stage5cm/source_digest_index.json")
    assert git_check_ignore("codex-output/stage5cm-codex-completion.md")


def test_stage5cm_deprecated_codex_output_root_absent() -> None:
    assert not (ROOT / "codex_output").exists()


def test_stage5cm_raw_and_deep_research_reports_not_tracked() -> None:
    assert git_check_ignore("data/raw/example.txt")
    assert git_check_ignore(
        "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
        "21_Stage-5CK-Deep-Research-Review.md"
    )
    assert not Path("codex_output").exists()
