from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_solved_fixture_cuda_repeat.score_summary_preflight import build_score_summary_preflight


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5o_score_summary_preflight_uses_stage4i_triage_only_contract(tmp_path: Path) -> None:
    records = build_score_summary_preflight(
        score_summary_preflight_out=tmp_path / "score-summary.yaml",
        out_dir=tmp_path,
    )

    assert records == [
        {
            **records[0],
            "score_summary_contract": "stage4i",
            "score_interpretation": "triage_only",
            "stage4i_confidence_labels_only": True,
            "new_scorer_added": False,
            "confidence_label": "scoring_not_available",
            "stage5p_ready": True,
            "solve_claim": False,
        }
    ]


def test_stage5o_score_summary_preflight_blocks_when_repeat_parity_is_not_clean(tmp_path: Path) -> None:
    parity = _records("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml")
    for record in parity:
        record["repeat_parity_status"] = "skipped_not_requested"
    parity_path = tmp_path / "repeat-parity.yaml"
    parity_path.write_text(yaml.safe_dump({"records": parity}, sort_keys=False), encoding="utf-8")

    records = build_score_summary_preflight(
        repeat_parity=parity_path,
        score_summary_preflight_out=tmp_path / "score-summary.yaml",
        out_dir=tmp_path,
    )

    assert records[0]["score_summary_shape_status"] == "blocked_repeat_parity_not_clean"
    assert records[0]["stage5p_ready"] is False
