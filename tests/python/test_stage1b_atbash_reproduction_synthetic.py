import json
from pathlib import Path

from libreprimus.solved_fixtures.direct_translation import sha256_text
from libreprimus.solved_fixtures.reproduction import (
    reproduce_atbash_family_fixtures,
    reproduce_direct_translation_fixtures,
)


def _base_atbash_fixture(expected: str, *, rotation: int | None = None) -> dict:
    source = "a-koan-a-man.fixture.json" if rotation is not None else "a-warning.fixture.json"
    payload = json.loads((Path("data/fixtures/solved-pages/atbash-family-v0") / source).read_text(encoding="utf-8"))
    payload["fixture_id"] = "synthetic-atbash"
    payload["expected_normalized_plaintext"] = expected
    payload["expected_normalized_plaintext_sha256"] = sha256_text(expected)
    payload["expected_rune_count"] = 2
    payload["span_selector"] = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 2,
        "page_candidate_ids": [],
        "notes": "Synthetic range.",
    }
    if rotation is not None:
        payload["transform_chain"] = [{"name": "rotated_reverse_gematria", "params": {"rotation": rotation}}]
        payload["method_family"] = "rotated_reverse_gematria"
    return payload


def _write_candidate(path: Path) -> None:
    path.mkdir(parents=True)
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 0, "latin_label": "F"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "index29": 28, "latin_label": "EA"},
    ]
    (path / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (path / "page_candidates.jsonl").write_text("", encoding="utf-8")


def test_reverse_fixture_reproduces_synthetic_plaintext(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(_base_atbash_fixture("EA F")), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)

    records, summary, warnings = reproduce_atbash_family_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)

    assert records[0].match_status == "pass"
    assert records[0].decoded_index_formula == "decoded_index = 28 - cipher_index"
    assert summary.pass_count == 1
    assert warnings == []


def test_rotated_reverse_fixture_reproduces_with_declared_rotation(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(_base_atbash_fixture("TH O", rotation=3)), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)

    records, summary, _ = reproduce_atbash_family_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)

    assert records[0].match_status == "pass"
    assert records[0].transform_parameters == {"rotation": 3}
    assert summary.pass_count == 1


def test_wrong_rotation_fails_by_hash(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(_base_atbash_fixture("WRONG", rotation=3)), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)

    records, summary, _ = reproduce_atbash_family_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)

    assert records[0].match_status == "fail"
    assert summary.fail_count == 1


def test_direct_fixture_regression_still_passes(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    payload = json.loads(Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json").read_text())
    payload["fixture_id"] = "synthetic-direct"
    payload["expected_normalized_plaintext"] = "F EA"
    payload["expected_normalized_plaintext_sha256"] = sha256_text("F EA")
    payload["expected_rune_count"] = 2
    payload["span_selector"] = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 2,
        "page_candidate_ids": [],
        "notes": "Synthetic range.",
    }
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(payload), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)

    records, summary, _ = reproduce_direct_translation_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)

    assert records[0].match_status == "pass"
    assert summary.pass_count == 1
