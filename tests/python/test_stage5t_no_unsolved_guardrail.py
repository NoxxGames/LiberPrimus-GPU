from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5t_no_unsolved_guardrails_remain_blocked() -> None:
    records = yaml.safe_load(
        Path("data/cuda/stage5t-cuda-no-unsolved-guardrail-review.yaml").read_text(encoding="utf-8")
    )["records"]
    by_guardrail = {record["guardrail_id"]: record for record in records}
    assert by_guardrail["unsolved_page_cuda"]["allowed"] is False
    assert by_guardrail["canonical_corpus_activation"]["allowed"] is False
    assert by_guardrail["page_boundary_finalisation"]["allowed"] is False
    assert by_guardrail["broad_solved_fixture_cuda"]["allowed"] is False
    assert by_guardrail["generated_body_publication"]["allowed"] is False
    assert by_guardrail["method_status_upgrade"]["allowed"] is False
    assert all(record["solve_claim"] is False for record in records)
