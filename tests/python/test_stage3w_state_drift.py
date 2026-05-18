from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.consistency.runner import CHECK_GROUPS, run_consistency_suite
from libreprimus.consistency.state_drift import (
    DEFAULT_OPERATIONAL_FILES,
    check_state_drift_consistency,
    scan_stale_current_state,
)


def test_stage3w_checker_passes_current_repository_docs() -> None:
    failures = [result for result in check_state_drift_consistency() if result.is_failure]

    assert failures == []


def test_stage3w_checker_fails_current_stage_0a() -> None:
    findings = scan_stale_current_state("Current stage is Stage 0A.\n", "README.md")

    assert findings
    assert findings[0][0] == "stale_current_stage_0a"


def test_stage3w_checker_fails_current_stage_0d() -> None:
    findings = scan_stale_current_state("Current stage: Stage 0D.\n", "AGENTS.md")

    assert findings
    assert findings[0][0] == "stale_current_stage_0d"


def test_stage3w_checker_allows_historical_stage0a_wording() -> None:
    findings = scan_stale_current_state("Implemented since Stage 0A scaffold bootstrap.\n", "README.md")

    assert findings == []


def test_stage3w_checker_allows_development_log_stage_history() -> None:
    findings = scan_stale_current_state("Current stage is Stage 0A.\n", "docs/development-logs/old.md")

    assert findings == []


def test_stage3w_checker_requires_cuda_deferred(tmp_path: Path) -> None:
    _write_minimal_docs(tmp_path, cuda_text="CUDA acceleration is active.\n")

    failures = check_state_drift_consistency(root=tmp_path)

    assert any(result.check_name == "cuda_deferred" for result in failures if result.is_failure)


def test_stage3w_checker_requires_canonical_corpus_inactive(tmp_path: Path) -> None:
    _write_minimal_docs(tmp_path, corpus_text="Canonical corpus is active.\n")

    failures = check_state_drift_consistency(root=tmp_path)

    assert any(
        result.check_name == "canonical_corpus_inactive" for result in failures if result.is_failure
    )


def test_stage3w_checker_requires_page_boundaries_reviewable(tmp_path: Path) -> None:
    _write_minimal_docs(tmp_path, page_text="Page boundaries are final.\n")

    failures = check_state_drift_consistency(root=tmp_path)

    assert any(
        result.check_name == "page_boundaries_reviewable" for result in failures if result.is_failure
    )


def test_stage3w_checker_requires_raw_generated_output_policy(tmp_path: Path) -> None:
    _write_minimal_docs(tmp_path, raw_text="Raw data is public and generated outputs are public.\n")

    failures = check_state_drift_consistency(root=tmp_path)

    assert any(
        result.check_name == "raw_generated_not_committed" for result in failures if result.is_failure
    )


def test_stage3w_checker_requires_discord_raw_log_policy(tmp_path: Path) -> None:
    _write_minimal_docs(tmp_path, discord_text="Discord raw logs may be published.\n")

    failures = check_state_drift_consistency(root=tmp_path)

    assert any(
        result.check_name == "discord_raw_logs_not_committed"
        for result in failures
        if result.is_failure
    )


def test_stage3w_cli_check_state_drift_works() -> None:
    result = CliRunner().invoke(app, ["consistency", "check-state-drift"])

    assert result.exit_code == 0, result.output
    assert "Consistency checks OK" in result.output


def test_stage3w_check_all_includes_state_drift() -> None:
    suite = run_consistency_suite(["state_drift"])

    assert "state_drift" in CHECK_GROUPS
    assert suite.check_count >= len(DEFAULT_OPERATIONAL_FILES)
    assert not suite.has_failures


def _write_minimal_docs(
    root: Path,
    *,
    cuda_text: str = "CUDA is deferred.\n",
    corpus_text: str = "Canonical corpus is inactive.\n",
    page_text: str = "Page boundaries are reviewable.\n",
    raw_text: str = "Raw data and generated outputs are not committed.\n",
    discord_text: str = "Discord raw logs are not committed.\n",
) -> None:
    for relative in DEFAULT_OPERATIONAL_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(
                [
                    "Stage 3V complete.",
                    "Stage 3W state consolidation and anti-drift hardening.",
                    corpus_text,
                    page_text,
                    cuda_text,
                    "No solve claim.",
                    raw_text,
                    discord_text,
                    "Local page images are not committed.",
                ]
            ),
            encoding="utf-8",
        )
    (root / "pyproject.toml").write_text(
        '[project]\ndescription = "Current bounded Liber Primus workbench"\n',
        encoding="utf-8",
    )
