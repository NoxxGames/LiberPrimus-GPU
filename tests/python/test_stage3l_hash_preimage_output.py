from __future__ import annotations

import json
import subprocess
from pathlib import Path

from jsonschema import validate

REPO = Path(__file__).resolve().parents[2]


def test_generated_candidate_record_schema_validates() -> None:
    schema = json.loads(
        (REPO / "schemas/web/hash-preimage-candidate-record-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    record = {
        "record_type": "hash_preimage_candidate_record",
        "run_id": "synthetic",
        "pack_id": "pack",
        "candidate_id": "candidate",
        "candidate_group": "group",
        "literal_text": "abc",
        "byte_variant": "raw",
        "encoding": "utf-8",
        "candidate_bytes_sha256": "a" * 64,
        "digest_algorithm": "sha256",
        "digest_hex": "a" * 64,
        "target_cookie_id": "cookie",
        "target_cookie_name": "167",
        "exact_match": False,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
        "notes": "test",
    }

    validate(instance=record, schema=schema)


def test_run_summary_schema_validates() -> None:
    schema = json.loads(
        (REPO / "schemas/web/hash-preimage-run-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    summary = {
        "record_type": "hash_preimage_run_summary",
        "run_id": "synthetic",
        "generated_at_utc": "2026-05-17T00:00:00Z",
        "algorithm": "sha256",
        "target_cookie_count": 2,
        "pack_count": 2,
        "candidate_count": 1809,
        "comparison_count": 3618,
        "exact_match_count": 0,
        "output_paths": {},
        "warnings": [],
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
    }

    validate(instance=summary, schema=schema)


def test_hash_preimage_generated_outputs_ignored() -> None:
    for path in [
        "experiments/results/hash-preimage/stage3l/hash_candidate_records.jsonl",
        "experiments/results/hash-preimage/stage3l/exact_matches.jsonl",
        "experiments/results/hash-preimage/stage3l/summary.json",
    ]:
        assert (
            subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=REPO, check=False).returncode
            == 0
        )
