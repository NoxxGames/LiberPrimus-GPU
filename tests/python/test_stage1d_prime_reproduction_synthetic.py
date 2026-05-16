import json
from pathlib import Path

from libreprimus.solved_fixtures.direct_translation import sha256_text
from libreprimus.solved_fixtures.reproduction import (
    reproduce_atbash_family_fixtures,
    reproduce_direct_translation_fixtures,
    reproduce_prime_stream_fixtures,
    reproduce_vigenere_fixtures,
)


def _base_prime_fixture(expected: str, *, prime_start_index: int = 0, payload_sha: str | None = None) -> dict:
    payload = json.loads(Path("data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json").read_text())
    payload["fixture_id"] = "synthetic-prime"
    payload["expected_normalized_plaintext"] = expected
    payload["expected_normalized_plaintext_sha256"] = sha256_text(expected)
    payload["expected_rune_count"] = 2
    payload["span_selector"] = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 4,
        "page_candidate_ids": [],
        "notes": "Synthetic range.",
    }
    payload["transform_chain"][0]["params"]["prime_start_index"] = prime_start_index
    payload["payload_checks"] = []
    if payload_sha is not None:
        payload["payload_checks"] = [
            {
                "payload_id": "payload",
                "payload_kind": "hex_literal_block",
                "expected_payload_text": "abc123",
                "expected_payload_sha256": payload_sha,
                "payload_selector": {
                    "selector_kind": "explicit_logical_line_range",
                    "start_logical_line_index": 1,
                    "end_logical_line_index": 1,
                },
                "preservation_policy": "preserve_exact_normalized_hex",
            }
        ]
    return payload


def _write_candidate(path: Path, *, payload_text: str = "abc123") -> None:
    path.mkdir(parents=True)
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 1, "latin_label": "U"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 1, "token_kind": "unknown_symbol", "raw_text": payload_text[:3]},
        {"token_index_global": 3, "logical_line_index": 1, "token_kind": "numeric_literal", "raw_text": payload_text[3:]},
        {"token_index_global": 4, "logical_line_index": 2, "token_kind": "rune", "index29": 3, "latin_label": "O"},
    ]
    (path / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (path / "corpus_candidate_manifest.json").write_text("{}", encoding="utf-8")
    (path / "page_candidates.jsonl").write_text("", encoding="utf-8")


def test_prime_stream_fixture_reproduces_synthetic_plaintext_and_payload(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    fixture = _base_prime_fixture("F U", payload_sha="6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090")
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(fixture), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)

    records, summary, _ = reproduce_prime_stream_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)

    assert records[0].match_status == "pass"
    assert records[0].payload_check_results[0]["match_status"] == "pass"
    assert summary.pass_count == 1


def test_wrong_prime_start_index_and_payload_mismatch_fail(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    fixture = _base_prime_fixture("F U", prime_start_index=1, payload_sha="bad")
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(fixture), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)

    records, summary, warnings = reproduce_prime_stream_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)

    assert records[0].match_status == "fail"
    assert records[0].payload_check_results[0]["match_status"] == "fail"
    assert summary.fail_count == 1
    assert warnings


def test_prior_stage_synthetic_regressions_still_pass(tmp_path: Path) -> None:
    candidate_dir = tmp_path / "candidate"
    candidate_dir.mkdir()
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 0, "latin_label": "F"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "index29": 1, "latin_label": "U"},
    ]
    (candidate_dir / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (candidate_dir / "corpus_candidate_manifest.json").write_text("{}", encoding="utf-8")
    (candidate_dir / "page_candidates.jsonl").write_text("", encoding="utf-8")
    direct_dir = tmp_path / "direct"
    atbash_dir = tmp_path / "atbash"
    vigenere_dir = tmp_path / "vigenere"
    for path in [direct_dir, atbash_dir, vigenere_dir]:
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
    (direct_dir / "direct.fixture.json").write_text(json.dumps(direct), encoding="utf-8")
    (atbash_dir / "atbash.fixture.json").write_text(json.dumps(atbash), encoding="utf-8")
    (vigenere_dir / "vigenere.fixture.json").write_text(json.dumps(vigenere), encoding="utf-8")

    assert reproduce_direct_translation_fixtures(fixture_dir=direct_dir, candidate_dir=candidate_dir)[1].pass_count == 1
    assert reproduce_atbash_family_fixtures(fixture_dir=atbash_dir, candidate_dir=candidate_dir)[1].pass_count == 1
    assert reproduce_vigenere_fixtures(fixture_dir=vigenere_dir, candidate_dir=candidate_dir)[1].pass_count == 1
