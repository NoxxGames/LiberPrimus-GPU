"""Stage 3T bounded GP/rune claim verifier."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root
from libreprimus.post_discord.export import read_json, resolve_path, write_json, write_jsonl

EXPERIMENT_ID = "EXP-3R-004"
DEFAULT_MANIFEST = (
    "experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml"
)
DEFAULT_OUTPUT_DIR = "experiments/results/post-discord/stage3t"
DEFAULT_PROMOTED_OBSERVATIONS = (
    "data/observations/discord/stage3r-promoted-observation-records.yaml"
)
DEFAULT_VISUAL_OBSERVATIONS = "data/observations/visual/visual-numeric-observations-v0.yaml"
SUPPORTED_STATUSES = (
    "verified",
    "unverified",
    "boundary_sensitive",
    "missing_source_span",
    "unsupported_claim_type",
    "duplicate_claim",
    "malformed_claim",
)
SUPPORTED_CLAIM_TYPES = {
    "rune_count_equals",
    "transformable_rune_count_equals",
    "gp_sum_equals",
    "gp_sum_mod29_equals",
    "numeric_value_present",
    "prime_status_claim",
    "derived_value_claim",
    "page_image_dimension_claim",
}


@dataclass(frozen=True)
class GpRuneManifest:
    """Validated Stage 3T manifest."""

    experiment_id: str
    claim_cap: int
    payload: dict[str, Any]


@dataclass(frozen=True)
class GpRuneClaim:
    """Normalized GP/rune or numeric claim."""

    claim_id: str
    source_basis: str
    claim_type: str
    target_span: dict[str, Any]
    claimed_value: Any
    value_type: str
    computation_policy: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    @property
    def dedupe_key(self) -> tuple[str, str, str, str]:
        """Return the stable claim identity used for duplicate detection."""
        target = json.dumps(self.target_span, sort_keys=True, ensure_ascii=False)
        claimed = json.dumps(self.claimed_value, sort_keys=True, ensure_ascii=False)
        return (self.source_basis, target, self.claim_type, claimed)


@dataclass(frozen=True)
class VerificationRecord:
    """Generated claim verification record."""

    record_type: str
    experiment_id: str
    claim_id: str
    source_basis: str
    claim_type: str
    target_span: dict[str, Any]
    claimed_value: Any
    value_type: str
    computed: dict[str, Any]
    verification_status: str
    duplicate_of: str | None
    warnings: list[str]
    raw_message_committed: bool
    username_committed: bool
    private_url_committed: bool
    cuda_used: bool
    no_solve_claim: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    notes: str


def load_gp_rune_manifest(path: Path) -> GpRuneManifest:
    """Load and validate the Stage 3T target manifest."""
    payload = _read_yaml_mapping(path)
    experiment_id = str(payload.get("experiment_id") or "")
    if experiment_id != EXPERIMENT_ID:
        raise ValueError(f"expected {EXPERIMENT_ID} manifest, got {experiment_id!r}")
    claim_cap = int(payload.get("candidate_count_cap") or 0)
    if claim_cap != 64:
        raise ValueError(f"{EXPERIMENT_ID} claim cap must be 64, got {claim_cap}")
    for field_name, expected in {
        "cpu_only": True,
        "cuda_enabled": False,
        "cloud_execution": False,
        "paid_services": False,
        "generated_outputs_committed": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
    }.items():
        if payload.get(field_name) is not expected:
            raise ValueError(f"{field_name} must be {str(expected).lower()}")
    return GpRuneManifest(experiment_id=experiment_id, claim_cap=claim_cap, payload=payload)


def validate_gp_rune_manifest(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Validate Stage 3T manifest without executing verification."""
    try:
        manifest = load_gp_rune_manifest(path)
    except (OSError, ValueError) as exc:
        return {}, [str(exc)]
    return {
        "experiment_id": manifest.experiment_id,
        "claim_cap": manifest.claim_cap,
        "execution_enabled": bool(manifest.payload.get("execution_enabled")),
        "cuda_enabled": bool(manifest.payload.get("cuda_enabled")),
        "no_solve_claim": bool(manifest.payload.get("no_solve_claim")),
    }, []


