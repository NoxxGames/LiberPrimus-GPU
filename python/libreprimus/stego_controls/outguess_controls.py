"""OutGuess positive-control matrix and guardrail records."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from libreprimus.token_block.models import FALSE_GUARDRAILS, STAGE_ID, write_json, write_yaml


POLICY_PATH = Path("data/stego/stage5ap-outguess-positive-control-policy.yaml")
MATRIX_PATH = Path("data/stego/stage5ap-outguess-positive-control-matrix.yaml")
GUARDRAIL_PATH = Path("data/stego/stage5ap-outguess-guardrail.yaml")
RESULTS_DIR = Path("experiments/results/stego-controls/stage5ap")


def build_outguess_policy(*, out: Path = POLICY_PATH) -> dict[str, Any]:
    record = {
        "record_type": "outguess_positive_control_policy",
        "schema": "schemas/stego/outguess-positive-control-policy-v0.schema.json",
        "stage_id": STAGE_ID,
        "policy_status": "active",
        "historical_fixture_execution_requires_cached_asset": True,
        "historical_fixture_execution_requires_expected_output_hash": True,
        "synthetic_controls_allowed_for_tests": True,
        "lp_page_outguess_execution_allowed": False,
        "broad_stego_scan_allowed": False,
        "tool_execution_allowed_stage5ap": False,
        "raw_fixture_committed": False,
        "extracted_payload_committed": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    return record


def build_positive_control_matrix(*, toolchain: Path, out: Path = MATRIX_PATH, results_dir: Path | None = RESULTS_DIR) -> dict[str, Any]:
    synthetic_payload_hash = hashlib.sha256(b"stage5ap synthetic positive payload\n").hexdigest()
    rows = [
        {
            "fixture_id": "stage5ap-outguess-synthetic-positive-control",
            "fixture_category": "synthetic_positive_control",
            "source_status": "synthetic_ci_only",
            "ready_state": "synthetic_ready",
            "expected_output_required": True,
            "expected_output_hash": synthetic_payload_hash,
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
        {
            "fixture_id": "stage5ap-outguess-synthetic-negative-control",
            "fixture_category": "synthetic_negative_control",
            "source_status": "synthetic_ci_only",
            "ready_state": "synthetic_ready",
            "expected_output_required": True,
            "expected_output_hash": hashlib.sha256(b"").hexdigest(),
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
        {
            "fixture_id": "stage5ap-historical-4gq25-jpg",
            "fixture_category": "outguess_known_positive_candidate",
            "source_status": "historical_source_reference",
            "ready_state": "blocked_asset_not_cached",
            "expected_output_required": True,
            "expected_output_hash": None,
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
        {
            "fixture_id": "stage5ap-historical-lp-outguessed-reference",
            "fixture_category": "lp_outguessed_reference",
            "source_status": "historical_source_reference",
            "ready_state": "blocked_expected_output_unknown",
            "expected_output_required": True,
            "expected_output_hash": None,
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
        {
            "fixture_id": "stage5ap-page49-51-lp-page-outguess",
            "fixture_category": "lp_page_outguess_blocked_guardrail",
            "source_status": "token_block_source_lock_candidate",
            "ready_state": "rejected_unsafe_or_out_of_scope",
            "expected_output_required": True,
            "expected_output_hash": None,
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
    ]
    record = {
        "record_type": "outguess_positive_control_matrix",
        "schema": "schemas/stego/outguess-positive-control-matrix-v0.schema.json",
        "stage_id": STAGE_ID,
        "matrix_record_count": len(rows),
        "synthetic_control_count": 2,
        "historical_fixture_count": 2,
        "lp_page_execution_candidate_count": 1,
        "ready_historical_fixture_count": 0,
        "toolchain_record": toolchain.as_posix(),
        "execution_enabled": False,
        "tool_executed": False,
        "lp_page_outguess_run_performed": False,
        "records": rows,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    if results_dir is not None:
        write_json(results_dir / "outguess_positive_control_matrix.json", record)
    return record


def build_guardrail(*, out: Path = GUARDRAIL_PATH) -> dict[str, Any]:
    record = {
        "record_type": "outguess_guardrail",
        "schema": "schemas/stego/outguess-guardrail-v0.schema.json",
        "stage_id": STAGE_ID,
        "guardrail_status": "active",
        "lp_page_outguess_run_performed": False,
        "historical_fixture_run_performed": False,
        "synthetic_fixture_run_performed": False,
        "broad_stego_scan_performed": False,
        "outguess_tool_executed": False,
        "openpuff_tool_executed": False,
        "mp3stego_tool_executed": False,
        "raw_fixture_committed": False,
        "extracted_payload_committed": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    return record
