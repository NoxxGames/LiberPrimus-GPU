"""Build and export Stage 4J observation-review records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.observation_review.decision_builder import build_review_decisions
from libreprimus.observation_review.loaders import load_observation_inputs, write_yaml_document, write_yaml_records
from libreprimus.observation_review.models import (
    DEFAULT_DECISIONS_OUT,
    DEFAULT_OUT_DIR,
    DEFAULT_POLICY_OUT,
    DEFAULT_PROMOTIONS_OUT,
    DEFAULT_QUARANTINE_OUT,
    DEFAULT_SUMMARY_OUT,
)
from libreprimus.observation_review.path_sanitisation import check_paths_summary
from libreprimus.observation_review.policy import build_policy_record
from libreprimus.observation_review.promotion_gates import evaluate_promotion
from libreprimus.observation_review.quarantine import build_quarantine_record
from libreprimus.observation_review.summary import summarize_review
from libreprimus.paths import repo_root


def build_observation_review(
    *,
    out_dir: Path = repo_root() / DEFAULT_OUT_DIR,
    policy_out: Path = repo_root() / DEFAULT_POLICY_OUT,
    decisions_out: Path = repo_root() / DEFAULT_DECISIONS_OUT,
    promotions_out: Path = repo_root() / DEFAULT_PROMOTIONS_OUT,
    quarantine_out: Path = repo_root() / DEFAULT_QUARANTINE_OUT,
    summary_out: Path = repo_root() / DEFAULT_SUMMARY_OUT,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Build committed Stage 4J review records and generated local reports."""

    out_dir.mkdir(parents=True, exist_ok=True)
    inputs = load_observation_inputs()
    decisions = build_review_decisions(inputs)
    promotions = [evaluate_promotion(decision) for decision in decisions]
    for decision, promotion in zip(decisions, promotions, strict=True):
        decision["promotion_blocked_reasons"] = promotion["blocked_reasons"]
    quarantines = [
        record for decision in decisions if (record := build_quarantine_record(decision)) is not None
    ]
    path_summary = check_paths_summary(repo_root())
    if path_summary["findings"] and not allow_warnings:
        raise ValueError("Path sanitisation or stale-document findings require repair.")

    policy = build_policy_record()
    summary = summarize_review(
        decisions=decisions,
        promotions=promotions,
        quarantines=quarantines,
        path_summary=path_summary,
    )

    write_yaml_document(policy_out, policy)
    write_yaml_records(
        decisions_out,
        record_set_id="stage4j-observation-review-decisions",
        schema="schemas/observations/observation-review-decision-v0.schema.json",
        records=decisions,
    )
    write_yaml_records(
        promotions_out,
        record_set_id="stage4j-observation-promotion-records",
        schema="schemas/observations/observation-promotion-record-v0.schema.json",
        records=promotions,
    )
    write_yaml_records(
        quarantine_out,
        record_set_id="stage4j-observation-quarantine-records",
        schema="schemas/observations/observation-quarantine-record-v0.schema.json",
        records=quarantines,
    )
    write_yaml_document(summary_out, summary)

    _write_json(out_dir / "review_decision_report.json", {"records": decisions})
    _write_json(out_dir / "quarantine_report.json", {"records": quarantines})
    _write_json(out_dir / "promotion_gate_report.json", {"records": promotions})
    _write_json(out_dir / "path_sanitisation_report.json", path_summary)
    (out_dir / "warnings.jsonl").write_text("", encoding="utf-8")

    return summary


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
