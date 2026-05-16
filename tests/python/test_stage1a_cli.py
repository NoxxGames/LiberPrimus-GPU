import json
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.solved_fixtures.direct_translation import sha256_text


def _write_fixture_and_candidate(tmp_path: Path) -> tuple[Path, Path]:
    fixture_dir = tmp_path / "fixtures"
    candidate_dir = tmp_path / "candidate"
    fixture_dir.mkdir()
    candidate_dir.mkdir()
    payload = json.loads(Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json").read_text())
    payload["fixture_id"] = "synthetic-cli"
    payload["expected_normalized_plaintext"] = "F A"
    payload["expected_normalized_plaintext_sha256"] = sha256_text("F A")
    payload["expected_rune_count"] = 2
    payload["span_selector"] = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 2,
        "page_candidate_ids": [],
        "notes": "Synthetic CLI fixture.",
    }
    (fixture_dir / "synthetic-cli.fixture.json").write_text(json.dumps(payload), encoding="utf-8")
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "latin_label": "F"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "latin_label": "A"},
    ]
    (candidate_dir / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (candidate_dir / "corpus_candidate_manifest.json").write_text("{}", encoding="utf-8")
    (candidate_dir / "page_candidates.jsonl").write_text("", encoding="utf-8")
    return fixture_dir, candidate_dir


def test_solved_fixture_cli_list_validate_reproduce_summary(tmp_path: Path) -> None:
    fixture_dir, candidate_dir = _write_fixture_and_candidate(tmp_path)
    out_dir = tmp_path / "out"
    runner = CliRunner()

    listed = runner.invoke(app, ["solved-fixture", "list", "--fixture-dir", str(fixture_dir)])
    assert listed.exit_code == 0, listed.output

    validated = runner.invoke(app, ["solved-fixture", "validate", "--fixture-dir", str(fixture_dir)])
    assert validated.exit_code == 0, validated.output

    reproduced = runner.invoke(
        app,
        [
            "solved-fixture",
            "reproduce-direct",
            "--fixture-dir",
            str(fixture_dir),
            "--candidate-dir",
            str(candidate_dir),
            "--out-dir",
            str(out_dir),
            "--allow-pending",
            "--allow-warnings",
        ],
    )
    assert reproduced.exit_code == 0, reproduced.output

    summary = runner.invoke(app, ["solved-fixture", "summary", "--results-dir", str(out_dir)])
    assert summary.exit_code == 0, summary.output
    assert "pass_count=1" in summary.output


def test_solved_fixture_missing_candidate_returns_nonzero(tmp_path: Path) -> None:
    fixture_dir, _ = _write_fixture_and_candidate(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "solved-fixture",
            "reproduce-direct",
            "--fixture-dir",
            str(fixture_dir),
            "--candidate-dir",
            str(tmp_path / "missing"),
        ],
    )

    assert result.exit_code != 0
    assert "missing" in result.output.lower()
