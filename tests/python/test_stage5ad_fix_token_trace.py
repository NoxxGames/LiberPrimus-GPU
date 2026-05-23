from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ad_fix_token_trace_preserves_bounded_tokens() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-token-trace.yaml").read_text())["records"][0]

    assert [token["index29"] for token in record["input_tokens"]] == [25, 11]
    assert [token["index29"] for token in record["formula_output_tokens"]] == [24, 9]
    assert [token["index29"] for token in record["stage5l_candidate_major_reference_last_output_tokens"]] == [24, 10]
    assert record["token_trace_status"] == "formula_trace_matches_cuda_hash_not_stage5l_reference_hash"
