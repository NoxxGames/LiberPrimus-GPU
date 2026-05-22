from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_parity.native_execution import build_native_run_records
from libreprimus.prime_minus_one_native_parity.parity_records import build_parity_records
from libreprimus.prime_minus_one_native_parity.score_summary_preflight import build_score_summary_preflight


def test_stage5x_score_summary_preflight_uses_stage4i_triage_labels(tmp_path: Path) -> None:
    run = tmp_path / "run.yaml"
    parity = tmp_path / "parity.yaml"
    score = tmp_path / "score.yaml"
    build_native_run_records(native_run_out=run, out_dir=tmp_path)
    build_parity_records(native_run=run, native_parity_out=parity, out_dir=tmp_path)
    records = build_score_summary_preflight(native_parity=parity, score_summary_preflight_out=score, out_dir=tmp_path)
    labels = {record["mapping_id"]: record["confidence_label"] for record in records}
    assert labels["stage5w-mapping-synthetic-prime-control-v0"] == "known_control"
    assert labels["stage5w-mapping-p56-stage4o-bounded-v0"] == "known_control"
    assert labels["stage5w-mapping-p56-full-fixture-blocked-v0"] == "scoring_not_available"
    assert all(record["score_interpretation"] == "triage_only" for record in records)