def load_claims(
    *,
    manifest_path: Path = Path(DEFAULT_MANIFEST),
    promoted_observations_path: Path = Path(DEFAULT_PROMOTED_OBSERVATIONS),
    visual_observations_path: Path = Path(DEFAULT_VISUAL_OBSERVATIONS),
) -> tuple[list[GpRuneClaim], list[str]]:
    """Load manifest, Stage 3R, and visual observation claims."""
    warnings: list[str] = []
    manifest_payload = _read_yaml_mapping(manifest_path)
    claims: list[GpRuneClaim] = []
    for item in manifest_payload.get("claims", []) or []:
        if isinstance(item, dict):
            claims.append(claim_from_mapping(item, source_basis="manifest"))

    promoted_path = resolve_path(promoted_observations_path)
    if promoted_path.is_file():
        promoted = _read_yaml_mapping(promoted_path)
        claims.extend(claims_from_stage3r_observations(promoted))
    else:
        warnings.append(f"promoted_observations_missing:{promoted_path}")

    visual_path = resolve_path(visual_observations_path)
    if visual_path.is_file():
        visual = _read_yaml_mapping(visual_path)
        claims.extend(claims_from_visual_observations(visual))
    else:
        warnings.append(f"visual_observations_missing:{visual_path}")
    return claims, warnings


def claim_from_mapping(payload: dict[str, Any], *, source_basis: str) -> GpRuneClaim:
    """Build a claim from a manifest/test mapping."""
    claim_id = str(payload.get("claim_id") or payload.get("observation_id") or "claim")
    return GpRuneClaim(
        claim_id=claim_id,
        source_basis=str(payload.get("source_basis") or source_basis),
        claim_type=str(payload.get("claim_type") or ""),
        target_span=dict(payload.get("target_span") or {}),
        claimed_value=payload.get("claimed_value"),
        value_type=str(payload.get("value_type") or "unknown"),
        computation_policy=dict(payload.get("computation_policy") or {}),
        notes=str(payload.get("notes") or ""),
    )


def claims_from_stage3r_observations(payload: dict[str, Any]) -> list[GpRuneClaim]:
    """Extract exact reviewable numeric claims from Stage 3R promoted observations."""
    claims: list[GpRuneClaim] = []
    for record in payload.get("records", []) or []:
        if not isinstance(record, dict):
            continue
        observation_id = str(record.get("observation_id") or "stage3r-observation")
        observation_type = str(record.get("observation_type") or "")
        values = record.get("values") or {}
        derived = record.get("derived_values") or {}
        source_basis = f"stage3r:{observation_id}"
        if observation_type == "cuneiform_review_candidate":
            reading = values.get("candidate_reading")
            if isinstance(reading, list) and reading == [17, 13, 55, 1]:
                for name, expected in {
                    "pairwise_17_13_base60": 1033,
                    "pairwise_55_1_base60": 3301,
                    "full_base60": 3722101,
                }.items():
                    claims.append(
                        _derived_claim(
                            f"{observation_id}-{name}",
                            source_basis,
                            {"kind": "cuneiform_digits", "digits": reading, "derived_name": name},
                            expected,
                            "integer",
                        )
                    )
            numeric_candidates = derived.get("numeric_candidates")
            if isinstance(numeric_candidates, list):
                for value in numeric_candidates:
                    claims.append(
                        _numeric_present_claim(
                            f"{observation_id}-numeric-{value}",
                            source_basis,
                            {"values": numeric_candidates, "observation_type": observation_type},
                            value,
                        )
                    )
        elif observation_type == "image_dimensions":
            width = values.get("width")
            height = values.get("height")
            if isinstance(width, int):
                claims.append(_prime_claim(f"{observation_id}-width-prime", source_basis, width, True))
            if isinstance(height, int):
                claims.append(_prime_claim(f"{observation_id}-height-prime", source_basis, height, True))
        elif observation_type == "historical_audio_duration_cluster":
            duration = values.get("duration_seconds")
            if isinstance(duration, int):
                claims.append(
                    _numeric_present_claim(
                        f"{observation_id}-duration-{duration}",
                        source_basis,
                        {"values": [duration], "observation_type": observation_type},
                        duration,
                    )
                )
        elif observation_type in {"dot_motif_review_candidate", "dead_oak_motif_review_candidate"}:
            claims.append(
                GpRuneClaim(
                    claim_id=f"{observation_id}-unsupported",
                    source_basis=source_basis,
                    claim_type="unsupported_visual_motif_claim",
                    target_span={"observation_type": observation_type},
                    claimed_value=None,
                    value_type="unknown",
                    notes="Visual motif has no exact GP/rune claim.",
                )
            )
    return claims


