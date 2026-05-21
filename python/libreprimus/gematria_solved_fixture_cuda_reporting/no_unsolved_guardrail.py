"""Build Stage 5N no-unsolved CUDA guardrail records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda_reporting.export import common_policy_fields, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_reporting.models import (
    NO_UNSOLVED_GUARDRAIL_JSON,
    NO_UNSOLVED_GUARDRAIL_PATH,
    OUTPUT_DIR,
)


def build_no_unsolved_guardrail(
    *,
    no_unsolved_guardrail_out: Path = NO_UNSOLVED_GUARDRAIL_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    guardrails = [
        ("canonical_corpus_inactive", "Canonical corpus remains inactive.", "enforced"),
        ("page_boundaries_reviewable", "Page boundaries remain reviewable, not final.", "enforced"),
        ("broad_search_not_started", "Broad CUDA search/campaign execution is not started.", "enforced"),
        ("no_raw_page_text_through_cuda", "Raw or real LP page text must not be sent through CUDA.", "enforced"),
        ("no_generated_output_publication", "Generated CUDA reports remain ignored and uncommitted.", "enforced"),
        ("score_labels_not_solve_evidence", "Score labels remain triage only.", "enforced"),
        ("no_gpu_benchmark", "GPU benchmarking remains out of scope.", "enforced"),
        ("no_unsolved_manifest_from_stage5m", "Stage 5M records must not generate unsolved CUDA manifests.", "enforced"),
        ("next_stages_solved_fixture_safe", "Next stages remain solved-fixture-safe unless explicitly rescoped.", "enforced"),
    ]
    records = [
        {
            "record_type": "gematria_no_unsolved_guardrail_record",
            "guardrail_record_id": f"stage5n-no-unsolved-{index:02d}",
            "guardrail_id": guardrail_id,
            "guardrail_statement": statement,
            "guardrail_status": status,
            "unsolved_page_cuda_allowed": False,
            **common_policy_fields(),
        }
        for index, (guardrail_id, statement, status) in enumerate(guardrails)
    ]
    write_record_set(no_unsolved_guardrail_out, records)
    write_report(out_dir, NO_UNSOLVED_GUARDRAIL_JSON, {"records": records})
    return records
