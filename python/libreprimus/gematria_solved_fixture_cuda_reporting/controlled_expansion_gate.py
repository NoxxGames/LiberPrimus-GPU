"""Build Stage 5N controlled expansion gate records."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda_reporting.export import common_policy_fields, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_reporting.models import (
    CONTROLLED_EXPANSION_GATE_JSON,
    CONTROLLED_EXPANSION_GATE_PATH,
    NEXT_STAGE,
    NEXT_STAGE_REASON,
    OUTPUT_DIR,
)


def build_controlled_expansion_gate(
    *,
    controlled_expansion_gate_out: Path = CONTROLLED_EXPANSION_GATE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    templates = [
        (
            "exact_repeat_verification_gate",
            "Repeat the exact Stage 5M solved-fixture-safe run to prove reproducibility.",
            "exact_same_five_stage5l_mapped_token_buffers",
            "approved_for_exact_repeat_only",
            [],
            "Stage 5O may prepare an exact-repeat verification pack; no benchmark or broader fixture class is allowed.",
        ),
        (
            "additional_solved_fixture_shift_score_gate",
            "Select additional solved-fixture-safe token streams for Gematria shift_score only.",
            "future_source_backed_solved_fixture_safe_shift_score_mappings",
            "needs_candidate_selection",
            ["needs_source_backed_token_mappings", "needs_native_output_hashes", "needs_explicit_future_stage_approval"],
            "Prepare candidate selection and mapping records before any CUDA execution.",
        ),
        (
            "result_store_score_summary_gate",
            "Prepare future solved-fixture CUDA results for Stage 4P and Stage 4I surfaces.",
            "committed_stage5m_hash_records_and_future_exact_repeat_records",
            "needs_result_store_preflight",
            ["needs_stage5o_result_store_preflight", "needs_score_summary_publication_shape"],
            "Use Stage 5O to prove result-store and score-summary preflight without publishing generated bodies.",
        ),
        (
            "broad_solved_fixture_cuda_gate",
            "Broader solved-fixture classes.",
            "broad_solved_fixture_classes",
            "blocked_broad_scope",
            ["controlled_expansion_not_proven", "result_store_integration_not_proven"],
            "Keep blocked until exact-repeat and result-store preflight are complete.",
        ),
        (
            "unsolved_page_cuda_gate",
            "Unsolved pages.",
            "unsolved_page_inputs",
            "blocked_unsolved",
            ["canonical_corpus_inactive", "page_boundaries_reviewable", "no_broad_search_approval"],
            "Keep blocked; Stage 5M parity does not authorize unsolved-page CUDA.",
        ),
    ]
    records = [
        {
            "record_type": "gematria_cuda_controlled_expansion_gate_record",
            "gate_record_id": f"stage5n-gate-{index:02d}",
            "gate_id": gate_id,
            "purpose": purpose,
            "input_scope": input_scope,
            "gate_status": status,
            "blockers": blockers,
            "recommendation": recommendation,
            "execution_permission_granted": status == "approved_for_exact_repeat_only",
            "selected_next_stage": NEXT_STAGE,
            "selected_next_stage_reason": NEXT_STAGE_REASON,
            **common_policy_fields(),
        }
        for index, (gate_id, purpose, input_scope, status, blockers, recommendation) in enumerate(templates)
    ]
    write_record_set(controlled_expansion_gate_out, records)
    write_report(
        out_dir,
        CONTROLLED_EXPANSION_GATE_JSON,
        {"records": records, "status_counts": dict(sorted(Counter(r["gate_status"] for r in records).items()))},
    )
    return records
