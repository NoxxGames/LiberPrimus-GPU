"""Build and export Stage 4L observation promotion records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.observation_promotion.ledger_builder import build_promotion_ledger
from libreprimus.observation_promotion.loaders import load_stage4l_inputs, write_yaml_document, write_yaml_records
from libreprimus.observation_promotion.manifest_readiness import build_manifest_readiness_records
from libreprimus.observation_promotion.models import (
    DEFAULT_BLOCKERS_OUT,
    DEFAULT_LEDGER_OUT,
    DEFAULT_MANIFEST_READINESS_OUT,
    DEFAULT_OUT_DIR,
    DEFAULT_READINESS_OUT,
    DEFAULT_SUMMARY_OUT,
)
from libreprimus.observation_promotion.summary import summarize_promotion
from libreprimus.paths import repo_root


def build_observation_promotion(
    *,
    out_dir: Path = repo_root() / DEFAULT_OUT_DIR,
    ledger_out: Path = repo_root() / DEFAULT_LEDGER_OUT,
    readiness_out: Path = repo_root() / DEFAULT_READINESS_OUT,
    blockers_out: Path = repo_root() / DEFAULT_BLOCKERS_OUT,
    manifest_readiness_out: Path = repo_root() / DEFAULT_MANIFEST_READINESS_OUT,
    summary_out: Path = repo_root() / DEFAULT_SUMMARY_OUT,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Build Stage 4L committed ledgers and ignored generated reports."""

    del allow_warnings
    out_dir.mkdir(parents=True, exist_ok=True)
    inputs = load_stage4l_inputs()
    decisions = inputs["decisions"]
    ledger_records, readiness_records, blocker_records = build_promotion_ledger(
        decisions,
        inputs["source_locks"],
    )
    manifest_readiness_records = build_manifest_readiness_records()
    summary = summarize_promotion(
        decisions=decisions,
        ledger_records=ledger_records,
        readiness_records=readiness_records,
        blocker_records=blocker_records,
        manifest_readiness_records=manifest_readiness_records,
    )
    summary["relevant_record_counts"] = inputs["relevant_record_counts"]
    summary["disabled_manifest_paths"] = inputs["disabled_manifest_paths"]

    write_yaml_records(
        ledger_out,
        record_set_id="stage4l-reviewed-observation-promotion-ledger",
        schema="schemas/observations/reviewed-observation-promotion-ledger-v0.schema.json",
        records=ledger_records,
    )
    write_yaml_records(
        readiness_out,
        record_set_id="stage4l-observation-promotion-readiness-records",
        schema="schemas/observations/observation-promotion-readiness-record-v0.schema.json",
        records=readiness_records,
    )
    write_yaml_records(
        blockers_out,
        record_set_id="stage4l-observation-promotion-blocker-records",
        schema="schemas/observations/observation-promotion-blocker-record-v0.schema.json",
        records=blocker_records,
    )
    write_yaml_records(
        manifest_readiness_out,
        record_set_id="stage4l-manifest-readiness-records",
        schema="schemas/experiments/manifest-readiness-record-v0.schema.json",
        records=manifest_readiness_records,
    )
    write_yaml_document(summary_out, summary)

    _write_json(out_dir / "promotion_ledger_report.json", {"records": ledger_records, "summary": summary})
    _write_json(out_dir / "manifest_readiness_report.json", {"records": manifest_readiness_records})
    _write_json(out_dir / "blocker_report.json", {"records": blocker_records})
    (out_dir / "warnings.jsonl").write_text("", encoding="utf-8")
    return summary


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
