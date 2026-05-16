import json
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.solved_fixtures.direct_translation import sha256_text


def _write_fixture_dirs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    direct_dir = tmp_path / "direct"
    atbash_dir = tmp_path / "atbash"
    vigenere_dir = tmp_path / "vigenere"
    candidate_dir = tmp_path / "candidate"
    for path in [direct_dir, atbash_dir, vigenere_dir, candidate_dir]:
        path.mkdir()
    selector = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 2,
        "page_candidate_ids": [],
        "notes": "Synthetic range.",
    }
    direct_payload = json.loads(Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json").read_text())
    direct_payload["fixture_id"] = "synthetic-direct"
    direct_payload["expected_normalized_plaintext"] = "F U"
    direct_payload["expected_normalized_plaintext_sha256"] = sha256_text("F U")
    direct_payload["span_selector"] = selector
    atbash_payload = json.loads(Path("data/fixtures/solved-pages/atbash-family-v0/a-warning.fixture.json").read_text())
    atbash_payload["fixture_id"] = "synthetic-atbash"
    atbash_payload["expected_normalized_plaintext"] = "EA IA"
    atbash_payload["expected_normalized_plaintext_sha256"] = sha256_text("EA IA")
    atbash_payload["span_selector"] = selector
    vigenere_payload = json.loads(Path("data/fixtures/solved-pages/vigenere-v0/welcome-divinity.fixture.json").read_text())
    vigenere_payload["fixture_id"] = "synthetic-vigenere"
    vigenere_payload["expected_normalized_plaintext"] = "EA F"
    vigenere_payload["expected_normalized_plaintext_sha256"] = sha256_text("EA F")
    vigenere_payload["span_selector"] = selector
    vigenere_payload["transform_chain"][0]["params"]["key_text"] = "U"
    vigenere_payload["transform_chain"][0]["params"].pop("skip_rule", None)
    (direct_dir / "direct.fixture.json").write_text(json.dumps(direct_payload), encoding="utf-8")
    (atbash_dir / "atbash.fixture.json").write_text(json.dumps(atbash_payload), encoding="utf-8")
    (vigenere_dir / "vigenere.fixture.json").write_text(json.dumps(vigenere_payload), encoding="utf-8")
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 0, "latin_label": "F"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "index29": 1, "latin_label": "U"},
    ]
    (candidate_dir / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (candidate_dir / "corpus_candidate_manifest.json").write_text("{}", encoding="utf-8")
    (candidate_dir / "page_candidates.jsonl").write_text("", encoding="utf-8")
    return direct_dir, atbash_dir, vigenere_dir, candidate_dir


def test_reproduce_vigenere_cli(tmp_path: Path) -> None:
    _, _, vigenere_dir, candidate_dir = _write_fixture_dirs(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "solved-fixture",
            "reproduce-vigenere",
            "--fixture-dir",
            str(vigenere_dir),
            "--candidate-dir",
            str(candidate_dir),
            "--out-dir",
            str(tmp_path / "vigenere-out"),
            "--allow-pending",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "pass_count=1" in result.output


def test_stage1c_smoke_cli(tmp_path: Path) -> None:
    direct_dir, atbash_dir, vigenere_dir, candidate_dir = _write_fixture_dirs(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "solved-fixture",
            "stage1c-smoke",
            "--direct-fixture-dir",
            str(direct_dir),
            "--atbash-fixture-dir",
            str(atbash_dir),
            "--vigenere-fixture-dir",
            str(vigenere_dir),
            "--candidate-dir",
            str(candidate_dir),
            "--direct-out-dir",
            str(tmp_path / "direct-out"),
            "--atbash-out-dir",
            str(tmp_path / "atbash-out"),
            "--vigenere-out-dir",
            str(tmp_path / "vigenere-out"),
            "--allow-pending",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "stage1c_summary=" in result.output


def test_reproduce_vigenere_missing_candidate_returns_nonzero(tmp_path: Path) -> None:
    _, _, vigenere_dir, _ = _write_fixture_dirs(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "solved-fixture",
            "reproduce-vigenere",
            "--fixture-dir",
            str(vigenere_dir),
            "--candidate-dir",
            str(tmp_path / "missing"),
        ],
    )

    assert result.exit_code != 0
    assert "missing" in result.output.lower()
