from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
PS1 = REPO / "scripts" / "ci" / "verify-remote-git-blobs.ps1"
SH = REPO / "scripts" / "ci" / "verify-remote-git-blobs.sh"
DOC = REPO / "docs" / "ci" / "remote-blob-verification.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_remote_blob_verifier_scripts_exist() -> None:
    assert PS1.is_file()
    assert SH.is_file()


def test_remote_blob_verifier_uses_git_show() -> None:
    script_text = _text(PS1) + "\n" + _text(SH)
    assert "git show" in script_text
    assert "git fetch" in script_text


def test_remote_blob_verifier_checks_line_counts() -> None:
    script_text = _text(PS1) + "\n" + _text(SH)
    assert "MinimumWorkflowLines" in script_text
    assert "MinimumGitattributesLines" in script_text
    assert "minimum_workflow_lines" in script_text
    assert "minimum_gitattributes_lines" in script_text


def test_remote_blob_verifier_warns_on_raw_url_mismatch() -> None:
    script_text = _text(PS1) + "\n" + _text(SH)
    assert "Raw/API mismatch warning only" in script_text
    assert "git blob remains authoritative" in script_text


def test_remote_blob_verifier_checks_required_workflow_commands() -> None:
    script_text = _text(PS1) + "\n" + _text(SH)
    for snippet in [
        "ruff check",
        "pytest -q",
        "transform-registry validate",
        "solved-baseline validate-manifest",
        "result-store validate-manifest",
    ]:
        assert snippet in script_text


def test_remote_blob_verifier_checks_required_gitattributes_patterns() -> None:
    script_text = _text(PS1) + "\n" + _text(SH)
    for snippet in [
        "*.json text eol=lf",
        "*.yml text eol=lf",
        "*.sh text eol=lf",
        "*.sha256 text eol=lf",
    ]:
        assert snippet in script_text


def test_remote_blob_verifier_does_not_require_gh() -> None:
    script_text = (_text(PS1) + "\n" + _text(SH)).lower()
    assert "gh run" not in script_text
    assert "gh api" not in script_text
    assert " gh " not in script_text


def test_docs_mention_remote_blob_verification() -> None:
    assert DOC.is_file()
    doc = _text(DOC)
    assert "git show origin/main:<path>" in doc
    assert "raw.githubusercontent.com" in doc
    assert "warning" in doc.lower()
