from __future__ import annotations

from pathlib import Path

from libreprimus.result_store.method_status_join import build_method_status_join
from libreprimus.result_store.stage4p_export import write_jsonl
from libreprimus.result_store.unified_models import UNIFIED_RESULT_JSONL


def test_method_status_join_preserves_noisy_state(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    write_jsonl(out_dir / UNIFIED_RESULT_JSONL, [_result("caesar_affine")])
    joins = build_method_status_join(out_dir=out_dir)
    assert joins[0]["method_status"] == "noisy"
    assert joins[0]["join_status"] == "joined"


def test_method_status_join_reports_missing_method(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    write_jsonl(out_dir / UNIFIED_RESULT_JSONL, [_result("not_a_method")])
    joins = build_method_status_join(out_dir=out_dir)
    assert joins[0]["join_status"] == "missing_method_status"
    assert joins[0]["warnings"]


def _result(method_family: str) -> dict:
    return {
        "record_type": "unified_result_record",
        "unified_result_id": "result-" + method_family,
        "method_family": method_family,
        "method_status": "unknown",
        "retirement_status": "unknown",
    }
