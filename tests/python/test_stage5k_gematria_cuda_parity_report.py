from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_cuda_parity_reporting.models import NATIVE_FIXTURE_HASH
from libreprimus.gematria_cuda_parity_reporting.parity_report import build_parity_report
from libreprimus.gematria_cuda_parity_reporting.validation import validate_stage5k_results


def test_stage5k_parity_report_requires_stage5j_hash_match(tmp_path: Path) -> None:
    parity_out = tmp_path / "parity.yaml"
    records = build_parity_report(parity_report_out=parity_out, out_dir=tmp_path)
    record = records[0]
    assert record["cuda_output_hash"] == NATIVE_FIXTURE_HASH
    assert record["cuda_native_hash_match"] is True
    assert record["gematria_cuda_synthetic_parity_verified"] is True
    assert record["gpu_benchmark_performed"] is False
    assert record["performance_claim"] is False
    assert record["speedup_claim"] is False


def test_stage5k_validation_rejects_performance_claims(tmp_path: Path) -> None:
    parity = tmp_path / "parity.yaml"
    audit = tmp_path / "audit.yaml"
    preflight = tmp_path / "preflight.yaml"
    score = tmp_path / "score.yaml"
    summary = tmp_path / "summary.yaml"
    for source, target in [
        ("data/cuda/stage5k-gematria-cuda-parity-report.yaml", parity),
        ("data/cuda/stage5k-gematria-cuda-device-code-audit.yaml", audit),
        ("data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml", preflight),
        ("data/cuda/stage5k-gematria-cuda-score-summary-preflight.yaml", score),
        ("data/cuda/stage5k-gematria-cuda-parity-reporting-summary.yaml", summary),
    ]:
        target.write_text(Path(source).read_text(encoding="utf-8"), encoding="utf-8")

    payload = yaml.safe_load(parity.read_text(encoding="utf-8"))
    payload["records"][0]["performance_claim"] = True
    parity.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    _, errors = validate_stage5k_results(
        parity_report_path=parity,
        device_code_audit_path=audit,
        preflight_path=preflight,
        score_preflight_path=score,
        summary_path=summary,
        results_dir=tmp_path,
    )
    assert any("performance_claim" in error for error in errors)
