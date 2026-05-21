"""Build Stage 5Q expansion candidate inventory records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, resolve_repo_path
from libreprimus.gematria_expansion_candidate_mapping.export import write_record_set, write_report
from libreprimus.gematria_expansion_candidate_mapping.models import (
    ATBASH_FIXTURE_DIR,
    CANDIDATE_INVENTORY_PATH,
    CANDIDATE_INVENTORY_REPORT,
    COMMON_POLICY_FLAGS,
    DIRECT_FIXTURE_DIR,
    OUTPUT_DIR,
    PRIME_FIXTURE_DIR,
    STAGE5L_TOKEN_MAPPING,
    VIGENERE_FIXTURE_DIR,
)
from libreprimus.paths import repo_root

CONSUMED_CONTROL_REASON = "Exact Stage 5L/5M/5O mapped buffer; retained only as a consumed control."


def build_candidate_inventory(
    *,
    stage5l_token_mapping: Path = STAGE5L_TOKEN_MAPPING,
    candidate_inventory_out: Path = CANDIDATE_INVENTORY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build the source-backed Stage 5Q candidate inventory."""

    consumed = _consumed_records(stage5l_token_mapping)
    consumed_fixture_ids = {str(record["fixture_id"]) for record in consumed}
    records: list[dict[str, Any]] = []
    for index, record in enumerate(consumed):
        records.append(_control_record(record=record, index=index))
    next_index = len(records)
    for fixture_path in sorted(resolve_repo_path(DIRECT_FIXTURE_DIR).glob("*.fixture.json")):
        payload = _read_fixture(fixture_path)
        fixture_id = str(payload["fixture_id"])
        if _is_consumed_fixture(fixture_id, consumed_fixture_ids):
            continue
        records.append(_direct_candidate_record(fixture_path=fixture_path, fixture=payload, index=next_index))
        next_index += 1
    for fixture_dir in (ATBASH_FIXTURE_DIR, VIGENERE_FIXTURE_DIR, PRIME_FIXTURE_DIR):
        for fixture_path in sorted(resolve_repo_path(fixture_dir).glob("*.fixture.json")):
            payload = _read_fixture(fixture_path)
            fixture_id = str(payload["fixture_id"])
            if _is_consumed_fixture(fixture_id, consumed_fixture_ids):
                continue
            records.append(_blocked_original_family_record(fixture_path=fixture_path, fixture=payload, index=next_index))
            next_index += 1
    records.sort(key=lambda item: str(item["candidate_inventory_id"]))
    write_record_set(candidate_inventory_out, records)
    write_report(out_dir, CANDIDATE_INVENTORY_REPORT, {"records": records})
    return records


def _consumed_records(stage5l_token_mapping: Path) -> list[dict[str, Any]]:
    records = read_yaml(stage5l_token_mapping).get("records", [])
    if not isinstance(records, list):
        raise ValueError("Stage 5L token mapping records must be a list")
    return [record for record in records if isinstance(record, dict)]


def _control_record(*, record: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "record_type": "gematria_expansion_candidate_inventory_record",
        "candidate_inventory_id": f"stage5q-consumed-control-{index:02d}",
        "candidate_class": "already_consumed_control",
        "source_stage": "stage-5l",
        "source_path": "data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml",
        "source_record_id_or_symbol": str(record["mapping_record_id"]),
        "fixture_id": str(record["fixture_id"]),
        "candidate_id": str(record["candidate_id"]),
        "source_input_stream_id": str(record["source_input_stream_id"]),
        "source_transform_family": str(record["transform_family"]),
        "candidate_origin": "stage5l_5m_5o_exact_pack",
        "already_consumed_by_stage5l_5m_5o": True,
        "candidate_status": "already_consumed_control",
        "reason": CONSUMED_CONTROL_REASON,
        "requires_new_cuda_kernel": False,
        "requires_cuda_execution": False,
        "requires_benchmark": False,
        "requires_unsolved_page_input": False,
        "raw_data_required": False,
        "canonical_corpus_required": False,
        **COMMON_POLICY_FLAGS,
    }


def _direct_candidate_record(*, fixture_path: Path, fixture: dict[str, Any], index: int) -> dict[str, Any]:
    fixture_id = str(fixture["fixture_id"])
    return {
        "record_type": "gematria_expansion_candidate_inventory_record",
        "candidate_inventory_id": f"stage5q-new-direct-fixture-{index:02d}",
        "candidate_class": "additional_solved_fixture_shift_score_candidate",
        "source_stage": "stage-1a",
        "source_path": _display_path(fixture_path),
        "source_record_id_or_symbol": fixture_id,
        "fixture_id": fixture_id,
        "candidate_id": f"stage5q-shift-score-{fixture_id}",
        "source_input_stream_id": f"stage5q-fixture-{fixture_id}",
        "source_transform_family": "direct_translation",
        "candidate_origin": "committed_direct_translation_solved_fixture",
        "already_consumed_by_stage5l_5m_5o": False,
        "candidate_status": "candidate_for_mapping",
        "reason": "Committed direct-translation solved fixture has source-backed plaintext labels and Gematria profile SHA-256 metadata; no original transform-family semantics are needed for shift_score token-buffer mapping.",
        "requires_new_cuda_kernel": False,
        "requires_cuda_execution": False,
        "requires_benchmark": False,
        "requires_unsolved_page_input": False,
        "raw_data_required": False,
        "canonical_corpus_required": False,
        **COMMON_POLICY_FLAGS,
    }


def _blocked_original_family_record(*, fixture_path: Path, fixture: dict[str, Any], index: int) -> dict[str, Any]:
    fixture_id = str(fixture["fixture_id"])
    method_family = _canonical_source_transform_family(str(fixture.get("method_family", "unknown")))
    return {
        "record_type": "gematria_expansion_candidate_inventory_record",
        "candidate_inventory_id": f"stage5q-blocked-original-family-{index:02d}",
        "candidate_class": "blocked_original_transform_family_contract_needed",
        "source_stage": "stage-1b-1d",
        "source_path": _display_path(fixture_path),
        "source_record_id_or_symbol": fixture_id,
        "fixture_id": fixture_id,
        "candidate_id": f"stage5q-blocked-{fixture_id}",
        "source_input_stream_id": f"stage5q-fixture-{fixture_id}",
        "source_transform_family": method_family,
        "candidate_origin": "committed_solved_fixture_requires_original_transform_family",
        "already_consumed_by_stage5l_5m_5o": False,
        "candidate_status": "blocked_requires_separate_kernel_contract",
        "reason": "Fixture is committed and solved-fixture-safe, but deriving a CUDA-ready input buffer would exercise original transform-family semantics rather than Stage 5Q shift_score-only mapping.",
        "requires_new_cuda_kernel": False,
        "requires_cuda_execution": False,
        "requires_benchmark": False,
        "requires_unsolved_page_input": False,
        "raw_data_required": False,
        "canonical_corpus_required": False,
        **COMMON_POLICY_FLAGS,
    }


def _read_fixture(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"fixture must be a JSON object: {path}")
    return payload


def _is_consumed_fixture(fixture_id: str, consumed_fixture_ids: set[str]) -> bool:
    return any(
        fixture_id == consumed
        or fixture_id.startswith(f"{consumed}-")
        or consumed.startswith(f"{fixture_id}-")
        for consumed in consumed_fixture_ids
    )


def _canonical_source_transform_family(method_family: str) -> str:
    if method_family == "vigenere":
        return "vigenere_explicit_key"
    return method_family


def _display_path(path: Path) -> str:
    resolved = resolve_repo_path(path)
    try:
        return resolved.relative_to(repo_root()).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")
