"""Validation for Stage 5AP OutGuess control records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.token_block.models import read_yaml


def validate_stage5ap_outguess(
    *,
    policy: Path,
    toolchain: Path,
    matrix: Path,
    historical: Path,
    guardrail: Path,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    records = {
        "policy": _read(errors, policy),
        "toolchain": _read(errors, toolchain),
        "matrix": _read(errors, matrix),
        "historical": _read(errors, historical),
        "guardrail": _read(errors, guardrail),
    }
    for name, payload in records.items():
        if payload.get("solve_claim") is not False:
            errors.append(f"{name}:solve_claim_not_false")
        for flag in [
            "tool_executed",
            "stego_tool_execution_performed",
            "lp_page_outguess_run_performed",
            "historical_fixture_run_performed",
            "network_fetch_performed",
            "cuda_execution_performed",
        ]:
            if flag in payload and payload[flag] is not False:
                errors.append(f"{name}:{flag}_not_false")
    for record in records["matrix"].get("records", []):
        if record.get("tool_executed") is not False:
            errors.append(f"matrix_record_tool_executed:{record.get('fixture_id')}")
        if record.get("solve_claim") is not False:
            errors.append(f"matrix_record_solve_claim:{record.get('fixture_id')}")
    counts = {
        "stage_id": "stage-5ap",
        "toolchain_state": records["toolchain"].get("toolchain_state"),
        "matrix_record_count": records["matrix"].get("matrix_record_count", 0),
        "synthetic_control_count": records["matrix"].get("synthetic_control_count", 0),
        "historical_fixture_count": records["historical"].get("historical_fixture_count", 0),
        "historical_fixture_ready_count": records["historical"].get("historical_fixture_ready_count", 0),
        "validation_error_count": len(errors),
    }
    return counts, errors


def _read(errors: list[str], path: Path) -> dict[str, Any]:
    try:
        payload = read_yaml(path)
    except (OSError, ValueError) as exc:
        errors.append(f"read_failed:{path}:{exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"record_not_mapping:{path}")
        return {}
    return payload
