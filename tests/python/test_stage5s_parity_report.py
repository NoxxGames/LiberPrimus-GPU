from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_expanded_cuda_result_store.parity_report import build_parity_report


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5s_parity_report_integrates_exact_three_stage5r_records() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-parity-report.yaml")
    assert [record["fixture_id"] for record in records] == [
        "p57-parable",
        "some-wisdom",
        "the-loss-of-divinity",
    ]
    assert len(records) == 3
    assert {record["parity_status"] for record in records} == {"passed"}
    assert all(record["stage5q_native_hash"] == record["stage5r_cuda_hash"] for record in records)
    assert all(record["executed_semantics"] == "gematria_shift_score_only" for record in records)
    assert all(record["original_transform_family_semantics_exercised"] is False for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
    assert all(record["stage5r_cuda_execution_performed"] is True for record in records)


def test_stage5s_parity_report_excludes_consumed_controls_and_blocked_original_families() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-parity-report.yaml")
    fixtures = {str(record["fixture_id"]) for record in records}
    assert fixtures.isdisjoint(
        {
            "a-warning",
            "an-instruction",
            "a-koan",
            "a-koan-a-man-rotated-reverse-gematria",
            "a-koan-during-firfumferenfe-vigenere",
        }
    )
    assert all(record["consumed_controls_excluded"] is True for record in records)
    assert all(record["blocked_original_family_fixtures_excluded"] is True for record in records)


def test_stage5s_parity_report_builder_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first.yaml"
    second = tmp_path / "second.yaml"
    out_dir = tmp_path / "out"
    build_parity_report(parity_report_out=first, out_dir=out_dir)
    build_parity_report(parity_report_out=second, out_dir=out_dir)
    assert first.read_text(encoding="utf-8") == second.read_text(encoding="utf-8")
