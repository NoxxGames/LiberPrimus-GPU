"""Constants for Stage 4I scoring consolidation."""

from __future__ import annotations

from pathlib import Path

DEFAULT_DATA_DIR = Path("data/scoring")
DEFAULT_OUT_DIR = Path("experiments/results/scoring-consolidation/stage4i")
DEFAULT_CPU_BATCH_SUMMARY = Path("data/research/stage4h-cpu-batch-api-summary.yaml")
STAGE3C_GENERATED_SUMMARY = Path("experiments/results/scoring-calibration/stage3c/calibration_summary.json")
STAGE3C_RESEARCH_LOG = Path("research-log/2026-05-16-stage-3c-scoring-calibration-summary.md")
METHOD_STATUS_RECORDS = Path("data/research/method-family-status-records-v0.yaml")
METHOD_RETIREMENT_RECORDS = Path("data/research/method-retirement-records-v0.yaml")

SCORER_SCHEMA = Path("schemas/scoring/scorer-record-v0.schema.json")
CALIBRATION_PROFILE_SCHEMA = Path("schemas/scoring/scoring-calibration-profile-v0.schema.json")
SCORE_SUMMARY_SCHEMA = Path("schemas/scoring/score-summary-record-v0.schema.json")
CONFIDENCE_LABEL_SCHEMA = Path("schemas/scoring/confidence-label-record-v0.schema.json")
COMPATIBILITY_MAP_SCHEMA = Path("schemas/scoring/scorer-compatibility-map-v0.schema.json")
CALIBRATION_REPORT_SCHEMA = Path("schemas/scoring/scoring-calibration-report-v0.schema.json")

SCORER_RECORDS_PATH = Path("scorer-records-v0.yaml")
CONFIDENCE_LABELS_PATH = Path("confidence-label-records-v0.yaml")
COMPATIBILITY_MAP_PATH = Path("scorer-compatibility-map-v0.yaml")
CALIBRATION_PROFILE_PATH = Path("stage4i-calibration-profile-v0.yaml")
CALIBRATION_REPORT_PATH = Path("stage4i-calibration-report-v0.yaml")

SCORER_ID = "minimal_triage_v0"
SCORER_VERSION = "minimal-triage-score-v0"
CALIBRATION_PROFILE_ID = "stage4i-stage3c-minimal-triage-calibration-v0"

CONFIDENCE_LABELS = (
    "positive_control_like",
    "plausible_lead",
    "weak_lead",
    "noisy",
    "inconclusive",
    "garbage",
    "negative_control_like",
    "scoring_not_available",
    "calibration_not_available",
)