def claims_from_visual_observations(payload: dict[str, Any]) -> list[GpRuneClaim]:
    """Extract exact arithmetic claims from committed visual numeric observations."""
    claims: list[GpRuneClaim] = []
    for record in payload.get("records", []) or []:
        if not isinstance(record, dict):
            continue
        observation_id = str(record.get("observation_id") or "visual-observation")
        source_basis = f"visual:{observation_id}"
        derived = record.get("derived_values") or {}
        if observation_id == "lp-cuneiform-sexagesimal-candidate-v0":
            digits = [17, 13, 55, 1]
            for name in [
                "pairwise_17_13_base60",
                "pairwise_55_1_base60",
                "full_base60",
                "full_base60_mod29",
                "1033_mod29",
                "3301_mod29",
            ]:
                if name in derived:
                    claims.append(
                        _derived_claim(
                            f"{observation_id}-{name}",
                            source_basis,
                            {"kind": "cuneiform_digits", "digits": digits, "derived_name": name},
                            derived[name],
                            "integer",
                        )
                    )
        if record.get("observation_type") == "prime_dimension_observation":
            values = record.get("candidate_readings", [{}])[0].get("value", [])
            if isinstance(values, list):
                for index, value in enumerate(values):
                    if isinstance(value, int):
                        claims.append(
                            _prime_claim(
                                f"{observation_id}-value-{index}-prime",
                                source_basis,
                                value,
                                True,
                            )
                        )
            product = derived.get("product")
            width = derived.get("width")
            height = derived.get("height")
            multiplier = derived.get("multiplier")
            if isinstance(product, int) and isinstance(width, int) and isinstance(height, int):
                target_span = {"kind": "dimension_product", "width": width, "height": height}
                if isinstance(multiplier, int):
                    target_span["multiplier"] = multiplier
                claims.append(
                    _derived_claim(
                        f"{observation_id}-product",
                        source_basis,
                        target_span,
                        product,
                        "integer",
                    )
                )
    return claims


