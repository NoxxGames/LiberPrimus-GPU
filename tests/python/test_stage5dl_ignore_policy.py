from __future__ import annotations

from test_stage5dl_common import ensure_stage5dl_built, git_check_ignore, load_yaml


def test_stage5dl_generated_outputs_and_handoff_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5dl/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5dl/source_lock_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5dl/warnings.jsonl")
    assert git_check_ignore("codex-output/stage5dl-codex-completion.md")


def test_stage5dl_raw_third_party_sources_are_ignored() -> None:
    assert git_check_ignore("third_party/NumberTriangleStuff/v2-number-triangles/messages.txt")
    assert git_check_ignore("third_party/DiskCipherStuff/DiskCipherStuff/alberti_v26_branchfix.html")
    assert git_check_ignore("third_party/RedditStuff/FibonacciSequence/fibonacci_sequence_3301.jpeg")
    assert git_check_ignore("third_party/koan_page.png")


def test_stage5dl_records_no_raw_or_generated_commits() -> None:
    ensure_stage5dl_built()
    summary = load_yaml("data/project-state/stage5dl-summary.yaml")
    digest = load_yaml("data/project-state/stage5dl-source-digest-index.yaml")

    assert summary["raw_body_committed"] is False
    assert summary["generated_outputs_committed"] is False
    assert digest["raw_files_committed"] is False
    assert digest["generated_outputs_committed"] is False
