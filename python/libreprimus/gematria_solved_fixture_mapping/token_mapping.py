"""Build Stage 5L solved-fixture-safe Gematria token mapping records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, resolve_repo_path
from libreprimus.gematria_solved_fixture_mapping.export import write_record_set, write_report
from libreprimus.gematria_solved_fixture_mapping.models import (
    COMMON_POLICY_FLAGS,
    OUTPUT_DIR,
    REMAINING_APPROVAL_BLOCKER,
    RESOLVABLE_BLOCKERS,
    STAGE4O_SOLVED_FIXTURE_MANIFEST,
    STAGE5K_PREFLIGHT_PATH,
    TOKEN_DOMAIN,
    TOKEN_DOMAIN_MAX,
    TOKEN_DOMAIN_MIN,
    TOKEN_MAPPING_JSON,
    TOKEN_MAPPING_PATH,
)
from libreprimus.paths import repo_root


def canonical_hash(payload: Any) -> str:
    """Return the Stage 5L stable SHA-256 hash over canonical JSON."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_token_mapping_records(
    *,
    source_manifest: Path = STAGE4O_SOLVED_FIXTURE_MANIFEST,
    preflight: Path = STAGE5K_PREFLIGHT_PATH,
    token_mapping_out: Path = TOKEN_MAPPING_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build source-backed 0..28 Gematria token mapping records."""

    manifest = read_yaml(source_manifest)
    if "source_manifest" in manifest and "input_streams" not in manifest:
        source_manifest_value = Path(str(manifest["source_manifest"]))
        source_manifest = (
            source_manifest_value
            if source_manifest_value.is_absolute()
            else resolve_repo_path(source_manifest_value)
        )
        manifest = read_yaml(source_manifest)
    preflight_records = _records(read_yaml(preflight))
    streams = {
        str(stream["input_stream_id"]): stream
        for stream in manifest.get("input_streams", [])
        if isinstance(stream, dict)
    }
    candidates = {
        str(candidate["candidate_id"]): candidate
        for candidate in manifest.get("transform_candidates", [])
        if isinstance(candidate, dict)
    }
    records: list[dict[str, Any]] = []
    for index, preflight_record in enumerate(preflight_records):
        stream_id = str(preflight_record["source_input_stream_id"])
        candidate_id = str(preflight_record["candidate_id"])
        stream = streams.get(stream_id)
        candidate = candidates.get(candidate_id)
        records.append(
            _record_from_preflight(
                preflight_record=preflight_record,
                stream=stream,
                candidate=candidate,
                source_manifest=source_manifest,
                index=index,
            )
        )
    write_record_set(token_mapping_out, records)
    write_report(out_dir, TOKEN_MAPPING_JSON, {"records": records})
    return records


def _record_from_preflight(
    *,
    preflight_record: dict[str, Any],
    stream: dict[str, Any] | None,
    candidate: dict[str, Any] | None,
    source_manifest: Path,
    index: int,
) -> dict[str, Any]:
    blockers: list[str] = []
    tokens = list(stream.get("tokens", [])) if stream else []
    token_values: list[int | None] = []
    token_kinds: list[str] = []
    latin_labels: list[str | None] = []
    transformable_mask: list[bool] = []
    separator_positions: list[int] = []
    token_records: list[dict[str, Any]] = []
    for position, token in enumerate(tokens):
        token_kind = str(token.get("token_kind", "unknown"))
        token_kinds.append(token_kind)
        is_rune = token_kind == "rune"
        transformable_mask.append(is_rune)
        value = token.get("index29")
        if is_rune:
            if not isinstance(value, int) or not TOKEN_DOMAIN_MIN <= value <= TOKEN_DOMAIN_MAX:
                blockers.append("blocked_missing_source_backed_0_28_token_value")
                token_values.append(None)
            else:
                token_values.append(value)
            latin_labels.append(str(token.get("latin_label")) if token.get("latin_label") is not None else None)
        else:
            token_values.append(None)
            latin_labels.append(None)
            separator_positions.append(position)
        token_records.append(
            {
                "position": position,
                "token_kind": token_kind,
                "index29": value if isinstance(value, int) else None,
                "latin_label": token.get("latin_label"),
                "raw_text": token.get("raw_text"),
                "transformable": is_rune,
            }
        )
    expected_token_count = int(preflight_record.get("solved_fixture_stream_token_count", len(tokens)))
    if stream is None:
        blockers.append("blocked_missing_stage4o_source_input_stream")
    if candidate is None:
        blockers.append("blocked_missing_stage4o_transform_candidate_link")
    if len(tokens) != expected_token_count:
        blockers.append("blocked_token_count_mismatch_against_stage5k_preflight")
    if len(transformable_mask) != len(tokens):
        blockers.append("blocked_transformable_mask_length_mismatch")
    mapped = not blockers
    mapping_status = "mapped" if mapped else "blocked"
    remaining_blockers = [REMAINING_APPROVAL_BLOCKER] if mapped else sorted(set(blockers))
    hash_material = {
        "mapping_id": preflight_record["mapping_id"],
        "source_input_stream_id": preflight_record["source_input_stream_id"],
        "fixture_id": preflight_record["fixture_id"],
        "token_domain": TOKEN_DOMAIN,
        "tokens": token_records,
        "transformable_mask": transformable_mask,
        "separator_positions": separator_positions,
    }
    return {
        "record_type": "gematria_solved_fixture_token_mapping_record",
        "mapping_record_id": f"stage5l-token-mapping-{index:02d}",
        "mapping_id": preflight_record["mapping_id"],
        "source_preflight_id": preflight_record["preflight_id"],
        "source_manifest": _display_path(source_manifest),
        "source_input_stream_id": preflight_record["source_input_stream_id"],
        "fixture_id": preflight_record["fixture_id"],
        "transform_family": preflight_record["transform_family"],
        "candidate_id": preflight_record["candidate_id"],
        "source_record_type": "stage4o_committed_safe_cpu_batch_input_stream",
        "token_mapping_source": "committed_stage4o_solved_fixture_stream_index29_values",
        "mapping_status": mapping_status,
        "readiness_status": "ready_for_future_cuda_approval" if mapped else "blocked",
        "token_domain_mapping_status": "mapped_to_gematria_0_28_buffers" if mapped else "blocked",
        "token_domain": TOKEN_DOMAIN,
        "token_domain_min": TOKEN_DOMAIN_MIN,
        "token_domain_max": TOKEN_DOMAIN_MAX,
        "token_count": len(tokens),
        "transformable_token_count": sum(1 for item in transformable_mask if item),
        "token_values": token_values,
        "token_kinds": token_kinds,
        "latin_labels": latin_labels,
        "transformable_mask": transformable_mask,
        "separator_positions": separator_positions,
        "token_records": token_records,
        "separator_metadata_preserved": True,
        "token_kind_metadata_preserved": True,
        "usable_as_token_domain_input_fixture": mapped,
        "compatible_with_shift_score_kernel_semantics": mapped,
        "shift_score_semantics_only": True,
        "original_transform_family_semantics_exercised": False,
        "original_transform_family_cuda_kernel_required": False,
        "stage4o_parity_expectation_linkage_status": "linked_to_stage4o_candidate_and_manifest"
        if candidate is not None
        else "blocked_missing_stage4o_candidate",
        "stage4o_candidate_transform_id": candidate.get("transform_id") if candidate else None,
        "source_backed_token_values": mapped,
        "source_backed_token_value_hash": canonical_hash(hash_material) if mapped else None,
        "blockers": remaining_blockers,
        "blocker_count": len(remaining_blockers),
        "blockers_resolved_by_stage5l": list(RESOLVABLE_BLOCKERS) if mapped else [],
        "future_stage_approval_required": True,
        **COMMON_POLICY_FLAGS,
    }


def _records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    return [record for record in records if isinstance(record, dict)]


def _display_path(path: Path) -> str:
    """Return a stable repository-relative path when possible."""

    resolved = resolve_repo_path(path)
    try:
        return resolved.relative_to(repo_root()).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")
