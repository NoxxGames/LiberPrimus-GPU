"""Validation helpers for Stage 5AP token-block records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .mapping import validate_mapping_preflight
from .models import read_yaml
from .transcription import validate_transcription_record


def validate_stage5ap(
    *,
    source_lock: Path,
    image_provenance: Path,
    transcription: Path,
    coordinates: Path,
    alphabet_registry: Path,
    mapping_preflight: Path,
    null_control_plan: Path,
    dwh_context: Path,
    research_summary: Path,
    next_stage_decision: Path,
    summary: Path,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    records = {
        "source_lock": _read(errors, source_lock),
        "image_provenance": _read(errors, image_provenance),
        "transcription": _read(errors, transcription),
        "coordinates": _read(errors, coordinates),
        "alphabet_registry": _read(errors, alphabet_registry),
        "mapping_preflight": _read(errors, mapping_preflight),
        "null_control_plan": _read(errors, null_control_plan),
        "dwh_context": _read(errors, dwh_context),
        "research_summary": _read(errors, research_summary),
        "next_stage_decision": _read(errors, next_stage_decision),
        "summary": _read(errors, summary),
    }
    errors.extend(validate_transcription_record(records["transcription"]))
    errors.extend(validate_mapping_preflight(records["mapping_preflight"]))
    if records["coordinates"].get("coordinate_record_count") != 256:
        errors.append("coordinate_record_count_not_256")
    if records["alphabet_registry"].get("primary_alphabet_length") != 60:
        errors.append("primary_alphabet_length_not_60")
    if records["alphabet_registry"].get("observed_suffix_count") != 59:
        errors.append("observed_suffix_count_not_59")
    if records["alphabet_registry"].get("lowercase_f_absent") is not True:
        errors.append("lowercase_f_not_marked_absent")
    for name, payload in records.items():
        if payload.get("solve_claim") is not False:
            errors.append(f"{name}:solve_claim_not_false")
        for flag in [
            "network_fetch_performed",
            "online_repo_clone_performed",
            "google_drive_storage_used",
            "deep_research_performed",
            "ocr_performed",
            "ai_ml_interpretation_performed",
            "hash_preimage_search_performed",
            "cuda_execution_performed",
            "benchmark_performed",
        ]:
            if flag in payload and payload[flag] is not False:
                errors.append(f"{name}:{flag}_not_false")
    if records["summary"].get("token_count") != 256:
        errors.append("summary_token_count_not_256")
    counts = {
        "stage_id": "stage-5ap",
        "source_locked_page_image_count": records["source_lock"].get("source_locked_page_image_count", 0),
        "page_image_provenance_records": records["image_provenance"].get("page_image_record_count", 0),
        "token_count": records["transcription"].get("token_count", 0),
        "coordinate_record_count": records["coordinates"].get("coordinate_record_count", 0),
        "observed_suffix_count": records["alphabet_registry"].get("observed_suffix_count", 0),
        "mapping_value_min": records["mapping_preflight"].get("value_min"),
        "mapping_value_max": records["mapping_preflight"].get("value_max"),
        "deep_research_next_ready": records["next_stage_decision"].get("deep_research_next_ready", False),
        "validation_error_count": len(errors),
    }
    return counts, errors


def _read(errors: list[str], path: Path) -> dict[str, Any]:
    try:
        payload = read_yaml(path)
    except (OSError, ValueError) as exc:
        errors.append(f"read_failed:{path}:{exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"record_not_mapping:{path}")
        return {}
    return payload
