"""SHA-256-only bounded preimage runner for archived cookie/hash records."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from libreprimus.hash_preimage.candidate_packs import expand_candidate_pack, load_candidate_packs
from libreprimus.hash_preimage.export import write_json, write_jsonl
from libreprimus.hash_preimage.models import CandidateText
from libreprimus.hash_preimage.validation import load_cookie_targets, validate_candidate_packs
from libreprimus.history.source_records import resolve_repo_path


def run_hash_preimage(
    *,
    cookies: Path,
    pack_dir: Path,
    out_dir: Path,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    targets = load_cookie_targets(cookies)
    pack_count, pack_errors = validate_candidate_packs(pack_dir)
    if pack_errors:
        raise ValueError("; ".join(pack_errors))
    packs = load_candidate_packs(pack_dir)
    expanded_packs = [expand_candidate_pack(pack) for pack in packs]

    warnings: list[str] = []
    total_before_dedup = sum(pack.total_generated_before_dedup for pack in expanded_packs)
    candidate_count = sum(len(pack.candidates) for pack in expanded_packs)
    duplicate_count = sum(pack.duplicate_count for pack in expanded_packs)
    if duplicate_count:
        warnings.append(f"deduplicated_candidate_byte_strings={duplicate_count}")
    if warnings and not allow_warnings:
        raise ValueError("; ".join(warnings))

    run_id = f"stage3l-cookie-hash-preimage-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    resolved_out = resolve_repo_path(out_dir)
    candidate_records: list[dict[str, Any]] = []
    match_records: list[dict[str, Any]] = []
    candidate_counter = 0
    for expanded_pack in expanded_packs:
        for candidate in expanded_pack.candidates:
            candidate_counter += 1
            candidate_id = f"{expanded_pack.pack_id}-candidate-{candidate_counter:06d}"
            digest_hex = sha256_hex(candidate.literal_text.encode(candidate.encoding))
            bytes_sha256 = digest_hex
            for target in targets:
                exact_match = digest_hex == target.cookie_value
                record = _candidate_record(
                    run_id=run_id,
                    candidate_id=candidate_id,
                    candidate=candidate,
                    candidate_bytes_sha256=bytes_sha256,
                    digest_hex=digest_hex,
                    target_cookie_id=target.cookie_id,
                    target_cookie_name=target.cookie_name,
                    exact_match=exact_match,
                )
                candidate_records.append(record)
                if exact_match:
                    match_records.append(_match_record(record))

    output_paths = {
        "hash_candidate_records": str(resolved_out / "hash_candidate_records.jsonl"),
        "exact_matches": str(resolved_out / "exact_matches.jsonl"),
        "summary": str(resolved_out / "summary.json"),
    }
    if warnings:
        output_paths["warnings"] = str(resolved_out / "warnings.jsonl")

    summary = {
        "record_type": "hash_preimage_run_summary",
        "run_id": run_id,
        "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "algorithm": "sha256",
        "target_cookie_count": len(targets),
        "target_cookie_ids": [target.cookie_id for target in targets],
        "pack_count": pack_count,
        "pack_ids": [pack.pack_id for pack in expanded_packs],
        "candidate_count_generated_before_dedup": total_before_dedup,
        "candidate_count": candidate_count,
        "duplicate_candidate_count": duplicate_count,
        "comparison_count": len(candidate_records),
        "exact_match_count": len(match_records),
        "exact_match_ids": [record["candidate_id"] for record in match_records],
        "base29_alphabet": "0123456789ABCDEFGHIJKLMNOPQRS",
        "output_paths": output_paths,
        "warnings": warnings,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
    }

    write_jsonl(resolved_out / "hash_candidate_records.jsonl", candidate_records)
    write_jsonl(resolved_out / "exact_matches.jsonl", match_records)
    write_json(resolved_out / "summary.json", summary)
    if warnings:
        write_jsonl(
            resolved_out / "warnings.jsonl",
            [{"record_type": "hash_preimage_warning", "run_id": run_id, "warning": warning} for warning in warnings],
        )
    return summary


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _candidate_record(
    *,
    run_id: str,
    candidate_id: str,
    candidate: CandidateText,
    candidate_bytes_sha256: str,
    digest_hex: str,
    target_cookie_id: str,
    target_cookie_name: str,
    exact_match: bool,
) -> dict[str, Any]:
    return {
        "record_type": "hash_preimage_candidate_record",
        "run_id": run_id,
        "pack_id": candidate.pack_id,
        "candidate_id": candidate_id,
        "candidate_group": candidate.candidate_group,
        "literal_text": candidate.literal_text,
        "byte_variant": candidate.byte_variant,
        "encoding": candidate.encoding,
        "candidate_bytes_sha256": candidate_bytes_sha256,
        "digest_algorithm": "sha256",
        "digest_hex": digest_hex,
        "target_cookie_id": target_cookie_id,
        "target_cookie_name": target_cookie_name,
        "exact_match": exact_match,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
        "notes": "Exact SHA-256 comparison only; no fuzzy or partial matching.",
    }


def _match_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "hash_preimage_match_record",
        "run_id": record["run_id"],
        "pack_id": record["pack_id"],
        "candidate_id": record["candidate_id"],
        "target_cookie_id": record["target_cookie_id"],
        "target_cookie_name": record["target_cookie_name"],
        "digest_algorithm": record["digest_algorithm"],
        "digest_hex": record["digest_hex"],
        "literal_text": record["literal_text"],
        "byte_variant": record["byte_variant"],
        "encoding": record["encoding"],
        "exact_match": True,
        "solve_claim": False,
        "notes": "Exact preimage candidate only; not LP solve evidence.",
    }
