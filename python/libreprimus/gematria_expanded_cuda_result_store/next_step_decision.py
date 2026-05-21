"""Build Stage 5S controlled next-step decision records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import write_record_set, write_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    COMMON_FLAGS,
    NEXT_DEEP_RESEARCH_PROMPT,
    NEXT_DEEP_RESEARCH_REASON,
    NEXT_STEP_DECISION_JSON,
    NEXT_STEP_DECISION_PATH,
    OUTPUT_DIR,
)

_DECISIONS = (
    ("additional_solved_fixture_shift_score_candidate_mapping", "strategic_ambiguity_review_first"),
    ("expanded_parity_exact_repeat", "available_but_not_selected"),
    ("original_transform_family_cuda_contract_review", "blocked_pending_contract_review"),
    ("deep_research_project_review", "recommended"),
    ("unsolved_page_cuda", "blocked_unsolved"),
    ("broad_solved_fixture_cuda_campaign", "blocked_broad_scope"),
)


def build_next_step_decision(
    *,
    next_step_decision_out: Path = NEXT_STEP_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [_record(index=index, decision_class=decision_class, status=status) for index, (decision_class, status) in enumerate(_DECISIONS)]
    write_record_set(next_step_decision_out, records)
    write_report(out_dir, NEXT_STEP_DECISION_JSON, {"records": records})
    return records


def _record(*, index: int, decision_class: str, status: str) -> dict[str, Any]:
    selected = decision_class == "deep_research_project_review"
    record = {
        "record_type": "gematria_expanded_cuda_next_step_decision_record",
        "next_step_decision_id": f"stage5s-next-step-decision-{index:02d}",
        "decision_class": decision_class,
        "decision_status": status,
        "selected": selected,
        "selected_next_prompt": NEXT_DEEP_RESEARCH_PROMPT if selected else None,
        "selected_next_stage_reason": NEXT_DEEP_RESEARCH_REASON if selected else "Not selected for the immediate next prompt.",
        "deep_research_recommended": selected,
        "deep_research_recommendation_reason": NEXT_DEEP_RESEARCH_REASON if selected else "Decision class is retained as blocked or available context.",
        "remaining_blockers": [],
        "newly_discovered_blockers": [],
        "additional_solved_fixture_candidate_status": "strategic_ambiguity_review_first",
        "original_transform_family_contract_status": "blocked_pending_contract_review",
        "broad_solved_fixture_cuda_status": "blocked_broad_scope",
        "unsolved_page_cuda_status": "blocked_unsolved",
    }
    record.update(COMMON_FLAGS)
    return record
