"""Build Stage 5T no-unsolved guardrail review records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import write_record_set, write_report
from libreprimus.cuda_solved_family_readiness.models import COMMON_FLAGS, NO_UNSOLVED_GUARDRAIL_PATH, NO_UNSOLVED_GUARDRAIL_REPORT_JSON, OUTPUT_DIR


def build_no_unsolved_guardrail(
    *,
    no_unsolved_guardrail_out: Path = NO_UNSOLVED_GUARDRAIL_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    guardrails = [
        ("unsolved_page_cuda", "blocked_unsolved", "No unsolved-page CUDA is allowed before explicit tiny-pilot gates."),
        ("canonical_corpus_activation", "blocked_corpus_inactive", "Canonical corpus remains inactive."),
        ("page_boundary_finalisation", "blocked_reviewable", "Page boundaries remain reviewable, not final."),
        ("broad_solved_fixture_cuda", "blocked_broad_scope", "Broad solved-fixture CUDA campaigns are outside Stage 5T."),
        ("generated_body_publication", "blocked_generated_body_publication", "Generated CUDA bodies remain ignored and unpublished."),
        ("method_status_upgrade", "blocked_method_status_upgrade", "Parity is backend correctness metadata, not solve evidence."),
    ]
    records = [
        {
            "record_type": "cuda_no_unsolved_guardrail_review_record",
            "guardrail_review_id": f"stage5t-guardrail-{index:02d}",
            "guardrail_id": guardrail_id,
            "guardrail_status": status,
            "allowed": False,
            "rationale": rationale,
            "requirements_before_future_tiny_pilot": [
                "Stage 5U unified batch ABI",
                "Stage 5W score-vector unification",
                "Stage 5X benchmark harness hardening",
                "explicit user approval",
            ],
            **COMMON_FLAGS,
        }
        for index, (guardrail_id, status, rationale) in enumerate(guardrails)
    ]
    write_record_set(no_unsolved_guardrail_out, records)
    write_report(out_dir, NO_UNSOLVED_GUARDRAIL_REPORT_JSON, {"records": records})
    return records
