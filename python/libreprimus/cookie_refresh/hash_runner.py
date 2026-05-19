"""Exact digest comparison runner for Stage 4G."""

from __future__ import annotations

import hashlib

from libreprimus.cookie_refresh.models import ExpandedCookieCandidate
from libreprimus.hash_preimage.models import CookieTarget


def run_exact_comparisons(
    *,
    candidates: list[ExpandedCookieCandidate],
    targets: list[CookieTarget],
    algorithms: tuple[str, ...],
    experiment_id: str,
) -> tuple[list[dict], list[dict]]:
    """Run manifest-declared exact digest comparisons only."""

    records: list[dict] = []
    matches: list[dict] = []
    for candidate in candidates:
        for algorithm in algorithms:
            digest_hex = _digest_hex(algorithm, candidate.candidate_bytes)
            for target in targets:
                exact_match = digest_hex == target.cookie_value
                record = {
                    "record_type": "cookie_refresh_candidate_record",
                    "experiment_id": experiment_id,
                    "candidate_id": candidate.candidate_id,
                    "base_string_id": candidate.base_string_id,
                    "source_record_id": candidate.source_record_id,
                    "source_basis": candidate.source_basis,
                    "raw_string_redacted_if_needed": candidate.raw_string_redacted_if_needed,
                    "byte_variant": candidate.byte_variant,
                    "encoding": candidate.encoding,
                    "algorithm": algorithm,
                    "candidate_bytes_sha256": candidate.candidate_bytes_sha256,
                    "digest_hex": digest_hex,
                    "target_cookie_id": target.cookie_id,
                    "target_cookie_value": target.cookie_value,
                    "exact_match": exact_match,
                    "previous_pack_duplicate": candidate.previous_pack_duplicate,
                    "no_solve_claim": True,
                    "cuda_used": False,
                    "cloud_execution": False,
                    "trusted_as_canonical": False,
                    "exact_match_only": True,
                    "fuzzy_matching": False,
                    "partial_matching": False,
                    "hashcat_used": False,
                    "broad_search": False,
                }
                records.append(record)
                if exact_match:
                    matches.append({**record, "record_type": "cookie_refresh_exact_preimage_candidate"})
    return records, matches


def _digest_hex(algorithm: str, payload: bytes) -> str:
    if algorithm == "sha256":
        return hashlib.sha256(payload).hexdigest()
    if algorithm == "sha1":
        return hashlib.sha1(payload).hexdigest()
    if algorithm == "sha512":
        return hashlib.sha512(payload).hexdigest()
    if algorithm == "md5":
        return hashlib.md5(payload, usedforsecurity=False).hexdigest()
    raise ValueError(f"unsupported algorithm: {algorithm}")
