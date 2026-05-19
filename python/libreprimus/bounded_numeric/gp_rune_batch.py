"""Stage 4D GP/rune batch002 exact-claim handling."""

from __future__ import annotations

from typing import Any

from libreprimus.bounded_numeric.manifest_loader import cap_for
from libreprimus.bounded_numeric.no_fudge_policy import enforce_cap
from libreprimus.post_discord.gp_rune_claim_verifier import GpRuneClaim, verify_claim


def run_gp_rune_batch(manifest: dict[str, Any], visual_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Verify exact website-derived GP/rune claims when Stage 4B supplied exact spans."""

    manifest_id = str(manifest.get("manifest_id"))
    cap = cap_for(manifest)
    claims = _extract_exact_claims(visual_records)
    if not claims:
        return [
            _base_result(
                result_id=f"{manifest_id}-skipped-no-exact-claims",
                manifest_id=manifest_id,
                audit_type="gp_rune_batch002",
                status="skipped_no_exact_claims",
                candidate_count=0,
                cap=cap,
                notes="No exact new Stage 4B website-derived GP/rune spans were present.",
            )
        ]
    capped_claims = claims[:cap]
    enforce_cap(capped_claims, cap, manifest_id)
    results: list[dict[str, Any]] = []
    for claim in capped_claims:
        verification = verify_claim(claim)
        results.append(
            _base_result(
                result_id=f"{manifest_id}-{claim.claim_id}",
                manifest_id=manifest_id,
                audit_type="gp_rune_batch002",
                status=f"verified_claim_{verification.verification_status}",
                candidate_count=1,
                cap=cap,
                raw_values={"target_span": claim.target_span, "claimed_value": claim.claimed_value},
                derived_values=[
                    {
                        "name": "verification_status",
                        "formula": "stage3t_exact_claim_verifier",
                        "source": "target_span_and_claimed_value",
                        "value": verification.verification_status,
                    }
                ],
                notes=verification.notes,
            )
        )
    return results


def _extract_exact_claims(records: list[dict[str, Any]]) -> list[GpRuneClaim]:
    claims: list[GpRuneClaim] = []
    for record in records:
        observation_id = str(record.get("observation_id") or "stage4b-visual")
        for item in record.get("candidate_readings", []) or []:
            if not isinstance(item, dict):
                continue
            target_span = item.get("target_span")
            claim_type = item.get("claim_type")
            if not isinstance(target_span, dict) or not claim_type:
                continue
            claims.append(
                GpRuneClaim(
                    claim_id=str(item.get("reading_id") or observation_id),
                    source_basis=f"stage4b:{observation_id}",
                    claim_type=str(claim_type),
                    target_span=target_span,
                    claimed_value=item.get("claimed_value"),
                    value_type=str(item.get("value_type") or "unknown"),
                    computation_policy=dict(item.get("computation_policy") or {}),
                    notes=str(item.get("notes") or ""),
                )
            )
    return claims


def _base_result(
    *,
    result_id: str,
    manifest_id: str,
    audit_type: str,
    status: str,
    candidate_count: int,
    cap: int,
    raw_values: Any = None,
    derived_values: list[dict[str, Any]] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    return {
        "record_type": "bounded_numeric_result_record",
        "result_id": result_id,
        "execution_manifest_id": manifest_id,
        "audit_type": audit_type,
        "status": status,
        "candidate_count": candidate_count,
        "cap": cap,
        "raw_values": raw_values,
        "derived_values": derived_values or [],
        "no_fudge_policy": True,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
        "generated_outputs_committed": False,
        "notes": notes,
    }
