"""Solved-fixture-safe CUDA adapter preflight records for Stage 5G."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_parity_reporting.export import write_record_set, write_report
from libreprimus.cuda_parity_reporting.models import COMMON_POLICY_FLAGS, NEXT_STAGE, OUTPUT_DIR, PREFLIGHT_JSON, PREFLIGHT_PATH, STAGE_ID

PREFLIGHT_BLOCKERS = [
    "need Gematria mod-29 native reference fixture contract",
    "need solved-fixture-safe adapter contract distinct from synthetic A-Z fixture",
    "need Stage 4O parity expectation mapping to chosen solved fixture",
    "need score-summary parity plan for Gematria output",
    "need no-real-data/no-unsolved-page guardrails for first solved-fixture-safe run",
]


def build_solved_fixture_preflight(
    *,
    preflight_out: Path = PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    record: dict[str, Any] = {
        "record_type": "cuda_solved_fixture_safe_preflight_record",
        "stage_id": STAGE_ID,
        "preflight_id": "stage5g-solved-fixture-safe-adapter-preflight",
        "current_stage5f_kernel_scope": "synthetic_uppercase_latin_only",
        "production_gematria_mod29_cuda_ready": False,
        "solved_fixture_cuda_execution_allowed": False,
        "preflight_blockers": PREFLIGHT_BLOCKERS,
        "preflight_blocker_count": len(PREFLIGHT_BLOCKERS),
        "recommended_next_stage": NEXT_STAGE,
        "cuda_source_modified": True,
        "notes": [
            "The current kernel may not process solved or unsolved Liber Primus material.",
            "Stage 5H should define the Gematria mod-29 contract and native fixture preparation first.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(preflight_out, records)
    write_report(out_dir, PREFLIGHT_JSON, {"records": records})
    return records
