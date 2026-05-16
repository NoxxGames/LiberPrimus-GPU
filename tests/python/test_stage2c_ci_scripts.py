from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT_DIR = REPO / "scripts" / "ci"


def test_ci_scripts_exist() -> None:
    for name in [
        "README.md",
        "run-python-ci.ps1",
        "run-python-ci.sh",
        "run-schema-manifest-checks.ps1",
        "run-schema-manifest-checks.sh",
        "validate-workflow-static.ps1",
        "validate-workflow-static.sh",
        "verify-lock-hashes.ps1",
        "verify-lock-hashes.sh",
        "verify-remote-workflow.ps1",
        "verify-remote-workflow.sh",
    ]:
        assert (SCRIPT_DIR / name).is_file()


def test_shell_scripts_use_strict_mode() -> None:
    for name in [
        "run-python-ci.sh",
        "run-schema-manifest-checks.sh",
        "validate-workflow-static.sh",
        "verify-lock-hashes.sh",
        "verify-remote-workflow.sh",
    ]:
        text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
        assert "set -euo pipefail" in text


def test_powershell_scripts_use_strict_mode() -> None:
    for name in [
        "run-python-ci.ps1",
        "run-schema-manifest-checks.ps1",
        "validate-workflow-static.ps1",
        "verify-lock-hashes.ps1",
        "verify-remote-workflow.ps1",
    ]:
        text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
        assert 'Set-StrictMode -Version Latest' in text
        assert '$ErrorActionPreference = "Stop"' in text


def test_ci_scripts_are_raw_data_free() -> None:
    for script in SCRIPT_DIR.glob("*"):
        if not script.is_file() or script.suffix not in {".ps1", ".sh"}:
            continue
        text = script.read_text(encoding="utf-8").lower()
        assert "data/raw" not in text
        assert "liberprimus-research-report.md" not in text


def test_ci_scripts_do_not_write_generated_result_outputs() -> None:
    for script in SCRIPT_DIR.glob("*"):
        if not script.is_file() or script.suffix not in {".ps1", ".sh"}:
            continue
        text = script.read_text(encoding="utf-8").lower()
        assert "experiments/results" not in text
        assert "data/normalized" not in text


def test_schema_manifest_script_validates_expected_manifests() -> None:
    text = (SCRIPT_DIR / "run-schema-manifest-checks.sh").read_text(encoding="utf-8")
    assert "verify-lock-hashes.sh" in text
    assert "profile summary" in text
    assert "transform-registry validate" in text
    assert "solved-baseline validate-manifest" in text
    assert "result-store validate-manifest" in text


def test_workflow_static_script_runs_static_workflow_test() -> None:
    for name in ["validate-workflow-static.ps1", "validate-workflow-static.sh"]:
        text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
        assert "test_stage2c_workflow_static.py" in text


def test_remote_workflow_scripts_do_not_require_gh() -> None:
    for name in ["verify-remote-workflow.ps1", "verify-remote-workflow.sh"]:
        text = (SCRIPT_DIR / name).read_text(encoding="utf-8").lower()
        assert "gh " not in text
        assert "raw.githubusercontent.com" in text
        assert "minimumlinecount" in text or "minimum_line_count" in text


def test_lock_hash_scripts_run_repair_check() -> None:
    for name in ["verify-lock-hashes.ps1", "verify-lock-hashes.sh"]:
        text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
        assert "repair-canonical-json-locks.py --check" in text
        assert ".gitattributes" in text
