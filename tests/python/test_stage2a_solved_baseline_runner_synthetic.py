import json
from pathlib import Path

import yaml

from libreprimus.solved_baselines.export import write_manifest_run_outputs
from libreprimus.solved_baselines.manifest_loader import load_manifest
from libreprimus.solved_baselines.runner import run_manifest
from libreprimus.solved_fixtures.direct_translation import sha256_text
from libreprimus.transforms.registry import load_registry


def _write_candidate(path: Path) -> None:
    path.mkdir()
    tokens = [
        {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": 0, "latin_label": "F"},
        {"token_index_global": 1, "logical_line_index": 0, "token_kind": "word_separator", "raw_text": "-"},
        {"token_index_global": 2, "logical_line_index": 0, "token_kind": "rune", "index29": 1, "latin_label": "U"},
    ]
    (path / "tokens.jsonl").write_text("\n".join(json.dumps(token) for token in tokens) + "\n", encoding="utf-8")
    (path / "corpus_candidate_manifest.json").write_text("{}", encoding="utf-8")
    (path / "page_candidates.jsonl").write_text("", encoding="utf-8")


def _fixture_payload(source: str, fixture_id: str, expected: str, selector: dict) -> dict:
    payload = json.loads(Path(source).read_text(encoding="utf-8"))
    payload.update(
        {
            "fixture_id": fixture_id,
            "expected_normalized_plaintext": expected,
            "expected_normalized_plaintext_sha256": sha256_text(expected),
            "span_selector": selector,
        }
    )
    return payload


def _write_synthetic_suite(tmp_path: Path) -> tuple[Path, Path]:
    candidate_dir = tmp_path / "candidate"
    _write_candidate(candidate_dir)
    selector = {
        "selector_kind": "explicit_token_range",
        "source": "rtkd-master-v0-candidate",
        "start_token_index": 0,
        "end_token_index": 2,
        "page_candidate_ids": [],
        "notes": "Synthetic Stage 2A range.",
    }
    fixture_groups = []
    fixtures = [
        ("direct-translation-v0", "direct", "direct_translation", ["direct_translation"], "synthetic-direct", "F U", "data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json"),
        ("atbash-family-v0", "atbash", "atbash_family", ["reverse_gematria"], "synthetic-atbash", "EA IA", "data/fixtures/solved-pages/atbash-family-v0/a-warning.fixture.json"),
        ("vigenere-v0", "vigenere", "vigenere", ["vigenere_explicit_key"], "synthetic-vigenere", "EA F", "data/fixtures/solved-pages/vigenere-v0/welcome-divinity.fixture.json"),
        ("prime-stream-v0", "prime", "prime_minus_one_stream", ["prime_minus_one_stream"], "synthetic-prime", "EA EA", "data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json"),
    ]
    for group_id, dirname, method, transforms, fixture_id, expected, source in fixtures:
        fixture_dir = tmp_path / dirname
        fixture_dir.mkdir()
        payload = _fixture_payload(source, fixture_id, expected, selector)
        if group_id == "vigenere-v0":
            payload["transform_chain"][0]["params"]["key_text"] = "U"
            payload["transform_chain"][0]["params"].pop("skip_rule", None)
        if group_id == "prime-stream-v0":
            payload["payload_checks"] = []
        (fixture_dir / f"{fixture_id}.fixture.json").write_text(json.dumps(payload), encoding="utf-8")
        fixture_groups.append(
            {
                "fixture_group_id": group_id,
                "fixture_dir": str(fixture_dir),
                "method_family": method,
                "transform_ids": transforms,
                "expected_fixture_count": 1,
                "expected_pass_count": 1,
                "allow_pending": False,
            }
        )
    manifest_path = tmp_path / "manifest.yaml"
    manifest = {
        "record_type": "solved_baseline_run_manifest",
        "manifest_id": "synthetic-stage2a",
        "manifest_version": "solved-baseline-run-v0",
        "description": "Synthetic Stage 2A manifest.",
        "registry_id": "cpu-reference-transforms-v0",
        "registry_sha256": load_registry().sha256,
        "corpus_candidate_id": "rtkd-master-v0-candidate",
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "search_enabled": False,
        "cuda_enabled": False,
        "scoring_enabled": False,
        "fixture_groups": fixture_groups,
        "output_dir": str(tmp_path / "out"),
        "allow_pending": False,
        "allow_warnings": True,
        "require_all_pass": True,
        "expected_counts": {"fixture_group_count": 4, "fixture_count": 4, "pass_count": 4},
        "provenance": {"source": "synthetic test"},
        "notes": ["Synthetic manifest for registry runner tests."],
    }
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=True), encoding="utf-8")
    return manifest_path, candidate_dir


def test_runner_executes_synthetic_fixture_groups_through_registry(tmp_path: Path) -> None:
    manifest_path, candidate_dir = _write_synthetic_suite(tmp_path)

    records, summary, warnings = run_manifest(load_manifest(manifest_path), candidate_dir=candidate_dir)

    assert len(records) == 4
    assert summary.pass_count == 4
    assert summary.fail_count == 0
    assert summary.pending_count == 0
    assert summary.direct_translation_pass_count == 1
    assert summary.atbash_family_pass_count == 1
    assert summary.vigenere_pass_count == 1
    assert summary.prime_stream_pass_count == 1
    assert summary.search_performed_any is False
    assert summary.cuda_used_any is False
    assert summary.scoring_used_any is False
    assert warnings == []
    for record in records:
        assert record.registry_id == "cpu-reference-transforms-v0"
        assert record.manifest_id == "synthetic-stage2a"
        assert record.search_performed is False
        assert record.cuda_used is False
        assert record.scoring_used is False


def test_runner_outputs_are_record_deterministic(tmp_path: Path) -> None:
    manifest_path, candidate_dir = _write_synthetic_suite(tmp_path)
    manifest = load_manifest(manifest_path)

    first_records, first_summary, first_warnings = run_manifest(manifest, candidate_dir=candidate_dir)
    second_records, second_summary, second_warnings = run_manifest(manifest, candidate_dir=candidate_dir)
    write_manifest_run_outputs(tmp_path / "out", first_records, first_summary, first_warnings)

    assert [record.source_record["fixture_id"] for record in first_records] == [
        record.source_record["fixture_id"] for record in second_records
    ]
    assert first_summary.pass_count == second_summary.pass_count
    assert first_warnings == second_warnings
    assert (tmp_path / "out" / "manifest_run_records.jsonl").is_file()