def run_gp_rune_verifier(
    *,
    manifest_path: Path = Path(DEFAULT_MANIFEST),
    promoted_observations_path: Path = Path(DEFAULT_PROMOTED_OBSERVATIONS),
    visual_observations_path: Path = Path(DEFAULT_VISUAL_OBSERVATIONS),
    out_dir: Path = Path(DEFAULT_OUTPUT_DIR),
) -> dict[str, Any]:
    """Execute only the Stage 3T GP/rune claim verifier."""
    manifest = load_gp_rune_manifest(manifest_path)
    loaded_claims, warnings = load_claims(
        manifest_path=manifest_path,
        promoted_observations_path=promoted_observations_path,
        visual_observations_path=visual_observations_path,
    )
    capped_claims = loaded_claims[: manifest.claim_cap]
    if len(loaded_claims) > manifest.claim_cap:
        warnings.append(f"claim_count_exceeds_cap:{len(loaded_claims)}>{manifest.claim_cap}")
    seen: dict[tuple[str, str, str, str], str] = {}
    records: list[VerificationRecord] = []
    duplicate_count = 0
    for claim in capped_claims:
        duplicate_of = seen.get(claim.dedupe_key)
        if duplicate_of:
            duplicate_count += 1
            records.append(_duplicate_record(claim, duplicate_of=duplicate_of))
            continue
        seen[claim.dedupe_key] = claim.claim_id
        records.append(verify_claim(claim))

    resolved_out = resolve_path(out_dir)
    status_groups: dict[str, list[VerificationRecord]] = {status: [] for status in SUPPORTED_STATUSES}
    for record in records:
        status_groups[record.verification_status].append(record)
    paths = {
        "verification_records": str(
            write_jsonl(resolved_out / "gp_rune_claim_verification_records.jsonl", records)
        ),
        "verified_claims": str(write_jsonl(resolved_out / "verified_claims.jsonl", status_groups["verified"])),
        "unverified_claims": str(
            write_jsonl(resolved_out / "unverified_claims.jsonl", status_groups["unverified"])
        ),
        "boundary_sensitive_claims": str(
            write_jsonl(
                resolved_out / "boundary_sensitive_claims.jsonl",
                status_groups["boundary_sensitive"],
            )
        ),
        "missing_source_span_claims": str(
            write_jsonl(
                resolved_out / "missing_source_span_claims.jsonl",
                status_groups["missing_source_span"],
            )
        ),
        "unsupported_claims": str(
            write_jsonl(
                resolved_out / "unsupported_claims.jsonl",
                status_groups["unsupported_claim_type"] + status_groups["malformed_claim"],
            )
        ),
    }
    if warnings:
        paths["warnings"] = str(write_jsonl(resolved_out / "warnings.jsonl", [{"warning": item} for item in warnings]))
    paths["summary"] = str(resolved_out / "summary.json")
    status_counts = Counter(record.verification_status for record in records)
    summary = {
        "record_type": "gp_rune_claim_verifier_summary",
        "experiment_id": manifest.experiment_id,
        "run_id": f"stage3t-{manifest.experiment_id.lower()}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}",
        "manifest_path": str(resolve_path(manifest_path)),
        "claim_cap": manifest.claim_cap,
        "claims_loaded": len(loaded_claims),
        "claims_deduplicated": len(seen),
        "claims_executed": len(capped_claims),
        "verified_count": status_counts["verified"],
        "unverified_count": status_counts["unverified"],
        "boundary_sensitive_count": status_counts["boundary_sensitive"],
        "missing_source_span_count": status_counts["missing_source_span"],
        "unsupported_claim_count": status_counts["unsupported_claim_type"],
        "malformed_claim_count": status_counts["malformed_claim"],
        "duplicate_claim_count": duplicate_count,
        "generated_outputs_ignored": True,
        "raw_message_committed": False,
        "username_committed": False,
        "private_url_committed": False,
        "cuda_used": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "trusted_as_canonical": False,
        "output_paths": paths,
        "warnings": warnings,
    }
    write_json(resolved_out / "summary.json", summary)
    return summary


def verify_claim(claim: GpRuneClaim) -> VerificationRecord:
    """Verify one normalized claim without searching neighbouring spans."""
    warnings: list[str] = []
    computed: dict[str, Any] = {}
    status: str
    if not claim.claim_type:
        status = "malformed_claim"
    elif claim.claim_type not in SUPPORTED_CLAIM_TYPES:
        status = "unsupported_claim_type"
    elif claim.computation_policy.get("boundary_sensitive") is True:
        status = "boundary_sensitive"
        computed["boundary_sensitive"] = True
    elif claim.claimed_value is None:
        status = "malformed_claim"
    elif claim.claim_type in {
        "rune_count_equals",
        "transformable_rune_count_equals",
        "gp_sum_equals",
        "gp_sum_mod29_equals",
    }:
        if not _has_exact_span(claim.target_span):
            status = "missing_source_span"
        else:
            computed = compute_rune_span(claim.target_span)
            status = _compare_claim(claim, computed)
    elif claim.claim_type == "numeric_value_present":
        values = claim.target_span.get("values")
        if not isinstance(values, list):
            status = "missing_source_span"
        else:
            computed = {"values": values, "present": claim.claimed_value in values}
            status = "verified" if computed["present"] else "unverified"
    elif claim.claim_type == "prime_status_claim":
        value = claim.target_span.get("value")
        if not isinstance(value, int):
            status = "malformed_claim"
        else:
            computed = {"value": value, "is_prime": is_prime(value)}
            status = "verified" if computed["is_prime"] == claim.claimed_value else "unverified"
    elif claim.claim_type in {"derived_value_claim", "page_image_dimension_claim"}:
        computed = compute_derived_value(claim.target_span)
        if "error" in computed:
            status = "unsupported_claim_type"
            warnings.append(str(computed["error"]))
        else:
            status = "verified" if computed.get("value") == claim.claimed_value else "unverified"
    else:
        status = "unsupported_claim_type"
    return _verification_record(claim, status=status, computed=computed, warnings=warnings)


