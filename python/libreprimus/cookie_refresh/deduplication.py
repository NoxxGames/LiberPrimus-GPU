"""Candidate expansion and duplicate detection for Stage 4G."""

from __future__ import annotations

import hashlib
from pathlib import Path

from libreprimus.cookie_refresh.byte_variants import apply_byte_variant
from libreprimus.cookie_refresh.models import (
    DEFAULT_STAGE3L_PACK_DIR,
    DEFAULT_STAGE3U_MANIFEST,
    CandidateBaseString,
    ExpandedCookieCandidate,
)
from libreprimus.hash_preimage.candidate_packs import expand_candidate_pack, load_candidate_packs
from libreprimus.history.source_records import resolve_repo_path
from libreprimus.post_discord.cookie_signed_variant_pack import expand_candidates as expand_stage3u_candidates
from libreprimus.post_discord.cookie_signed_variant_pack import load_cookie_manifest as load_stage3u_manifest


def expand_and_deduplicate_candidates(
    *,
    bases: list[CandidateBaseString],
    byte_variants: tuple[str, ...],
    cap: int,
    previous_hashes: set[str] | None = None,
) -> tuple[list[ExpandedCookieCandidate], list[dict], int]:
    """Expand variants and deduplicate exact UTF-8 bytes."""

    previous_hashes = previous_hashes or set()
    generated: list[tuple[CandidateBaseString, str, str, bytes, str]] = []
    for base in bases:
        for variant in byte_variants:
            candidate_text = apply_byte_variant(base.text, variant)
            candidate_bytes = candidate_text.encode("utf-8")
            candidate_hash = hashlib.sha256(candidate_bytes).hexdigest()
            generated.append((base, variant, candidate_text, candidate_bytes, candidate_hash))

    candidates: list[ExpandedCookieCandidate] = []
    duplicates: list[dict] = []
    seen: dict[str, str] = {}
    for base, variant, candidate_text, candidate_bytes, candidate_hash in generated:
        if candidate_hash in seen:
            duplicates.append(
                {
                    "record_type": "cookie_refresh_duplicate_candidate",
                    "duplicate_of": seen[candidate_hash],
                    "base_string_id": base.base_string_id,
                    "byte_variant": variant,
                    "candidate_bytes_sha256": candidate_hash,
                }
            )
            continue
        candidate_id = f"stage4g-cookie-candidate-{len(candidates) + 1:06d}"
        seen[candidate_hash] = candidate_id
        candidates.append(
            ExpandedCookieCandidate(
                candidate_id=candidate_id,
                base_string_id=base.base_string_id,
                source_record_id=base.source_record_id,
                source_basis=base.source_basis,
                raw_string_redacted_if_needed=base.text,
                byte_variant=variant,
                encoding="utf-8",
                candidate_text=candidate_text,
                candidate_bytes=candidate_bytes,
                candidate_bytes_sha256=candidate_hash,
                previous_pack_duplicate=candidate_hash in previous_hashes,
            )
        )
    if len(candidates) > cap:
        raise ValueError(f"candidate_cap_exceeded:{len(candidates)}>{cap}")
    return candidates, duplicates, len(generated)


def load_previous_candidate_hashes(
    *,
    stage3u_manifest: Path = DEFAULT_STAGE3U_MANIFEST,
    stage3l_pack_dir: Path = DEFAULT_STAGE3L_PACK_DIR,
) -> set[str]:
    """Regenerate prior bounded pack candidate byte hashes for duplicate marking."""

    hashes: set[str] = set()
    stage3u_path = resolve_repo_path(stage3u_manifest)
    if stage3u_path.is_file():
        manifest = load_stage3u_manifest(stage3u_path)
        candidates, _duplicate_count = expand_stage3u_candidates(manifest)
        hashes.update(candidate.candidate_bytes_sha256 for candidate in candidates)

    stage3l_dir = resolve_repo_path(stage3l_pack_dir)
    if stage3l_dir.is_dir():
        for pack in load_candidate_packs(stage3l_dir):
            expanded = expand_candidate_pack(pack)
            for candidate in expanded.candidates:
                hashes.add(hashlib.sha256(candidate.literal_text.encode(candidate.encoding)).hexdigest())
    return hashes
