"""Stage 4P result-store and score-summary unification models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

STAGE4P_OUTPUT_DIR = Path("experiments/results/result-store-unification/stage4p")
STAGE4P_SUMMARY_PATH = Path(
    "data/research/stage4p-result-store-score-summary-unification-summary.yaml"
)

UNIFIED_RESULT_SCHEMA = Path("schemas/results/unified-result-record-v0.schema.json")
UNIFIED_SCORE_SCHEMA = Path("schemas/results/unified-score-summary-record-v0.schema.json")
SOURCE_INVENTORY_SCHEMA = Path("schemas/results/result-source-inventory-v0.schema.json")
METHOD_STATUS_JOIN_SCHEMA = Path("schemas/results/result-method-status-join-v0.schema.json")
CROSS_STAGE_REPORT_SCHEMA = Path("schemas/results/cross-stage-comparison-report-v0.schema.json")
UNIFICATION_SUMMARY_SCHEMA = Path("schemas/results/result-store-unification-summary-v0.schema.json")

SOURCE_INVENTORY_JSON = "source_inventory.json"
UNIFIED_RESULT_JSONL = "unified_result_records.jsonl"
UNIFIED_SCORE_JSONL = "unified_score_summary_records.jsonl"
METHOD_STATUS_JOIN_JSON = "method_status_join.json"
CROSS_STAGE_REPORT_JSON = "cross_stage_report.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

CONFIDENCE_LABELS = {
    "positive_control_like",
    "plausible_lead",
    "weak_lead",
    "noisy",
    "inconclusive",
    "garbage",
    "negative_control_like",
    "scoring_not_available",
    "calibration_not_available",
}

METHOD_STATUS_ALIASES = {
    "infrastructure_only": "infrastructure_only",
    "infrastructure": "infrastructure",
    "active": "active",
    "noisy": "noisy",
    "inconclusive": "inconclusive",
    "negative": "negative",
    "retired": "retired",
    "deferred": "deferred",
    "blocked": "blocked",
    "unknown": "unknown",
}


@dataclass(frozen=True)
class ResultSourceDefinition:
    """Configured source for Stage 4P inventory."""

    source_id: str
    source_stage_id: str
    result_source_kind: str
    source_path: str
    required: bool
    optional_generated: bool = False
    raw_required: bool = False
    method_family: str = "unknown"
    source_record_type: str = "summary"
    schema_hint: str | None = None
    notes: tuple[str, ...] = ()