def compute_rune_span(target_span: dict[str, Any]) -> dict[str, Any]:
    """Compute rune counts and GP sum for an exact synthetic/locked rune span."""
    indices = target_span.get("rune_indices")
    tokens = target_span.get("tokens")
    if indices is None and isinstance(tokens, list):
        indices = [item.get("index") for item in tokens if isinstance(item, dict) and "index" in item]
    if not isinstance(indices, list) or not all(isinstance(item, int) for item in indices):
        raise ValueError("exact rune_indices are required")
    separator_count = int(target_span.get("separator_count") or 0)
    primes = primes_by_index()
    gp_sum = sum(primes[index] for index in indices)
    return {
        "rune_count": len(indices),
        "transformable_rune_count": len(indices),
        "separator_count": separator_count,
        "gp_sum": gp_sum,
        "gp_sum_mod29": gp_sum % 29,
    }


def compute_derived_value(target_span: dict[str, Any]) -> dict[str, Any]:
    """Compute supported exact derived numeric observations."""
    kind = target_span.get("kind")
    if kind == "cuneiform_digits":
        digits = target_span.get("digits")
        name = str(target_span.get("derived_name") or "")
        if digits != [17, 13, 55, 1]:
            return {"error": "unsupported_cuneiform_digit_sequence"}
        values = {
            "pairwise_17_13_base60": 17 * 60 + 13,
            "pairwise_55_1_base60": 55 * 60 + 1,
            "full_base60": ((17 * 60 + 13) * 60 + 55) * 60 + 1,
            "full_base60_mod29": (((17 * 60 + 13) * 60 + 55) * 60 + 1) % 29,
            "1033_mod29": 1033 % 29,
            "3301_mod29": 3301 % 29,
        }
        if name not in values:
            return {"error": f"unsupported_derived_name:{name}"}
        return {"derived_name": name, "value": values[name]}
    if kind == "dimension_product":
        width = target_span.get("width")
        height = target_span.get("height")
        multiplier = target_span.get("multiplier")
        if isinstance(width, int) and isinstance(height, int):
            value = width * height
            if isinstance(multiplier, int):
                value *= multiplier
            return {"value": value, "width": width, "height": height, "multiplier": multiplier}
    return {"error": f"unsupported_derived_kind:{kind}"}


def validate_results(results_dir: Path, *, allow_missing: bool = False) -> tuple[dict[str, Any], list[str]]:
    """Validate generated Stage 3T outputs if present."""
    resolved = resolve_path(results_dir)
    summary_path = resolved / "summary.json"
    if not summary_path.is_file():
        if allow_missing:
            return {"summary_present": False}, []
        return {}, [f"missing Stage 3T summary: {summary_path}"]
    summary = read_json(summary_path)
    errors: list[str] = []
    if summary.get("experiment_id") != EXPERIMENT_ID:
        errors.append("summary experiment_id must be EXP-3R-004")
    for field_name, expected in {
        "generated_outputs_ignored": True,
        "raw_message_committed": False,
        "username_committed": False,
        "private_url_committed": False,
        "cuda_used": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "trusted_as_canonical": False,
    }.items():
        if summary.get(field_name) is not expected:
            errors.append(f"summary {field_name} must be {str(expected).lower()}")
    if int(summary.get("claim_cap") or 0) > 64:
        errors.append("claim cap must be <= 64")
    for name in [
        "gp_rune_claim_verification_records.jsonl",
        "verified_claims.jsonl",
        "unverified_claims.jsonl",
        "summary.json",
    ]:
        if not (resolved / name).is_file():
            errors.append(f"missing generated output: {resolved / name}")
    return summary, errors


