from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_guardrails_block_execution_and_interpretation() -> None:
    payload = yaml.safe_load((ROOT / "data/token-block/stage5av-guardrail.yaml").read_text(encoding="utf-8"))
    false_fields = [
        "automatic_case_resolution_performed",
        "canonical_transcription_changed",
        "variant_byte_streams_generated",
        "full_cartesian_product_enumerated",
        "experiment_execution_performed",
        "dwh_hash_search_performed",
        "decode_attempt_performed",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ]
    assert all(payload[field] is False for field in false_fields)
