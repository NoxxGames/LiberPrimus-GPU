"""Expected-output metadata for real and synthetic Stage 4N controls."""

from __future__ import annotations

import hashlib
from typing import Any

from libreprimus.stego_positive_controls.models import COMMON_FALSE_FLAGS


def build_expected_output_record(record: dict[str, Any], *, category: str, synthetic: bool = False) -> dict[str, Any]:
    """Build expected-output metadata without extracting payloads."""

    source_record_id = str(record.get("fixture_id") or record.get("artifact_id") or "unknown")
    payload_hash = record.get("expected_payload_sha256")
    text_hash = record.get("expected_payload_text_sha256")
    is_reference = "reference_only" in category or category == "lp_outguessed_reference"
    if synthetic:
        expected_payload = f"stage4n:{source_record_id}:synthetic-payload\n".encode("utf-8")
        status = "synthetic_known"
        expected_required = category == "synthetic_positive_control"
        payload_hash = hashlib.sha256(expected_payload).hexdigest() if expected_required else None
        text_hash = payload_hash
    elif payload_hash or text_hash:
        status = "known_hash" if payload_hash else "known_text_hash"
        expected_required = True
    elif is_reference:
        status = "not_required_reference_only"
        expected_required = False
    else:
        status = "unknown"
        expected_required = True
    return {
        "record_type": "stego_expected_output_record",
        "expected_output_id": f"stage4n-expected-{source_record_id}",
        "source_record_id": source_record_id,
        "fixture_category": category,
        "expected_output_status": status,
        "expected_output_required": expected_required,
        "expected_payload_sha256": payload_hash,
        "expected_payload_text_sha256": text_hash,
        "synthetic": synthetic,
        "notes": "Historical readiness remains blocked unless exact expected output metadata is known.",
        **COMMON_FALSE_FLAGS,
    }
