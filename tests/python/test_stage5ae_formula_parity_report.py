from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.corrected_bounded_p56_reporting.models import CORRECTED_FORMULA_HASH, HISTORICAL_EXPECTED_HASH
from libreprimus.corrected_bounded_p56_reporting.records import build_formula_parity_records


def test_stage5ae_formula_parity_consumes_stage5ad_fix_summary() -> None:
    record = build_formula_parity_records()[0]
    assert record["source_evidence"]["source_primary_root_cause"] == "expected_hash_reference_lineage_mismatch"
    assert record["source_evidence"]["source_cuda_formula_matches_stage5x_formula"] is True


def test_stage5ae_formula_parity_preserves_historical_failure() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-formula-parity-report.yaml").read_text())["records"][0]
    assert record["historical_stage5ad_status"] == "failed_hash_mismatch"
    assert record["stage5ad_historical_failure_preserved"] is True
    assert record["historical_stage5ad_reclassified_as_passed"] is False
    assert record["historical_expected_hash"] == HISTORICAL_EXPECTED_HASH
    assert record["corrected_formula_expected_hash"] == CORRECTED_FORMULA_HASH
    assert record["corrected_formula_computed_hash"] == CORRECTED_FORMULA_HASH
    assert record["corrected_formula_parity_status"] == "passed"
