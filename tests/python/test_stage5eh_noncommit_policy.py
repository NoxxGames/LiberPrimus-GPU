from __future__ import annotations

from pathlib import Path

from test_stage5eh_common import stage5eh_data


def test_stage5eh_raw_and_generated_roots_not_tracked_by_stage_records() -> None:
    proof = stage5eh_data("raw_source_noncommit_proof")

    assert proof["third_party_raw_files_staged"] is False
    assert proof["data_raw_files_staged"] is False
    assert proof["experiments_results_staged"] is False
    assert proof["codex_output_staged"] is False
    assert proof["raw_third_party_files_committed"] is False


def test_stage5eh_completion_handoff_is_ignored_path() -> None:
    handoff = stage5eh_data("codex_handoff_policy")

    assert handoff["completion_summary_path"] == "codex-output/stage5eh-codex-completion.md"
    assert handoff["codex_output_committed"] is False
    assert handoff["completion_summary_path"].startswith("codex-output/")
    assert "codex-output/**" in Path(".gitignore").read_text(encoding="utf-8")
