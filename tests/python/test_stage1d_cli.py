import json
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.solved_fixtures.direct_translation import sha256_text


def _write_stage1d_fixture_dirs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    direct_dir = tmp_path / "direct"
    atbash_dir = tmp_path / "atbash"
    vigenere_dir = tmp_path / "vigenere"
    prime_dir = tmp_path / "prime"
    candidate_dir = tmp_path / "candidate"
    for path in [direct_dir, atbash_dir, vigenere_dir, prime_dir, candidate_dir]:
        path.mkdir()
    selector = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 2,
        "page_candidate_ids": [],
        "notes": "Synthetic range.",
    }
    direct = json.loads(Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json").read_text())
    direct.update({"fixture_id": "synthetic-direct", "expected_normalized_plaintext": "F U", "expected_normalized_plaintext_sha256": sha256_text("F U"), "span_selector": selector})
    atbash = json.loads(Path("data/fixtures/solved-pages/atbash-family-v0/a-warning.fixture.json").read_text())
    atbash.update({"fixture_id": "synthetic-atbash", "expected_normalized_plaintext": "EA IA", "expected_normalized_plaintext_sha256": sha256_text("EA IA"), "span_selector": selector})
    vigenere = json.loads(Path("data/fixtures/solved-pages/vigenere-v0/welcome-divinity.fixture.json").read_text())
    vigenere.update({"fixture_id": "synthetic-vigenere", "expected_normalized_plaintext": "EA F", "expected_normalized_plaintext_sha256": sha256_text("EA F"), "span_selector": selector})
    vigenere["transform_chain"][0]["params"]["key_text"] = "U"
    vigenere["transform_chain"][0]["params"].pop("skip_rule", None)
    prime = json.loads(Path("data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json").read_text())
    prime.update({"fixture_id": "synthetic-prime", "expected_normalized_plaintext": "EA EA", "expected_normalized_plaintext_sha256": sha256_text("EA EA"), "span_selector": selector, "payload_checks": []})
    (direct_dir / "direct.fixture.json").write_text(json.dumps(direct), encoding="utf-8")
    (atbash_dir / "atbash.fixture.json").write_text(json.dumps(atbash), encoding="utf-8")
    (vigenere_dir / "vigenere.fixture.json").write_text(json.dumps(vigenere), encoding="utf-8")
    (prime_dir / "prime.fixture.json").write_text(json.dumps(prime), encoding="utf-8")
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 0, "latin_label": "F"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "index29": 1, "latin_label": "U"},
    ]
    (candidate_dir / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (candidate_dir / "corpus_candidate_manifest.json").write_text("{}", encoding="utf-8")
    (candidate_dir / "page_candidates.jsonl").write_text("", encoding="utf-8")
    return direct_dir, atbash_dir, vigenere_dir, prime_dir, candidate_dir


def test_reproduce_prime_stream_cli(tmp_path: Path) -> None:
    _, _, _, prime_dir, candidate_dir = _write_stage1d_fixture_dirs(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "solved-fixture",
            "reproduce-prime-stream",
            "--fixture-dir",
            str(prime_dir),
            "--candidate-dir",
            str(candidate_dir),
            "--out-dir",
            str(tmp_path / "prime-out"),
            "--allow-pending",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "pass_count=1" in result.output
    assert "payload_check_status" in result.output


def test_stage1d_smoke_cli(tmp_path: Path) -> None:
    direct_dir, atbash_dir, vigenere_dir, prime_dir, candidate_dir = _write_stage1d_fixture_dirs(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "solved-fixture",
            "stage1d-smoke",
            "--direct-fixture-dir",
            str(direct_dir),
            "--atbash-fixture-dir",
            str(atbash_dir),
            "--vigenere-fixture-dir",
            str(vigenere_dir),
            "--prime-fixture-dir",
            str(prime_dir),
            "--candidate-dir",
            str(candidate_dir),
            "--direct-out-dir",
            str(tmp_path / "direct-out"),
            "--atbash-out-dir",
            str(tmp_path / "atbash-out"),
            "--vigenere-out-dir",
            str(tmp_path / "vigenere-out"),
            "--prime-out-dir",
            str(tmp_path / "prime-out"),
            "--allow-pending",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "stage1d_summary=" in result.output


def test_reproduce_prime_stream_missing_candidate_returns_nonzero(tmp_path: Path) -> None:
    _, _, _, prime_dir, _ = _write_stage1d_fixture_dirs(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "solved-fixture",
            "reproduce-prime-stream",
            "--fixture-dir",
            str(prime_dir),
            "--candidate-dir",
            str(tmp_path / "missing"),
        ],
    )

    assert result.exit_code != 0
    assert "missing" in result.output.lower()
