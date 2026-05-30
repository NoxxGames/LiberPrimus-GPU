from pathlib import Path

import yaml

from libreprimus.token_block.stage5ca import (
    REQUIRED_CITATION_PATHS,
    validate_stage5ca_citation_contract,
)
from test_stage5ca_common import ROOT, load_yaml


def test_stage5ca_citation_contract_is_exact_and_resolvable() -> None:
    payload = load_yaml("data/token-block/stage5ca-future-runner-exact-citation-contract.yaml")
    citations = payload["future_runner_must_cite_exactly"]
    assert citations == REQUIRED_CITATION_PATHS
    assert all((ROOT / path).is_file() for path in citations)


def test_stage5ca_citation_validator_rejects_missing_required_path(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ca-future-runner-exact-citation-contract.yaml")
    payload["future_runner_must_cite_exactly"] = payload["future_runner_must_cite_exactly"][:-1]
    candidate = tmp_path / "citation.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ca_citation_contract(citation_contract=candidate)
    assert counts["stage5ca_citation_contract_valid"] is False
    assert any(error.startswith("missing_required_citation=") for error in errors)


def test_stage5ca_citation_validator_rejects_unresolved_path(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ca-future-runner-exact-citation-contract.yaml")
    payload["future_runner_must_cite_exactly"] = [
        *payload["future_runner_must_cite_exactly"][:-1],
        "data/token-block/stage5ca-missing-required-path.yaml",
    ]
    candidate = tmp_path / "citation.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ca_citation_contract(citation_contract=candidate)
    assert counts["stage5ca_citation_contract_valid"] is False
    assert any(error.startswith("citation_path_unresolved=") for error in errors)
