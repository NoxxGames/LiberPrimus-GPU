"""Stage 3U bounded cookie SHA-256 signed-variant pack."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from libreprimus.hash_preimage.validation import load_cookie_targets
from libreprimus.post_discord.export import read_json, resolve_path, write_json, write_jsonl

EXPERIMENT_ID = "EXP-3R-001"
DEFAULT_MANIFEST = (
    "experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml"
)
DEFAULT_COOKIES = "data/observations/web/cookie-hash-records-v0.yaml"
DEFAULT_OUTPUT_DIR = "experiments/results/post-discord/stage3u"
REQUIRED_COOKIE_IDS = ("cookie-2013-167-v0", "cookie-2013-761-v0")
SUPPORTED_BYTE_VARIANTS = {
    "raw",
    "lower",
    "upper",
    "trailing_lf",
    "trailing_crlf",
    "leading_space",
    "trailing_space",
    "wrapped_space",
    "compact_no_spaces",
    "compact_upper",
    "compact_lower",
    "quoted",
}


@dataclass(frozen=True)
class CookieManifest:
    """Validated Stage 3U manifest."""

    experiment_id: str
    candidate_cap: int
    algorithm: str
    base_strings: tuple[str, ...]
    byte_variants: tuple[str, ...]
    payload: dict[str, Any]


@dataclass(frozen=True)
class ExpandedCandidate:
    """A deduplicated byte-string candidate."""

    candidate_id: str
    base_string_id: str
    base_string: str
    source_basis: str
    byte_variant: str
    encoding: str
    candidate_text: str
    candidate_bytes: bytes
    candidate_bytes_sha256: str


def load_cookie_manifest(path: Path) -> CookieManifest:
    """Load and validate the EXP-3R-001 manifest."""
    resolved = resolve_path(path)
    payload = _read_yaml_mapping(resolved)
    experiment_id = str(payload.get("experiment_id", ""))
    if not experiment_id.startswith(EXPERIMENT_ID):
        raise ValueError("manifest experiment_id must be EXP-3R-001")
    if payload.get("cuda_enabled") is not False:
        raise ValueError("manifest cuda_enabled must be false")
    if payload.get("cloud_execution") is not False:
        raise ValueError("manifest cloud_execution must be false")
    if payload.get("paid_services") is not False:
        raise ValueError("manifest paid_services must be false")
    if payload.get("no_solve_claim") is not True:
        raise ValueError("manifest no_solve_claim must be true")
    if payload.get("canonical_corpus_active") is not False:
        raise ValueError("manifest canonical_corpus_active must be false")
    if payload.get("page_boundaries_final") is not False:
        raise ValueError("manifest page_boundaries_final must be false")
    cap = int(payload.get("candidate_count_cap", 0))
    if cap <= 0 or cap > 576:
        raise ValueError("manifest candidate_count_cap must be in 1..576")
    generation = payload.get("candidate_generation")
    if not isinstance(generation, dict):
        raise ValueError("manifest candidate_generation must be a mapping")
    algorithm = str(generation.get("algorithm", ""))
    if algorithm != "sha256":
        raise ValueError("manifest candidate_generation.algorithm must be sha256")
    if generation.get("fuzzy_matching") is not False:
        raise ValueError("manifest fuzzy_matching must be false")
    if generation.get("gpu_hashcat") is not False:
        raise ValueError("manifest gpu_hashcat must be false")
    base_strings = tuple(str(item) for item in generation.get("base_strings", []))
    byte_variants = tuple(str(item) for item in generation.get("byte_variants", []))
    if not base_strings:
        raise ValueError("manifest must declare at least one base string")
    if not byte_variants:
        raise ValueError("manifest must declare at least one byte variant")
    unsupported = sorted(set(byte_variants) - SUPPORTED_BYTE_VARIANTS)
    if unsupported:
        raise ValueError(f"unsupported byte variants: {', '.join(unsupported)}")
    return CookieManifest(
        experiment_id=experiment_id,
        candidate_cap=cap,
        algorithm=algorithm,
        base_strings=base_strings,
        byte_variants=byte_variants,
        payload=payload,
    )


def validate_cookie_manifest(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Validate a cookie manifest without executing it."""
    try:
        manifest = load_cookie_manifest(path)
    except Exception as exc:  # noqa: BLE001
        return {}, [str(exc)]
    generated_before_dedup = len(manifest.base_strings) * len(manifest.byte_variants)
    return {
        "cookie_manifest_valid": True,
        "experiment_id": manifest.experiment_id,
        "candidate_cap": manifest.candidate_cap,
        "algorithm": manifest.algorithm,
        "base_string_count": len(manifest.base_strings),
        "byte_variant_count": len(manifest.byte_variants),
        "generated_before_dedup": generated_before_dedup,
        "execution_enabled": bool(manifest.payload.get("execution_enabled")),
        "cuda_enabled": bool(manifest.payload.get("cuda_enabled")),
        "no_solve_claim": bool(manifest.payload.get("no_solve_claim")),
    }, []


