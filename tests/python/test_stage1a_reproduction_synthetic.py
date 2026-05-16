import json
from pathlib import Path

from libreprimus.solved_fixtures.direct_translation import sha256_text
from libreprimus.solved_fixtures.export import write_reproduction_outputs
from libreprimus.solved_fixtures.reproduction import reproduce_direct_translation_fixtures


def _base_fixture(expected: str, *, fixture_id: str = "synthetic") -> dict:
    payload = json.loads(Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json").read_text())
    payload["fixture_id"] = fixture_id
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
    return payload


def _write_candidate(path: Path) -> None:
    path.mkdir(parents=True)
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "latin_label": "F"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "latin_label": "A"},
    ]
    (path / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (path / "page_candidates.jsonl").write_text("", encoding="utf-8")


def test_synthetic_direct_fixture_reproduces(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(_base_fixture("F A")), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)

    records, summary, warnings = reproduce_direct_translation_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)

    assert records[0].match_status == "pass"
    assert summary.pass_count == 1
    assert warnings == []


def test_synthetic_mismatch_fails(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(_base_fixture("WRONG")), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)

    records, summary, _ = reproduce_direct_translation_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)

    assert records[0].match_status == "fail"
    assert summary.fail_count == 1


def test_reproduction_outputs_are_deterministic_shape(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "synthetic.fixture.json").write_text(json.dumps(_base_fixture("F A")), encoding="utf-8")
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)
    records, summary, warnings = reproduce_direct_translation_fixtures(fixture_dir=fixture_dir, candidate_dir=candidate_dir)
    paths = write_reproduction_outputs(tmp_path / "out", records, summary, warnings)

    assert paths["summary"].is_file()
    assert "pass_count" in paths["summary"].read_text(encoding="utf-8")
