from __future__ import annotations

from pathlib import Path

from test_stage5dn_common import ROOT, ensure_stage5dn_built, git_check_ignore


def test_stage5dn_generated_outputs_and_handoff_are_ignored() -> None:
    ensure_stage5dn_built()

    assert git_check_ignore("experiments/results/token-block/stage5dn/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5dn/disk_source_lock_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5dn/disk_file_inventory.json")
    assert git_check_ignore("experiments/results/token-block/stage5dn/candidate_bridge_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5dn/preservation_report.json")
    assert git_check_ignore("codex-output/stage5dn-codex-completion.md")


def test_stage5dn_raw_diskcipher_sources_remain_ignored() -> None:
    ensure_stage5dn_built()

    assert git_check_ignore("third_party/DiskCipherStuff/DiskCipherStuff/results.png")
    assert git_check_ignore("third_party/DiskCipherStuff/DiskCipherStuff/message_bodies.txt")
    assert git_check_ignore("third_party/DiskCipherStuff/DiskCipherStuff/alberti_v26_branchfix.html")


def test_stage5dn_deprecated_codex_output_absent() -> None:
    ensure_stage5dn_built()

    assert not (ROOT / "codex_output").exists()
    assert Path("codex-output").as_posix() == "codex-output"
