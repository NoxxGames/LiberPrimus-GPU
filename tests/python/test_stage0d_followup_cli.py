from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app

S = "\u16cb"
H = "\u16bb"


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_stage0d_followup_smoke_cli_writes_expected_outputs(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{S}{H}}}\n{{{{53,23}}}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"{S}\n{H}\n")
    out_dir = tmp_path / "out"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "corpus-alignment",
            "stage0d-followup-smoke",
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
    assert (out_dir / "transcript_views_summary.json").is_file()
    assert (out_dir / "alignment_gap_summary.json").is_file()
    assert (out_dir / "page_boundary_audit.json").is_file()
    assert "stream_subsequence_match_count" in result.output


def test_gap_report_and_audit_boundaries_cli(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{S}{H}}}\n{{{{53,23}}}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"%\n{S}{H}/\n")
    out_dir = tmp_path / "out"
    runner = CliRunner()

    smoke = runner.invoke(
        app,
        [
            "corpus-alignment",
            "stage0d-followup-smoke",
            "--pastebin",
            str(pastebin),
            "--transcript",
            str(transcript),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert smoke.exit_code == 0

    gap = runner.invoke(
        app,
        [
            "corpus-alignment",
            "gap-report",
            "--pastebin",
            str(pastebin),
            "--transcript",
            str(transcript),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert gap.exit_code == 0
    assert (out_dir / "alignment_gap_diagnostics.jsonl").is_file()

    audit = runner.invoke(
        app,
        [
            "corpus-alignment",
            "audit-boundaries",
            "--alignment",
            str(out_dir / "pastebin_alignment.jsonl"),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert audit.exit_code == 0
    assert (out_dir / "page_boundary_confidence_audit.jsonl").is_file()


def test_followup_absent_inputs_return_nonzero() -> None:
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "corpus-alignment",
            "stage0d-followup-smoke",
            "--pastebin",
            "missing.txt",
            "--transcript",
            "missing-rtkd.txt",
        ],
    )

    assert result.exit_code != 0
    assert "not found" in result.output
