"""Score-vector conformance records for Stage 5V."""

from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import COMMON_FLAGS, OUTPUT_DIR, REPORT_FILES, SCORE_VECTOR_CONFORMANCE_PATH

COMPONENTS = [
    "candidate_id",
    "score_status",
    "confidence_label",
    "score_value",
    "component_scores",
    "scorer_id",
    "calibration_profile_id",
]


def build_score_vector_conformance(
    *,
    score_vector_conformance_out: Path = SCORE_VECTOR_CONFORMANCE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    records = [
        {
            **COMMON_FLAGS,
            "record_type": "score_vector_conformance_record",
            "schema": "schemas/cuda/score-vector-conformance-record-v0.schema.json",
            "score_vector_id": f"stage5v-score-vector-{component}",
            "score_component": component,
            "conformance_status": "passed",
            "score_status": "scored" if component != "calibration_profile_id" else "calibration_not_available",
            "confidence_label": "inconclusive" if component != "calibration_profile_id" else "calibration_not_available",
            "score_interpretation": "triage_only",
            "stage4i_compatible": True,
            "generated_body_committed": False,
        }
        for component in COMPONENTS
    ]
    write_record_set(score_vector_conformance_out, records)
    write_report(out_dir, REPORT_FILES["score_vector"], {"records": records, "count": len(records)})
    return records
