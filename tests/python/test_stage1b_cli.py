import json
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.solved_fixtures.direct_translation import sha256_text


def _write_fixture_and_candidate(tmp_path: Path) -> tuple[Path, Path, Path]:
    atbash_dir = tmp_path / "atbash"
    direct_dir = tmp_path / "direct"
    candidate_dir = tmp_path / "candidate"
    atbash_dir.mkdir()
    direct_dir.mkdir()
    candidate_dir.mkdir()
    atbash_payload = json.loads(Path("data/fixtures/solved-pages/atbash-family-v0/a-warning.fixture.json").read_text())
    atbash_payload["fixture_id"] = "synthetic-atbash-cli"
    atbash_payload["expected_normalized_plaintext"] = "EA F"
    atbash_payload["expected_normalized_plaintext_sha256"] = sha256_text("EA F")
    atbash_payload["expected_rune_count"] = 2
    atbash_payload["span_selector"] = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 2,
        "page_candidate_ids": [],
        "notes": "Synthetic range.",
    }
    direct_payload = json.loads(Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json").read_text())
    direct_payload["fixture_id"] = "synthetic-direct-cli"
    direct_payload["expected_normalized_plaintext"] = "F EA"
    direct_payload["expected_normalized_plaintext_sha256"] = sha256_text("F EA")
    direct_payload["expected_rune_count"] = 2
    direct_payload["span_selector"] = atbash_payload["span_selector"]
    (atbash_dir / "synthetic-atbash.fixture.json").write_text(json.dumps(atbash_payload), encoding="utf-8")
    (direct_dir / "synthetic-direct.fixture.json").write_text(json.dumps(direct_payload), encoding="utf-8")
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 0, "latin_label": "F"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "index29": 28, "latin_label": "EA"},
    ]
    (candidate_dir / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (candidate_dir / "corpus_candidate_manifest.json").write_text("{}", encoding="utf-8")
    (candidate_dir / "page_candidates.jsonl").write_text("", encoding="utf-8")
    return direct_dir, atbash_dir, candidate_dir


def test_solved_fixture_reproduce_atbash_family_cli(tmp_path: Path) -> None:
    _, atbash_dir, candidate_dir = _write_fixture_and_candidate(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "solved-fixture",
            "reproduce-atbash-family",
            "--fixture-dir",
            str(atbash_dir),
            "--candidate-dir",
            str(candidate_dir),
            "--out-dir",
            str(tmp_path / "atbash-out"),
            "--allow-pending",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "pass_count=1" in result.output


def test_solved_fixture_stage1b_smoke_cli(tmp_path: Path) -> None:
    direct_dir, atbash_dir, candidate_dir = _write_fixture_and_candidate(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "solved-fixture",
            "stage1b-smoke",
            "--direct-fixture-dir",
            str(direct_dir),
            "--atbash-fixture-dir",
            str(atbash_dir),
            "--candidate-dir",
            str(candidate_dir),
            "--direct-out-dir",
            str(tmp_path / "direct-out"),
            "--atbash-out-dir",
            str(tmp_path / "atbash-out"),
            "--allow-pending",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "stage1b_summary=" in result.output


def test_reproduce_atbash_missing_candidate_returns_nonzero(tmp_path: Path) -> None:
    _, atbash_dir, _ = _write_fixture_and_candidate(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "solved-fixture",
            "reproduce-atbash-family",
            "--fixture-dir",
            str(atbash_dir),
            "--candidate-dir",
            str(tmp_path / "missing"),
        ],
    )

    assert result.exit_code != 0
    assert "missing" in result.output.lower()
