"""Export Stage 4I scoring consolidation records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root
from libreprimus.scoring_consolidation.calibration_profiles import build_calibration_profile
from libreprimus.scoring_consolidation.compatibility import compatibility_records
from libreprimus.scoring_consolidation.confidence_labels import confidence_label_records
from libreprimus.scoring_consolidation.cpu_batch_integration import check_cpu_batch_summary
from libreprimus.scoring_consolidation.inventory import scorer_records
from libreprimus.scoring_consolidation.models import (
    CALIBRATION_PROFILE_PATH,
    CALIBRATION_REPORT_PATH,
    COMPATIBILITY_MAP_PATH,
    CONFIDENCE_LABELS_PATH,
    DEFAULT_CPU_BATCH_SUMMARY,
    DEFAULT_DATA_DIR,
    DEFAULT_OUT_DIR,
    SCORER_RECORDS_PATH,
)
from libreprimus.scoring_consolidation.report_builder import build_calibration_report


def consolidate_scoring(*, out_dir: Path = DEFAULT_OUT_DIR, data_dir: Path = DEFAULT_DATA_DIR, allow_warnings: bool = False) -> dict[str, Any]:
    """Build committed scoring records and ignored generated reports."""

    resolved_data = _resolve(data_dir)
    resolved_out = _resolve(out_dir)
    resolved_data.mkdir(parents=True, exist_ok=True)
    resolved_out.mkdir(parents=True, exist_ok=True)
    scorers = scorer_records()
    labels = confidence_label_records()
    mappings = compatibility_records()
    profile = build_calibration_profile()
    report = build_calibration_report(profile)
    compatibility = check_cpu_batch_summary(str(DEFAULT_CPU_BATCH_SUMMARY))
    warnings = _warnings(profile, compatibility)
    _write_record_set(resolved_data / SCORER_RECORDS_PATH, "scorer-records-v0", "schemas/scoring/scorer-record-v0.schema.json", scorers)
    _write_record_set(
        resolved_data / CONFIDENCE_LABELS_PATH,
        "confidence-label-records-v0",
        "schemas/scoring/confidence-label-record-v0.schema.json",
        labels,
    )
    _write_record_set(
        resolved_data / COMPATIBILITY_MAP_PATH,
        "scorer-compatibility-map-v0",
        "schemas/scoring/scorer-compatibility-map-v0.schema.json",
        mappings,
    )
    _write_record_set(
        resolved_data / CALIBRATION_PROFILE_PATH,
        "stage4i-calibration-profile-v0",
        "schemas/scoring/scoring-calibration-profile-v0.schema.json",
        [profile],
    )
    _write_record_set(
        resolved_data / CALIBRATION_REPORT_PATH,
        "stage4i-calibration-report-v0",
        "schemas/scoring/scoring-calibration-report-v0.schema.json",
        [report],
    )
    _write_json(resolved_out / "scorer_inventory.json", {"records": scorers})
    _write_json(resolved_out / "calibration_report_generated.json", report)
    _write_json(resolved_out / "cpu_batch_score_compatibility.json", compatibility)
    _write_jsonl(resolved_out / "warnings.jsonl", warnings)
    if warnings and not allow_warnings:
        raise ValueError("; ".join(str(item["warning"]) for item in warnings))
    return _summary(scorers, labels, mappings, profile, report, compatibility, warnings)


def _summary(
    scorers: list[dict[str, Any]],
    labels: list[dict[str, Any]],
    mappings: list[dict[str, Any]],
    profile: dict[str, Any],
    report: dict[str, Any],
    compatibility: dict[str, Any],
    warnings: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "record_type": "stage4i_scoring_consolidation_summary",
        "scorer_record_count": len(scorers),
        "confidence_label_count": len(labels),
        "compatibility_mapping_count": len(mappings),
        "calibration_profile_count": 1,
        "positive_controls_available": bool(report["positive_controls_available"]),
        "null_controls_available": bool(report["null_controls_available"]),
        "negative_controls_available": bool(report["negative_controls_available"]),
        "known_noisy_family_count": len(report["known_noisy_families"]),
        "known_negative_or_deprioritised_family_count": len(report["known_negative_or_deprioritised_families"]),
        "cpu_batch_compatible": bool(compatibility["compatible"]),
        "calibration_source": profile["calibration_source"],
        "warning_count": len(warnings),
        "solve_claim": False,
        "trusted_as_canonical": False,
        "cuda_used": False,
    }


def _warnings(profile: dict[str, Any], compatibility: dict[str, Any]) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    if profile["calibration_source"] != "generated_summary":
        warnings.append({"record_type": "stage4i_scoring_warning", "warning": "Stage 3C generated calibration summary unavailable; using research log summary."})
    if not compatibility["compatible"]:
        warnings.append({"record_type": "stage4i_scoring_warning", "warning": "CPU batch score compatibility check failed."})
    return warnings


def _write_record_set(path: Path, record_set_id: str, schema: str, records: list[dict[str, Any]]) -> None:
    payload = {"record_set_id": record_set_id, "schema": schema, "records": records}
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