def load_gp_rune_summary(results_dir: Path) -> dict[str, Any]:
    """Load a generated Stage 3T summary."""
    path = resolve_path(results_dir) / "summary.json"
    if not path.is_file():
        raise FileNotFoundError(f"Stage 3T summary not found: {path}")
    return read_json(path)


def _compare_claim(claim: GpRuneClaim, computed: dict[str, Any]) -> str:
    lookup = {
        "rune_count_equals": "rune_count",
        "transformable_rune_count_equals": "transformable_rune_count",
        "gp_sum_equals": "gp_sum",
        "gp_sum_mod29_equals": "gp_sum_mod29",
    }
    key = lookup[claim.claim_type]
    return "verified" if computed.get(key) == claim.claimed_value else "unverified"


def _has_exact_span(target_span: dict[str, Any]) -> bool:
    indices = target_span.get("rune_indices")
    tokens = target_span.get("tokens")
    return isinstance(indices, list) or isinstance(tokens, list)


def _verification_record(
    claim: GpRuneClaim,
    *,
    status: str,
    computed: dict[str, Any],
    warnings: list[str],
    duplicate_of: str | None = None,
) -> VerificationRecord:
    return VerificationRecord(
        record_type="gp_rune_claim_verification_record",
        experiment_id=EXPERIMENT_ID,
        claim_id=claim.claim_id,
        source_basis=claim.source_basis,
        claim_type=claim.claim_type,
        target_span=claim.target_span,
        claimed_value=claim.claimed_value,
        value_type=claim.value_type,
        computed=computed,
        verification_status=status,
        duplicate_of=duplicate_of,
        warnings=warnings,
        raw_message_committed=False,
        username_committed=False,
        private_url_committed=False,
        cuda_used=False,
        no_solve_claim=True,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        notes=claim.notes,
    )


def _duplicate_record(claim: GpRuneClaim, *, duplicate_of: str) -> VerificationRecord:
    return _verification_record(
        claim,
        status="duplicate_claim",
        computed={"duplicate_of": duplicate_of},
        warnings=[],
        duplicate_of=duplicate_of,
    )


def _derived_claim(
    claim_id: str,
    source_basis: str,
    target_span: dict[str, Any],
    value: Any,
    value_type: str,
) -> GpRuneClaim:
    return GpRuneClaim(
        claim_id=claim_id,
        source_basis=source_basis,
        claim_type="derived_value_claim",
        target_span=target_span,
        claimed_value=value,
        value_type=value_type,
    )


def _numeric_present_claim(
    claim_id: str,
    source_basis: str,
    target_span: dict[str, Any],
    value: Any,
) -> GpRuneClaim:
    return GpRuneClaim(
        claim_id=claim_id,
        source_basis=source_basis,
        claim_type="numeric_value_present",
        target_span=target_span,
        claimed_value=value,
        value_type="integer",
    )


def _prime_claim(claim_id: str, source_basis: str, value: int, expected: bool) -> GpRuneClaim:
    return GpRuneClaim(
        claim_id=claim_id,
        source_basis=source_basis,
        claim_type="prime_status_claim",
        target_span={"value": value},
        claimed_value=expected,
        value_type="boolean",
    )


def primes_by_index() -> dict[int, int]:
    """Load Gematria Primus prime values by index."""
    payload = json.loads((repo_root() / "data/profiles/gematria/gematria-primus-v0.json").read_text(encoding="utf-8"))
    return {int(entry["index"]): int(entry["prime"]) for entry in payload["entries"]}


def is_prime(value: int) -> bool:
    """Return true if value is prime."""
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    resolved = resolve_path(path)
    with resolved.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"expected mapping YAML at {resolved}")
    return payload
