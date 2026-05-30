from pathlib import Path

import yaml

from libreprimus.token_block.stage5ca import INCORRECT_STAGE5AW_PATH
from libreprimus.token_block.stage5ce import validate_stage5ce_citation_negative_tests
from test_stage5ce_common import load_yaml


def test_stage5ce_citation_negative_hardening_record_lists_direct_tests() -> None:
    payload = load_yaml("data/token-block/stage5ce-stage5cc-citation-negative-test-hardening.yaml")
    assert payload["stage5cc_citation_contract_negative_tests_hardened"] is True
    assert payload["missing_required_citation_fails"] is True
    assert payload["extra_citation_fails"] is True
    assert payload["unresolved_citation_path_fails"] is True
    assert payload["deprecated_stage5aw_path_fails"] is True


def test_stage5ce_missing_required_citation_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-proposal-package-citation-set.yaml")
    payload["future_runner_must_cite_exactly"] = payload["future_runner_must_cite_exactly"][:-1]
    candidate = tmp_path / "citations.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_citation_negative_tests(citation_set=candidate)
    assert counts["stage5ce_citation_negative_tests_valid"] is False
    assert any(error.startswith("missing_required_citation=") for error in errors)


def test_stage5ce_extra_citation_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-proposal-package-citation-set.yaml")
    payload["future_runner_must_cite_exactly"] = [
        *payload["future_runner_must_cite_exactly"],
        "data/token-block/unclassified-future-record.yaml",
    ]
    candidate = tmp_path / "citations.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_citation_negative_tests(citation_set=candidate)
    assert counts["stage5ce_citation_negative_tests_valid"] is False
    assert "extra_citation=data/token-block/unclassified-future-record.yaml" in errors


def test_stage5ce_unresolved_citation_path_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-proposal-package-citation-set.yaml")
    payload["future_runner_must_cite_exactly"] = [
        *payload["future_runner_must_cite_exactly"][:-1],
        "data/token-block/stage5ce-missing-required-path.yaml",
    ]
    candidate = tmp_path / "citations.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_citation_negative_tests(citation_set=candidate)
    assert counts["stage5ce_citation_negative_tests_valid"] is False
    assert "citation_path_unresolved=data/token-block/stage5ce-missing-required-path.yaml" in errors


def test_stage5ce_deprecated_stage5aw_path_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-proposal-package-citation-set.yaml")
    payload["future_runner_must_cite_exactly"] = [
        *payload["future_runner_must_cite_exactly"],
        INCORRECT_STAGE5AW_PATH,
    ]
    candidate = tmp_path / "citations.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_citation_negative_tests(citation_set=candidate)
    assert counts["stage5ce_citation_negative_tests_valid"] is False
    assert "deprecated_stage5aw_path_present" in errors
