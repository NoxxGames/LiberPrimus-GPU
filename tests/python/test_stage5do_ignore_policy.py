from __future__ import annotations

from pathlib import Path

from test_stage5do_common import ROOT, ensure_stage5do_built, git_check_ignore


def test_stage5do_generated_outputs_and_handoff_are_ignored() -> None:
    ensure_stage5do_built()

    assert git_check_ignore("experiments/results/token-block/stage5do/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5do/number_facts_source_lock_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5do/potential_hint_source_lock_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5do/image_anchor_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5do/candidate_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5do/preservation_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5do/warnings.jsonl")
    assert git_check_ignore("codex-output/stage5do-codex-completion.md")


def test_stage5do_raw_numberfacts_and_potentialhint_sources_remain_ignored() -> None:
    ensure_stage5do_built()

    assert git_check_ignore("third_party/NumberFactsCollection/messages.txt")
    assert git_check_ignore("third_party/NumberFactsCollection/futhork_rune_values_are_used.jpg")
    assert git_check_ignore("third_party/PotentialHint-3301-on-Page32/messages.txt")
    assert git_check_ignore("third_party/PotentialHint-3301-on-Page32/page-32.jpg")
    assert git_check_ignore("third_party/PotentialHint-3301-on-Page32/prime_color_frequencies.txt")


def test_stage5do_deprecated_codex_output_absent() -> None:
    ensure_stage5do_built()

    assert not (ROOT / "codex_output").exists()
    assert Path("codex-output").as_posix() == "codex-output"
