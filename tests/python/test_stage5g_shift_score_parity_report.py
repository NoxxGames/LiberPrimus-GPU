from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_parity_reporting.parity_report import build_parity_report


EXPECTED_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"


def test_stage5g_parity_report_requires_stage5f_hash_match() -> None:
    payload = yaml.safe_load(Path("data/cuda/stage5g-shift-score-parity-report.yaml").read_text(encoding="utf-8"))
    record = payload["records"][0]
    assert record["stage5f_cuda_native_hash_match"] is True
    assert record["stage5f_cuda_output_hash"] == EXPECTED_HASH
    assert record["native_reference_hash"] == EXPECTED_HASH
    assert record["production_gematria_mod29_cuda_ready"] is False


def test_stage5g_parity_report_builder_writes_raw_data_free_record(tmp_path: Path) -> None:
    out_dir = tmp_path / "reports"
    records = build_parity_report(parity_report_out=tmp_path / "parity.yaml", out_dir=out_dir)
    assert records[0]["stage5f_cuda_native_hash_match"] is True
    assert records[0]["real_liber_primus_data_used"] is False
    assert (out_dir / "shift_score_parity_report.json").is_file()
