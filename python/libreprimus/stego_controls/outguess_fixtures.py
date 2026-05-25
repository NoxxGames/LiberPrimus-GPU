"""Historical OutGuess fixture readiness records for Stage 5AP."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.token_block.models import FALSE_GUARDRAILS, STAGE_ID, write_json, write_yaml

HISTORICAL_PATH = Path("data/stego/stage5ap-outguess-historical-fixture-readiness.yaml")


def build_historical_fixture_readiness(*, out: Path = HISTORICAL_PATH, results_dir: Path | None = Path("experiments/results/stego-controls/stage5ap")) -> dict[str, Any]:
    records = [
        {
            "fixture_id": "stage5ap-historical-4gq25-jpg",
            "fixture_category": "image_fixture_candidate",
            "source_record_id": "stage4f_or_stage4e_reference",
            "ready_state": "blocked_asset_not_cached",
            "blockers": ["asset_not_cached", "expected_output_unknown", "toolchain_unverified"],
            "expected_output_required": True,
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
        {
            "fixture_id": "stage5ap-historical-lp-outguessed-reference",
            "fixture_category": "lp_outguessed_reference",
            "source_record_id": "stage4f_or_stage4e_reference",
            "ready_state": "source_only_missing_expected_output",
            "blockers": ["expected_output_unknown", "manual_source_review_required"],
            "expected_output_required": True,
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
        {
            "fixture_id": "stage5ap-historical-interconnectedness-mp3",
            "fixture_category": "openpuff_interconnectedness_candidate",
            "source_record_id": "stage4f_audio_reference",
            "ready_state": "reference_only",
            "blockers": ["openpuff_manual_required", "expected_output_unknown"],
            "expected_output_required": True,
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
        {
            "fixture_id": "stage5ap-historical-761-instar-mp3",
            "fixture_category": "mp3_instar_candidate",
            "source_record_id": "stage4f_audio_reference",
            "ready_state": "reference_only",
            "blockers": ["mp3stego_manual_required", "expected_output_unknown"],
            "expected_output_required": True,
            "execution_enabled": False,
            "tool_executed": False,
            "solve_claim": False,
        },
    ]
    payload = {
        "record_type": "outguess_historical_fixture_readiness",
        "schema": "schemas/stego/outguess-historical-fixture-readiness-v0.schema.json",
        "stage_id": STAGE_ID,
        "historical_fixture_count": len(records),
        "historical_fixture_ready_count": 0,
        "historical_fixture_blocked_count": len(records),
        "execution_enabled": False,
        "tool_executed": False,
        "records": records,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    if results_dir is not None:
        write_json(results_dir / "outguess_historical_fixture_readiness.json", payload)
    return payload
