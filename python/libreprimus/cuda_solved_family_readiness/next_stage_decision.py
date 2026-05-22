"""Build Stage 5T controlled next-stage decision records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import read_record_set, write_record_set, write_report
from libreprimus.cuda_solved_family_readiness.models import (
    BATCH_ABI_GAPS_PATH,
    COMMON_FLAGS,
    NEXT_STAGE_DECISION_JSON,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_REASON,
    NEXT_STAGE_TITLE,
    OUTPUT_DIR,
)


def build_next_stage_decision(
    *,
    batch_abi_gaps: Path = BATCH_ABI_GAPS_PATH,
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Select the next bounded engineering stage from readiness records."""

    gaps = read_record_set(batch_abi_gaps)
    needs_shared_abi = sum(1 for record in gaps if record.get("blocking"))
    rows = [
        (
            "stage5u_unified_candidate_batch_abi",
            "selected",
            True,
            "Codex",
            NEXT_STAGE_TITLE,
            NEXT_STAGE_REASON,
            True,
            False,
        ),
        (
            "affine_mod29_cuda_contract",
            "deferred_until_abi",
            False,
            "Codex",
            "Stage 5U - affine mod-29 CUDA contract and native parity preparation",
            "Affine/Caesar contract work should wait until the shared batch ABI is stable.",
            False,
            False,
        ),
        (
            "vigenere_key_schedule_contract",
            "deferred_until_key_schedule_abi",
            False,
            "Codex",
            "Stage 5U - explicit-key Vigenere CUDA contract and key-schedule ABI preparation",
            "Vigenere is high value but key scheduling is itself an ABI gap.",
            False,
            False,
        ),
        (
            "prime_stream_contract",
            "deferred_until_stream_abi",
            False,
            "Codex",
            "Stage 5U - prime-minus-one stream CUDA contract and native parity preparation",
            "Prime-stream work is high value but needs stream schedule ABI first.",
            False,
            False,
        ),
        (
            "pause_cuda_for_research",
            "not_selected",
            False,
            "Deep Research",
            "Deep Research - CUDA readiness strategic review",
            "Stage 5T found no contradiction requiring another Deep Research pause.",
            False,
            False,
        ),
    ]
    records = [
        {
            "record_type": "cuda_next_stage_decision_record",
            "next_stage_decision_id": f"stage5t-next-stage-{index:02d}",
            "decision_id": decision_id,
            "decision_status": status,
            "selected": selected,
            "recommended_prompt_type": prompt_type,
            "recommended_stage_title": title,
            "rationale": rationale,
            "requires_stage5u_batch_abi": requires_stage5u,
            "cuda_execution_allowed": False,
            "benchmark_execution_allowed": False,
            "unsolved_page_cuda_allowed": False,
            "generated_body_publication_allowed": False,
            "method_status_upgrade_allowed": False,
            "deep_research_recommended_next": deep_research,
            "blocking_batch_abi_gap_count": needs_shared_abi,
            "blockers": [] if selected else ["superseded_by_stage5u_batch_abi"],
            **COMMON_FLAGS,
        }
        for index, (
            decision_id,
            status,
            selected,
            prompt_type,
            title,
            rationale,
            requires_stage5u,
            deep_research,
        ) in enumerate(rows)
    ]
    write_record_set(next_stage_decision_out, records)
    write_report(out_dir, NEXT_STAGE_DECISION_JSON, {"records": records})
    return records
