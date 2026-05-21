from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5n_no_unsolved_guardrail_requires_inactive_corpus_and_reviewable_boundaries() -> None:
    records = {record["guardrail_id"]: record for record in yaml.safe_load(Path("data/cuda/stage5n-gematria-no-unsolved-guardrail.yaml").read_text(encoding="utf-8"))["records"]}
    assert records["canonical_corpus_inactive"]["canonical_corpus_active"] is False
    assert records["page_boundaries_reviewable"]["page_boundaries_final"] is False
    assert all(record["unsolved_page_cuda_allowed"] is False for record in records.values())


def test_stage5n_no_unsolved_guardrails_are_enforced() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5n-gematria-no-unsolved-guardrail.yaml").read_text(encoding="utf-8"))["records"]
    assert len(records) == 9
    assert {record["guardrail_status"] for record in records} == {"enforced"}
