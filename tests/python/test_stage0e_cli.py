from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_profile_validation_cli_commands() -> None:
    runner = CliRunner()
    for args in [
        ["profile", "validate-gematria", "--profile", "data/profiles/gematria/gematria-primus-v0.json"],
        [
            "profile",
            "validate-glyph-variants",
            "--gematria",
            "data/profiles/gematria/gematria-primus-v0.json",
            "--variants",
            "data/profiles/glyph-variants/glyph-variants-v0.json",
        ],
        ["profile", "validate-separators", "--grammar", "data/profiles/separators/rtkd-separator-grammar-v0.json"],
    ]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output


def test_corpus_candidate_cli_build_validate_summary(tmp_path: Path) -> None:
    transcript = tmp_path / "rtkd.txt"
    transcript.write_text("\u16a0/\n", encoding="utf-8")
    out_dir = tmp_path / "candidate"
    runner = CliRunner()

    build = runner.invoke(
        app,
        [
            "corpus-candidate",
            "build-rtkd-v0",
            "--transcript",
            str(transcript),
            "--out-dir",
            str(out_dir),
            "--allow-boundary-warnings",
        ],
    )
    assert build.exit_code == 0, build.output
    assert (out_dir / "tokens.jsonl").is_file()

    validate = runner.invoke(app, ["corpus-candidate", "validate", "--candidate-dir", str(out_dir), "--allow-warnings"])
    assert validate.exit_code == 0, validate.output

    summary = runner.invoke(app, ["corpus-candidate", "summary", "--candidate-dir", str(out_dir)])
    assert summary.exit_code == 0, summary.output
    assert "canonical_corpus_active=false" in summary.output


def test_corpus_candidate_missing_input_returns_nonzero() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["corpus-candidate", "build-rtkd-v0", "--transcript", "missing.txt"])

    assert result.exit_code != 0
    assert "not found" in result.output
