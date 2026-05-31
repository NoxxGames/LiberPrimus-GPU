from pathlib import Path

from test_stage5ck_common import ROOT, git_check_ignore


def test_stage5ck_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5ck/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5ck/fixture_pack_report.json")
    assert git_check_ignore("codex-output/stage5ck-codex-completion.md")


def test_stage5ck_deprecated_codex_output_directory_absent() -> None:
    assert not (ROOT / "codex_output").exists()


def test_stage5ck_raw_and_human_review_roots_are_not_part_of_record_set() -> None:
    forbidden_prefixes = ("data/raw/", "human-review-packs/", "third_party/")
    for path in Path(ROOT / "data/project-state").glob("stage5ck*.yaml"):
        text = path.read_text(encoding="utf-8")
        assert not any(prefix in text for prefix in forbidden_prefixes)
