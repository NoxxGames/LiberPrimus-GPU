"""Build and export Stage 4G cookie refresh records."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from libreprimus.cookie_refresh.candidate_sources import load_source_backed_base_strings
from libreprimus.cookie_refresh.deduplication import expand_and_deduplicate_candidates, load_previous_candidate_hashes
from libreprimus.cookie_refresh.hash_runner import run_exact_comparisons
from libreprimus.cookie_refresh.manifest_loader import load_cookie_refresh_manifest
from libreprimus.hash_preimage.validation import load_cookie_targets
from libreprimus.history.source_records import resolve_repo_path


def run_cookie_refresh(
    *,
    manifest: Path,
    candidate_sources: Path,
    cookie_targets: Path,
    out_dir: Path,
    summary_out: Path,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Run the bounded Stage 4G exact cookie candidate refresh."""

    manifest_record = load_cookie_refresh_manifest(resolve_repo_path(manifest))
    targets = load_cookie_targets(resolve_repo_path(cookie_targets))
    bases = load_source_backed_base_strings(resolve_repo_path(candidate_sources), resolve_repo_path(cookie_targets))
    previous_hashes = load_previous_candidate_hashes()
    candidates, duplicates, generated_before_dedup = expand_and_deduplicate_candidates(
        bases=bases,
        byte_variants=manifest_record.byte_variants,
        cap=manifest_record.candidate_count_upper_bound,
        previous_hashes=previous_hashes,
    )
    warnings: list[dict[str, str]] = []
    if not candidates:
        warnings.append({"record_type": "cookie_refresh_warning", "warning": "no_candidates_generated"})
    if warnings and not allow_warnings:
        raise ValueError("; ".join(warning["warning"] for warning in warnings))

    candidate_records, exact_matches = run_exact_comparisons(
        candidates=candidates,
        targets=targets,
        algorithms=manifest_record.algorithms,
        experiment_id=manifest_record.manifest_id,
    )
    previous_duplicate_count = sum(1 for candidate in candidates if candidate.previous_pack_duplicate)
    summary = {
        "record_type": "cookie_refresh_summary",
        "stage": "stage4g",
        "experiment_id": manifest_record.manifest_id,
        "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "target_cookie_count": len(targets),
        "target_cookie_ids": [target.cookie_id for target in targets],
        "source_backed_base_string_count": len(bases),
        "byte_variant_count": len(manifest_record.byte_variants),
        "byte_variants": list(manifest_record.byte_variants),
        "algorithms_run": list(manifest_record.algorithms),
        "generated_candidates_before_dedup": generated_before_dedup,
        "candidates_after_dedup": len(candidates),
        "duplicate_count": len(duplicates),
        "previous_pack_duplicate_count": previous_duplicate_count,
        "comparison_count": len(candidate_records),
        "exact_match_count": len(exact_matches),
        "exact_match_candidate_ids": [record["candidate_id"] for record in exact_matches],
        "candidate_count_upper_bound": manifest_record.candidate_count_upper_bound,
        "exact_match_only": True,
        "fuzzy_matching": False,
        "partial_matching": False,
        "hashcat_used": False,
        "cuda_used": False,
        "cloud_execution": False,
        "no_solve_claim": True,
        "trusted_as_canonical": False,
        "generated_outputs_committed": False,
        "raw_discord_processed": False,
        "raw_lp_images_processed": False,
        "output_paths": {
            "candidate_records": str(resolve_repo_path(out_dir) / "candidate_records.jsonl"),
            "exact_matches": str(resolve_repo_path(out_dir) / "exact_matches.jsonl"),
            "duplicate_candidates": str(resolve_repo_path(out_dir) / "duplicate_candidates.jsonl"),
            "summary": str(resolve_repo_path(out_dir) / "summary.json"),
            "warnings": str(resolve_repo_path(out_dir) / "warnings.jsonl"),
        },
    }

    resolved_out = resolve_repo_path(out_dir)
    _write_jsonl(resolved_out / "candidate_records.jsonl", candidate_records)
    _write_jsonl(resolved_out / "exact_matches.jsonl", exact_matches)
    _write_jsonl(resolved_out / "duplicate_candidates.jsonl", duplicates)
    _write_json(resolved_out / "summary.json", summary)
    _write_jsonl(resolved_out / "warnings.jsonl", warnings)
    _write_yaml(resolve_repo_path(summary_out), summary)
    return summary


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
