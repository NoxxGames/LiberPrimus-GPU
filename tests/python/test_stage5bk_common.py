import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


FORBIDDEN_TRUE_FLAGS = {
    "token_experiment_executed",
    "token_experiments_executed",
    "real_byte_stream_generated",
    "real_token_block_byte_streams_generated",
    "decoded_bytes_committed",
    "full_hex_body_committed",
    "raw_source_committed",
    "generated_outputs_committed",
    "cuda_execution_performed",
    "scoring_performed",
    "benchmark_performed",
    "solve_claim",
    "canonical_corpus_active",
    "page_boundaries_final",
    "active_token_block_manifest_changed",
    "codex_output_used",
    "hash_search_performed",
    "dwh_hash_search_performed",
    "decode_attempt_performed",
    "stego_tool_execution_performed",
}


def assert_no_forbidden_true(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN_TRUE_FLAGS:
                assert item in (False, 0, None), f"{key}={item!r}"
            assert_no_forbidden_true(item)
    elif isinstance(value, list):
        for item in value:
            assert_no_forbidden_true(item)
