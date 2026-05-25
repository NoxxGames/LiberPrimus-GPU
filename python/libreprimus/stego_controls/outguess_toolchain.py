"""Best-effort OutGuess toolchain detection without extraction execution."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from libreprimus.token_block.models import FALSE_GUARDRAILS, STAGE_ID, write_yaml


def detect_outguess_toolchain(*, out: Path) -> dict[str, Any]:
    outguess_path = shutil.which("outguess") or shutil.which("outguess.exe")
    strings_path = shutil.which("strings")
    certutil_path = shutil.which("certutil")
    record = {
        "record_type": "outguess_toolchain_readiness",
        "schema": "schemas/stego/outguess-toolchain-readiness-v0.schema.json",
        "stage_id": STAGE_ID,
        "tool_name": "outguess",
        "tool_available": outguess_path is not None,
        "tool_path_recorded": outguess_path,
        "toolchain_state": "outguess_available_unverified" if outguess_path else "outguess_missing",
        "strings_available": strings_path is not None,
        "certutil_available": certutil_path is not None,
        "tool_executed": False,
        "extraction_executed": False,
        "lp_page_outguess_run_performed": False,
        "historical_fixture_run_performed": False,
        "synthetic_fixture_run_performed": False,
        "expected_output_policy_required": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    return record
