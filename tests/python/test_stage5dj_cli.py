from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from libreprimus.token_block import stage5dj
from test_stage5dj_common import ROOT


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dj_cli_validate_and_summary() -> None:
    validate_output = run_cli("validate-stage5dj")
    assert "token_block_stage5dj_valid=true" in validate_output

    summary_output = run_cli("stage5dj-summary")
    assert "music_candidate_family_id=music_3301_instar_crab_canon_v0" in summary_output
    assert "pivot_option_count=7" in summary_output
    assert "execution_authorized_now=false" in summary_output
    assert "recommended_next_stage_id=stage-5dk" in summary_output


def test_stage5dj_focused_cli_commands() -> None:
    focused_commands = [
        ("validate-stage5dj-music-source-lock", "token_block_stage5dj_music_source_lock_valid=true"),
        ("validate-stage5dj-music-file-hashes", "token_block_stage5dj_music_file_hashes_valid=true"),
        ("validate-stage5dj-mp3-metadata", "token_block_stage5dj_mp3_metadata_valid=true"),
        ("validate-stage5dj-pdf-metadata", "token_block_stage5dj_pdf_metadata_valid=true"),
        ("validate-stage5dj-761-parable", "token_block_stage5dj_761_parable_valid=true"),
        (
            "validate-stage5dj-music-number-analysis",
            "token_block_stage5dj_music_number_analysis_valid=true",
        ),
        (
            "validate-stage5dj-music-candidate-family",
            "token_block_stage5dj_music_candidate_family_valid=true",
        ),
        ("validate-stage5dj-pivot-integration", "token_block_stage5dj_pivot_integration_valid=true"),
        (
            "validate-stage5dj-stage5dg-preservation",
            "token_block_stage5dj_stage5dg_preservation_valid=true",
        ),
        (
            "validate-stage5dj-stage5bd-preservation",
            "token_block_stage5dj_stage5bd_preservation_valid=true",
        ),
        (
            "validate-stage5dj-active-lineage-preservation",
            "token_block_stage5dj_active_lineage_preservation_valid=true",
        ),
        ("validate-stage5dj-sidecar-gates", "token_block_stage5dj_sidecar_gates_valid=true"),
        (
            "validate-stage5dj-handoff-continuity",
            "token_block_stage5dj_handoff_continuity_valid=true",
        ),
        (
            "validate-stage5dj-credential-redaction-policy",
            "token_block_stage5dj_credential_redaction_policy_valid=true",
        ),
        ("validate-stage5dj-governance-scope", "token_block_stage5dj_governance_scope_valid=true"),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)


def test_stage5dj_build_cli_reports_music_pivot() -> None:
    output = run_cli("build-stage5dj")
    assert "stage_id=stage-5dj" in output
    assert "music_candidate_family_id=music_3301_instar_crab_canon_v0" in output
    assert "pivot_option_count=7" in output
    assert "recommended_next_stage_id=stage-5dk" in output


def test_stage5dj_validation_allows_missing_ignored_generated_reports(tmp_path: Path) -> None:
    counts, errors = stage5dj.validate_stage5dj(results_dir=tmp_path / "missing-stage5dj")

    assert counts["missing_generated_report_count"] == len(stage5dj.GENERATED_REPORT_NAMES)
    assert counts["missing_generated_reports_allowed"] is True
    assert not [error for error in errors if error.startswith("missing_generated_report:")]


def test_stage5dj_handoff_allows_missing_ignored_codex_output(
    monkeypatch: object, tmp_path: Path
) -> None:
    monkeypatch.setattr(stage5dj, "CODEX_COMPLETION_PATH", tmp_path / "missing.md")

    counts, errors = stage5dj.validate_stage5dj_handoff_continuity()

    assert errors == []
    assert counts["stage5dj_codex_completion_summary_present"] is False
    assert counts["stage5dj_codex_completion_summary_missing_allowed"] is True
