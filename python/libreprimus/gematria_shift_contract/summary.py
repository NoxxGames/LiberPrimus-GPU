"""Stage 5H Gematria shift contract summary generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_shift_contract.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_shift_contract.models import (
    ARITHMETIC_DIRECTION,
    COMMON_POLICY_FLAGS,
    CONTRACT_ID,
    CONTRACT_PATH,
    FIXTURE_ID,
    FIXTURES_PATH,
    MAPPING_PATH,
    NEXT_STAGE,
    OUTPUT_DIR,
    SCORE_PLAN_PATH,
    SEPARATOR_POLICY,
    SUMMARY_JSON,
    SUMMARY_PATH,
    TOKEN_DOMAIN,
)


def build_summary(
    *,
    contract_path: Path = CONTRACT_PATH,
    fixtures_path: Path = FIXTURES_PATH,
    mapping_path: Path = MAPPING_PATH,
    score_summary_plan_path: Path = SCORE_PLAN_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    """Build the committed Stage 5H aggregate summary."""

    contracts = read_record_set(contract_path)
    fixtures = read_record_set(fixtures_path)
    mappings = read_record_set(mapping_path)
    score_plans = read_record_set(score_summary_plan_path)
    fixture = fixtures[0] if fixtures else {}
    blocker_count = max((int(record.get("preflight_blocker_count", 0)) for record in mappings), default=0)
    summary = {
        "record_type": "stage5h_gematria_shift_contract_summary",
        "stage_id": "stage-5h",
        "status": "complete",
        "contract_records": len(contracts),
        "native_fixture_records": len(fixtures),
        "solved_fixture_safe_mapping_records": len(mappings),
        "score_summary_parity_plan_records": len(score_plans),
        "contract_id": CONTRACT_ID,
        "selected_future_kernel_id": "shift_score_kernel",
        "token_domain": TOKEN_DOMAIN,
        "arithmetic_direction": ARITHMETIC_DIRECTION,
        "separator_policy": SEPARATOR_POLICY,
        "native_fixture_id": FIXTURE_ID,
        "native_fixture_hash": fixture.get("expected_output_hash"),
        "preflight_blocker_count": blocker_count,
        "next_stage": NEXT_STAGE,
        **COMMON_POLICY_FLAGS,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_JSON, summary)
    write_warnings(out_dir, [])
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    """Load a Stage 5H summary."""

    return read_yaml(summary_path)