def run_cookie_signed_variant_pack(
    *,
    manifest_path: Path = Path(DEFAULT_MANIFEST),
    cookies_path: Path = Path(DEFAULT_COOKIES),
    out_dir: Path = Path(DEFAULT_OUTPUT_DIR),
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Execute EXP-3R-001 with exact SHA-256 comparisons only."""
    manifest = load_cookie_manifest(manifest_path)
    targets = [target for target in load_cookie_targets(cookies_path) if target.cookie_id in REQUIRED_COOKIE_IDS]
    missing = sorted(set(REQUIRED_COOKIE_IDS) - {target.cookie_id for target in targets})
    if missing:
        raise ValueError(f"missing required cookie targets: {', '.join(missing)}")
    if len(targets) != len(REQUIRED_COOKIE_IDS):
        raise ValueError("cookie target count mismatch")

    warnings: list[str] = []
    generated_before_dedup = len(manifest.base_strings) * len(manifest.byte_variants)
    candidates, duplicate_count = expand_candidates(manifest)
    if duplicate_count:
        warnings.append(f"deduplicated_candidate_byte_strings={duplicate_count}")
    if len(candidates) > manifest.candidate_cap:
        raise ValueError(f"candidate_cap_exceeded:{len(candidates)}>{manifest.candidate_cap}")
    if warnings and not allow_warnings:
        raise ValueError("; ".join(warnings))

    run_id = f"stage3u-{manifest.experiment_id.lower()}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    records: list[dict[str, Any]] = []
    matches: list[dict[str, Any]] = []
    for candidate in candidates:
        digest_hex = hashlib.sha256(candidate.candidate_bytes).hexdigest()
        for target in targets:
            exact_match = digest_hex == target.cookie_value
            record = _candidate_record(
                run_id=run_id,
                manifest=manifest,
                candidate=candidate,
                digest_hex=digest_hex,
                target_cookie_id=target.cookie_id,
                target_cookie_name=target.cookie_name,
                exact_match=exact_match,
            )
            records.append(record)
            if exact_match:
                matches.append(_exact_match_record(record))

    resolved_out = resolve_path(out_dir)
    output_paths = {
        "hash_candidate_records": str(resolved_out / "hash_candidate_records.jsonl"),
        "exact_matches": str(resolved_out / "exact_matches.jsonl"),
        "summary": str(resolved_out / "summary.json"),
    }
    if warnings:
        output_paths["warnings"] = str(resolved_out / "warnings.jsonl")
    summary = {
        "record_type": "cookie_signed_variant_pack_summary",
        "experiment_id": manifest.experiment_id,
        "run_id": run_id,
        "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "manifest_path": str(resolve_path(manifest_path)),
        "target_cookie_count": len(targets),
        "target_cookie_ids": [target.cookie_id for target in targets],
        "base_string_count": len(manifest.base_strings),
        "byte_variant_count": len(manifest.byte_variants),
        "candidate_count_generated_before_dedup": generated_before_dedup,
        "candidate_count_after_dedup": len(candidates),
        "duplicate_candidate_count": duplicate_count,
        "comparison_count": len(records),
        "exact_match_count": len(matches),
        "exact_match_candidate_ids": [record["candidate_id"] for record in matches],
        "algorithm": manifest.algorithm,
        "encoding": "utf-8",
        "fuzzy_matching": False,
        "partial_matching": False,
        "generated_outputs_ignored": True,
        "raw_message_committed": False,
        "username_committed": False,
        "private_url_committed": False,
        "cuda_used": False,
        "cloud_execution": False,
        "paid_services": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "trusted_as_canonical": False,
        "output_paths": output_paths,
        "warnings": warnings,
    }

    write_jsonl(resolved_out / "hash_candidate_records.jsonl", records)
    write_jsonl(resolved_out / "exact_matches.jsonl", matches)
    write_json(resolved_out / "summary.json", summary)
    if warnings:
        write_jsonl(
            resolved_out / "warnings.jsonl",
            [
                {
                    "record_type": "cookie_signed_variant_warning",
                    "experiment_id": manifest.experiment_id,
                    "run_id": run_id,
                    "warning": warning,
                }
                for warning in warnings
            ],
        )
    return summary


def expand_candidates(manifest: CookieManifest) -> tuple[list[ExpandedCandidate], int]:
    """Expand and deduplicate manifest-declared byte-string candidates."""
    seen: set[bytes] = set()
    candidates: list[ExpandedCandidate] = []
    duplicate_count = 0
    source_basis = ",".join(str(item) for item in manifest.payload.get("source_basis", []))
    for base_index, base_string in enumerate(manifest.base_strings, start=1):
        base_string_id = f"{manifest.experiment_id}-base-string-{base_index:03d}"
        for byte_variant in manifest.byte_variants:
            candidate_text = apply_byte_variant(base_string, byte_variant)
            candidate_bytes = candidate_text.encode("utf-8")
            if candidate_bytes in seen:
                duplicate_count += 1
                continue
            seen.add(candidate_bytes)
            candidate_number = len(candidates) + 1
            candidates.append(
                ExpandedCandidate(
                    candidate_id=f"{manifest.experiment_id}-candidate-{candidate_number:06d}",
                    base_string_id=base_string_id,
                    base_string=base_string,
                    source_basis=source_basis,
                    byte_variant=byte_variant,
                    encoding="utf-8",
                    candidate_text=candidate_text,
                    candidate_bytes=candidate_bytes,
                    candidate_bytes_sha256=hashlib.sha256(candidate_bytes).hexdigest(),
                )
            )
    return candidates, duplicate_count


def apply_byte_variant(base_string: str, byte_variant: str) -> str:
    """Apply one manifest-declared byte variant."""
    if byte_variant == "raw":
        return base_string
    if byte_variant == "lower":
        return base_string.lower()
    if byte_variant == "upper":
        return base_string.upper()
    if byte_variant == "trailing_lf":
        return f"{base_string}\n"
    if byte_variant == "trailing_crlf":
        return f"{base_string}\r\n"
    if byte_variant == "leading_space":
        return f" {base_string}"
    if byte_variant == "trailing_space":
        return f"{base_string} "
    if byte_variant == "wrapped_space":
        return f" {base_string} "
    if byte_variant == "compact_no_spaces":
        return _compact_no_spaces(base_string)
    if byte_variant == "compact_upper":
        return _compact_no_spaces(base_string).upper()
    if byte_variant == "compact_lower":
        return _compact_no_spaces(base_string).lower()
    if byte_variant == "quoted":
        return f'"{base_string}"'
    raise ValueError(f"unsupported byte variant: {byte_variant}")


def validate_results(results_dir: Path, *, allow_missing: bool = False) -> tuple[dict[str, Any], list[str]]:
    """Validate generated Stage 3U outputs if present."""
    resolved = resolve_path(results_dir)
    summary_path = resolved / "summary.json"
    if not summary_path.is_file():
        if allow_missing:
            return {"summary_present": False}, []
        return {}, [f"missing Stage 3U summary: {summary_path}"]
    summary = read_json(summary_path)
    errors: list[str] = []
    if summary.get("experiment_id") != EXPERIMENT_ID:
        errors.append("summary experiment_id must be EXP-3R-001")
    if summary.get("algorithm") != "sha256":
        errors.append("summary algorithm must be sha256")
    for field_name, expected in {
        "fuzzy_matching": False,
        "partial_matching": False,
        "generated_outputs_ignored": True,
        "cuda_used": False,
        "cloud_execution": False,
        "paid_services": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "trusted_as_canonical": False,
    }.items():
        if summary.get(field_name) is not expected:
            errors.append(f"summary {field_name} must be {str(expected).lower()}")
    if int(summary.get("candidate_count_after_dedup") or 0) > 576:
        errors.append("candidate count must be <= 576")
    for name in ["hash_candidate_records.jsonl", "exact_matches.jsonl", "summary.json"]:
        if not (resolved / name).is_file():
            errors.append(f"missing generated output: {resolved / name}")
    return summary, errors


def load_cookie_signed_summary(results_dir: Path) -> dict[str, Any]:
    """Load a generated Stage 3U summary."""
    path = resolve_path(results_dir) / "summary.json"
    if not path.is_file():
        raise FileNotFoundError(f"Stage 3U summary not found: {path}")
    return read_json(path)


def _candidate_record(
    *,
    run_id: str,
    manifest: CookieManifest,
    candidate: ExpandedCandidate,
    digest_hex: str,
    target_cookie_id: str,
    target_cookie_name: str,
    exact_match: bool,
) -> dict[str, Any]:
    return {
        "record_type": "cookie_signed_variant_candidate_record",
        "experiment_id": manifest.experiment_id,
        "pack_id": manifest.experiment_id,
        "manifest_id": manifest.experiment_id,
        "run_id": run_id,
        "candidate_id": candidate.candidate_id,
        "base_string_id": candidate.base_string_id,
        "base_string": candidate.base_string,
        "source_basis": candidate.source_basis,
        "byte_variant": candidate.byte_variant,
        "encoding": candidate.encoding,
        "candidate_bytes_sha256": candidate.candidate_bytes_sha256,
        "digest_algorithm": manifest.algorithm,
        "digest_hex": digest_hex,
        "target_cookie_id": target_cookie_id,
        "target_cookie_name": target_cookie_name,
        "exact_match": exact_match,
        "solve_claim": False,
        "cuda_used": False,
        "cloud_execution": False,
        "trusted_as_canonical": False,
        "notes": "Exact SHA-256 comparison only; no fuzzy, partial, dictionary, GPU, or solve claim.",
    }


def _exact_match_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "cookie_signed_variant_exact_match_record",
        "experiment_id": record["experiment_id"],
        "run_id": record["run_id"],
        "candidate_id": record["candidate_id"],
        "base_string_id": record["base_string_id"],
        "base_string": record["base_string"],
        "byte_variant": record["byte_variant"],
        "encoding": record["encoding"],
        "candidate_bytes_sha256": record["candidate_bytes_sha256"],
        "digest_algorithm": record["digest_algorithm"],
        "digest_hex": record["digest_hex"],
        "target_cookie_id": record["target_cookie_id"],
        "target_cookie_name": record["target_cookie_name"],
        "exact_match": True,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
        "notes": "Exact preimage candidate only; not Liber Primus solve evidence.",
    }


def _compact_no_spaces(value: str) -> str:
    return "".join(value.split())


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    with resolve_path(path).open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"expected mapping YAML at {path}")
    return payload
