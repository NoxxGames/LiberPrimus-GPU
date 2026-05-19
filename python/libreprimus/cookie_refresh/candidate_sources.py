"""Source-backed cookie candidate base-string loading."""

from __future__ import annotations

from pathlib import Path

from libreprimus.cookie_refresh.models import CandidateBaseString
from libreprimus.hash_preimage.validation import load_cookie_targets
from libreprimus.history.source_records import resolve_repo_path
from libreprimus.visual_observations.validation import load_records


def load_source_backed_base_strings(candidate_sources: Path, cookie_targets: Path) -> list[CandidateBaseString]:
    """Build conservative base strings from Stage 4B source records and cookie records."""

    source_records = load_records(resolve_repo_path(candidate_sources))
    targets = load_cookie_targets(resolve_repo_path(cookie_targets))
    bases: list[CandidateBaseString] = []
    seen: set[str] = set()

    for record in source_records:
        source_id = str(record.get("source_id") or record.get("record_id") or "stage4b-cookie-source")
        if record.get("solve_claim") is not False:
            raise ValueError(f"{source_id}: solve_claim must be false")
        source_basis = str(record.get("title") or record.get("notes") or "Stage 4B cookie candidate source record")
        text_blob = " ".join(str(record.get(key, "")) for key in ("title", "notes", "url", "normalized_url"))
        for token in ("167", "761"):
            if token in text_blob:
                _append_base(
                    bases,
                    seen,
                    CandidateBaseString(
                        base_string_id=f"{source_id}-{token}",
                        source_record_id=source_id,
                        source_basis=source_basis,
                        text=token,
                    ),
                )

    for target in targets:
        source_basis = f"Existing cookie hash artefact record {target.cookie_id}"
        _append_base(
            bases,
            seen,
            CandidateBaseString(
                base_string_id=f"{target.cookie_id}-name",
                source_record_id=target.cookie_id,
                source_basis=source_basis,
                text=target.cookie_name,
            ),
        )
        _append_base(
            bases,
            seen,
            CandidateBaseString(
                base_string_id=f"{target.cookie_id}-assignment",
                source_record_id=target.cookie_id,
                source_basis=source_basis,
                text=f"{target.cookie_name}={target.cookie_value}",
            ),
        )

    if not bases:
        raise ValueError("no source-backed cookie candidate base strings found")
    return bases


def _append_base(bases: list[CandidateBaseString], seen: set[str], base: CandidateBaseString) -> None:
    if not base.text:
        return
    if base.text in seen:
        return
    seen.add(base.text)
    bases.append(base)
