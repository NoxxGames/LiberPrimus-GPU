from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_transcript_source_summary_cli(tmp_path: Path) -> None:
    transcript = _write(tmp_path / "rtkd.txt", "%\nᛋ/\n")
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["transcript-source", "summary", "--source", "rtkd-master", "--input", str(transcript)],
    )

    assert result.exit_code == 0
    assert "physical_line_count" in result.output


def test_stage0d_smoke_and_glyph_variant_cli(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", "{ᛂ}\n{{37}}\n")
    transcript = _write(tmp_path / "rtkd.txt", "ᛄ/\n")
    out_dir = tmp_path / "out"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "corpus-alignment",
            "stage0d-smoke",
            "--pastebin",
            str(pastebin),
            "--transcript",
            str(transcript),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0
    assert (out_dir / "transcript_lines.jsonl").is_file()
    assert (out_dir / "pastebin_alignment.jsonl").is_file()
    assert (out_dir / "page_boundary_candidates.jsonl").is_file()
    assert (out_dir / "glyph_variant_observations.jsonl").is_file()
    assert (out_dir / "alignment_summary.json").is_file()

    glyph_out = tmp_path / "glyphs.jsonl"
    result = runner.invoke(
        app,
        [
            "corpus-alignment",
            "glyph-variants",
            "--pastebin",
            str(pastebin),
            "--transcript",
            str(transcript),
            "--out",
            str(glyph_out),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0
    assert glyph_out.is_file()
    assert "glyph_variant_occurrence_count=1" in result.output


def test_absent_inputs_return_nonzero() -> None:
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "corpus-alignment",
            "align-pastebin",
            "--pastebin",
            "missing.txt",
            "--transcript",
            "missing-rtkd.txt",
        ],
    )

    assert result.exit_code != 0
    assert "not found" in result.output
