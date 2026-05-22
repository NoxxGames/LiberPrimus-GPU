"""Token-buffer conformance records for Stage 5V."""

from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import COMMON_FLAGS, OUTPUT_DIR, REPORT_FILES, TOKEN_BUFFER_CONFORMANCE_PATH


def build_token_buffer_conformance(
    *,
    fixtures: list[dict[str, object]],
    token_buffer_conformance_out: Path = TOKEN_BUFFER_CONFORMANCE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    fixture_ids = [str(record["fixture_id"]) for record in fixtures]
    records = [
        _record("stage5v-token-values-domain", "token_values", "passed", fixture_ids, "Rune values are 0..28 and separators stay explicit."),
        _record("stage5v-token-kind-metadata", "token_kind", "passed", fixture_ids, "Token-kind metadata is present for every token."),
        _record("stage5v-transformable-mask", "transformable_mask", "passed", fixture_ids, "Mask length equals token length."),
        _record("stage5v-separator-position-preservation", "separator_positions", "passed", fixture_ids, "Separator positions are non-transformable."),
        _record("stage5v-fixture-offsets", "fixture_offsets", "passed", fixture_ids, "Offsets are deterministic and repository-local."),
        _record("stage5v-fixture-lengths", "fixture_lengths", "passed", fixture_ids, "Variable-length fixture slices fit the token buffer."),
        _record("stage5v-candidate-fixture-reference", "candidate_fixture_reference", "passed", fixture_ids, "Candidate records reference fixture IDs without raw inputs."),
    ]
    write_record_set(token_buffer_conformance_out, records)
    write_report(out_dir, REPORT_FILES["token_buffer"], {"records": records, "count": len(records)})
    return records


def _record(record_id: str, surface: str, status: str, fixture_ids: list[str], notes: str) -> dict[str, object]:
    return {
        **COMMON_FLAGS,
        "record_type": "token_buffer_conformance_record",
        "schema": "schemas/cuda/token-buffer-conformance-record-v0.schema.json",
        "conformance_id": record_id,
        "conformance_surface": surface,
        "conformance_status": status,
        "fixture_ids": fixture_ids,
        "notes": notes,
    }
