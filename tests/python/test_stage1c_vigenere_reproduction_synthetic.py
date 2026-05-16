import json
from pathlib import Path

from libreprimus.solved_fixtures.direct_translation import sha256_text
from libreprimus.solved_fixtures.reproduction import reproduce_vigenere_fixtures


def _base_fixture(expected: str, *, key_text: str = "U", skip_rule: dict | None = None) -> dict:
    payload = json.loads(
        Path("data/fixtures/solved-pages/vigenere-v0/welcome-divinity.fixture.json").read_text()
    )
    payload["fixture_id"] = "synthetic-vigenere"
    payload["expected_normalized_plaintext"] = expected
    payload["expected_normalized_plaintext_sha256"] = sha256_text(expected)
    payload["expected_rune_count"] = 1
    payload["span_selector"] = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 2,
        "page_candidate_ids": [],
        "notes": "Synthetic range.",
    }
    payload["transform_chain"][0]["params"]["key_text"] = key_text
    if skip_rule is None:
        payload["transform_chain"][0]["params"].pop("skip_rule", None)
    else:
        payload["transform_chain"][0]["params"]["skip_rule"] = skip_rule
    return payload


def _write_candidate(path: Path, tokens: list[dict]) -> None:
    path.mkdir(parents=True)
    (path / "tokens.jsonl").write_text(
        "\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8"
    )
    (path / "page_candidates.jsonl").write_text("", encoding="utf-8")


def test_synthetic_vigenere_fixture_reproduces(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "synthetic.fixture.json").write_text(
        json.dumps(_base_fixture("F")), encoding="utf-8"
    )
    candidate_dir = tmp_path / "candidate"
    _write_candidate(
        candidate_dir,
        [{"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 1}],
    )

    records, summary, warnings = reproduce_vigenere_fixtures(
        fixture_dir=fixture_dir, candidate_dir=candidate_dir
    )

    assert records[0].match_status == "pass"
    assert records[0].key_indices == [1]
    assert summary.pass_count == 1
    assert warnings == []


def test_synthetic_vigenere_skip_rule_reproduces(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    skip_rule = {
        "name": "cleartext_f_pass_through",
        "cleartext_pass_through_rune_indices": [0],
        "advance_key_on_skip": False,
    }
    (fixture_dir / "synthetic.fixture.json").write_text(
        json.dumps(_base_fixture("F F", skip_rule=skip_rule)), encoding="utf-8"
    )
    candidate_dir = tmp_path / "candidate"
    _write_candidate(
        candidate_dir,
        [
            {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 0},
            {
                "token_index_global": 1,
                "logical_line_index": 0,
                "token_kind": "word_separator",
                "raw_text": "-",
            },
            {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "index29": 1},
        ],
    )

    records, summary, _ = reproduce_vigenere_fixtures(
        fixture_dir=fixture_dir, candidate_dir=candidate_dir
    )

    assert records[0].match_status == "pass"
    assert records[0].skip_rule_applied_count == 1
    assert summary.pass_count == 1


def test_wrong_key_fails_and_pending_is_not_failure(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "wrong.fixture.json").write_text(
        json.dumps(_base_fixture("F", key_text="A")), encoding="utf-8"
    )
    pending = _base_fixture("F")
    pending["fixture_id"] = "pending-vigenere"
    pending["method_status"] = "pending_reference_text"
    pending["in_scope_for_stage"] = False
    pending["expected_normalized_plaintext"] = None
    pending["expected_normalized_plaintext_sha256"] = None
    pending["span_selector"]["selector_kind"] = "pending"
    (fixture_dir / "pending.fixture.json").write_text(json.dumps(pending), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(
        candidate_dir,
        [{"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 1}],
    )

    records, summary, _ = reproduce_vigenere_fixtures(
        fixture_dir=fixture_dir, candidate_dir=candidate_dir
    )

    assert {record.match_status for record in records} == {"fail", "pending"}
    assert summary.fail_count == 1
    assert summary.pending_count == 1
