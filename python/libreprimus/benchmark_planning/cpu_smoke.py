"""Tiny deterministic CPU-only smoke diagnostics for Stage 4Q."""

from __future__ import annotations

import hashlib
import time
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path, write_jsonl
from libreprimus.benchmark_planning.models import CPU_ONLY_POLICY, SMOKE_JSONL, STAGE4Q_OUTPUT_DIR

SMOKE_INPUT = "stage4q synthetic cpu benchmark smoke input"
SMOKE_CANDIDATES = (
    ("stage4q-smoke-direct-translation", "direct_translation", "stage4q synthetic cpu benchmark smoke input"),
    ("stage4q-smoke-reverse-gematria", "reverse_gematria", "tupni ekoms kramhcneb upc citehtnys q4egats"),
    ("stage4q-smoke-prime-minus-one", "prime_minus_one_stream", "stage4q|prime-minus-one|diagnostic"),
)


def run_cpu_smoke(*, out_dir: Path = STAGE4Q_OUTPUT_DIR) -> list[dict[str, Any]]:
    """Write deterministic CPU-only smoke records without making performance claims."""

    records: list[dict[str, Any]] = []
    for candidate_id, transform_family, output_text in SMOKE_CANDIDATES:
        start_ns = time.perf_counter_ns()
        token_hash = _sha256(f"{candidate_id}:{SMOKE_INPUT}:{output_text}".encode("utf-8"))
        text_hash = _sha256(output_text.encode("utf-8"))
        elapsed_ns = max(time.perf_counter_ns() - start_ns, 0)
        records.append(
            {
                "record_type": "cpu_benchmark_smoke_record",
                "benchmark_scope": "cpu_smoke",
                "benchmark_status": "smoke_passed",
                "candidate_id": candidate_id,
                "input_stream_id": "stage4q-synthetic-smoke-stream",
                "transform_family": transform_family,
                "output_token_hash": token_hash,
                "output_text_hash": text_hash,
                "diagnostic_elapsed_ns": elapsed_ns,
                "timing_is_diagnostic": True,
                "performance_claim": False,
                **CPU_ONLY_POLICY,
            }
        )
    write_jsonl(resolve_repo_path(out_dir) / SMOKE_JSONL, records)
    return records


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()
