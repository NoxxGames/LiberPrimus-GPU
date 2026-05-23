from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ad_fix_stream_trace_uses_stage5w_bounded_values() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-stream-trace.yaml").read_text())["records"][0]

    assert record["first_n_primes"] == [2, 3]
    assert record["stream_values_used"] == [1, 2]
    assert record["stream_formula"] == "(prime_i - 1) mod 29"
    assert record["raw_data_required"] is False
