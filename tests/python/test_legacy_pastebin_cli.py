from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def _write_synthetic(path: Path, *, bad: bool = False) -> Path:
    prime = "999" if bad else "53"
    path.write_text("{ᛋ}\n{{" + prime + "}}\n{}\n{}\n{ᛈᚪᚱᚪᛒᛚᛖ}\n{{43,97,11,97,61,73,67}}\n", encoding="utf-8")
    return path


def test_cli_summary_validate_extract_and_anchors(tmp_path: Path) -> None:
    input_path = _write_synthetic(tmp_path / "pastebin.txt")
    out_dir = tmp_path / "out"
    runner = CliRunner()

    result = runner.invoke(app, ["legacy-pastebin", "summary", "--input", str(input_path)])
    assert result.exit_code == 0
    assert "line_pair_count" in result.output

    result = runner.invoke(app, ["legacy-pastebin", "validate", "--input", str(input_path)])
    assert result.exit_code == 0

    result = runner.invoke(
        app,
        ["legacy-pastebin", "extract", "--input", str(input_path), "--out-dir", str(out_dir)],
    )
    assert result.exit_code == 0
    assert (out_dir / "line_pairs.jsonl").is_file()
    assert (out_dir / "anchors.json").is_file()
    assert (out_dir / "summary.json").is_file()
    assert (out_dir / "warnings.jsonl").is_file()

    result = runner.invoke(app, ["legacy-pastebin", "anchors", "--input", str(input_path)])
    assert result.exit_code == 0
    assert "parable_anchor_detected=true" in result.output


def test_cli_validate_fails_on_bad_mapping_unless_warnings_allowed(tmp_path: Path) -> None:
    input_path = _write_synthetic(tmp_path / "bad.txt", bad=True)
    runner = CliRunner()

    result = runner.invoke(app, ["legacy-pastebin", "validate", "--input", str(input_path)])
    assert result.exit_code == 1

    result = runner.invoke(
        app,
        ["legacy-pastebin", "validate", "--input", str(input_path), "--allow-warnings"],
    )
    assert result.exit_code == 0
